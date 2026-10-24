
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# ---------------- CONFIGURATION ----------------

load_dotenv()

st.set_page_config(
    page_title="DayForge AI | Daily Planner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"

if not API_KEY:
    st.error("GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at top left, #211c48 0%, transparent 38%),
        #0b0d17;
    color: #f4f5ff;
}

.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.6px;
}

.hero {
    padding: 30px;
    border: 1px solid #343453;
    border-radius: 24px;
    background: linear-gradient(130deg, #1d2040, #151525 65%, #26163c);
    margin-bottom: 24px;
}

.hero-tag {
    display: inline-block;
    background: #302653;
    color: #d7c5ff;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 48px);
    margin: 14px 0 8px;
    color: #ffffff;
}

.hero p {
    color: #b4b7d0;
    font-size: 16px;
}

.section-card {
    padding: 20px;
    border: 1px solid #303148;
    border-radius: 18px;
    background: rgba(24, 26, 44, 0.85);
    margin-bottom: 16px;
}

div[data-testid="stTextArea"] textarea {
    background: #111321;
    color: #f4f5ff;
    border: 1px solid #363850;
    border-radius: 12px;
    line-height: 1.6;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #a78bfa;
    box-shadow: 0 0 0 1px #a78bfa;
}

.stButton > button {
    background: linear-gradient(100deg, #8b5cf6, #6d5dfc);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 18px;
    min-height: 48px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(100deg, #a78bfa, #818cf8);
    color: white;
    transform: translateY(-1px);
}

div[data-testid="stTabs"] button {
    border-radius: 10px;
}

div[data-testid="stSidebar"] {
    background: #10111f;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stMarkdownContainer"] {
    overflow-wrap: anywhere;
}

.footer {
    text-align: center;
    color: #777b9a;
    font-size: 12px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LLM FUNCTION ----------------

def llm_reply(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=1.5,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content or "No output generated."


# ---------------- PROMPT CHAIN: STEP 1 ----------------

def step1_task_analysis(tasks):
    system_prompt = """
    You are an expert productivity strategist.
    Analyze tasks, prioritize important study and work,
    account for deadlines and task dependencies, and
    keep non-negotiable activities protected.

    Return a numbered priority list.
    Include a short reason for each priority.
    Do not invent deadlines or task durations.
    """

    user_prompt = f"""
    Analyze these daily tasks:

    {tasks}

    Return the prioritized task list with concise reasoning.
    """

    return llm_reply(system_prompt, user_prompt)


# ---------------- PROMPT CHAIN: STEP 2 ----------------

def step2_workout_planner(exercises):
    system_prompt = """
    You are a sensible fitness coach designing a beginner
    weekly exercise plan.

    Respect the user's stated running distance, equipment,
    experience and recovery needs. Include warm-up, stretching
    and appropriate rest or recovery. Progress gradually;
    do not force an increase every day. Include running
    distances only when running is requested.

    Output Monday through Sunday, with exercises as bullets.
    Keep the response concise and practical.
    """

    user_prompt = f"""
    Create a weekly exercise plan using these preferences:

    {exercises}

    Include a sensible progression from the current fitness
    level. Make the plan easy to follow.
    """

    return llm_reply(system_prompt, user_prompt)


# ---------------- PROMPT CHAIN: STEP 3 ----------------

def step3_schedule_planner(schedule, tasks, task_analysis, exercise_plan):
    today = datetime.now().strftime("%A, %d %B %Y")

    system_prompt = """
    You are an expert daily scheduling assistant.

    Build a realistic 24-hour time-blocked schedule.
    Respect every fixed commitment and non-negotiable.
    Prioritize important study and research tasks.

    Rules:
    - Use 24-hour time.
    - Do not schedule overlapping activities.
    - Include reasonable transitions and buffer time.
    - Respect stated sleep and wake times.
    - Account for meals, bathing, rest and other fixed events.
    - Respect minimum and maximum task-slot lengths when feasible.
    - Do not silently discard a task if the day is too full.
      Identify scheduling conflicts and suggest what to move.
    - Include the workout and running from the exercise plan
      only if compatible with the user's constraints.
    - Do not invent commitments.
    - If constraints conflict, explicitly identify the conflict.
    - Use clear time ranges and task names.
    - Return only the final schedule and any essential
      constraint warnings.
    """

    user_prompt = f"""
    TODAY: {today}

    USER'S SCHEDULE AND CONSTRAINTS:
    {schedule}

    TASKS:
    {tasks}

    TASK PRIORITY ANALYSIS:
    {task_analysis}

    WEEKLY EXERCISE PLAN:
    {exercise_plan}

    Generate today's practical time-blocked schedule.
    Start with the date and day. Use 24-hour format.
    """

    return llm_reply(system_prompt, user_prompt)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <span class="hero-tag">⚡ AI PRODUCTIVITY STUDIO</span>
    <h1>Build your day.<br>Own your time.</h1>
    <p>
        Three inputs. Three AI steps. One actionable plan.
        Turn your tasks, routines and fitness goals into a
        structured day.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## ⚡ DayForge AI")
    st.caption("Your personal planning workspace")
    st.divider()

    st.markdown("### How it works")
    st.markdown("""
    **01 · Prioritize**
    
    AI organizes your tasks.

    **02 · Train**
    
    AI builds a weekly workout plan.

    **03 · Schedule**
    
    AI combines everything into a daily timetable.
    """)

    st.divider()
    st.markdown("### Model settings")
    st.caption(f"Model: `{MODEL}`")
    st.caption("Temperature: 1.5")
    st.caption("Provider: Groq")

    st.info(
        "Your API key stays on the server. "
        "Never enter it in a public text box."
    )

# ---------------- USER INPUTS ----------------

st.markdown("## Configure your day")
st.caption("Edit all three sections before generating your plans.")

with st.form("planner_form"):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 🎯 Your tasks")
        tasks = st.text_area(
            "Tasks and priorities",
            value=(
                "Workout\n"
                "Research paper study\n"
                "AI Engineering learning\n"
                "Create 4 YouTube videos, 1 hour each\n"
                "Talk to girlfriend"
            ),
            height=220,
            help="List everything you want to accomplish.",
        )

        st.markdown("### 🏃 Exercise preferences")
        exercises = st.text_area(
            "Exercises and fitness goals",
            value=(
                "Running: currently 2 km\n"
                "Stretching\n"
                "Beginner level\n"
                "Create a Monday-to-Sunday plan"
            ),
            height=190,
            help="Mention your current level, equipment and limitations.",
        )

    with col2:
        st.markdown("### 🕒 Daily schedule")
        schedule = st.text_area(
            "Routine and constraints",
            value=(
                "Wake up at 07:30 and sleep at 23:30.\n"
                "Morning running is non-negotiable.\n"
                "Bath: 30 minutes, in the morning.\n"
                "Lunch at 13:00, followed by rest.\n"
                "Task slots should be 2–3 hours where feasible.\n"
                "Prioritize studying and research.\n"
                "Workout is non-negotiable."
            ),
            height=300,
            help="Include fixed events, meals, sleep and slot constraints.",
        )

        st.markdown("### ✨ Planning preference")
        st.caption(
            "The AI will respect your fixed commitments, "
            "prioritize study and flag impossible constraints."
        )

    submitted = st.form_submit_button(
        "⚡ Generate My Daily Plan",
        use_container_width=True,
    )

# ---------------- GENERATE PLANS ----------------

if submitted:
    if not tasks.strip() or not exercises.strip() or not schedule.strip():
        st.error("Please fill in all three input sections.")
        st.stop()

    st.session_state.pop("planner_results", None)

    try:
        with st.status("Building your personalized plan...", expanded=True) as status:
            st.write("① Analyzing tasks and priorities...")
            task_analysis = step1_task_analysis(tasks)

            st.write("② Designing your weekly workout plan...")
            exercise_plan = step2_workout_planner(exercises)

            st.write("③ Combining everything into your schedule...")
            schedule_plan = step3_schedule_planner(
                schedule,
                tasks,
                task_analysis,
                exercise_plan,
            )

            st.session_state["planner_results"] = {
                "tasks": task_analysis,
                "exercise": exercise_plan,
                "schedule": schedule_plan,
            }

            status.update(
                label="Your plans are ready!",
                state="complete",
                expanded=False,
            )

    except Exception as e:
        st.error(f"Unable to generate your plan: {e}")
        st.info(
            "Check your API key, internet connection, model availability "
            "and Groq API limits, then try again."
        )

# ---------------- RESULTS DASHBOARD ----------------

if "planner_results" in st.session_state:
    results = st.session_state["planner_results"]

    st.divider()
    st.markdown("## Your planning dashboard")
    st.caption("Review each result below. Regenerate the plan after changing inputs.")

    tab1, tab2, tab3 = st.tabs([
        "🎯 Task priorities",
        "🏃 Workout plan",
        "🗓️ Daily schedule",
    ])

    with tab1:
        st.markdown("### Priority breakdown")
        st.markdown(results["tasks"])
        st.download_button(
            "⬇️ Download task analysis",
            data=results["tasks"],
            file_name="task_analysis.md",
            mime="text/markdown",
            key="download_tasks",
        )

    with tab2:
        st.markdown("### Your weekly exercise plan")
        st.markdown(results["exercise"])
        st.download_button(
            "⬇️ Download workout plan",
            data=results["exercise"],
            file_name="weekly_workout.md",
            mime="text/markdown",
            key="download_exercise",
        )

    with tab3:
        st.markdown("### Your time-blocked day")
        st.markdown(results["schedule"])
        st.download_button(
            "⬇️ Download daily schedule",
            data=results["schedule"],
            file_name="daily_schedule.md",
            mime="text/markdown",
            key="download_schedule",
        )

    full_plan = (
        "# DayForge AI — Daily Plan\n\n"
        "## Task Analysis\n\n" + results["tasks"] +
        "\n\n## Weekly Exercise Plan\n\n" + results["exercise"] +
        "\n\n## Daily Schedule\n\n" + results["schedule"]
    )

    st.download_button(
        "📦 Download complete plan",
        data=full_plan,
        file_name="dayforge_complete_plan.md",
        mime="text/markdown",
        use_container_width=True,
        key="download_all",
    )

else:
    st.markdown("""
    <div class="section-card">
        <h3>✨ Your next productive day starts here</h3>
        <p style="color:#b4b7d0;">
            Fill in your tasks, routine and exercise preferences above.
            Your generated plans will appear here.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    DAYFORGE AI · Plan with intention. Execute with consistency.
</div>
""", unsafe_allow_html=True)

