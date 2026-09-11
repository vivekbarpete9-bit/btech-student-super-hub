"""
pages/jobs_hub.py
-----------------
Jobs Hub — India and global job platforms plus preparation tips.
"""

import streamlit as st
from utils.data_loader import load_jobs
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
    section_header("Jobs Hub", "Explore job platforms in India and globally — and learn how to prepare.", "👔")

    data = load_jobs()
    india   = data.get("india", [])
    global_ = data.get("global", [])
    tips    = data.get("tips", [])

    col1, col2 = st.columns(2)
    col1.metric("🇮🇳 India Job Platforms", len(india))
    col2.metric("🌐 Global Job Platforms", len(global_))

    st.divider()

    tabs = st.tabs(["🇮🇳 India", "🌐 Global", "💡 Preparation Tips"])

    with tabs[0]:
        st.subheader("India Job Platforms")
        for item in india:
            _card(item)

    with tabs[1]:
        st.subheader("Global Job Platforms")
        for item in global_:
            _card(item)

    with tabs[2]:
        st.subheader("Job Preparation Tips")
        for tip in tips:
            st.markdown(f"✅ {tip}")
        st.divider()
        st.markdown("""
**Placement Preparation Checklist:**

- [ ] Resume reviewed and under 1 page
- [ ] LinkedIn profile complete (photo, headline, about, skills, projects)
- [ ] GitHub with 3+ public projects
- [ ] 100+ LeetCode problems solved (mix of Easy/Medium)
- [ ] System design basics understood
- [ ] At least one internship or project experience
- [ ] Mock interviews practiced (Pramp, interviewing.io, peers)
        """)
