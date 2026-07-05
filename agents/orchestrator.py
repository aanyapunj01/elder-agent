"""
agents/orchestrator.py
------------------------
ORCHESTRATOR AGENT
===================
The "front door" agent. Every user message passes through here first.
It decides which specialist agent(s) should handle it, then combines
their outputs into one natural reply.

Routing order matters:
  1. Emergency Agent is ALWAYS consulted first, regardless of what else
     the message is about. Safety takes priority over convenience.
  2. If no emergency, the Orchestrator classifies intent (reminder vs.
     general chat) and routes accordingly.
  3. If nothing matches a specialist, it falls back to a normal
     conversational reply from the LLM itself.
"""

from agents.reminder_agent import ReminderAgent
from agents.emergency_agent import EmergencyAgent
from gemini_client import GeminiClient


class Orchestrator:
    def __init__(self):
        self.llm = GeminiClient()
        self.reminder_agent = ReminderAgent()
        self.emergency_agent = EmergencyAgent(llm_client=self.llm)

    def handle_message(self, user_message: str) -> str:
        # --- Step 1: safety first, always ---
        alert = self.emergency_agent.handle(user_message)
        if alert:
            return (
                f"I noticed you might be in distress. I've alerted "
                f"{alert['to']} right away. Please stay where you are if "
                f"you can — help is being contacted."
            )

        # --- Step 2: classify intent for routing ---
        intent = self._classify_intent(user_message)

        if intent == "add_reminder":
            return self._handle_add_reminder(user_message)
        elif intent == "list_reminders":
            return self._handle_list_reminders()
        else:
            return self._handle_general_chat(user_message)

    # ---------- intent classification ----------

    def _classify_intent(self, user_message: str) -> str:
        lower = user_message.lower()
        if any(w in lower for w in ["remind", "medicine", "medication", "appointment", "tablet", "pill"]):
            if any(w in lower for w in ["what", "list", "show", "do i have"]):
                return "list_reminders"
            return "add_reminder"
        return "general_chat"

    # ---------- specialist handlers ----------

    def _handle_add_reminder(self, user_message: str) -> str:
        prompt = (
            "Extract a short reminder title and a time (HH:MM, 24hr) from "
            f"this message. Reply ONLY as 'TITLE | HH:MM'.\nMessage: \"{user_message}\""
        )
        result = self.llm.simple_generate(prompt)

        try:
            title, time_str = [part.strip() for part in result.split("|")]
        except ValueError:
            title, time_str = user_message, "09:00"

        reminder = self.reminder_agent.add_reminder(title=title, time_str=time_str)
        return f"Got it — I've set a reminder: \"{reminder['title']}\" at {reminder['time']}."

    def _handle_list_reminders(self) -> str:
        reminders = self.reminder_agent.list_reminders()
        if not reminders:
            return "You have no pending reminders right now."
        lines = [f"- {r['title']} at {r['time']}" for r in reminders]
        return "Here are your pending reminders:\n" + "\n".join(lines)

    def _handle_general_chat(self, user_message: str) -> str:
        prompt = (
            "You are a warm, patient voice assistant for an elderly or "
            "disabled user. Keep replies short, clear, and kind, avoiding "
            f"jargon.\n\nUser: {user_message}"
        )
        return self.llm.simple_generate(prompt)