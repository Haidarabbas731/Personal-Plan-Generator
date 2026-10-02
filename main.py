import os

import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openrouter import ChatOpenRouter

load_dotenv()

st.set_page_config(page_title="Personal Plan Generator", page_icon="🧭", layout="centered")


def get_key(name: str) -> str | None:
    """Read a key from the environment (.env) or Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name)
    except Exception:
        return None


GOOGLE_API_KEY = get_key("GOOGLE_API_KEY")
OPENROUTER_API_KEY = get_key("OPENROUTER_API_KEY")

CATEGORIES = [
    "Programming 💻",
    "Art 🎨",
    "Music 🎶",
    "Fitness 🏋️",
    "Cooking 🍳",
    "Languages 🌍",
    "Learning ✍️",
    "Business 📈",
]

# ---------------------------------------------------------------- prompt
plan_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior {category} coach with 20 years of experience teaching people "
            "to reach real competence. You write realistic, specific study plans, not "
            "motivational filler. Every task is something the learner can start immediately "
            "and know when it is finished.",
        ),
        (
            "human",
            """Build a day-by-day plan.

Skill: {skill}
Category: {category}
Days available: {days_available}
Time per day: {daily_time} hour(s)
Milestone every: {milestone_interval} day(s)

Rules:
- Output exactly {days_available} days, numbered Day 1 to Day {days_available}. Never skip, merge or summarise days.
- Group days under a `## Week N: <theme>` heading (last week may be shorter). Each week theme should build on the previous one.
- Format each day as:
  **Day N · <short title>** (~{daily_time}h)
  - Learn: <specific concept or resource type>
  - Practice: <concrete exercise with a measurable result>
  - Review: <what to recall or fix from earlier days>
- Split each day's time sensibly across Learn / Practice / Review, favouring Practice.
- Every {milestone_interval} days, add a line `🏁 Milestone: <small project or test and how to judge it>` directly after that day.
- Start with a 2-sentence overview of the path. Finish with a short "Where you'll be on Day {days_available}" paragraph.
- No intro chatter, no closing questions. Markdown only.""",
        ),
    ]
)


# ---------------------------------------------------------------- model discovery
@st.cache_data(ttl=3600, show_spinner=False)
def list_gemini_models(api_key: str) -> list[str]:
    client = genai.Client(api_key=api_key)
    names = []
    for m in client.models.list():
        actions = m.supported_actions or []
        name = (m.name or "").removeprefix("models/")
        if "generateContent" in actions and name.startswith("gemini"):
            names.append(name)
    return sorted(set(names), reverse=True)


@st.cache_data(ttl=3600, show_spinner=False)
def list_openrouter_models(api_key: str) -> list[str]:
    resp = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=15,
    )
    resp.raise_for_status()
    ids = []
    for m in resp.json().get("data", []):
        outputs = (m.get("architecture") or {}).get("output_modalities") or ["text"]
        if outputs == ["text"] and not m["id"].endswith(":batch"):
            ids.append(m["id"])
    return sorted(ids)


def build_llm(provider: str, model: str):
    if provider == "Google Gemini":
        return ChatGoogleGenerativeAI(model=model, google_api_key=GOOGLE_API_KEY)
    return ChatOpenRouter(model=model, api_key=OPENROUTER_API_KEY)


# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --paper: #eef1ec;
  --card: #fbfcfa;
  --ink: #12211d;
  --muted: #5b6b66;
  --line: #cfd8d2;
  --signal: #ff5a1f;
  --signal-ink: #ffffff;
  --moss: #1f5c4a;
}

html, body, [data-testid="stApp"] { background: var(--paper); color: var(--ink); }
[data-testid="stApp"] { font-family: 'Instrument Sans', system-ui, sans-serif; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px; padding-top: 2.5rem; padding-bottom: 5rem; }

/* masthead */
.eyebrow { font: 600 0.72rem 'JetBrains Mono', monospace; letter-spacing: .14em;
  text-transform: uppercase; color: var(--moss); margin-bottom: .6rem; }
.title { font: 800 clamp(2.4rem, 7vw, 3.8rem)/0.98 'Bricolage Grotesque', sans-serif;
  letter-spacing: -0.035em; margin: 0 0 .9rem; }
.title em { font-style: normal; color: var(--signal); }
.lede { color: var(--muted); font-size: 1.05rem; max-width: 52ch; margin: 0 0 2rem; }

/* section labels */
.label { font: 600 0.72rem 'JetBrains Mono', monospace; letter-spacing: .12em;
  text-transform: uppercase; color: var(--muted); margin: 1.6rem 0 .4rem;
  padding-bottom: .35rem; border-bottom: 1px solid var(--line); }

/* widgets */
[data-testid="stWidgetLabel"] p { font-weight: 600; font-size: .9rem; color: var(--ink); }
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"],
[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input {
  background: var(--card) !important; border-radius: 8px !important;
  border-color: var(--line) !important; color: var(--ink) !important; }
[data-baseweb="select"] > div:focus-within, [data-baseweb="input"]:focus-within {
  border-color: var(--moss) !important; box-shadow: 0 0 0 3px rgba(31,92,74,.18) !important; }
[data-testid="stNumberInput"] button { background: var(--card) !important; color: var(--ink) !important; }

/* primary button */
.stButton > button {
  width: 100%; margin-top: 1.4rem; padding: .9rem 1.2rem; border-radius: 10px; border: 0;
  background: var(--signal); color: var(--signal-ink);
  font: 700 1.05rem 'Bricolage Grotesque', sans-serif; letter-spacing: -0.01em;
  box-shadow: 0 3px 0 #b83a0c; transition: transform .12s ease, box-shadow .12s ease; }
.stButton > button:hover { background: #ff6c36; color: var(--signal-ink); transform: translateY(-1px);
  box-shadow: 0 4px 0 #b83a0c; }
.stButton > button:active { transform: translateY(2px); box-shadow: 0 1px 0 #b83a0c; }
.stButton > button:focus-visible { outline: 3px solid var(--moss); outline-offset: 3px; }

/* time budget strip */
.budget { display: flex; flex-wrap: wrap; gap: 1px; background: var(--line);
  border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin-top: 1.4rem; }
.budget div { flex: 1 1 120px; background: var(--card); padding: .7rem .9rem; }
.budget b { display: block; font: 700 1.5rem 'Bricolage Grotesque', sans-serif; letter-spacing: -0.02em; }
.budget span { font: 400 .7rem 'JetBrains Mono', monospace; letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted); }

/* generated plan */
.plan-head { display: flex; justify-content: space-between; align-items: baseline;
  margin: 2.6rem 0 .8rem; gap: 1rem; flex-wrap: wrap; }
.plan-head h2 { font: 800 1.9rem 'Bricolage Grotesque', sans-serif; letter-spacing: -0.03em; margin: 0; }
.plan-head code { font: 400 .75rem 'JetBrains Mono', monospace; color: var(--muted); background: none; }
.plan { background: var(--card); border: 1px solid var(--line); border-left: 6px solid var(--moss);
  border-radius: 12px; padding: 1.4rem 1.6rem; }
.plan h2 { font: 700 1.3rem 'Bricolage Grotesque', sans-serif; color: var(--moss);
  margin: 1.8rem 0 .6rem; padding-bottom: .4rem; border-bottom: 1px dashed var(--line); }
.plan h2:first-child { margin-top: 0; }
.plan strong { font-family: 'Bricolage Grotesque', sans-serif; }

@media (prefers-reduced-motion: reduce) { .stButton > button { transition: none; } }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- masthead
st.markdown(
    """
