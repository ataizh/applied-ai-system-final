import random
import streamlit as st
from dotenv import load_dotenv
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
from ai_coach import get_coach_advice
from chatbot import get_response

load_dotenv()

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "outcomes" not in st.session_state:
    st.session_state.outcomes = []

if "coach_advice" not in st.session_state:
    st.session_state.coach_advice = None

if "coach_error" not in st.session_state:
    st.session_state.coach_error = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    st.write("Outcomes:", st.session_state.outcomes)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)
with col4:
    ask_coach = st.button("Ask AI Coach 🤖")

if ask_coach:
    advice, error = get_coach_advice(
        history=st.session_state.history,
        outcomes=st.session_state.outcomes,
        low=low,
        high=high,
        attempts_left=attempt_limit - st.session_state.attempts,
        difficulty=difficulty,
    )
    st.session_state.coach_advice = advice
    st.session_state.coach_error = error

if st.session_state.coach_error:
    st.warning(f"AI Coach unavailable: {st.session_state.coach_error}")
elif st.session_state.coach_advice:
    adv = st.session_state.coach_advice
    st.info(
        f"**AI Coach** | Strategy: *{adv['strategy']}* | "
        f"Suggested guess: **{adv['next_guess']}** | "
        f"Confidence: {adv['confidence']}%\n\n"
        f"_{adv['reasoning']}_"
    )

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.outcomes = []
    st.session_state.score = 0
    st.session_state.coach_advice = None
    st.session_state.coach_error = None
    st.session_state.chat_history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.history.append(guess_int)
        st.session_state.outcomes.append(outcome)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.subheader("Game Assistant (RAG Chatbot)")
st.caption("Ask anything about strategy, rules, or math. Powered by Llama 3 + knowledge base retrieval.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask the assistant...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    game_state = {
        "low": low,
        "high": high,
        "attempts_left": attempt_limit - st.session_state.attempts,
        "history": st.session_state.history,
    }

    reply, sources = get_response(
        user_message=user_input,
        chat_history=st.session_state.chat_history[:-1],
        game_state=game_state,
    )

    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if sources:
        reply += f"\n\n*Sources: {', '.join(sources)}*"

    with st.chat_message("assistant"):
        st.write(reply)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
