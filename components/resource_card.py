"""
components/resource_card.py
---------------------------
The single reusable resource card used across every section of the app.

Call resource_card(resource) with any resource dict from resources.json
and it will render a consistent card with title, tags, type badge and link.
"""

import streamlit as st

# Icon map for resource type badges
TYPE_COLOURS = {
    "Video": "🎬",
    "Course": "📚",
    "Article": "📄",
    "Practice": "💻",
    "Project": "🛠️",
    "Notes": "📝",
    "Lab": "🔬",
    "Reference": "📖",
    "Website": "🌐",
    "Platform": "🖥️",
    "Tool": "🔧",
}

# Colour map for important tags
TAG_EMOJI = {
    "Free": "🆓",
    "Paid": "💰",
    "Government": "🏛️",
    "Official": "✅",
    "Certificate": "🏅",
    "YouTube": "▶️",
    "Practice": "💻",
    "Projects": "🛠️",
    "Beginner": "🌱",
    "Intermediate": "📈",
    "Advanced": "🔥",
    "India": "🇮🇳",
    "Global": "🌐",
}


def resource_card(resource: dict) -> None:
    """
    Renders a single resource as a Streamlit card.

    Args:
        resource: a dict with keys: id, title, url, type, tags,
                  subjects, skills, branches, description
    """
    title = resource.get("title", "Untitled")
    url = resource.get("url", "#")
    rtype = resource.get("type", "Resource")
    tags = resource.get("tags", [])
    description = resource.get("description", "")

    # Type icon
    icon = TYPE_COLOURS.get(rtype, "📌")

    # Build tag pills string
    tag_pills = " ".join(TAG_EMOJI.get(tag, f"[{tag}]") for tag in tags)

    with st.container(border=True):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"**{icon} [{title}]({url})**")
        with col2:
            st.caption(rtype)

        if description:
            st.caption(description)

        if tag_pills:
            st.markdown(tag_pills)
