"""
pages/dashboard.py
------------------
Dashboard — Home page of the B.Tech Student Super-Hub.
"""

import streamlit as st
from utils.data_loader import (
    load_branches, load_resources, load_skills, load_tracker,
    load_platforms, load_youtube_channels, load_roadmaps
)
from components.section_header import section_header
from components.progress_bar import skill_progress_bar


def show() -> None:
    section_header(
        title="Welcome to B.Tech Student Super-Hub",
        subtitle="Your all-in-one companion for academics, skills, and career.",
        icon="🏠",
    )

    # ── Quick stats row ────────────────────────────────────────────────────────
    branches   = load_branches()
    resources  = load_resources()
    skills_data = load_skills()
    platforms  = load_platforms()
    channels   = load_youtube_channels()
    roadmaps   = load_roadmaps()

    total_subjects = sum(
        len(sem_data.get("subjects", []))
        for branch in branches.values()
        for year in branch.get("years", {}).values()
        for sem_data in year.get("semesters", {}).values()
    )

    all_skills_count = (
        len(skills_data.get("technical", []))
        + len(skills_data.get("career", []))
        + len(skills_data.get("life", []))
        + sum(len(v) for v in skills_data.get("branch_specific", {}).values())
    )

    tracker      = load_tracker()
    tasks_done   = len(tracker.get("completed_tasks", []))

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("🏛️ Branches", len(branches))
    col2.metric("📖 Resources", len(resources))
    col3.metric("📚 Subjects", total_subjects)
    col4.metric("🛠️ Skills", all_skills_count)
    col5.metric("🌐 Platforms", len(platforms))
    col6.metric("🗺️ Roadmaps", len(roadmaps))

    st.divider()

    # ── What's inside ─────────────────────────────────────────────────────────
    st.subheader("📌 What's Inside")
    sections = [
        ("📚", "Academic Hub",          "Browse by Branch → Year → Semester → Subject."),
        ("🛠️", "Skills Hub",            "Technical, branch-specific, career & life skills."),
        ("📖", "Learning Resources",    "Platforms and YouTube channels — filtered by tag."),
        ("💻", "Coding & Practice",     "LeetCode, HackerRank, CodeChef & more."),
        ("🚀", "Project Hub",           "Project ideas, build tools, hackathons."),
        ("🏆", "Courses & Certificates","Free and paid courses with certifications."),
        ("💼", "Internship Hub",        "India & global internship platforms + tips."),
        ("👔", "Jobs Hub",              "Job platforms India & global + prep checklist."),
        ("🗺️", "Career Roadmaps",       "Step-by-step paths for 22+ roles."),
        ("📈", "Skill Tracker",         "Track your personal learning progress."),
        ("📅", "Daily Tasks",           "Daily micro-tasks to build skills consistently."),
        ("🌱", "Life & Career Skills",  "Soft skills, finance, communication."),
        ("🤖", "AI Assistant",          "Personalised advice powered by AI."),
        ("🔍", "Search",                "Find any resource across the entire hub."),
    ]
    cols = st.columns(3)
    for idx, (icon, name, desc) in enumerate(sections):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"**{icon} {name}**")
                st.caption(desc)

    st.divider()

    # ── Skill progress snapshot ────────────────────────────────────────────────
    tracked_skills = tracker.get("skills", {})

    if tracked_skills or tasks_done:
        st.subheader("📈 Your Progress Snapshot")
        snap_cols = st.columns(3)
        snap_cols[0].metric("Skills Tracked", len(tracked_skills))
        snap_cols[1].metric("Skills Completed", sum(1 for v in tracked_skills.values() if v.get("status") == "Completed"))
        snap_cols[2].metric("Tasks Done", tasks_done)

    if tracked_skills:
        in_progress = {k: v for k, v in tracked_skills.items() if v.get("status") != "Completed"}
        completed   = {k: v for k, v in tracked_skills.items() if v.get("status") == "Completed"}

        if in_progress:
            st.caption("In progress:")
            for skill_name, info in list(in_progress.items())[:5]:
                skill_progress_bar(skill_name, info.get("progress", 0), info.get("notes", ""))

        if completed:
            st.caption(f"✅ {len(completed)} skill(s) completed.")
    else:
        with st.container(border=True):
            st.info("🌱 No skills tracked yet. Go to **📈 Skill Tracker** to start tracking your progress.")

    st.divider()

    # ── Getting started ────────────────────────────────────────────────────────
    st.subheader("🚀 Getting Started")
    st.markdown("""
1. Go to **📚 Academic Hub** — select your branch, year and semester.
2. Visit **🛠️ Skills Hub** to explore technical and career skills.
3. Browse **📖 Learning Resources** for platforms and YouTube channels.
4. Check **🗺️ Career Roadmaps** for a step-by-step path to your target role.
5. Track your learning in **📈 Skill Tracker**.
6. Use **🤖 AI Assistant** for personalised advice (requires API key).
    """)
