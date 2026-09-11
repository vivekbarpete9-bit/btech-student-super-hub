"""
components/tag_filter.py
------------------------
Reusable tag and type filter bar.

Renders multiselect widgets and returns the user's selected values.
Import this into any page that needs filtering.
"""

import streamlit as st
from utils.filters import VALID_TAGS, VALID_TYPES


def tag_filter(key_prefix: str = "filter") -> tuple:
    """
    Renders tag and resource-type filter widgets.

    Args:
        key_prefix: unique string to avoid Streamlit widget key conflicts
                    when the same filter is used on multiple pages.

    Returns:
        (selected_tags: list, selected_types: list)
    """
    col1, col2 = st.columns(2)

    with col1:
        selected_tags = st.multiselect(
            "Filter by tags",
            options=VALID_TAGS,
            default=[],
            key=f"{key_prefix}_tags",
            help="Select one or more tags to narrow down resources.",
        )

    with col2:
        selected_types = st.multiselect(
            "Filter by type",
            options=VALID_TYPES,
            default=[],
            key=f"{key_prefix}_types",
            help="Select resource types (Video, Course, Article, Practice, Project).",
        )

    return selected_tags, selected_types


def keyword_search_bar(key: str = "search_kw", placeholder: str = "Search resources…") -> str:
    """
    Renders a simple text input for keyword search.

    Args:
        key: unique widget key
        placeholder: placeholder text shown inside the input

    Returns:
        The keyword string entered by the user (may be empty).
    """
    return st.text_input("🔍 Search", placeholder=placeholder, key=key)
