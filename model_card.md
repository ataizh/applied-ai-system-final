# Model Card — Game Glitch Investigator AI System

## System Overview

This system extends a number guessing game with two AI-powered components: an AI Coach that recommends optimal guesses using agentic reasoning, and a RAG-powered chatbot that answers strategy and rules questions by retrieving from a curated knowledge base. Both components use the Llama 3.3 70B model served via the Groq API.

---

## AI Collaboration

### How AI Was Used During Development

Claude Code was used throughout this project to help write, structure, and debug code. It assisted with:
- Designing the module structure (`ai_coach.py`, `chatbot.py`, `rag_retriever.py` as separate concerns)
- Writing the Groq API integration and prompt templates
- Building the reliability test harness and RAG comparison script
- Drafting README sections and documentation

### Helpful AI Suggestion

The most helpful suggestion was structuring the RAG retriever as a completely separate module (`rag_retriever.py`) rather than embedding retrieval logic inside `chatbot.py`. This made the retriever independently testable, reusable across components, and easy to swap out for a more advanced solution (e.g., vector embeddings) in the future.

### Flawed AI Suggestion

The initial AI Coach prompt only passed guess numbers to the model — `"50, 25, 37"` — without including the outcome of each guess. This caused the model to loop between the same numbers with a 10% win rate because it had no information about which direction to narrow. The fix required diagnosing why the model was cycling, understanding that the LLM needed explicit Higher/Lower labels to reason about the remaining range, and redesigning the prompt to pass `"50 -> Too High, 25 -> Too Low"`. Win rate jumped to 90% after this change.

---

## Biases and Limitations

### API Dependency
The system requires the Groq API to be available. If the API is down or rate-limited, AI features degrade to a warning message and the base game continues working. This is handled via try/except guardrails in both `ai_coach.py` and `chatbot.py`.

### RAG Retrieval Bias
The RAG retriever uses keyword overlap scoring, which favors exact word matches over semantic similarity. A player asking "how do I win faster?" will retrieve less relevant results than one asking "what is binary search strategy?" — even though both questions have the same intent. This is a known limitation of lexical retrieval vs. embedding-based retrieval.

### Coach Drift on Edge Cases
The AI Coach occasionally drifts from binary search to sequential guessing when the secret is near the extremes of the range (e.g., secret=1 or secrets in the 76-99 range). This happens because the LLM's reasoning becomes less precise when the remaining range is small and the guess history is long. The reliability test harness captures this — the "Low edge case" scenario (secret=1) consistently fails.

### Knowledge Base Coverage
The RAG chatbot can only answer questions covered by the four knowledge base documents. Questions outside these topics (e.g., "who made this game?") will receive a generic response without retrieved context.

---

## Testing Results

### Unit Tests
- **11 tests** in `tests/test_game_logic.py`
- **All 11 pass**
- Covers: correct outcomes, hint messages, edge case inputs (decimals, negatives, whitespace, large numbers)

### Scenario Test Harness
- **5 predefined scenarios** with fixed secrets and attempt thresholds
- **4/5 scenarios pass** (Low edge case fails — known limitation)
- Run with: `python tests/test_reliability.py`

### Random Game Reliability
- **10 automated games** simulated using AI Coach suggestions
- **Win rate: 70%** average across runs (range: 40–90% depending on secrets drawn)
- **Average attempts on wins: 5.1** (well under the 7-attempt binary search maximum)

### RAG Quality Comparison
- **3 questions** tested with and without retrieval
- **3/3 responses improved** with RAG — notably, the scoring question was answered incorrectly without retrieval and correctly with it
- Run with: `python tests/test_rag_quality.py`

---

## Future Improvements

- Replace keyword overlap with sentence-transformer embeddings for semantic RAG retrieval
- Add a diversity rule to the coach preventing it from suggesting the same number twice
- Limit the AI Coach to one use per game to preserve challenge
- Expand the knowledge base with more strategy documents and difficulty-specific tips