<div class="eyebrow">Personal plan generator</div>
<h1 class="title">Pick a skill.<br>Get a <em>day-by-day</em> plan.</h1>
<p class="lede">Tell it what you want to learn and how much time you have. It writes one plan,
with a task for every day and a checkpoint on your schedule.</p>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- provider + model
providers = []
if GOOGLE_API_KEY:
    providers.append("Google Gemini")
if OPENROUTER_API_KEY:
    providers.append("OpenRouter")

if not providers:
    st.error(
        "No API key found. Set `GOOGLE_API_KEY` and/or `OPENROUTER_API_KEY` in your `.env` "
        "file, or in Streamlit Cloud under Settings → Secrets."
    )
    st.stop()

st.markdown('<div class="label">Model</div>', unsafe_allow_html=True)
col_provider, col_model = st.columns([1, 2])
with col_provider:
    provider = st.selectbox("Provider", providers)

try:
    with st.spinner("Loading models available to your key…"):
        models = (
            list_gemini_models(GOOGLE_API_KEY)
            if provider == "Google Gemini"
            else list_openrouter_models(OPENROUTER_API_KEY)
        )
except Exception as exc:
    st.error(f"Could not load the {provider} model list: {exc}")
    st.stop()

if not models:
    st.error(f"{provider} returned no text models for this key.")
    st.stop()

with col_model:
    model_name = st.selectbox("Model", models, help=f"{len(models)} models available from {provider}.")

# ---------------------------------------------------------------- inputs
st.markdown('<div class="label">Your goal</div>', unsafe_allow_html=True)
col_cat, col_skill = st.columns([1, 2])
with col_cat:
    category = st.selectbox("Category", CATEGORIES)
with col_skill:
    skill = st.text_input("Skill to master", placeholder="e.g. Python for data analysis")

st.markdown('<div class="label">Your time</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    days_available = st.number_input("Days", min_value=1, max_value=365, value=30, step=1)
with c2:
    daily_time = st.number_input("Hours per day", min_value=1, max_value=24, value=2, step=1)
with c3:
    milestone_interval = st.number_input("Milestone every (days)", min_value=1, max_value=30, value=5, step=1)

total_hours = days_available * daily_time
milestones = days_available // milestone_interval
st.markdown(
    f"""
<div class="budget">
  <div><b>{total_hours}</b><span>Total hours</span></div>
  <div><b>{-(-days_available // 7)}</b><span>Weeks</span></div>
  <div><b>{milestones}</b><span>Milestones</span></div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- generate
if st.button("Generate my plan"):
    if not skill.strip():
        st.error("Enter the skill you want to master.")
    else:
        chain = plan_prompt | build_llm(provider, model_name) | StrOutputParser()
        try:
            with st.spinner(f"Writing your plan with {model_name}…"):
                plan = chain.invoke(
                    {
                        "skill": skill.strip(),
                        "category": category,
                        "days_available": days_available,
                        "daily_time": daily_time,
                        "milestone_interval": milestone_interval,
                    }
                ).strip()
        except Exception as exc:
            st.error(f"{provider} could not generate the plan with `{model_name}`: {exc}")
            st.stop()

        st.markdown(
            f'<div class="plan-head"><h2>{skill.strip()}</h2><code>{model_name}</code></div>',
            unsafe_allow_html=True,
        )
        with st.container(border=False):
            st.markdown(plan)
        st.download_button(
            "Download as Markdown", plan, file_name="plan.md", mime="text/markdown"
        )
