"""
app.py
------
B.Tech Student Super-Hub — Main Entry Point

Configures the Streamlit app and the sidebar navigation.
Each section is a separate page module in pages/.
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
from pages.dashboard          import show as show_dashboard
from pages.academic_hub       import show as show_academic_hub
from pages.skills_hub         import show as show_skills_hub
from pages.learning_resources import show as show_learning_resources
from pages.coding_practice    import show as show_coding_practice
from pages.project_hub        import show as show_project_hub
from pages.courses_certificates import show as show_courses
from pages.internship_hub     import show as show_internship_hub
from pages.jobs_hub           import show as show_jobs_hub
from pages.career_roadmaps    import show as show_career_roadmaps
from pages.skill_tracker      import show as show_skill_tracker
from pages.daily_tasks        import show as show_daily_tasks
from pages.life_career_skills import show as show_life_career_skills
from pages.ai_assistant       import show as show_ai_assistant
from pages.search             import show as show_search

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
