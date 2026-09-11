"""
utils/data_loader.py
--------------------
Loads and caches JSON data files.

All pages import from here instead of reading files directly.
"""

import json
import os
import streamlit as st

# Path to the data directory (relative to the project root)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load_json(filename: str):
    """Reads a JSON file from the data/ directory (no Streamlit cache — used internally)."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        st.error(f"Data file not found: {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_json_plain(filename: str):
    """Reads a JSON file without Streamlit — safe to call from tests."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_branches() -> dict:
    """Returns the full branches dictionary (branch → year → semester → subjects)."""
    return _load_json("branches.json") or {}


@st.cache_data
def load_resources() -> list:
    """Returns the full list of resource dictionaries."""
    return _load_json("resources.json") or []


@st.cache_data
def load_skills() -> dict:
    """Returns the skills dictionary (technical, branch_specific, career, life)."""
    return _load_json("skills.json") or {}


@st.cache_data
def load_roadmaps() -> dict:
    """Returns the career roadmaps dictionary."""
    return _load_json("roadmaps.json") or {}


@st.cache_data
def load_daily_tasks() -> list:
    """Returns the list of daily skill tasks."""
    return _load_json("daily_tasks.json") or []


@st.cache_data
def load_platforms() -> list:
    """Returns the list of learning platform dictionaries."""
    return _load_json("platforms.json") or []


@st.cache_data
def load_youtube_channels() -> list:
    """Returns the list of YouTube channel dictionaries."""
    return _load_json("youtube_channels.json") or []


@st.cache_data
def load_internships() -> dict:
    """Returns the internship platforms dictionary."""
    return _load_json("internships.json") or {}


@st.cache_data
def load_jobs() -> dict:
    """Returns the job platforms dictionary."""
    return _load_json("jobs.json") or {}


def load_tracker() -> dict:
    """
    Returns the user's personal tracker data.
    NOT cached — the user can update it during the session.
    Uses plain file read (no st.error) so it is safe to call from tests too.
    """
    data = _load_json_plain("tracker.json")
    if data is None:
        return {"skills": {}, "completed_tasks": []}
    return data


def get_resources_by_ids(resource_ids: list) -> list:
    """Given a list of resource IDs, returns matching resource dicts."""
    all_resources = load_resources()
    id_set = set(resource_ids)
    return [r for r in all_resources if r["id"] in id_set]


def get_resources_by_subject(subject: str) -> list:
    """Returns all resources that list the given subject name."""
    all_resources = load_resources()
    return [r for r in all_resources if subject in r.get("subjects", [])]


def get_resources_by_branch(branch: str) -> list:
    """Returns all resources that include the given branch code."""
    all_resources = load_resources()
    return [r for r in all_resources if branch in r.get("branches", [])]


def get_resources_by_skill(skill: str) -> list:
    """Returns all resources whose skills list contains the given skill (case-insensitive)."""
    all_resources = load_resources()
    skill_lower = skill.lower()
    return [
        r for r in all_resources
        if any(skill_lower in s.lower() for s in r.get("skills", []))
    ]


def get_platforms_by_category(category: str) -> list:
    """Returns platforms matching the given category string (case-insensitive)."""
    all_platforms = load_platforms()
    cat = category.strip().lower()
    return [p for p in all_platforms if cat in p.get("category", "").lower()]


def get_channels_by_category(category: str) -> list:
    """Returns YouTube channels matching the given category string (case-insensitive)."""
    all_channels = load_youtube_channels()
    cat = category.strip().lower()
    return [c for c in all_channels if cat in c.get("category", "").lower()]
