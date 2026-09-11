"""
pages/skills_hub.py
-------------------
Skills Hub — Explore technical, branch-specific, career and life skills.

Displays skill lists with associated resources for each skill category.
"""

import streamlit as st
from utils.data_loader import load_skills, load_resources
from utils.filters import apply_all_filters
from components.section_header import section_header
from components.resource_card import resource_card
from components.tag_filter import tag_filter, keyword_search_bar


# Map category keys to display labels and icons
CATEGORY_META = {
    "technical": ("⚙️", "Technical Skills", "Core computer science and engineering fundamentals."),
    "career": ("💼", "Career Skills", "Skills to find jobs, crack interviews and grow professionally."),
    "life": ("🌱", "Life Skills", "Productivity, communication and personal development."),
}


def _get_resources_for_skill(skill_name: str, all_resources: list) -> list:
    """Returns all resources whose 'skills' list contains the given skill name."""
    skill_lower = skill_name.lower()
    return [
        r for r in all_resources
        if any(skill_lower in s.lower() for s in r.get("skills", []))
    ]


def _show_skill_category(
    category_key: str,
    skills: list,
    all_resources: list,
    branch_filter: str = "",
) -> None:
    """Renders one skill category section with expandable resource listings."""
    icon, label, desc = CATEGORY_META[category_key]

    st.subheader(f"{icon} {label}")
    st.caption(desc)

    if not skills:
        st.info("No skills listed for this category yet.")
        return

    for skill_name in skills:
        resources = _get_resources_for_skill(skill_name, all_resources)
        label_text = f"{skill_name}"
        if resources:
            label_text += f"  *(  {len(resources)} resource{'s' if len(resources) != 1 else ''} )*"

        with st.expander(label_text):
            if resources:
                for res in resources:
                    resource_card(res)
            else:
                st.caption(
                    "No resources linked to this skill yet. "
                    "Resources will be added in upcoming phases."
                )


def show() -> None:
    """Renders the Skills Hub page."""

    section_header(
        title="Skills Hub",
        subtitle="Discover and learn the skills that matter for your B.Tech journey.",
        icon="🛠️",
    )

    skills_data = load_skills()
    all_resources = load_resources()

    if not skills_data:
        st.error("Could not load skills data. Please check data/skills.json.")
        return

    # ── Tab layout: one tab per category ─────────────────────────────────────
    tabs = st.tabs(["⚙️ Technical", "🏭 Branch-Specific", "💼 Career", "🌱 Life"])

    # ── Technical Skills tab ──────────────────────────────────────────────────
    with tabs[0]:
        _show_skill_category(
            "technical",
            skills_data.get("technical", []),
            all_resources,
        )

    # ── Branch-Specific Skills tab ─────────────────────────────────────────────
    with tabs[1]:
        st.subheader("🏭 Branch-Specific Skills")
        st.caption("Skills most relevant to your engineering branch.")

        branch_specific = skills_data.get("branch_specific", {})

        if not branch_specific:
            st.info("No branch-specific skills listed yet.")
        else:
            branch_options = list(branch_specific.keys())
            selected_branch = st.selectbox(
                "Select your branch",
                options=branch_options,
                key="skills_branch",
            )

            if selected_branch:
                branch_skills = branch_specific.get(selected_branch, [])
                if branch_skills:
                    for skill_name in branch_skills:
                        resources = _get_resources_for_skill(skill_name, all_resources)
                        label_text = f"{skill_name}"
                        if resources:
                            label_text += f"  *( {len(resources)} resource{'s' if len(resources) != 1 else ''} )*"
                        with st.expander(label_text):
                            if resources:
                                for res in resources:
                                    resource_card(res)
                            else:
                                st.caption("No resources linked yet.")
                else:
                    st.info(f"No branch-specific skills listed for {selected_branch} yet.")

    # ── Career Skills tab ─────────────────────────────────────────────────────
    with tabs[2]:
        _show_skill_category(
            "career",
            skills_data.get("career", []),
            all_resources,
        )

    # ── Life Skills tab ───────────────────────────────────────────────────────
    with tabs[3]:
        _show_skill_category(
            "life",
            skills_data.get("life", []),
            all_resources,
        )

    st.divider()

    # ── All Skills Quick Search ────────────────────────────────────────────────
    st.subheader("🔍 Quick Skill Resource Search")
    st.caption("Search resources by skill keyword across all categories.")

    keyword = keyword_search_bar(key="skills_kw", placeholder="e.g. Python, DSA, Resume…")
    selected_tags, selected_types = tag_filter(key_prefix="skills")

    filtered = apply_all_filters(
        all_resources,
        keyword=keyword,
        selected_tags=selected_tags,
        selected_types=selected_types,
    )

    if keyword or selected_tags or selected_types:
        st.caption(f"Found {len(filtered)} resource(s)")
        if filtered:
            for res in filtered:
                resource_card(res)
        else:
            st.warning("No resources match your search. Try different keywords or remove filters.")
    else:
        st.info("Enter a keyword or select filters above to search skill resources.")
