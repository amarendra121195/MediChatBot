EURI_API_KEY="euri-088f3f95ae17e68a8a5703efcddf13e801566cde7521d2d26a1ee9162380970b"



# EURI_API_KEY = "euri-0e6c51b589d3c68ac63a1d98a720cfe69eaf67395ecbfcf2468bcb4b7f6e2420"
try:
    # Preferred: put {"EURI_API_KEY": "..." } in .streamlit/secrets.toml
    import streamlit as st  # noqa: F401
    from streamlit import secrets
    EURI_API_KEY = secrets.get("euri-088f3f95ae17e68a8a5703efcddf13e801566cde7521d2d26a1ee9162380970b") or ""
except Exception:
    # Fallback to hardcoded default (replace with a safe value or leave empty)
    EURI_API_KEY = "euri-088f3f95ae17e68a8a5703efcddf13e801566cde7521d2d26a1ee9162380970b" # ← put your key here if you aren't using secrets