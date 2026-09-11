"""
utils/tracker_utils.py
----------------------
Read and write the user's personal skill tracker (data/tracker.json).

Schema:
  skills: {
    skill_name: {
      status: "Not Started" | "Learning" | "Practicing" | "Completed",
      progress: int (0-100),
      notes: str,
      certificate_earned: bool,
      project_completed: bool,
      course_completed: bool
    }
  }
  completed_tasks: [ task_id, ... ]
"""

import json
import os

TRACKER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "tracker.json"
)

_DEFAULT = {"skills": {}, "completed_tasks": []}

_SKILL_DEFAULT = {
    "status": "Not Started",
    "progress": 0,
    "notes": "",
    "certificate_earned": False,
    "project_completed": False,
    "course_completed": False,
}


def _tracker_path() -> str:
    """Returns the current TRACKER_PATH (indirected so tests can patch it)."""
    import utils.tracker_utils as _self
    return _self.TRACKER_PATH


def load_tracker() -> dict:
    """Reads tracker.json and returns its contents as a dict."""
    path = _tracker_path()
    if not os.path.exists(path):
        return dict(_DEFAULT)
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            data.setdefault("skills", {})
            data.setdefault("completed_tasks", [])
            return data
        except json.JSONDecodeError:
            return dict(_DEFAULT)


def save_tracker(data: dict) -> None:
    """Writes the tracker dict back to tracker.json."""
    with open(_tracker_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_skill_entry(skill_name: str) -> dict:
    """Returns the tracker entry for a skill (with defaults if not tracked yet)."""
    data = load_tracker()
    entry = data["skills"].get(skill_name, {})
    return {**_SKILL_DEFAULT, **entry}


def update_skill(
    skill_name: str,
    status: str = None,
    progress: int = None,
    notes: str = None,
    certificate_earned: bool = None,
    project_completed: bool = None,
    course_completed: bool = None,
) -> None:
    """
    Updates any combination of fields for a tracked skill.
    Only provided (non-None) fields are updated.
    """
    data = load_tracker()
    entry = {**_SKILL_DEFAULT, **data["skills"].get(skill_name, {})}

    if status is not None:
        entry["status"] = status
    if progress is not None:
        entry["progress"] = max(0, min(100, progress))
    if notes is not None:
        entry["notes"] = notes
    if certificate_earned is not None:
        entry["certificate_earned"] = certificate_earned
    if project_completed is not None:
        entry["project_completed"] = project_completed
    if course_completed is not None:
        entry["course_completed"] = course_completed

    # Auto-sync status with progress
    if entry["progress"] == 100 and entry["status"] != "Completed":
        entry["status"] = "Completed"

    data["skills"][skill_name] = entry
    save_tracker(data)


def remove_skill(skill_name: str) -> None:
    """Removes a skill from the tracker."""
    data = load_tracker()
    data["skills"].pop(skill_name, None)
    save_tracker(data)


# ── Keep old API working (used in Phase 1 tests) ──────────────────────────────

def update_skill_progress(skill_name: str, progress: int, notes: str = "") -> None:
    """Legacy: updates progress and notes. Use update_skill() for full control."""
    update_skill(skill_name, progress=progress, notes=notes)


def mark_task_complete(task_id: str) -> None:
    """Adds task_id to the completed_tasks list if not already there."""
    data = load_tracker()
    if task_id not in data["completed_tasks"]:
        data["completed_tasks"].append(task_id)
    save_tracker(data)


def unmark_task(task_id: str) -> None:
    """Removes task_id from the completed_tasks list."""
    data = load_tracker()
    data["completed_tasks"] = [t for t in data["completed_tasks"] if t != task_id]
    save_tracker(data)


def get_skill_progress(skill_name: str) -> dict:
    """Legacy: returns { 'progress': int, 'notes': str } for a skill."""
    entry = get_skill_entry(skill_name)
    return {"progress": entry["progress"], "notes": entry["notes"]}


def get_today_completed_tasks(tasks: list) -> list:
    """
    Returns the subset of tasks that the user has already completed today.
    'tasks' is a list of task dicts from daily_tasks.json.
    """
    data = load_tracker()
    completed = set(data.get("completed_tasks", []))
    return [t for t in tasks if t["id"] in completed]
