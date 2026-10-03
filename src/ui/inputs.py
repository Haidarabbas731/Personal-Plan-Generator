import streamlit as st

from ..config import CATEGORIES


def render_goal_inputs() -> tuple[str, str]:
    """Returns (category, skill)."""
    st.markdown('<div class="label">Your goal</div>', unsafe_allow_html=True)
    col_cat, col_skill = st.columns([1, 2])
    with col_cat:
        category = st.selectbox("Category", CATEGORIES)
    with col_skill:
        skill = st.text_input("Skill to master", placeholder="e.g. Python for data analysis")
    return category, skill


def render_time_inputs() -> tuple[int, int, int]:
    """Returns (days_available, daily_time, milestone_interval) and shows the time budget."""
    st.markdown('<div class="label">Your time</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        days_available = st.number_input("Days", min_value=1, max_value=365, value=30, step=1)
    with c2:
        daily_time = st.number_input("Hours per day", min_value=1, max_value=24, value=2, step=1)
    with c3:
        milestone_interval = st.number_input(
            "Milestone every (days)", min_value=1, max_value=30, value=5, step=1
        )

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
    return days_available, daily_time, milestone_interval
