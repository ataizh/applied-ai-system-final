import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from logic_utils import check_guess, get_range_for_difficulty
from ai_coach import get_coach_advice

DIFFICULTY = "Normal"
ATTEMPT_LIMIT = 8

# Predefined scenarios for the test harness
# Each has a fixed secret and a max_attempts threshold to pass
SCENARIOS = [
    {"name": "Midpoint secret",   "secret": 50,  "max_attempts": 5},
    {"name": "Low edge case",     "secret": 1,   "max_attempts": 8},
    {"name": "High edge case",    "secret": 100, "max_attempts": 8},
    {"name": "Lower quarter",     "secret": 25,  "max_attempts": 7},
    {"name": "Upper quarter",     "secret": 75,  "max_attempts": 7},
]


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
            return {"won": True, "attempts": attempt, "history": history}

    return {"won": False, "attempts": ATTEMPT_LIMIT, "history": history}


def run_scenario_tests():
    """Run predefined scenarios and print PASS/FAIL for each."""
    low, high = get_range_for_difficulty(DIFFICULTY)

    print(f"\n{'='*65}")
    print(f"  SCENARIO TEST HARNESS — {DIFFICULTY} difficulty (range {low}-{high})")
    print(f"{'='*65}")
    print(f"{'Scenario':<22} {'Secret':<8} {'Result':<6} {'Attempts':<10} {'Threshold':<10} {'Status'}")
    print("-" * 65)

    passed = 0
    for s in SCENARIOS:
        result = simulate_game(s["secret"], low, high)
        won = result["won"]
        attempts = result["attempts"]
        threshold = s["max_attempts"]
        status = "PASS" if won and attempts <= threshold else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"{s['name']:<22} {s['secret']:<8} {'WIN' if won else 'LOSS':<6} {attempts:<10} {threshold:<10} {status}")

    print("-" * 65)
    print(f"Scenario results: {passed}/{len(SCENARIOS)} passed\n")
    return passed, len(SCENARIOS)


def run_random_games(num_games=10):
    """Run random-secret games and report overall win rate."""
    low, high = get_range_for_difficulty(DIFFICULTY)
    results = []

    print(f"{'='*65}")
    print(f"  RANDOM GAME TEST — {num_games} games")
    print(f"{'='*65}")
    print(f"{'Game':<6} {'Secret':<8} {'Result':<6} {'Attempts':<10} {'Guesses'}")
    print("-" * 65)

    for i in range(1, num_games + 1):
        secret = random.randint(low, high)
        result = simulate_game(secret, low, high)
        results.append(result)
        status = "WIN" if result["won"] else "LOSS"
        print(f"{i:<6} {secret:<8} {status:<6} {result['attempts']:<10} {result['history']}")

    wins = sum(1 for r in results if r["won"])
    avg = sum(r["attempts"] for r in results if r["won"]) / wins if wins else 0
    win_rate = wins / num_games * 100

    print("-" * 65)
    print(f"Win rate     : {wins}/{num_games} ({win_rate:.0f}%)")
    print(f"Avg attempts : {avg:.1f}  (binary search max = 7)")
    print(f"{'='*65}\n")
    return win_rate


if __name__ == "__main__":
    passed, total = run_scenario_tests()
    win_rate = run_random_games(num_games=10)

    print("FINAL SUMMARY")
    print(f"  Scenario tests : {passed}/{total} passed")
    print(f"  Random win rate: {win_rate:.0f}%")
    overall_pass = passed >= 3 and win_rate >= 40
    print(f"  Overall        : {'PASS' if overall_pass else 'FAIL'}")
    if not overall_pass:
        print(f"  Note: coach struggles with high-range numbers (known limitation).")
    assert overall_pass, "Reliability test failed."
