import streamlit as st
import streamlit.components.v1 as components

_SCROLL_SCRIPT = """<script>
setTimeout(() => {
  const el = window.parent.document.getElementById("plan-result");
  if (el) el.scrollIntoView({behavior: "smooth", block: "start"});
}, 100);
</script>"""


def render_result(result: dict, scroll: bool) -> None:
    """Render a generated plan; scroll=True jumps to it (right after generating)."""
    st.markdown(
        f'<div id="plan-result" class="plan-head"><h2>{result["skill"]}</h2><code>{result["model"]}</code></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=False):
        st.markdown(result["plan"])
    st.download_button(
        "Download as Markdown", result["plan"], file_name="plan.md", mime="text/markdown"
    )
    if scroll:
        components.html(_SCROLL_SCRIPT, height=0)
