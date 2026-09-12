"""
pages/ai_assistant.py
---------------------
AI Assistant — Lightweight in-app AI advisor for B.Tech students.

The assistant is powered by an external API (OpenAI or Groq).
If no API key is configured, this page gracefully explains how to enable it.
No personal data is stored. No API keys are hard-coded.
"""

import streamlit as st
from utils.ai_assistant import is_ai_available, get_ai_status, ask_ai, build_context_from_data
from utils.data_loader import load_resources, load_skills, load_roadmaps
from components.section_header import section_header

# Example prompts to help students get started
EXAMPLE_PROMPTS = [
    "I'm a 2nd-year CSE student. I know Python basics. I want to become an AI Engineer. What should I learn next?",
    "I'm in ECE, 3rd year. I want to learn embedded systems. Where do I start?",
    "What are the best free resources to learn DSA for placements?",
    "I have 1 hour per day. I want to get an internship at a product company. Make me a 3-month plan.",
    "What skills should a Civil Engineering student build for a government job?",
    "Explain the difference between ML Engineer and Data Scientist.",
    "I'm a fresher ME student. Which software skills should I learn?",
]


def show() -> None:
    section_header("AI Assistant", "Your personalised B.Tech academic and career advisor.", "🤖")

    # ── Status banner ──────────────────────────────────────────────────────────
    status = get_ai_status()
    if is_ai_available():
        st.success(status)
    else:
        st.warning(status)
        st.markdown("""
**To enable the AI Assistant:**
1. Copy `.env.example` to `.env` in the project root.
2. Add your API key:
   - **OpenAI:** `OPENAI_API_KEY=sk-...`
   - **Groq (free tier):** `GROQ_API_KEY=gsk_...`
3. Set the key in your shell before running:
   ```
   # Windows PowerShell
   $env:OPENAI_API_KEY = "sk-..."
   streamlit run app.py
   ```
4. Restart the app.

> The rest of the application works normally without the AI assistant.
> Your API key is read from environment variables and is never stored in the project files.
        """)
        st.divider()
        st.subheader("💡 Can't enable AI right now?")
        st.markdown(
            "Use the **Career Roadmaps**, **Skills Hub**, and **Search** pages — "
            "they provide structured guidance without AI."
        )
        return

    # ── Load data context ──────────────────────────────────────────────────────
    resources = load_resources()
    skills    = load_skills()
    roadmaps  = load_roadmaps()
    context   = build_context_from_data(resources, skills, roadmaps)

    # ── Chat history in session state ──────────────────────────────────────────
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []

    # ── Example prompts ────────────────────────────────────────────────────────
    if not st.session_state.ai_chat_history:
        st.subheader("💬 Example questions to ask:")
        cols = st.columns(2)
        for i, prompt in enumerate(EXAMPLE_PROMPTS):
            with cols[i % 2]:
                if st.button(prompt[:70] + "…" if len(prompt) > 70 else prompt, key=f"ex_{i}"):
                    st.session_state.ai_prefill = prompt

    st.divider()

    # ── Display chat history ───────────────────────────────────────────────────
    for msg in st.session_state.ai_chat_history:
        role = msg["role"]
        with st.chat_message(role):
            st.markdown(msg["content"])

    # ── Input ──────────────────────────────────────────────────────────────────
    prefill = st.session_state.pop("ai_prefill", "")
    user_input = st.chat_input("Ask anything about your B.Tech journey…", key="ai_input")

    if not user_input and prefill:
        user_input = prefill

    if user_input:
        # Show user message
        st.session_state.ai_chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                response = ask_ai(
                    user_message=user_input,
                    context=context,
                    chat_history=st.session_state.ai_chat_history[:-1],
                )
            if response:
                st.markdown(response)
                st.session_state.ai_chat_history.append({"role": "assistant", "content": response})
            else:
                err = "Sorry, I couldn't get a response. Please check your API key and try again."
                st.error(err)

    # ── Clear chat ─────────────────────────────────────────────────────────────
    if st.session_state.ai_chat_history:
        if st.button("🗑️ Clear conversation", key="ai_clear"):
            st.session_state.ai_chat_history = []
            st.rerun()

    # ── Disclaimer ─────────────────────────────────────────────────────────────
    st.divider()
    st.caption(
        "⚠️ **Disclaimer:** The AI assistant may make mistakes. "
        "Always verify important information from official sources. "
        "This assistant does not store your conversation or personal details."
    )
