"""
pages/academic_hub.py
---------------------
Academic Hub — Browse study resources by:
    Branch → Year → Semester → Subject → Resources

Uses the branches.json data and the shared resource pool.
"""

import streamlit as st
from utils.data_loader import load_branches, get_resources_by_ids, get_resources_by_subject
from utils.filters import apply_all_filters
from components.section_header import section_header
from components.resource_card import resource_card
from components.tag_filter import tag_filter, keyword_search_bar


def show() -> None:
    """Renders the Academic Hub page."""

    section_header(
        title="Academic Hub",
        subtitle="Find study resources for your branch, year, semester and subject.",
        icon="📚",
    )

    branches = load_branches()

    if not branches:
        st.error("Could not load branch data. Please check data/branches.json.")
        return

    # ── Step 1: Branch selection ───────────────────────────────────────────────
    st.subheader("Step 1 — Select Your Branch")

    branch_options = {
        code: f"{code} — {info['full_name']}"
        for code, info in branches.items()
    }

    selected_branch_code = st.selectbox(
        "Branch",
        options=list(branch_options.keys()),
        format_func=lambda code: branch_options[code],
        key="acad_branch",
    )

    if not selected_branch_code:
        return

    branch_data = branches[selected_branch_code]
    years = branch_data.get("years", {})

    st.divider()

    # ── Step 2: Year selection ─────────────────────────────────────────────────
    st.subheader("Step 2 — Select Your Year")

    year_options = sorted(years.keys(), key=lambda y: int(y))
    selected_year = st.radio(
        "Year",
        options=year_options,
        format_func=lambda y: f"Year {y}",
        horizontal=True,
        key=f"acad_year_{selected_branch_code}",
    )

    if not selected_year:
        return

    semesters = years[selected_year].get("semesters", {})

    st.divider()

    # ── Step 3: Semester selection ─────────────────────────────────────────────
    st.subheader("Step 3 — Select Your Semester")

    sem_options = sorted(semesters.keys(), key=lambda s: int(s))
    selected_sem = st.radio(
        "Semester",
        options=sem_options,
        format_func=lambda s: f"Semester {s}",
        horizontal=True,
        key=f"acad_sem_{selected_branch_code}_{selected_year}",
    )

    if not selected_sem:
        return

    sem_data = semesters[selected_sem]
    subjects = sem_data.get("subjects", [])
    sem_resource_ids = sem_data.get("resource_ids", [])

    st.divider()

    # ── Subjects list ─────────────────────────────────────────────────────────
    st.subheader(
        f"📋 {selected_branch_code} | Year {selected_year} | Semester {selected_sem} — Subjects"
    )

    if subjects:
        cols = st.columns(3)
        for idx, subject in enumerate(subjects):
            with cols[idx % 3]:
                st.markdown(f"• {subject}")
    else:
        st.info("No subjects listed for this semester yet.")

    st.divider()

    # ── Step 4: Subject-specific resource drill-down ───────────────────────────
    st.subheader("Step 4 — Find Resources for a Subject")

    subject_choice = st.selectbox(
        "Select a subject to find resources",
        options=["— All Resources for this Semester —"] + subjects,
        key="acad_subject",
    )

    # Collect resources: subject-specific + semester-level
    if subject_choice == "— All Resources for this Semester —":
        # Show all resources linked to this semester
        resources = get_resources_by_ids(sem_resource_ids)
        # Also pull any resources that match any subject in this semester
        extra = []
        for subj in subjects:
            extra.extend(get_resources_by_subject(subj))
        # Merge and deduplicate by id
        seen = {r["id"] for r in resources}
        for r in extra:
            if r["id"] not in seen:
                resources.append(r)
                seen.add(r["id"])
    else:
        resources = get_resources_by_subject(subject_choice)
        # Also include semester-level resources if any
        sem_resources = get_resources_by_ids(sem_resource_ids)
        seen = {r["id"] for r in resources}
        for r in sem_resources:
            if r["id"] not in seen:
                resources.append(r)
                seen.add(r["id"])

    st.divider()

    # ── Filters ───────────────────────────────────────────────────────────────
    st.subheader("🔎 Filter Resources")
    keyword = keyword_search_bar(key="acad_kw")
    selected_tags, selected_types = tag_filter(key_prefix="acad")

    # Apply filters
    filtered = apply_all_filters(
        resources,
        keyword=keyword,
        selected_tags=selected_tags,
        selected_types=selected_types,
    )

    st.divider()

    # ── Results ───────────────────────────────────────────────────────────────
    subject_label = subject_choice if subject_choice != "— All Resources for this Semester —" else "this semester"
    st.subheader(f"📖 Resources for {subject_label}")

    if not resources:
        st.info(
            f"No dedicated resources are linked to **{subject_label}** yet.  \n\n"
            "**Try these general options while more resources are being added:**\n"
            "- 🏛️ [NPTEL](https://nptel.ac.in/) — Search for your subject by name\n"
            "- 🎓 [MIT OpenCourseWare](https://ocw.mit.edu/) — Free lecture notes and exams\n"
            "- 📺 [YouTube – Gate Smashers](https://www.youtube.com/@GateSmashers) — Core CS/ECE subjects\n"
            "- 📺 [YouTube – Neso Academy](https://www.youtube.com/@nesoacademy) — Electronics & CS\n"
            "- 📚 [GeeksforGeeks](https://www.geeksforgeeks.org/) — CS/IT articles and practice\n"
            "- 🔬 [Khan Academy](https://www.khanacademy.org/) — Maths and science foundations\n"
        )
        return

    if not filtered:
        st.warning("No resources match your current filters. Try removing some filters.")
        return

    # ── Resource type legend ───────────────────────────────────────────────────
    type_counts: dict = {}
    for r in filtered:
        t = r.get("type", "Other")
        type_counts[t] = type_counts.get(t, 0) + 1

    type_icons = {
        "Course": "📚", "Video": "🎬", "Notes": "📝", "Lab": "🔬",
        "Reference": "📖", "Practice": "💻", "Article": "📄",
        "Website": "🌐", "Project": "🛠️",
    }
    legend_parts = [
        f"{type_icons.get(t, '📌')} **{t}** ×{n}"
        for t, n in sorted(type_counts.items())
    ]
    st.caption(
        f"Showing **{len(filtered)}** resource(s)  ·  " + "  ·  ".join(legend_parts)
    )

    for res in filtered:
        resource_card(res)
