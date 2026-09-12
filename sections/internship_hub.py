"""
pages/internship_hub.py
-----------------------
Internship Hub — India and global internship platforms with tips.
"""

import streamlit as st
from utils.data_loader import load_internships
from components.section_header import section_header


def _card(item: dict) -> None:
    with st.container(border=True):
        col1, col2 = st.columns([0.82, 0.18])
        with col1:
            st.markdown(f"**[{item['name']}]({item['url']})**")
        with col2:
            st.caption(item.get("type", "Platform"))
        if item.get("description"):
            st.caption(item["description"])
        tags = item.get("tags", [])
        if tags:
            st.markdown(" ".join(f"`{t}`" for t in tags))


def show() -> None:
    section_header("Internship Hub", "Find internships in India and globally — plus tips to get selected.", "💼")

    data = load_internships()
    india   = data.get("india", [])
    global_ = data.get("global", [])
    tips    = data.get("tips", [])

    col1, col2 = st.columns(2)
    col1.metric("🇮🇳 India Platforms", len(india))
    col2.metric("🌐 Global Platforms", len(global_))

    st.divider()

    tabs = st.tabs(["🇮🇳 India", "🌐 Global", "💡 Tips & Strategy"])

    with tabs[0]:
        st.subheader("India Internship Platforms")
        for item in india:
            _card(item)

    with tabs[1]:
        st.subheader("Global Internship Platforms")
        for item in global_:
            _card(item)

    with tabs[2]:
        st.subheader("How to Land Your First Internship")
        for tip in tips:
            st.markdown(f"✅ {tip}")
        st.divider()
        st.markdown("""
**Internship Timeline for B.Tech Students:**

| Year | What to Do |
|---|---|
| Year 1 | Build foundational skills — C, Python, Web basics |
| Year 2 | First internship (start/summer), build 1–2 projects |
| Year 3 | Core internship — target your domain, contribute to open source |
| Year 4 | Pre-placement offers (PPO), final placements, or higher studies prep |
        """)
