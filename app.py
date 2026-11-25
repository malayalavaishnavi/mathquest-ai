
import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="MathQuest AI",
    page_icon="🧙",
    layout="wide"
)

# ---------------- SESSION DATA ----------------

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "answered" not in st.session_state:
    st.session_state.answered = False

if "question_id" not in st.session_state:
    st.session_state.question_id = 0

if "student_class" not in st.session_state:
    st.session_state.student_class = "Class 8"

# ---------------- AVATAR LEVEL ----------------

xp = st.session_state.xp

if xp >= 100:
    avatar = "🧙‍♂️"
    avatar_level = "Math Champion"
elif xp >= 50:
    avatar = "🦸"
    avatar_level = "Math Wizard"
else:
    avatar = "🧑‍🎓"
    avatar_level = "Math Explorer"

# ---------------- HEADER ----------------

st.title("🌟 MathQuest AI")
st.subheader("Explore Mathematics. Solve Challenges. Level Up!")

st.divider()

left, right = st.columns([1, 3])

with left:
    st.markdown(f"<h1 style='text-align:center;font-size:90px'>{avatar}</h1>",
                unsafe_allow_html=True)

with right:
    st.header("Welcome, Math Explorer!")
    st.write(f"**Your Avatar:** {avatar_level}")
    st.write(f"⭐ **XP Points:** {xp}")
    st.progress(min(xp / 100, 1.0))

st.divider()

# ---------------- STUDENT SETTINGS ----------------

st.header("🎯 Choose Your Mathematics Challenge")

st.session_state.student_class = st.selectbox(
    "Select your class",
    ["Class 8", "Class 9"]
)

# ---------------- QUESTION GENERATOR ----------------

def generate_question(level):

    if level == "Easy":
        a = random.randint(10, 30)
        b = random.randint(5, 20)

        return {
            "question": f"What is {a} + {b}?",
            "answer": a + b,
            "explanation": f"{a} + {b} = {a+b}",
            "time": 60
        }

    elif level == "Moderate":
        price = random.choice([500, 600, 800, 1000])
        discount = random.choice([10, 15, 20, 25])
        answer = price * (100 - discount) / 100

        return {
            "question": (
                f"A product costs ₹{price}. "
                f"It has a {discount}% discount. "
                "Find its final price."
            ),
            "answer": answer,
            "explanation": (
                f"Discount = {discount}% of {price} "
                f"= ₹{price * discount / 100:.2f}. "
                f"Final price = ₹{price} - "
                f"₹{price * discount / 100:.2f} "
                f"= ₹{answer:.2f}."
            ),
            "time": 45
        }

    else:
        a = random.randint(2, 9)
        b = random.randint(2, 10)
        x = random.randint(2, 8)
        result = a * x + b

        return {
            "question": (
                f"Solve the equation: {a}x + {b} = {result}. "
                "Find x."
            ),
            "answer": x,
            "explanation": (
                f"{a}x + {b} = {result}\n"
                f"{a}x = {result} - {b} = {a*x}\n"
                f"x = {a*x}/{a} = {x}"
            ),
            "time": 30
        }

# ---------------- TIMER ----------------

if (st.session_state.question is not None
        and not st.session_state.answered):

    q = st.session_state.question
    elapsed = time.time() - st.session_state.start_time

    if elapsed < q["time"]:
        st_autorefresh(
            interval=1000,
            key="mathquest_timer"
        )

# ---------------- CHALLENGE TABS ----------------

easy_tab, moderate_tab, difficult_tab = st.tabs(
    ["🟢 Easy", "🟡 Moderate", "🔴 Difficult"]
)

def show_challenge(level):

    st.subheader(f"{level} Mathematics Challenge")

    if st.button(
        f"Generate {level} Question",
        key=f"generate_{level}"
    ):
        st.session_state.question = generate_question(level)
        st.session_state.question["level"] = level
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.session_state.question_id += 1
        st.rerun()

    q = st.session_state.question

    if q is not None and q["level"] == level:

        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, q["time"] - int(elapsed))

        st.markdown("### 📝 Your Question")
        st.info(q["question"])

        st.metric("⏳ Time Remaining", f"{remaining} seconds")

        st.progress(remaining / q["time"])

        if remaining == 0 and not st.session_state.answered:
            st.error("⏰ Time is up! Try another question.")
            st.write("Correct answer:", q["answer"])
            st.write("Explanation:", q["explanation"])

        elif not st.session_state.answered:

            answer = st.text_input(
                "Enter your answer",
                key=f"answer_{st.session_state.question_id}"
            )

            if st.button(
                "Submit Answer",
                key=f"submit_{st.session_state.question_id}"
            ):

                if time.time() - st.session_state.start_time >= q["time"]:
                    st.error("Time is up!")
                else:
                    try:
                        correct = float(answer) == float(q["answer"])
                    except ValueError:
                        correct = False

                    st.session_state.answered = True

                    if correct:
                        st.session_state.xp += 10
                        st.success("🎉 Excellent! Correct answer! +10 XP")
                        st.balloons()
                    else:
                        st.error("Not quite! Keep practising.")

                    st.write("**Correct answer:**", q["answer"])
                    st.write("**Explanation:**", q["explanation"])

        else:
            st.info("You have completed this question. Generate another!")

with easy_tab:
    show_challenge("Easy")

with moderate_tab:
    show_challenge("Moderate")

with difficult_tab:
    show_challenge("Difficult")

# ---------------- REAL LIFE MATHEMATICS ----------------

st.divider()
st.header("🌍 Real-Life Mathematics Missions")

st.write("### 🛍️ Shopping Discount Calculator")

price = st.number_input(
    "Original price (₹)",
    min_value=0,
    value=1000
)

discount = st.slider(
    "Discount percentage",
    min_value=0,
    max_value=90,
    value=20
)

saving = price * discount / 100
final_price = price - saving

col1, col2 = st.columns(2)

with col1:
    st.metric("You Save", f"₹{saving:.2f}")

with col2:
    st.metric("Final Price", f"₹{final_price:.2f}")

st.write(
    f"Calculation: {price} - ({price} × {discount}/100) "
    f"= ₹{final_price:.2f}"
)

# ---------------- VISUAL MATHEMATICS ----------------

st.divider()
st.header("📊 Visual Mathematics Lab")

st.write("Change the values and observe how the graph changes.")

col1, col2, col3 = st.columns(3)

with col1:
    a = st.slider("Value of a", 1, 5, 1)

with col2:
    b = st.slider("Value of b", -5, 5, 0)

with col3:
    c = st.slider("Value of c", -10, 10, 0)

x = np.linspace(-10, 10, 200)
y = a * x**2 + b * x + c

fig, ax = plt.subplots()

ax.plot(x, y, linewidth=2)
ax.axhline(0)
ax.axvline(0)
ax.set_title(f"y = {a}x² + {b}x + {c}")
ax.set_xlabel("X values")
ax.set_ylabel("Y values")
ax.grid(True)

st.pyplot(fig)

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<h3 style='text-align:center'>"
    "🌟 Keep Learning. Keep Growing. Become a Math Champion! "
    "</h3>",
    unsafe_allow_html=True
)
