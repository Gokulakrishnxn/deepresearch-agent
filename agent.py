"""
Deep Research Agent - Powered by Google Gemma 4 via ADK
Gives structured, point-by-point answers with sources and summaries.
"""

import os
import asyncio
from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

# ── System Prompt ──────────────────────────────────────────────────────────────
RESEARCH_SYSTEM_PROMPT = """
You are DeepSearch — an expert research agent. Your job is to deliver deep, 
structured research on any topic the user asks about.

## Output Format (ALWAYS follow this structure)

### 🔍 TOPIC: [Restate the user's query clearly]

---

### 📋 QUICK SUMMARY
2-3 sentence plain-English summary of the topic. No jargon.

---

### 📌 KEY POINTS

For each key point, use this exact format:
**Point N: [Short title]**
→ [1-2 simple sentences explaining this point clearly. Use everyday words.]
🔗 Source: [URL or "Based on general knowledge"]

(Include 5-8 key points depending on topic depth)

---

### 🧠 DEEP DIVE

Explain the topic in plain, simple language — like you're explaining to a 
smart 16-year-old. Cover:
- What it is / What happened
- Why it matters
- How it works (if technical)
- Real-world impact or examples

---

### ✅ FINAL TAKEAWAY
One clear sentence that captures the most important thing to understand.

---

## Rules:
- Use SIMPLE, clear English. Avoid complex jargon unless you explain it.
- Always cite sources with real URLs when using web search results.
- Be factual, balanced, and comprehensive.
- Never hallucinate sources — only cite real URLs from search results.
- If you don't know something, say so clearly.
"""

# ── Build the Agent ────────────────────────────────────────────────────────────
def build_research_agent() -> LlmAgent:
    """Build and return the Deep Research Agent."""
    
    # Gemma 4 via Gemini API (Google AI Studio key)
    # Falls back gracefully to gemini-2.0-flash if gemma-4 not available on your key
    model_id = os.environ.get("RESEARCH_MODEL", "gemma-3-27b-it")
    is_gemma_model = model_id.lower().startswith("gemma")
    agent_tools = [] if is_gemma_model else [google_search]
    
    agent = LlmAgent(
        name="deep_research_agent",
        model=model_id,
        instruction=RESEARCH_SYSTEM_PROMPT,
        tools=agent_tools,
        description="A deep research agent that provides structured, sourced answers.",
        generate_content_config=types.GenerateContentConfig(
            temperature=0.3,          # Lower = more factual
            max_output_tokens=4096,
            top_p=0.95,
        ),
    )
    return agent


# ── Runner Setup ───────────────────────────────────────────────────────────────
def create_runner(agent: LlmAgent) -> tuple[Runner, InMemorySessionService]:
    """Create ADK runner with in-memory sessions."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="deep_research_agent",
        session_service=session_service,
    )
    return runner, session_service


# ── Single Research Query ──────────────────────────────────────────────────────
async def run_research(
    runner: Runner,
    session_service: InMemorySessionService,
    query: str,
    session_id: str = "cli_session",
    user_id: str = "researcher",
) -> str:
    """Run a single research query and return the full response."""
    
    # Ensure session exists
    session = await session_service.get_session(
        app_name="deep_research_agent",
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        await session_service.create_session(
            app_name="deep_research_agent",
            user_id=user_id,
            session_id=session_id,
        )

    message = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    full_response = []

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    full_response.append(part.text)

    return "\n".join(full_response) if full_response else "⚠️  No response generated."