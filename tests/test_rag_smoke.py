"""Optional smoke test; requires a valid Gemini API key and network access."""
import os
import pytest

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="GEMINI_API_KEY not set")
def test_rag_retrieves_collection_policy():
    from rag import get_rag_assistant
    hits=get_rag_assistant().retrieve("What should customers retain for collection?")
    assert hits
    assert any("collection" in h["text"].lower() or "order reference" in h["text"].lower() for h in hits)
