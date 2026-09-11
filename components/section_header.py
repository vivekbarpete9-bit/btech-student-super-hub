"""
components/section_header.py
-----------------------------
Renders a consistent section title, subtitle and optional divider.

Use this at the top of every page so all sections look uniform.
"""

import streamlit as st


def section_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """
    Renders a page/section heading with an optional icon and subtitle.

    Args:
        title: main heading text
        subtitle: smaller description text shown below the title
        icon: emoji icon placed before the title (e.g. "📚")
    """
    display_title = f"{icon} {title}" if icon else title
    st.title(display_title)
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.divider()
