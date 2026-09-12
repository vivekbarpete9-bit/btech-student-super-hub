"""
app.py
------
B.Tech Student Super-Hub — Main Entry Point

Configures the Streamlit app and the sidebar navigation.
Each section is a separate page module in sections/.

NOTE: Page modules live in `sections/` (NOT `pages/`) to avoid Streamlit's
built-in multipage auto-discovery, which would register every file in a
`pages/` directory as a separate URL route and produce blank pages (the
module-level code runs but show() is never called by Streamlit's runner).
"""

import streamlit as st

# ─── Page config (must be the very first Streamlit call) ───────────────────────
st.set_page_config(
    page_title="B.Tech Student Super-Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Import page modules ───────────────────────────────────────────────────────
from sections.dashboard          import show as show_dashboard
from sections.academic_hub       import show as show_academic_hub
from sections.skills_hub         import show as show_skills_hub
from sections.learning_resources import show as show_learning_resources
from sections.coding_practice    import show as show_coding_practice
from sections.project_hub        import show as show_project_hub
from sections.courses_certificates import show as show_courses
from sections.internship_hub     import show as show_internship_hub
from sections.jobs_hub           import show as show_jobs_hub
from sections.career_roadmaps    import show as show_career_roadmaps
from sections.skill_tracker      import show as show_skill_tracker
from sections.daily_tasks        import show as show_daily_tasks
from sections.life_career_skills import show as show_life_career_skills
from sections.ai_assistant       import show as show_ai_assistant
from sections.search             import show as show_search

# ─── Navigation map ────────────────────────────────────────────────────────────
PAGES = {
    "🏠 Dashboard":             show_dashboard,
    "📚 Academic Hub":          show_academic_hub,
    "🛠️ Skills Hub":            show_skills_hub,
    "📖 Learning Resources":    show_learning_resources,
    "💻 Coding & Practice":     show_coding_practice,
    "🚀 Project Hub":           show_project_hub,
    "🏆 Courses & Certificates": show_courses,
    "💼 Internship Hub":        show_internship_hub,
    "👔 Jobs Hub":              show_jobs_hub,
    "🗺️ Career Roadmaps":       show_career_roadmaps,
    "📈 Skill Tracker":         show_skill_tracker,
    "📅 Daily Tasks":           show_daily_tasks,
    "🌱 Life & Career Skills":  show_life_career_skills,
    "🤖 AI Assistant":          show_ai_assistant,
    "🔍 Search":                show_search,
}

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎓 B.Tech Super-Hub")
    st.caption("Your all-in-one student companion")
    st.divider()

    page_names = list(PAGES.keys())
    selected = st.radio(
        "Navigate to",
        options=page_names,
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Phase 2 — Full Feature Release")

# ─── Render selected page ───────────────────────────────────────────────────────
page_fn = PAGES.get(selected)
if page_fn is not None:
    page_fn()
