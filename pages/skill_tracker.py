"""
pages/skill_tracker.py
----------------------
Personal Skill Tracker — Track learning status, progress, certificates and projects.
"""

import streamlit as st
from utils.data_loader import load_skills
from utils.tracker_utils import (
    load_tracker, update_skill, remove_skill, get_skill_entry
)
from utils.filters import SKILL_STATUSES
from components.section_header import section_header
from components.progress_bar import skill_progress_bar


STATUS_EMOJI = {
    "Not Started": "⭕",
    "Learning":    "📖",
    "Practicing":  "🔧",
    "Completed":   "✅",
}


def _all_skill_names(skills_data: dict) -> list:
    """Returns a flat sorted list of all skill names across all categories."""
    names = set(skills_data.get("technical", []))
    names.update(skills_data.get("career", []))
    names.update(skills_data.get("life", []))
    for branch_skills in skills_data.get("branch_specific", {}).values():
        names.update(branch_skills)
    return sorted(names)


def _safe_key(skill_name: str) -> str:
    """Converts a skill name into a valid Streamlit widget key (no special chars)."""
    return skill_name.replace(" ", "_").replace("+", "plus").replace("/", "_").replace("(", "").replace(")", "").replace("&", "and").replace(".", "")


def show() -> None:
    section_header("Personal Skill Tracker", "Track your skills, certificates and project completions.", "📈")

    skills_data = load_skills()
    tracker     = load_tracker()
    tracked     = tracker.get("skills", {})

    all_skills = _all_skill_names(skills_data)

    # ── Add a new skill ────────────────────────────────────────────────────────
    st.subheader("➕ Add a Skill to Track")
    col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
    with col1:
        untracked = [s for s in all_skills if s not in tracked]
        new_skill = st.selectbox("Choose a skill", ["— select —"] + untracked, key="tracker_new_skill")
    with col2:
        new_status = st.selectbox("Status", SKILL_STATUSES, key="tracker_new_status")
    with col3:
        st.write("")
        st.write("")
        if st.button("Add Skill", key="tracker_add_btn") and new_skill != "— select —":
            update_skill(new_skill, status=new_status, progress=0)
            st.success(f"Added **{new_skill}**!")
            st.rerun()

    st.divider()

    # ── Tracked skills dashboard ───────────────────────────────────────────────
    if not tracked:
        st.info("No skills tracked yet. Add your first skill above!")
        return

    # Summary stats
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tracked", len(tracked))
    c2.metric("Completed", sum(1 for e in tracked.values() if e.get("status") == "Completed"))
    c3.metric("Certificates Earned", sum(1 for e in tracked.values() if e.get("certificate_earned")))
    c4.metric("Projects Done", sum(1 for e in tracked.values() if e.get("project_completed")))

    st.divider()
    st.subheader("📊 Your Skills")

    # Filter by status
    status_filter = st.radio("Show", ["All"] + SKILL_STATUSES, horizontal=True, key="tracker_filter")

    for skill_name, entry in list(tracked.items()):
        if status_filter != "All" and entry.get("status") != status_filter:
            continue

        status = entry.get("status", "Not Started")
        progress = entry.get("progress", 0)

        sk = _safe_key(skill_name)
        with st.container(border=True):
            row1, row2 = st.columns([0.8, 0.2])
            with row1:
                st.markdown(f"**{STATUS_EMOJI.get(status, '')} {skill_name}**")
            with row2:
                if st.button("Remove", key=f"remove_{sk}"):
                    remove_skill(skill_name)
                    st.rerun()

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                new_status_val = st.selectbox(
                    "Status", SKILL_STATUSES,
                    index=SKILL_STATUSES.index(status) if status in SKILL_STATUSES else 0,
                    key=f"status_{sk}"
                )
            with col_b:
                new_prog = st.slider("Progress %", 0, 100, progress, step=5, key=f"prog_{sk}")
            with col_c:
                cert  = st.checkbox("🏅 Certificate", value=entry.get("certificate_earned", False), key=f"cert_{sk}")
                proj  = st.checkbox("🛠️ Project done", value=entry.get("project_completed", False), key=f"proj_{sk}")
                course = st.checkbox("📚 Course done", value=entry.get("course_completed", False), key=f"course_{sk}")

            notes = st.text_input("Notes", value=entry.get("notes", ""), key=f"notes_{sk}", label_visibility="collapsed", placeholder="Notes…")

            if st.button("Save", key=f"save_{sk}"):
                update_skill(
                    skill_name,
                    status=new_status_val,
                    progress=new_prog,
                    notes=notes,
                    certificate_earned=cert,
                    project_completed=proj,
                    course_completed=course,
                )
                st.success("Saved!")
                st.rerun()

            # Progress bar
            skill_progress_bar(skill_name, new_prog)
