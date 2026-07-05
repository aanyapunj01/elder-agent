# CareCircle — Project Writeup

## Problem Statement

Millions of elderly and disabled people live independently but need support with two very different kinds of things every day: staying on top of routine tasks (medication, appointments), and having someone notice quickly if something goes wrong (a fall, a health scare). Family caregivers want to help but can't be present 24/7. Existing apps tend to solve only one of these problems at a time, and most assume a level of smartphone fluency that isn't a safe assumption for this user group. We wanted a single, conversational assistant that quietly handles both — one that talks like a person, not an app.

## Why Agents

A single chatbot answering "what's my next reminder?" doesn't need to be agentic — a lookup function would do. What makes this problem genuinely suited to an agentic approach is that the assistant has to make decisions no static script can, under real stakes:

- It has to notice an emergency embedded in an otherwise ordinary message, before doing anything else.
- It has to decide whether a distress signal is severe enough to escalate, weighing the cost of a false alarm against the cost of a missed one.
- It has to route between fundamentally different tasks (reminders vs. safety vs. casual conversation) using natural language, since the user won't navigate menus.

Splitting this into cooperating agents — rather than one large prompt — also means each piece can be reasoned about, tested, and improved independently.

## Solution Overview

CareCircle is built as three agents coordinated by an Orchestrator:

1. **Orchestrator Agent** — the single entry point for every user message. It enforces one hard rule above all else: check for an emergency first, on every message, no exceptions.
2. **Reminder Agent** — owns medication/appointment reminders as its own piece of state, exposing simple tools (add, list, mark done, check what's due).
3. **Emergency Agent** — runs a two-stage safety check: a fast local keyword screen, followed by an LLM confirmation step only when the screen trips.

## Architecture

See the diagram in README.md. Every message flows through the Orchestrator, which always checks the Emergency Agent first, then routes to either the Reminder Agent or a general conversational reply.

## The Journey

I started by asking what would make this genuinely agent-shaped rather than just an LLM wrapper, and landed on the safety-first routing decision as the core design commitment. I deliberately scoped down from a larger multi-agent idea (which would have added home automation and dedicated communication agents) to 3 agents, choosing depth over breadth given the project timeline. During development, I hit a real-world snag: Google's free-tier Gemini quota was unavailable on my account during testing, so the system includes a mock mode that lets it run and demo fully offline with zero cost — this turned into a genuine design strength rather than just a workaround, since it means anyone can clone and run the project immediately.

## Build Notes

Built in Python using the Gemini API (`gemini-2.0-flash`) for language understanding, with a local JSON store for reminder persistence and a CLI standing in for a future voice interface.