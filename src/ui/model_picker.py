import streamlit as st

from ..config import GOOGLE, GOOGLE_API_KEY, OPENROUTER, OPENROUTER_API_KEY
from ..models import list_gemini_models, list_openrouter_models


def render_model_picker() -> tuple[str, str]:
    """Show provider + model selectors. Returns (provider, model); stops the app on error."""
    providers = []
    if GOOGLE_API_KEY:
        providers.append(GOOGLE)
    if OPENROUTER_API_KEY:
        providers.append(OPENROUTER)

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
                if provider == GOOGLE
                else list_openrouter_models(OPENROUTER_API_KEY)
            )
    except Exception as exc:
        st.error(f"Could not load the {provider} model list: {exc}")
        st.stop()

    if not models:
        st.error(f"{provider} returned no text models for this key.")
        st.stop()

    with col_model:
        model_name = st.selectbox(
            "Model", models, help=f"{len(models)} models available from {provider}."
        )
    return provider, model_name
