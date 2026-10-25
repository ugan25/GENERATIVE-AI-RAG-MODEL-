# Project 46 — Printing Services Assistant (RAG)

A Flask web app with:
- A separate `rag.py` module for Retrieval-Augmented Generation.
- Sentence Transformers embeddings (`all-MiniLM-L6-v2`).
- Cosine-similarity retrieval over the three knowledge documents.
- Ollama as the local LLM runtime (default model: `llama3.2`).
- A deterministic `calculate_print_order()` tool for price and paper calculations.
- Explicit scope boundary: no file uploads, document inspection, printer access, or live order tracking.

## 1. Requirements

- Python 3.10 or newer
- Internet access the first time the embedding model is downloaded
- Ollama installed locally for LLM-generated answers. The app's basic retrieval fallback works if Ollama is not running.

## 2. Setup

Open a terminal in this folder.

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Start the local LLM (recommended)

Install Ollama from https://ollama.com, then run:

```bash
ollama pull llama3.2
ollama run llama3.2
```

Keep Ollama running in its terminal. If the model is already downloaded, `ollama run llama3.2` starts it.

## 4. Run the web app

Open another terminal in this project folder, activate the virtual environment, then:

```bash
python app.py
```

Visit http://127.0.0.1:5000

## 5. Run RAG in the terminal only

```bash
python rag.py
```

Ask:
- Does double-sided printing reduce the printing charge?
- What should customers retain for collection?
- Has my document finished printing?

The final question is intentionally out of scope.

## 6. Verify the calculator examples

Run:

```bash
python -c "from print_tool import calculate_print_order as c; print(c(5,3,'black_white',True,True)); print(c(4,2,'colour',False,False))"
```

Expected key values:
- 5 pages × 3 copies, black-and-white, double-sided, binding: 15 sides, 9 sheets, INR 30 printing, INR 90 binding, INR 120 total.
- 4 pages × 2 copies, colour, single-sided, no binding: 8 sides, 8 sheets, INR 64 printing, INR 0 binding, INR 64 total.

## 7. RAG pipeline

1. `knowledge/*.txt` are read by `rag.py`.
2. Text is grouped into chunks.
3. `SentenceTransformer` converts chunks and each user question into vectors (embeddings).
4. Cosine similarity ranks the document chunks.
5. The best chunks are added to the prompt sent to Ollama.
6. The model answers using the retrieved context; an in-scope fallback is used if Ollama is unavailable.

The knowledge base is small, so this example computes cosine similarity directly with NumPy instead of maintaining a separate vector database. This is a vector-retrieval implementation; you can replace it with FAISS or Chroma if the knowledge base grows.

## Project structure

```text
project46_printing_assistant/
├── app.py
├── rag.py
├── print_tool.py
├── requirements.txt
├── README.md
├── knowledge/
│   ├── print_specifications.txt
│   ├── print_order_guide.txt
│   └── collection_policy.txt
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Important notes

- `pages_per_copy` and `copies` must be positive integers.
- Accepted colour modes are exactly `black_white` and `colour`.
- Double-sided sheets are rounded up per copy, then multiplied by copies. An odd final page from one copy is never combined with another copy.
- Charges are calculated per printed side, not per paper sheet.
- The displayed total is an estimate only.
