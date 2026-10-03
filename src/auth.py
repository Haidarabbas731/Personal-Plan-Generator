import hmac
import threading
import time

import streamlit as st

from .config import APP_PASSWORD

MAX_ATTEMPTS = 5
BASE_LOCKOUT_SECONDS = 5 * 60
MAX_LOCKOUT_SECONDS = 60 * 60


@st.cache_resource
def _guard() -> dict:
    """Server-wide attempt state, shared by every session (a refresh can't reset it)."""
    return {"lock": threading.Lock(), "failures": 0, "locked_until": 0.0}


def _format_wait(seconds: float) -> str:
    minutes, secs = divmod(int(seconds) + 1, 60)
    return f"{minutes}m {secs:02d}s" if minutes else f"{secs}s"


def require_password() -> None:
    """Block the app behind APP_PASSWORD. Returns only once the visitor is unlocked."""
    if st.session_state.get("authed"):
        return

    if not APP_PASSWORD:
        st.error("`APP_PASSWORD` is not set, so the app is locked. Set it in `.env` or Secrets.")
        st.stop()

    guard = _guard()
    remaining = guard["locked_until"] - time.time()
    locked = remaining > 0

    with st.form("login"):
        entered = st.text_input("Password", type="password", disabled=locked)
        submitted = st.form_submit_button("Unlock", disabled=locked)

    if submitted:
        with guard["lock"]:
            remaining = guard["locked_until"] - time.time()
            if remaining > 0:
                locked = True
            elif hmac.compare_digest(entered.encode(), APP_PASSWORD.encode()):
                guard["failures"] = 0
                st.session_state["authed"] = True
                st.rerun()
            else:
                guard["failures"] += 1
                over = guard["failures"] - MAX_ATTEMPTS
                if over >= 0:
                    lockout = min(BASE_LOCKOUT_SECONDS * 2**over, MAX_LOCKOUT_SECONDS)
                    guard["locked_until"] = time.time() + lockout
                    remaining = lockout
                    locked = True
                else:
                    st.error(f"Wrong password. {MAX_ATTEMPTS - guard["failures"]} attempt(s) left before a lockout.")

    if locked:
        st.error(f"Too many wrong attempts. Try again in {_format_wait(remaining)}.")
    st.stop()
