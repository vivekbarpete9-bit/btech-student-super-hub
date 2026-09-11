"""
components/progress_bar.py
--------------------------
Renders a labelled skill progress bar.

Used by the Skill Tracker and Dashboard pages.
"""

import streamlit as st


def skill_progress_bar(skill_name: str, progress: int, notes: str = "") -> None:
    """
    Renders a skill name with a progress bar (0–100%) and optional notes.

    Args:
        skill_name: name of the skill (e.g. "DSA")
        progress: integer 0 to 100 representing completion percentage
        notes: optional short text note about the skill
    """
    # Clamp to valid range
    progress = max(0, min(100, progress))

    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.markdown(f"**{skill_name}**")
        st.progress(progress / 100)
    with col2:
        st.metric(label="Progress", value=f"{progress}%")
        if notes:
            st.caption(notes)
