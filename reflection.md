# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it looked normal, but once I started playing I noticed things were wrong right away.

Bug 1 — Hints are backwards: When the target was 47 and I guessed 46, the game told me to go lower even though I needed to go higher. I expected the hint to point me toward the secret number but it was doing the opposite every time.

Bug 2 — Can't start a new game after losing: After I used up all my attempts, the game showed "Game over" but clicking New Game didn't fix it, the screen stayed stuck on game over and I couldn't play again without refreshing the page.

Bug 3 — Same number gives different hints each time: When I entered the same guess twice in a row, sometimes it said go higher and then go lower for the exact same number. I expected the same guess to always get the same hint, but the result kept flipping back and forth.

---

## 2. How did you use AI as a teammate?

I used Claude (Claude Code) as my AI teammate throughout this project to help investigate bugs and refactor the code.

Correct suggestion: I described Bug 3: the same number giving different hints on different attempts and asked Claude to explain the logic. Claude correctly identified that on even-numbered attempts the secret number was being converted to a string, so comparing an integer guess against a string was causing unpredictable results. I verified this by reading lines 158–161 in app.py and confirming the str() conversion was exactly where Claude said it was.

Incorrect or misleading suggestion: When I first asked about the new game bug, Claude's initial explanation focused only on the missing status reset. But when I actually looked at the new game block, I noticed it also wasn't resetting the history or score  so the fix needed to be more complete than what was first suggested. I verified this by testing the game manually and noticing the old guesses were still showing in the history after clicking New Game.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed in two ways: first by running pytest to confirm the logic tests passed, and second by running the live app with streamlit run app.py and manually testing the exact scenario that originally broke.

For the backwards hints bug, I wrote a pytest test called test_too_high_message_says_go_lower that calls check_guess(60, 50) and checks that the word "LOWER" appears in the message. Before the fix this test would have failed because the original code returned "Go HIGHER!" for a too-high guess. After moving the corrected logic into logic_utils.py, all 7 tests passed. I also wrote test_same_guess_always_returns_same_result which calls check_guess(47, 50) twice and confirms both results are identical — this directly caught the type-flip bug that caused hints to flip between attempts.

Claude helped me understand why the existing starter tests were also broken — they were comparing the full return value of check_guess to a plain string like "Win", but the function actually returns a tuple ("Win", "🎉 Correct!"). Claude suggested unpacking the tuple in each test, which I verified by running pytest and seeing all tests pass after the fix.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because Streamlit reruns the entire Python file from top to bottom every single time you click a button. So `random.randint()` was being called again on every click, generating a brand new secret each time — there was nothing holding onto the old one.

I'd explain it to a friend like this: imagine every time you click something on the page, the whole script restarts from scratch like it was never run before. Session state is basically a sticky notepad that survives those restarts — anything you write to it stays there even when the page reruns.

The fix was wrapping the secret generation in `if "secret" not in st.session_state` — that check was already there in the original code, but the type-flip bug on even attempts was still making comparisons fail. Once I removed that and kept the secret as a plain integer throughout, the game finally had a stable number the whole round.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is adding `# FIXME` comments before touching anything. It forced me to pinpoint exactly where I thought the problem was before jumping in, and it made it easier to explain the bug to the AI too.

Next time I'd verify AI suggestions against the actual code before accepting them — a couple times the explanation was right but the fix was incomplete, and I had to catch that myself.

This project made me realize AI-generated code looks totally fine on the surface but can have subtle logic bugs buried inside it. I'll never just run AI code without reading it first.
