"""
utils/ai_assistant.py
---------------------
Lightweight AI Assistant for the B.Tech Student Super-Hub.

Architecture:
- Reads API key from environment variable OPENAI_API_KEY (or GROQ_API_KEY).
- If no key is set, the assistant falls back gracefully — the rest of the app
  continues to work normally.
- Does NOT hard-code any secrets.
- Uses the project's own resource/skill data as its primary knowledge base.
- Will NOT invent resource URLs — it pulls only from the local database.

Supported provider: OpenAI-compatible API (OpenAI, Groq, etc.)
To switch provider, change AI_PROVIDER in .env or set it as an env var.
"""

import os
from typing import Optional

# ── Configuration ──────────────────────────────────────────────────────────────
# Read from environment variables. Never set real keys here.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
AI_PROVIDER    = os.environ.get("AI_PROVIDER", "openai").lower()   # "openai" or "groq"
AI_MODEL       = os.environ.get("AI_MODEL", "gpt-4o-mini")         # default model

# Which key to use based on provider
_ACTIVE_KEY = GROQ_API_KEY if AI_PROVIDER == "groq" else OPENAI_API_KEY

# Base URLs
_BASE_URLS = {
    "openai": "https://api.openai.com/v1",
    "groq":   "https://api.groq.com/openai/v1",
}


def is_ai_available() -> bool:
    """Returns True if an API key is configured and the provider is recognised."""
    return bool(_ACTIVE_KEY) and AI_PROVIDER in _BASE_URLS


def get_ai_status() -> str:
    """Human-readable status string shown in the UI."""
    if not _ACTIVE_KEY:
        return "⚠️ AI Assistant is disabled — no API key configured. See `.env.example`."
    if AI_PROVIDER not in _BASE_URLS:
        return f"⚠️ Unknown AI_PROVIDER '{AI_PROVIDER}'. Set to 'openai' or 'groq'."
    return f"✅ AI Assistant enabled ({AI_PROVIDER} / {AI_MODEL})"


def _build_system_prompt(context: dict) -> str:
    """
    Builds the system prompt injecting the project's resource/skill data
    so the AI answers from our database rather than inventing content.

    context keys (all optional):
      resources_summary: list of {title, url, tags, skills, subjects}
      skills_summary:    flat list of skill name strings
      roadmap_roles:     list of role name strings
    """
    resources = context.get("resources_summary", [])
    skills    = context.get("skills_summary", [])
    roles     = context.get("roadmap_roles", [])

    res_text = "\n".join(
        f"- {r['title']} ({', '.join(r.get('tags', []))}) → {r['url']}"
        for r in resources[:60]   # cap to avoid token overflow
    ) or "No resources loaded."

    skills_text = ", ".join(skills[:80]) or "No skills loaded."
    roles_text  = ", ".join(roles) or "No roadmaps loaded."

    return f"""You are a helpful academic advisor for B.Tech engineering students in India.
You help students plan their learning path, discover skills, find resources, and prepare for careers.

IMPORTANT RULES:
1. Use ONLY the resources listed below when recommending learning materials.
   Do NOT invent or guess URLs. If no matching resource exists, say so clearly.
2. Be encouraging, concise and beginner-friendly.
3. Tailor advice to the student's branch, year, and goals.
4. Do not share personal data beyond what the student explicitly provides in this conversation.
5. Do not recommend paid resources unless the student asks or there is no free alternative.

AVAILABLE RESOURCES IN THE DATABASE:
{res_text}

AVAILABLE SKILLS:
{skills_text}

AVAILABLE CAREER ROADMAP ROLES:
{roles_text}

When suggesting resources, always include the exact URL from the database above.
When no database resource covers a topic, say: "I don't have a specific resource for this in the database yet, but you can search for it on NPTEL (nptel.ac.in) or freeCodeCamp (freecodecamp.org)."
"""


def ask_ai(
    user_message: str,
    context: dict,
    chat_history: list = None,
) -> Optional[str]:
    """
    Sends a message to the configured AI provider and returns the response text.

    Args:
        user_message:  The student's question/message.
        context:       Dict with resources_summary, skills_summary, roadmap_roles.
        chat_history:  List of {"role": "user"|"assistant", "content": str} dicts.

    Returns:
        The assistant's reply string, or None if the API call fails.
    """
    if not is_ai_available():
        return None

    try:
        import urllib.request
        import json as _json

        system_prompt = _build_system_prompt(context)
        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            messages.extend(chat_history[-10:])   # last 10 turns for context window

        messages.append({"role": "user", "content": user_message})

        payload = _json.dumps({
            "model": AI_MODEL,
            "messages": messages,
            "max_tokens": 800,
            "temperature": 0.4,
        }).encode("utf-8")

        base_url = _BASE_URLS[AI_PROVIDER]
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_ACTIVE_KEY}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = _json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()

    except Exception as exc:
        # Return a safe error message so the UI can display it
        return f"⚠️ AI request failed: {exc}"


def build_context_from_data(resources: list, skills: dict, roadmaps: dict) -> dict:
    """
    Converts the app's data structures into a compact context dict
    suitable for passing to ask_ai().

    Args:
        resources: full list from load_resources()
        skills:    full dict from load_skills()
        roadmaps:  full dict from load_roadmaps()
    """
    resources_summary = [
        {
            "title":    r.get("title", ""),
            "url":      r.get("url", ""),
            "tags":     r.get("tags", []),
            "skills":   r.get("skills", []),
            "subjects": r.get("subjects", []),
        }
        for r in resources
    ]

    all_skills = (
        skills.get("technical", [])
        + skills.get("career", [])
        + skills.get("life", [])
        + [s for branch_skills in skills.get("branch_specific", {}).values() for s in branch_skills]
    )

    return {
        "resources_summary": resources_summary,
        "skills_summary":    all_skills,
        "roadmap_roles":     list(roadmaps.keys()),
    }
