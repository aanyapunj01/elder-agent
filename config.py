"""
config.py
---------
Central place for configuration and API-key loading.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env if present; does nothing if it's absent

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# If the key looks missing or is still the placeholder, we run in mock mode.
MOCK_MODE = (not GEMINI_API_KEY) or ("your_gemini_api_key_here" in GEMINI_API_KEY)

CAREGIVER_NAME = os.getenv("CAREGIVER_NAME", "Emergency Contact")
CAREGIVER_CONTACT = os.getenv("CAREGIVER_CONTACT", "unset")

GEMINI_MODEL = "gemini-2.0-flash"  # fast + cheap, good enough for routing + chat

REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "data", "reminders.json")