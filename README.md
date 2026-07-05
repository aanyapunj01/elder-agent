# CareCircle — Multi-Agent Assistant for Elderly & Disabled Users

**Track:** Agents for Good
**Submission for:** AI Agents: Intensive Vibe Coding Capstone Project (Kaggle)

## The Problem

Elderly and disabled people frequently manage complex daily routines — medication schedules, appointments, and their own physical safety — often alone, or with family caregivers who cannot be present around the clock. Missed medication and undetected falls are two of the most common, preventable causes of hospitalization in this population. Existing solutions are usually single-purpose (a pill reminder app, or a fall sensor) and don't combine routine support with safety monitoring in one simple, conversational interface that doesn't require technical literacy.

## The Solution

**CareCircle** is a multi-agent assistant that a user talks to naturally (by text here, by voice in a full product) and which quietly handles two things in the background: staying on top of their reminders, and watching for signs of a genuine emergency — escalating to a caregiver immediately if one is detected.

It is built as **three cooperating agents** rather than one monolithic chatbot, because each responsibility has genuinely different priorities, latency needs, and failure tolerance:

| Agent | Responsibility | Why it's separate |
|---|---|---|
| **Orchestrator Agent** | Routes every message, always checks for emergencies first | Central place where the "safety-first" policy is enforced |
| **Reminder Agent** | Stores/retrieves medication & appointment reminders | Owns its own persistent state; simple, auditable tool interface |
| **Emergency Agent** | Screens for distress signals, confirms severity, escalates to caregiver | Needs a fast cheap filter + a slower accurate confirmation step |

## Architecture
              ┌─────────────────────┐
    User input   │   Orchestrator Agent │
   ─────────────▶│  (routes & prioritizes) │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
 ┌────────────────┐ ┌────────────────┐ ┌─────────────────┐
 │ Emergency Agent │ │ Reminder Agent │ │  General Chat   │
 │ (checked FIRST) │ │ (add/list)     │ │  (Gemini LLM)   │
 └────────┬────────┘ └────────────────┘ └─────────────────┘
          │
          ▼
 Simulated caregiver alert
 (SMS/call integration point for future work)
**Safety-first routing:** the Orchestrator always runs the Emergency Agent's screen on every message before deciding anything else. **Two-stage emergency detection:** a cheap keyword screen gates a slower, more accurate LLM confirmation call.

## The Build

- **Language:** Python 3
- **LLM:** Google Gemini via `google-generativeai` SDK
- **Persistence:** local JSON file for reminders
- **Interface:** CLI, standing in for a future voice interface
- **Mock mode:** if no `GEMINI_API_KEY` is configured, falls back to simple rule-based responses so the project runs with zero setup or cost

## Setup & Running

```bash
git clone https://github.com/aanyapunj01/elder-agent.git
cd elder-agent
pip install -r requirements.txt
copy .env.example .env
```
Then edit `.env` and add your own Gemini API key (free tier at aistudio.google.com/app/apikey).

```bash
python main.py
```

Try:
- `Remind me to take my blood pressure tablet at 09:00`
- `What reminders do I have?`
- `I fell down and I can't get up` (triggers emergency escalation)
- `How are you today?` (general chat fallback)

## Known Limitations & Future Work

- Emergency escalation is simulated (printed/logged), not wired to a real SMS/voice API — Twilio integration is a natural next step.
- Time parsing for reminders is lightweight for demo purposes.
- Voice input/output is the natural next layer on top of this text-based core.
- No authentication/multi-user support yet.

## Responsible AI Notes

- No API keys or secrets are committed (`.env` is git-ignored).
- Emergency screening errs on the side of caution given real-world stakes.