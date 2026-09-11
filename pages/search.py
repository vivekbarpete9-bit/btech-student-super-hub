"""
pages/search.py
---------------
Global Search — Search all resources, platforms and YouTube channels
by keyword, tag and type.
"""

import streamlit as st
from utils.data_loader import load_resources, load_platforms, load_youtube_channels, load_branches
from utils.filters import apply_all_filters
from components.section_header import section_header
from components.resource_card import resource_card
from components.tag_filter import tag_filter, keyword_search_bar


def _platform_card(item: dict) -> None:
    with st.container(border=True):
        col1, col2 = st.columns([0.82, 0.18])
        with col1:
            st.markdown(f"**[{item.get('name', item.get('title',''))}]({item['url']})**")
        with col2:
            st.caption(item.get("type", ""))
        if item.get("description"):
            st.caption(item["description"])
        tags = item.get("tags", [])
        if tags:
            st.markdown(" ".join(f"`{t}`" for t in tags))


def show() -> None:
    section_header("Search", "Find any resource, platform or channel across the entire B.Tech Super-Hub.", "🔍")

    all_resources = load_resources()
    all_platforms = load_platforms()
    all_channels  = load_youtube_channels()

    if not all_resources:
        st.error("Could not load resources. Please check data/resources.json.")
        return

    # ── Search bar ────────────────────────────────────────────────────────────
    keyword = keyword_search_bar(
        key="global_search_kw",
        placeholder="Search by title, subject, skill or description…",
    )

    # ── Filters ───────────────────────────────────────────────────────────────
    selected_tags, selected_types = tag_filter(key_prefix="global_search")

    # ── Branch filter ─────────────────────────────────────────────────────────
    branches = load_branches()
    branch_codes = ["All Branches"] + list(branches.keys())
    selected_branch = st.selectbox(
        "Filter by branch",
        options=branch_codes,
        key="global_search_branch",
    )

    st.divider()

    has_any_filter = bool(keyword or selected_tags or selected_types or selected_branch != "All Branches")

    # ── Apply filters ─────────────────────────────────────────────────────────
    filtered_resources = apply_all_filters(
        all_resources,
        keyword=keyword,
        selected_tags=selected_tags,
        selected_types=selected_types,
    )
    if selected_branch != "All Branches":
        filtered_resources = [r for r in filtered_resources if selected_branch in r.get("branches", [])]

    # Platforms and channels: keyword + tag filter only (they have no branch field)
    filtered_platforms = apply_all_filters(
        all_platforms,
        keyword=keyword,
        selected_tags=selected_tags,
        selected_types=selected_types,
    ) if has_any_filter else []

    filtered_channels = []
    if has_any_filter and keyword:
        kw = keyword.lower()
        filtered_channels = [
            c for c in all_channels
            if kw in c.get("name", "").lower() or kw in c.get("description", "").lower()
        ]

    # ── No filter state — show all resources ─────────────────────────────────
    if not has_any_filter:
        st.subheader(f"📖 All Resources ({len(all_resources)})")
        st.caption("Use the search bar or filters above to narrow down results.")
        for res in all_resources:
            resource_card(res)
        return

    # ── Results ───────────────────────────────────────────────────────────────
    total_found = len(filtered_resources) + len(filtered_platforms) + len(filtered_channels)
    st.subheader(f"🔎 Search Results ({total_found})")

    if total_found == 0:
        st.warning(
            "No results matched your search.  \n"
            "Try different keywords, remove some filters, or check spelling."
        )
        st.markdown("**Suggestions:**")
        st.markdown("- Try broader keywords like *Python*, *DSA*, *Cloud*, *NPTEL*")
        st.markdown("- Remove tag or type filters")
        st.markdown("- Select **All Branches**")
        return

    filter_desc = []
    if keyword:
        filter_desc.append(f"keyword: *{keyword}*")
    if selected_tags:
        filter_desc.append(f"tags: {', '.join(selected_tags)}")
    if selected_types:
        filter_desc.append(f"types: {', '.join(selected_types)}")
    if selected_branch != "All Branches":
        filter_desc.append(f"branch: {selected_branch}")
    st.caption("  ·  ".join(filter_desc))

    if filtered_resources:
        st.markdown(f"**📖 Study Resources ({len(filtered_resources)})**")
        for res in filtered_resources:
            resource_card(res)

    if filtered_platforms:
        st.markdown(f"**🌐 Learning Platforms ({len(filtered_platforms)})**")
        for p in filtered_platforms:
            _platform_card(p)

    if filtered_channels:
        st.markdown(f"**▶️ YouTube Channels ({len(filtered_channels)})**")
        for c in filtered_channels:
            _platform_card(c)
