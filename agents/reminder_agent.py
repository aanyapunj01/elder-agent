"""
agents/reminder_agent.py
-------------------------
REMINDER AGENT
==============
Manages medication and appointment reminders for the user.
Owns its own state (a local JSON file) and exposes simple tools
(add / list / mark done / due_now) that the Orchestrator can call.
"""

import json
import os
import uuid
from datetime import datetime

from config import REMINDERS_FILE


class ReminderAgent:
    def __init__(self):
        self._ensure_store_exists()

    def _ensure_store_exists(self):
        os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
        if not os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, "w") as f:
                json.dump([], f)

    def _load(self):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)

    def _save(self, reminders):
        with open(REMINDERS_FILE, "w") as f:
            json.dump(reminders, f, indent=2, default=str)

    def add_reminder(self, title: str, time_str: str, category: str = "medication") -> dict:
        reminders = self._load()
        reminder = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "time": time_str,
            "category": category,
            "done": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        reminders.append(reminder)
        self._save(reminders)
        return reminder

    def list_reminders(self, only_pending: bool = True) -> list:
        reminders = self._load()
        if only_pending:
            return [r for r in reminders if not r["done"]]
        return reminders

    def mark_done(self, reminder_id: str) -> bool:
        reminders = self._load()
        for r in reminders:
            if r["id"] == reminder_id:
                r["done"] = True
                self._save(reminders)
                return True
        return False

    def due_now(self, current_time_hhmm: str) -> list:
        due = []
        for r in self.list_reminders(only_pending=True):
            stored_time = r["time"][-5:]
            if stored_time <= current_time_hhmm:
                due.append(r)
        return due