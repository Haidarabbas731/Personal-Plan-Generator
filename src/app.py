import streamlit as st

from .config import PAGE_ICON, PAGE_TITLE
from .generator import PlanRequest, generate_plan
from .ui import (
    inject_styles,
    render_goal_inputs,
    render_header,
    render_model_picker,
    render_result,
    render_time_inputs,
)


def run() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")
    inject_styles()
    render_header()

    provider, model_name = render_model_picker()
    category, skill = render_goal_inputs()
    days_available, daily_time, milestone_interval = render_time_inputs()

    if st.button("Generate my plan"):
        if not skill.strip():
            st.error("Enter the skill you want to master.")
        else:
            request = PlanRequest(
                provider=provider,
                model=model_name,
                category=category,
                skill=skill.strip(),
                days_available=days_available,
                daily_time=daily_time,
                milestone_interval=milestone_interval,
            )
            try:
                with st.spinner(f"Writing your plan with {model_name}…"):
                    plan = generate_plan(request)
            except Exception as exc:
                st.error(f"{provider} could not generate the plan with `{model_name}`: {exc}")
                st.stop()

            # Keep the plan across reruns (e.g. clicking the download button).
            st.session_state["result"] = {
                "skill": request.skill,
                "model": model_name,
                "plan": plan,
            }
            st.session_state["scroll_to_plan"] = True

    result = st.session_state.get("result")
    if result:
        render_result(result, scroll=st.session_state.pop("scroll_to_plan", False))
