import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PAGE_TITLE = "Personal Plan Generator"
PAGE_ICON = "🧭"

GOOGLE = "Google Gemini"
OPENROUTER = "OpenRouter"

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
APP_PASSWORD = get_key("APP_PASSWORD")
