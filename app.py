from __future__ import annotations
import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from calculator import calculate_print_order

load_dotenv()
app=Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/estimate")
def estimate():
    try:
        pages_raw=request.form.get("pages", "").strip()
        copies_raw=request.form.get("copies", "").strip()
        # Reject decimals and empty values before converting.
        if not pages_raw.isdigit() or not copies_raw.isdigit():
            raise ValueError("Page count and copies must be positive whole numbers.")
        result=calculate_print_order(
            pages_per_copy=int(pages_raw),
            copies=int(copies_raw),
            colour_mode=request.form.get("colour_mode", "black_white"),
            double_sided=request.form.get("double_sided") == "yes",
            binding_required=request.form.get("binding_required") == "yes",
        )
        return render_template("index.html", result=result, submitted=True)
    except ValueError as exc:
        return render_template("index.html", error=str(exc), submitted=True), 400

@app.post("/ask")
def ask():
    payload=request.get_json(silent=True) or request.form
    question=str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"error":"Enter a question."}), 400
    try:
        # Lazy load: the calculator works even before RAG has been initialized.
        from rag import answer_question
        return jsonify(answer_question(question))
    except Exception as exc:
        app.logger.exception("RAG request failed")
        return jsonify({"error":"The RAG assistant could not answer. Check your Gemini API key, model name, and internet connection.", "details":str(exc)}), 500

@app.get("/health")
def health():
    return jsonify({"status":"ok", "service":"project46_printing_assistant"})

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
