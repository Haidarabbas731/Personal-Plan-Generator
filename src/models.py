import requests
import streamlit as st
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openrouter import ChatOpenRouter

from .config import GOOGLE, GOOGLE_API_KEY, OPENROUTER_API_KEY


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
    if provider == GOOGLE:
        return ChatGoogleGenerativeAI(model=model, google_api_key=GOOGLE_API_KEY)
    return ChatOpenRouter(model=model, api_key=OPENROUTER_API_KEY)

