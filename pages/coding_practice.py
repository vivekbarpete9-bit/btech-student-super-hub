"""
pages/coding_practice.py
------------------------
Coding & Practice Hub — Curated platforms for coding practice, competitions,
and projects.
"""

import streamlit as st
from utils.data_loader import load_platforms
from components.section_header import section_header
from components.tag_filter import keyword_search_bar
from utils.filters import apply_all_filters


def show() -> None:
    section_header("Coding & Practice Hub", "Build problem-solving skills with the best coding platforms.", "💻")

    all_platforms = load_platforms()
    coding = [p for p in all_platforms if any(
        kw in p.get("category","").lower()
        for kw in ("coding", "practice", "web development", "projects")
    )]

    # ── Stats ──────────────────────────────────────────────────────────────────
    free_count = sum(1 for p in coding if "Free" in p.get("tags",[]))
    col1, col2, col3 = st.columns(3)
    col1.metric("Platforms", len(coding))
    col2.metric("Free / Open", free_count)
    col3.metric("With Certificates", sum(1 for p in coding if "Certificate" in p.get("tags",[])))

    st.divider()

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tabs = st.tabs(["🏆 Competitive", "🌐 Web Practice", "🤖 Data/AI", "🔧 All Tools", "💡 Tips"])

    def _card(p):
        with st.container(border=True):
            col1, col2 = st.columns([0.82, 0.18])
            with col1:
                st.markdown(f"**[{p['name']}]({p['url']})**")
            with col2:
                st.caption(p.get("type",""))
            if p.get("description"):
                st.caption(p["description"])
            st.markdown(" ".join(f"`{t}`" for t in p.get("tags",[])))

    with tabs[0]:
        competitive = ["LeetCode","HackerRank","CodeChef","Codeforces","GeeksforGeeks","Exercism"]
        items = [p for p in all_platforms if p["name"] in competitive]
        for p in items:
            _card(p)

    with tabs[1]:
        web = ["Frontend Mentor","The Odin Project","freeCodeCamp","W3Schools","MDN Web Docs","Codecademy"]
        items = [p for p in all_platforms if p["name"] in web]
        for p in items:
            _card(p)

    with tabs[2]:
        data = ["Kaggle","Kaggle Learn","HackerRank","DataCamp","Hugging Face Learn"]
        items = [p for p in all_platforms if p["name"] in data]
        for p in items:
            _card(p)

    with tabs[3]:
        kw = keyword_search_bar(key="cp_all_kw", placeholder="Search platforms…")
        filtered = apply_all_filters(coding, keyword=kw)
        for p in filtered:
            _card(p)

    with tabs[4]:
        st.subheader("💡 Coding Practice Tips")
        tips = [
            "🌱 **Beginners:** Start with HackerRank Easy problems or freeCodeCamp to build confidence.",
            "📈 **Intermediate:** Solve 2–3 LeetCode problems daily — focus on patterns, not grinding.",
            "🏆 **Competitive:** Join CodeChef Starters (weekly) and Codeforces Div. 2 contests.",
            "📁 **Projects:** Push every project to GitHub — recruiters check your commit history.",
            "🔥 **Consistency beats intensity:** 30 minutes daily > 5 hours on weekends.",
            "🤖 **AI/Data:** Kaggle competitions are the best real-world ML practice.",
            "📝 **Track progress:** Mark problems on a spreadsheet or use LeetCode's built-in tracker.",
        ]
        for tip in tips:
            st.markdown(tip)
