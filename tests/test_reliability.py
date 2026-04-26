import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from logic_utils import check_guess, get_range_for_difficulty
from ai_coach import get_coach_advice

NUM_GAMES = 10
DIFFICULTY = "Normal"
ATTEMPT_LIMIT = 8


def simulate_game(secret: int, low: int, high: int) -> dict:
    """Run one full game using the AI Coach for every guess."""
    history = []
    outcomes = []

    for attempt in range(1, ATTEMPT_LIMIT + 1):
        attempts_left = ATTEMPT_LIMIT - attempt + 1
        advice, error = get_coach_advice(
            history=history,
            outcomes=outcomes,
            low=low,
            high=high,
            attempts_left=attempts_left,
            difficulty=DIFFICULTY,
        )

        if error or advice is None or advice["next_guess"] is None:
            guess = random.randint(low, high)
        else:
            guess = max(low, min(high, advice["next_guess"]))

        outcome, _ = check_guess(guess, secret)
        history.append(guess)
        outcomes.append(outcome)

        if outcome == "Win":
            return {"won": True, "attempts": attempt, "history": history, "outcomes": outcomes}

    return {"won": False, "attempts": ATTEMPT_LIMIT, "history": history, "outcomes": outcomes}


def run_reliability_test():
    low, high = get_range_for_difficulty(DIFFICULTY)
    results = []

    print(f"\nReliability Test — {NUM_GAMES} games on {DIFFICULTY} (range {low}-{high}, limit {ATTEMPT_LIMIT})\n")
    print(f"{'Game':<6} {'Secret':<8} {'Won':<6} {'Attempts':<10} {'Guesses'}")
    print("-" * 70)

    for i in range(1, NUM_GAMES + 1):
        secret = random.randint(low, high)
        result = simulate_game(secret, low, high)
        results.append(result)
        status = "WIN" if result["won"] else "LOSS"
        print(f"{i:<6} {secret:<8} {status:<6} {result['attempts']:<10} {result['history']}")

    wins = sum(1 for r in results if r["won"])
    avg_attempts = sum(r["attempts"] for r in results if r["won"]) / wins if wins else 0
    win_rate = wins / NUM_GAMES * 100

    print("\n" + "=" * 70)
    print(f"Win rate      : {wins}/{NUM_GAMES} ({win_rate:.0f}%)")
    print(f"Avg attempts  : {avg_attempts:.1f} (optimal binary search = 7 max)")
    print(f"Games lost    : {NUM_GAMES - wins}")
    print("=" * 70)

    assert win_rate >= 50, f"Win rate too low: {win_rate:.0f}%"
    print("\nReliability check passed.")


if __name__ == "__main__":
    run_reliability_test()
