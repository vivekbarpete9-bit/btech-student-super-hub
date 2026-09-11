"""
pages/career_roadmaps.py
------------------------
Career Roadmaps — Step-by-step learning roadmaps for 22 roles.
"""

import streamlit as st
from utils.data_loader import load_roadmaps, get_resources_by_ids
from components.section_header import section_header
from components.resource_card import resource_card


def show() -> None:
    section_header("Career Roadmaps", "Step-by-step paths to your dream role — curated for B.Tech students.", "🗺️")

    roadmaps = load_roadmaps()
    if not roadmaps:
        st.error("Could not load roadmaps data.")
        return

    role_names = list(roadmaps.keys())
    if not role_names:
        st.info("No roadmaps available yet.")
        return

    col_sel, col_ext = st.columns([0.65, 0.35])
    with col_sel:
        selected_role = st.selectbox("Select a career role", role_names, key="rm_role")
    with col_ext:
        if selected_role:
            ext_url = roadmaps[selected_role].get("external_roadmap", "")
            if ext_url:
                st.markdown(f"\n\n🔗 [View full interactive roadmap on roadmap.sh]({ext_url})")

    if not selected_role:
        return

    roadmap = roadmaps[selected_role]
    st.caption(roadmap.get("description", ""))
    st.divider()

    steps = roadmap.get("steps", [])
    if not steps:
        st.info("Roadmap steps coming soon for this role.")
        return

    st.subheader(f"🗺️ Roadmap: {selected_role}")

    for step in steps:
        num   = step.get("step", "?")
        title = step.get("title", "")
        detail = step.get("detail", "")
        res_ids = step.get("resource_ids", [])

        with st.container(border=True):
            cols = st.columns([0.08, 0.92])
            with cols[0]:
                st.markdown(f"### {num}")
            with cols[1]:
                st.markdown(f"**{title}**")
                if detail:
                    st.caption(detail)

                if res_ids:
                    resources = get_resources_by_ids(res_ids)
                    if resources:
                        with st.expander(f"📚 {len(resources)} Resource(s)"):
                            for res in resources:
                                resource_card(res)

    st.divider()
    st.subheader("📋 All Available Roadmaps")
    cols = st.columns(3)
    for idx, (role, data) in enumerate(roadmaps.items()):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"**{role}**")
                desc = data.get("description", "")
                st.caption(desc[:80] + ("…" if len(desc) > 80 else ""))
                ext = data.get("external_roadmap", "")
                if ext:
                    st.markdown(f"[roadmap.sh →]({ext})")
