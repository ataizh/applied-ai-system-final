import os
import logging
from groq import Groq
from rag_retriever import load_chunks, retrieve

logger = logging.getLogger(__name__)

_CHUNKS = load_chunks()

_SYSTEM_TEMPLATE = """You are a friendly game assistant for a number guessing game.

Current game state:
- Range: {low} to {high}
- Attempts left: {attempts_left}
- Guess history: {history}

Relevant knowledge retrieved for this question:
{context}

Answer the player's question in 2-3 sentences. Use the retrieved knowledge when relevant. If the knowledge is not relevant, answer from general knowledge."""


def get_response(user_message: str, chat_history: list, game_state: dict):
    """
    Get a RAG-powered chatbot response.

    Args:
        user_message: the player's question
        chat_history: list of {"role": "user"/"assistant", "content": str}
        game_state: dict with keys low, high, attempts_left, history

    Returns: (reply: str, retrieved_sources: list[str])
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY is not set.", []

    relevant_chunks = retrieve(user_message, _CHUNKS)
    context = "\n\n".join(
        f"[{c['source']}] {c['text']}" for c in relevant_chunks
    ) if relevant_chunks else "No specific knowledge found."

    history_str = ", ".join(str(g) for g in game_state.get("history", [])) or "No guesses yet"

    system_prompt = _SYSTEM_TEMPLATE.format(
        low=game_state.get("low", 1),
        high=game_state.get("high", 100),
        attempts_left=game_state.get("attempts_left", 0),
        history=history_str,
        context=context,
    )

    messages = (
        [{"role": "system", "content": system_prompt}]
        + chat_history
        + [{"role": "user", "content": user_message}]
    )

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,
        )
        reply = response.choices[0].message.content.strip()
        sources = list({c["source"] for c in relevant_chunks})
        logger.info("Chatbot reply generated. Sources: %s", sources)
        return reply, sources
    except Exception as exc:
        logger.error("Chatbot API error: %s", exc)
        return f"Error: {exc}", []
