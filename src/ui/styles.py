from pathlib import Path

import streamlit as st

_CSS = (Path(__file__).parent / "styles.css").read_text(encoding="utf-8")


def inject_styles() -> None:
    st.markdown(f"<style>\n{_CSS}\n</style>", unsafe_allow_html=True)
