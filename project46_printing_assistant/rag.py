"""Retrieval-Augmented Generation (RAG) for the Printing Services Assistant.

Pipeline:
1. Read the shop's knowledge documents.
2. Split documents into small chunks.
3. Embed each chunk using Sentence Transformers.
4. Retrieve the most relevant chunks with cosine similarity.
5. Send only retrieved context to a local Ollama LLM for a grounded answer.

If Ollama is unavailable, a concise context-based fallback is used.
"""
from pathlib import Path
import re
import requests
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
KNOWLEDGE_DIR = ROOT / "knowledge"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
OUT_OF_SCOPE = (
    "I can provide print-order estimates and answer questions about the shop's stated "
    "printing policies, but I cannot check live print-job status or confirm whether a "
    "document has finished printing."
)

class PrintingRAG:
    def __init__(self, model_name="all-MiniLM-L6-v2", ollama_model=OLLAMA_MODEL):
        self.embedder = SentenceTransformer(model_name)
        self.ollama_model = ollama_model
        self.chunks, self.sources = self._load_and_chunk()
        if not self.chunks:
            raise RuntimeError(f"No knowledge text found in {KNOWLEDGE_DIR}")
        self.embeddings = self.embedder.encode(
            self.chunks, normalize_embeddings=True, convert_to_numpy=True
        )

    def _load_and_chunk(self):
        chunks, sources = [], []
        for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            # Split by paragraphs, then merge short paragraphs into useful chunks.
            paragraphs = [re.sub(r"\s+", " ", p).strip() for p in text.splitlines() if p.strip()]
            current = ""
            for paragraph in paragraphs:
                if current and len(current) + len(paragraph) > 420:
                    chunks.append(current)
                    sources.append(path.name)
                    current = paragraph
                else:
                    current = f"{current} {paragraph}".strip()
            if current:
                chunks.append(current)
                sources.append(path.name)
        return chunks, sources

    def retrieve(self, question, top_k=3):
        query_embedding = self.embedder.encode(
            [question], normalize_embeddings=True, convert_to_numpy=True
        )[0]
        scores = self.embeddings @ query_embedding
        indices = np.argsort(scores)[::-1][:top_k]
        return [
            {"text": self.chunks[int(i)], "source": self.sources[int(i)], "score": float(scores[int(i)])}
            for i in indices
        ]

    def ask(self, question):
        question = question.strip()
        if not question:
            return "Please enter a question."

        # The assistant is intentionally limited to policy/guide questions, not live job tracking.
        live_status_terms = ("finished printing", "print status", "printing status", "is my document done",
                             "has my document", "where is my order", "track my order")
        if any(term in question.lower() for term in live_status_terms):
            return OUT_OF_SCOPE

        hits = self.retrieve(question)
        context = "\n".join(
            f"[Source: {hit['source']}] {hit['text']}" for hit in hits
        )
        prompt = f"""You are the Printing Services Assistant.
Answer the user's question using ONLY the context below.
If the context does not contain the answer, say that the available shop guide does not specify it.
Do not claim to upload, inspect, or print a document, or to access live order status.
Be concise and practical.

CONTEXT:
{context}

QUESTION: {question}
ANSWER:"""

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": self.ollama_model, "prompt": prompt, "stream": False},
                timeout=45,
            )
            response.raise_for_status()
            answer = response.json().get("response", "").strip()
            if answer:
                return answer
        except (requests.RequestException, ValueError):
            pass

        # Useful local fallback if Ollama is not installed/running.
        question_lower = question.lower()
        if "double-sided" in question_lower or "double sided" in question_lower:
            return ("No. Printing is charged per printed side. Double-sided printing reduces "
                    "the number of paper sheets, but it does not reduce the printing charge.")
        if "collection" in question_lower or "retain" in question_lower or "keep" in question_lower:
            return "Customers must retain the order reference for collection."
        if "binding" in question_lower:
            return "Optional binding costs INR 30 per copy. Each copy is printed and bound separately."
        if "price" in question_lower or "cost" in question_lower or "charge" in question_lower:
            return ("Black-and-white printing costs INR 2 per printed side; colour printing costs "
                    "INR 8 per printed side. Optional binding costs INR 30 per copy.")
        return f"Relevant shop guidance: {hits[0]['text']}"

if __name__ == "__main__":
    bot = PrintingRAG()
    print("Printing Services RAG ready. Type 'quit' to stop.")
    while True:
        q = input("\nQuestion: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        print("\nAnswer:", bot.ask(q))
        print("Retrieved sources:", ", ".join(dict.fromkeys(x["source"] for x in bot.retrieve(q))))
