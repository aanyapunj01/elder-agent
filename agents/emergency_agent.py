"""
agents/emergency_agent.py
---------------------------
EMERGENCY / WELLBEING AGENT
===========================
Notices when the user's message suggests distress, illness, or danger,
and escalates to a human caregiver.

Design: keyword pre-filter + LLM confirmation.
A cheap local keyword screen catches likely distress signals fast.
Only if that screen trips does it ask the LLM to confirm severity,
before triggering an escalation. This avoids both false positives from
naive keyword matching and the cost/latency of calling an LLM on every
single message.

IMPORTANT: escalation here is SIMULATED (printed + logged). Wiring this
to a real SMS/call API (e.g. Twilio) is documented as a next step.
"""

from config import CAREGIVER_NAME, CAREGIVER_CONTACT

DISTRESS_KEYWORDS = [
    "fell", "fallen", "can't breathe", "chest pain", "help me",
    "dizzy", "faint", "hurt", "bleeding", "emergency", "call ambulance",
    "i am scared", "i'm scared", "not feeling well", "very sick",
]


class EmergencyAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.log = []

    def screen(self, user_message: str) -> bool:
        """Fast local keyword pre-filter."""
        text = user_message.lower()
        return any(keyword in text for keyword in DISTRESS_KEYWORDS)

    def confirm_severity(self, user_message: str) -> bool:
        """Ask the LLM to confirm whether this is a genuine emergency."""
        if self.llm_client is None:
            return True

        prompt = (
            "A person said the following message. Decide if it genuinely "
            "indicates a real health or safety emergency requiring immediate "
            "caregiver notification. Answer with only YES or NO.\n\n"
            f"Message: \"{user_message}\""
        )
        response = self.llm_client.simple_generate(prompt).strip().upper()
        return response.startswith("YES")

    def escalate(self, user_message: str) -> dict:
        """Simulated escalation: logs/prints instead of calling a real API."""
        alert = {
            "to": CAREGIVER_NAME,
            "contact": CAREGIVER_CONTACT,
            "message": f"ALERT: possible emergency detected. User said: \"{user_message}\"",
        }
        self.log.append(alert)
        print("\n[EMERGENCY AGENT] Escalation triggered!")
        print(f"    -> Notifying {alert['to']} ({alert['contact']})")
        print(f"    -> Message: {alert['message']}\n")
        return alert

    def handle(self, user_message: str):
        """Full pipeline: screen -> confirm -> escalate."""
        if not self.screen(user_message):
            return None
        if self.confirm_severity(user_message):
            return self.escalate(user_message)
        return None