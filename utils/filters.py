"""
utils/filters.py
----------------
Tag-based and keyword-based filter logic.

The VALID_TAGS constant defines every allowed tag in the system.
All resource cards and filter widgets use this same list so filters
are consistent across every page.
"""

# ─────────────────────────────────────────────
# Canonical tag vocabulary
# ─────────────────────────────────────────────
VALID_TAGS = [
    "Free",
    "Paid",
    "Government",
    "Certificate",
    "YouTube",
    "Practice",
    "Projects",
    "Beginner",
    "Intermediate",
    "Advanced",
    "India",
    "Global",
    "Official",
]

# Resource types used across the app
VALID_TYPES = ["Video", "Course", "Article", "Practice", "Project", "Platform", "Channel", "Tool", "Notes", "Lab", "Reference", "Website"]

# Skill status options for the tracker
SKILL_STATUSES = ["Not Started", "Learning", "Practicing", "Completed"]


def filter_by_tags(resources: list, selected_tags: list) -> list:
    """
    Returns resources that contain ALL of the selected tags.

    If no tags are selected, returns all resources unchanged.
    """
    if not selected_tags:
        return resources
    return [
        r for r in resources
        if all(tag in r.get("tags", []) for tag in selected_tags)
    ]


def filter_by_type(resources: list, selected_types: list) -> list:
    """
    Returns resources whose 'type' field matches any of the selected types.
    If no types are selected, returns all resources unchanged.
    """
    if not selected_types:
        return resources
    return [r for r in resources if r.get("type") in selected_types]


def filter_by_keyword(resources: list, keyword: str) -> list:
    """
    Returns resources where the keyword appears in title, description,
    subjects, skills, or category fields (case-insensitive).
    """
    if not keyword or not keyword.strip():
        return resources

    kw = keyword.strip().lower()

    def matches(resource: dict) -> bool:
        if kw in resource.get("title", "").lower():
            return True
        if kw in resource.get("description", "").lower():
            return True
        if any(kw in s.lower() for s in resource.get("subjects", [])):
            return True
        if any(kw in s.lower() for s in resource.get("skills", [])):
            return True
        if kw in resource.get("category", "").lower():
            return True
        if kw in resource.get("name", "").lower():
            return True
        return False

    return [r for r in resources if matches(r)]


def filter_by_category(resources: list, category: str) -> list:
    """
    Returns resources whose 'category' field matches the given string
    (case-insensitive). Returns all if category is empty.
    """
    if not category or category.strip().lower() == "all":
        return resources
    cat = category.strip().lower()
    return [r for r in resources if cat in r.get("category", "").lower()]


def apply_all_filters(
    resources: list,
    keyword: str = "",
    selected_tags: list = None,
    selected_types: list = None,
    category: str = "",
) -> list:
    """
    Convenience function: applies keyword, tag, type and category filters in sequence.
    """
    result = resources
    result = filter_by_keyword(result, keyword)
    result = filter_by_tags(result, selected_tags or [])
    result = filter_by_type(result, selected_types or [])
    result = filter_by_category(result, category)
    return result
