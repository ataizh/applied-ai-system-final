import re
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"


def load_chunks() -> list[dict]:
    """Load all markdown files and split into paragraph-level chunks."""
    chunks = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for para in paragraphs:
            chunks.append({"source": path.stem, "text": para})
    return chunks


def retrieve(query: str, chunks: list[dict], top_k: int = 3) -> list[dict]:
    """Return top_k chunks most relevant to query using word overlap scoring."""
    query_words = set(re.findall(r"\w+", query.lower()))
    scored = []
    for chunk in chunks:
        chunk_words = set(re.findall(r"\w+", chunk["text"].lower()))
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored[:top_k] if score > 0]
