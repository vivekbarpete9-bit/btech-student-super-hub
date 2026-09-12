"""
pages/courses_certificates.py
------------------------------
Courses & Certificates — Browse and filter courses by Free/Paid/Government,
level, and region.
"""

import streamlit as st
from utils.data_loader import load_platforms
from utils.filters import apply_all_filters
from components.section_header import section_header
from components.tag_filter import tag_filter, keyword_search_bar


def show() -> None:
    section_header("Courses & Certificates", "Find the right course or certification for your career goals.", "🏆")

    platforms = load_platforms()
    # Show only platforms that offer courses or certificates
    courses = [p for p in platforms if p.get("type") in ("Platform", "Course") and "Certificate" in p.get("tags", [])]
    all_with_cert = [p for p in platforms if "Certificate" in p.get("tags", [])]

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Platforms", len(platforms))
    col2.metric("With Certificates", len(all_with_cert))
    col3.metric("Free Certificates", sum(1 for p in all_with_cert if "Free" in p.get("tags",[])))
    col4.metric("Government / Official", sum(1 for p in all_with_cert if "Government" in p.get("tags",[]) or "Official" in p.get("tags",[])))

    st.divider()

    tabs = st.tabs(["🆓 Free Certificates", "🏛️ Government / Official", "🌱 Beginner", "🔥 Advanced", "🔍 Search All"])

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
        free_cert = [p for p in all_with_cert if "Free" in p.get("tags",[])]
        st.caption(f"{len(free_cert)} free certificate platforms")
        for p in free_cert:
            _card(p)

    with tabs[1]:
        gov_cert = [p for p in all_with_cert if "Government" in p.get("tags",[]) or "Official" in p.get("tags",[])]
        st.caption(f"{len(gov_cert)} government / official platforms")
        for p in gov_cert:
            _card(p)

    with tabs[2]:
        beg_cert = [p for p in all_with_cert if "Beginner" in p.get("tags",[])]
        st.caption(f"{len(beg_cert)} beginner-level platforms")
        for p in beg_cert:
            _card(p)

    with tabs[3]:
        adv_cert = [p for p in all_with_cert if "Advanced" in p.get("tags",[]) or "Intermediate" in p.get("tags",[])]
        st.caption(f"{len(adv_cert)} intermediate / advanced platforms")
        for p in adv_cert:
            _card(p)

    with tabs[4]:
        kw = keyword_search_bar(key="cert_kw", placeholder="Search courses…")
        selected_tags, selected_types = tag_filter(key_prefix="cert")
        filtered = apply_all_filters(platforms, keyword=kw, selected_tags=selected_tags, selected_types=selected_types)
        st.caption(f"{len(filtered)} results")
        for p in filtered:
            _card(p)

    st.divider()
    st.subheader("📋 Certificate Tips")
    st.markdown("""
- **NPTEL** and **SWAYAM** are government-recognized in India — list them prominently on your resume.
- **Google**, **Microsoft**, **IBM**, and **AWS** offer free official certifications — highly valued by employers.
- Prioritize certificates that are **project-based** over those that are just quiz completions.
- Add LinkedIn badges for certificates — recruiters search for certified skills.
- Free audit ≠ free certificate on Coursera/edX — check before enrolling if you need the certificate.
    """)
