"""
gemini_client.py
------------------
Thin wrapper around the Gemini API, shared by all agents.
Implements MOCK MODE: if no API key is configured, it returns simple
rule-based canned responses instead of calling the network.
"""

from config import MOCK_MODE, GEMINI_API_KEY, GEMINI_MODEL

if not MOCK_MODE:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)


class GeminiClient:
    def __init__(self):
        self.mock = MOCK_MODE
        if not self.mock:
            self.model = genai.GenerativeModel(GEMINI_MODEL)

    def simple_generate(self, prompt: str) -> str:
        """Single-turn text generation, no tool calling."""
        if self.mock:
            return self._mock_response(prompt)
        response = self.model.generate_content(prompt)
        return response.text

    def _mock_response(self, prompt: str) -> str:
        """
        Extremely simple rule-based stand-in used only when no API key is
        present, so the CLI demo still behaves sensibly offline.
        """
        lower = prompt.lower()
        if "emergency" in lower or "distress" in lower or "yes or no" in lower:
            return "YES"
        return "I'm here to help. (mock mode: connect a GEMINI_API_KEY for real responses)"