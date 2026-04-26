import os
import logging
from groq import Groq

logging.basicConfig(
    filename="coach.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = """
You are a coach for a number guessing game.

Game state:
- Range: {low} to {high}
- Difficulty: {difficulty}
- Attempts left: {attempts_left}
- Guess history with outcomes: {history}

Each entry is "guess -> outcome" where outcome is Too High, Too Low, or Win.
Use the outcomes to narrow down the remaining range and pick the optimal next guess.

Analyze the player's guesses and respond in exactly this format (no extra text):
STRATEGY: <one of: No guesses yet / Random / Sequential / Binary Search / Narrowing>
NEXT_GUESS: <single integer within the remaining valid range>
REASONING: <one sentence explaining why>
CONFIDENCE: <integer 0-100>
""".strip()


def get_coach_advice(history: list, outcomes: list, low: int, high: int, attempts_left: int, difficulty: str):
    """
    Call Groq API to analyze guess history and return strategic advice.

    Args:
        history: list of integer guesses
        outcomes: list of outcome strings matching each guess ("Too High", "Too Low", "Win")
    Returns: (advice: dict | None, error: str | None)
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None, "GROQ_API_KEY is not set. Add it to your .env file."

    if history:
        history_str = ", ".join(
            f"{g} -> {o}" for g, o in zip(history, outcomes)
        )
    else:
        history_str = "none"

    prompt = _PROMPT_TEMPLATE.format(
        low=low,
        high=high,
        difficulty=difficulty,
        attempts_left=attempts_left,
        history=history_str,
    )

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        raw = response.choices[0].message.content.strip()
        logger.info("Groq response received. History: %s", history_str)
        advice = _parse_response(raw)
        return advice, None
    except Exception as exc:
        logger.error("Groq API error: %s", exc)
        return None, f"API error: {exc}"


def _parse_response(text: str) -> dict:
    """Parse the structured Groq response into a dict."""
    result = {"strategy": "Unknown", "next_guess": None, "reasoning": "", "confidence": 0}
    for line in text.splitlines():
        if line.startswith("STRATEGY:"):
            result["strategy"] = line.split(":", 1)[1].strip()
        elif line.startswith("NEXT_GUESS:"):
            try:
                result["next_guess"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif line.startswith("REASONING:"):
            result["reasoning"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                result["confidence"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
    return result
