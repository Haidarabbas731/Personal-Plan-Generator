import streamlit as st


def render_header() -> None:
    st.markdown(
        """
<div class="eyebrow">Personal plan generator</div>
<h1 class="title">Pick a skill.<br>Get a <em>day-by-day</em> plan.</h1>
<p class="lede">Tell it what you want to learn and how much time you have. It writes one plan,
with a task for every day and a checkpoint on your schedule.</p>
""",
        unsafe_allow_html=True,
    )
