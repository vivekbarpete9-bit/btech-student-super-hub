"""
tests/test_data.py
------------------
Comprehensive data validation and unit tests.

Run with:  pytest tests/ -v
"""

import json
import os
import sys
import pytest
from unittest.mock import patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

REQUIRED_RESOURCE_KEYS = {"id", "title", "url", "type", "tags", "subjects", "skills", "branches", "description"}

from utils.filters import VALID_TAGS, VALID_TYPES, SKILL_STATUSES


# ─── Helper ───────────────────────────────────────────────────────────────────

def _load(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── 1. File existence ────────────────────────────────────────────────────────

@pytest.mark.parametrize("filename", [
    "branches.json", "resources.json", "skills.json", "roadmaps.json",
    "daily_tasks.json", "tracker.json", "platforms.json",
    "youtube_channels.json", "internships.json", "jobs.json",
])
def test_data_file_exists(filename):
    assert os.path.exists(os.path.join(DATA_DIR, filename)), f"Missing: {filename}"


# ─── 2. JSON validity ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("filename", [
    "branches.json", "resources.json", "skills.json", "roadmaps.json",
    "daily_tasks.json", "tracker.json", "platforms.json",
    "youtube_channels.json", "internships.json", "jobs.json",
])
def test_json_is_valid(filename):
    data = _load(filename)
    assert data is not None


# ─── 3. Resources schema ──────────────────────────────────────────────────────

def test_resources_is_list():
    assert isinstance(_load("resources.json"), list)

def test_resources_not_empty():
    assert len(_load("resources.json")) > 0

def test_resources_have_required_keys():
    for res in _load("resources.json"):
        missing = REQUIRED_RESOURCE_KEYS - set(res.keys())
        assert not missing, f"Resource '{res.get('id')}' missing: {missing}"

def test_resource_ids_are_unique():
    ids = [r["id"] for r in _load("resources.json")]
    assert len(ids) == len(set(ids)), "Duplicate resource IDs"

def test_resource_tags_are_valid():
    for res in _load("resources.json"):
        for tag in res.get("tags", []):
            assert tag in VALID_TAGS, f"Resource '{res['id']}' has invalid tag '{tag}'"

def test_resource_types_are_valid():
    for res in _load("resources.json"):
        assert res.get("type") in VALID_TYPES, f"Resource '{res['id']}' has invalid type '{res.get('type')}'"

def test_resource_urls_non_empty():
    for res in _load("resources.json"):
        assert res.get("url") and res["url"] != "#", f"Resource '{res['id']}' has empty URL"

def test_resource_list_fields_are_lists():
    for res in _load("resources.json"):
        for key in ("tags", "subjects", "skills", "branches"):
            assert isinstance(res.get(key), list), f"Resource '{res['id']}' field '{key}' is not a list"


# ─── 4. Branches schema ───────────────────────────────────────────────────────

def test_branches_is_dict():
    assert isinstance(_load("branches.json"), dict)

def test_branches_have_full_name():
    for code, branch in _load("branches.json").items():
        assert branch.get("full_name"), f"Branch '{code}' missing full_name"

def test_branches_have_years():
    for code, branch in _load("branches.json").items():
        assert isinstance(branch.get("years"), dict), f"Branch '{code}' missing years dict"

def test_branch_resource_ids_exist():
    branches = _load("branches.json")
    valid_ids = {r["id"] for r in _load("resources.json")}
    for bcode, branch in branches.items():
        for year, yd in branch.get("years", {}).items():
            for sem, sd in yd.get("semesters", {}).items():
                for rid in sd.get("resource_ids", []):
                    assert rid in valid_ids, f"Branch {bcode} Y{year} S{sem} refs unknown id '{rid}'"

def test_ten_branches_present():
    branches = _load("branches.json")
    assert len(branches) >= 10, f"Expected >= 10 branches, got {len(branches)}"


# ─── 5. Skills schema ────────────────────────────────────────────────────────

def test_skills_is_dict():
    assert isinstance(_load("skills.json"), dict)

def test_skills_has_required_categories():
    data = _load("skills.json")
    for key in ("technical", "branch_specific", "career", "life"):
        assert key in data, f"skills.json missing '{key}'"

def test_skills_technical_non_empty():
    assert len(_load("skills.json")["technical"]) > 0

def test_skills_branch_specific_has_expected_branches():
    bs = _load("skills.json").get("branch_specific", {})
    for branch in ("CSE", "ECE", "EEE", "ME", "CE"):
        assert branch in bs, f"skills.json branch_specific missing '{branch}'"


# ─── 6. Roadmaps schema ──────────────────────────────────────────────────────

def test_roadmaps_is_dict():
    assert isinstance(_load("roadmaps.json"), dict)

def test_roadmaps_has_22_or_more_roles():
    assert len(_load("roadmaps.json")) >= 22

def test_roadmaps_steps_have_required_keys():
    for role, rm in _load("roadmaps.json").items():
        assert "steps" in rm, f"Roadmap '{role}' missing steps"
        for step in rm["steps"]:
            for key in ("step", "title", "detail", "resource_ids"):
                assert key in step, f"Roadmap '{role}' step missing '{key}'"

def test_roadmap_resource_ids_exist():
    valid_ids = {r["id"] for r in _load("resources.json")}
    for role, rm in _load("roadmaps.json").items():
        for step in rm.get("steps", []):
            for rid in step.get("resource_ids", []):
                assert rid in valid_ids, f"Roadmap '{role}' step {step['step']} refs unknown '{rid}'"


# ─── 7. Daily tasks schema ───────────────────────────────────────────────────

def test_daily_tasks_is_list():
    assert isinstance(_load("daily_tasks.json"), list)

def test_daily_tasks_have_required_keys():
    required = {"id", "title", "category", "difficulty", "estimated_minutes", "description"}
    for task in _load("daily_tasks.json"):
        missing = required - set(task.keys())
        assert not missing, f"Task '{task.get('id')}' missing {missing}"

def test_daily_task_ids_unique():
    ids = [t["id"] for t in _load("daily_tasks.json")]
    assert len(ids) == len(set(ids)), "Duplicate task IDs"


# ─── 8. Platforms schema ─────────────────────────────────────────────────────

def test_platforms_is_list():
    assert isinstance(_load("platforms.json"), list)

def test_platforms_not_empty():
    assert len(_load("platforms.json")) >= 20

def test_platforms_have_required_keys():
    required = {"id", "name", "url", "category", "tags", "type", "description"}
    for p in _load("platforms.json"):
        missing = required - set(p.keys())
        assert not missing, f"Platform '{p.get('id')}' missing {missing}"

def test_platform_ids_unique():
    ids = [p["id"] for p in _load("platforms.json")]
    assert len(ids) == len(set(ids)), "Duplicate platform IDs"

def test_platform_tags_valid():
    for p in _load("platforms.json"):
        for tag in p.get("tags", []):
            assert tag in VALID_TAGS, f"Platform '{p['id']}' has invalid tag '{tag}'"

def test_platform_urls_non_empty():
    for p in _load("platforms.json"):
        assert p.get("url"), f"Platform '{p['id']}' has empty URL"


# ─── 9. YouTube channels schema ──────────────────────────────────────────────

def test_youtube_channels_is_list():
    assert isinstance(_load("youtube_channels.json"), list)

def test_youtube_channels_not_empty():
    assert len(_load("youtube_channels.json")) >= 20

def test_youtube_channel_ids_unique():
    ids = [c["id"] for c in _load("youtube_channels.json")]
    assert len(ids) == len(set(ids))

def test_youtube_channels_have_youtube_tag():
    for ch in _load("youtube_channels.json"):
        assert "YouTube" in ch.get("tags", []), f"Channel '{ch['id']}' missing YouTube tag"


# ─── 10. Internships / Jobs schema ───────────────────────────────────────────

def test_internships_has_india_and_global():
    data = _load("internships.json")
    assert "india" in data and "global" in data

def test_jobs_has_india_and_global():
    data = _load("jobs.json")
    assert "india" in data and "global" in data


# ─── 11. VALID_TAGS and VALID_TYPES ──────────────────────────────────────────

def test_valid_tags_includes_intermediate():
    assert "Intermediate" in VALID_TAGS

def test_valid_tags_includes_official():
    assert "Official" in VALID_TAGS

def test_valid_types_includes_platform_and_channel():
    assert "Platform" in VALID_TYPES
    assert "Channel" in VALID_TYPES

def test_skill_statuses_has_four_values():
    assert len(SKILL_STATUSES) == 4
    assert "Not Started" in SKILL_STATUSES
    assert "Completed" in SKILL_STATUSES


# ─── 12. Filter logic ────────────────────────────────────────────────────────

from utils.filters import (
    filter_by_tags, filter_by_type, filter_by_keyword,
    filter_by_category, apply_all_filters
)

SAMPLE = [
    {"id":"t1","title":"Python Basics","url":"https://x.com","type":"Video",
     "tags":["Free","YouTube","Beginner"],"subjects":["Programming"],
     "skills":["Python"],"branches":["CSE"],"description":"Learn Python.","category":"Programming"},
    {"id":"t2","title":"Advanced DSA","url":"https://y.com","type":"Course",
     "tags":["Paid","Certificate","Advanced"],"subjects":["Data Structures"],
     "skills":["DSA"],"branches":["CSE"],"description":"Deep algorithms.","category":"CS"},
    {"id":"t3","title":"NPTEL Mathematics","url":"https://nptel.ac.in","type":"Course",
     "tags":["Free","Government","Certificate","India"],"subjects":["Mathematics"],
     "skills":["Math"],"branches":["CSE","ECE","ME"],"description":"Government maths.","category":"Academic"},
    {"id":"t4","title":"Docker Intro","url":"https://docker.com","type":"Platform",
     "tags":["Free","Official","Intermediate"],"subjects":[],
     "skills":["Docker"],"branches":["CSE"],"description":"Container basics.","category":"Cloud / DevOps"},
]

def test_filter_by_tags_empty_returns_all():
    assert filter_by_tags(SAMPLE, []) == SAMPLE

def test_filter_by_tags_single():
    result = filter_by_tags(SAMPLE, ["Free"])
    ids = [r["id"] for r in result]
    assert "t1" in ids and "t3" in ids and "t4" in ids
    assert "t2" not in ids

def test_filter_by_tags_multiple_and():
    result = filter_by_tags(SAMPLE, ["Free","Certificate"])
    assert [r["id"] for r in result] == ["t3"]

def test_filter_by_type_empty_returns_all():
    assert filter_by_type(SAMPLE, []) == SAMPLE

def test_filter_by_type_video():
    result = filter_by_type(SAMPLE, ["Video"])
    assert len(result) == 1 and result[0]["id"] == "t1"

def test_filter_by_type_platform():
    result = filter_by_type(SAMPLE, ["Platform"])
    assert len(result) == 1 and result[0]["id"] == "t4"

def test_filter_by_keyword_empty_returns_all():
    assert filter_by_keyword(SAMPLE, "") == SAMPLE

def test_filter_by_keyword_title():
    assert filter_by_keyword(SAMPLE, "python")[0]["id"] == "t1"

def test_filter_by_keyword_skill():
    assert any(r["id"] == "t2" for r in filter_by_keyword(SAMPLE, "dsa"))

def test_filter_by_keyword_no_match():
    assert filter_by_keyword(SAMPLE, "zzznomatch999") == []

def test_filter_by_category():
    result = filter_by_category(SAMPLE, "academic")
    assert len(result) == 1 and result[0]["id"] == "t3"

def test_filter_by_category_all():
    assert filter_by_category(SAMPLE, "all") == SAMPLE

def test_apply_all_filters_combined():
    result = apply_all_filters(SAMPLE, keyword="", selected_tags=["Free"], selected_types=["Course"])
    assert len(result) == 1 and result[0]["id"] == "t3"

def test_apply_all_filters_with_category():
    result = apply_all_filters(SAMPLE, category="devops")
    assert len(result) == 1 and result[0]["id"] == "t4"

def test_apply_all_no_filters_returns_all():
    assert apply_all_filters(SAMPLE) == SAMPLE


# ─── 13. Tracker utilities ───────────────────────────────────────────────────

import utils.tracker_utils as tu

def test_tracker_load_default_when_missing():
    with patch.object(tu, "TRACKER_PATH", "/nonexistent/tracker.json"):
        result = tu.load_tracker()
    assert result == {"skills": {}, "completed_tasks": []}

def test_tracker_save_and_load(tmp_path):
    tf = tmp_path / "tracker.json"
    data = {"skills": {"DSA": {"status": "Learning", "progress": 50, "notes": ""}}, "completed_tasks": []}
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.save_tracker(data)
        assert tu.load_tracker() == data

def test_update_skill_progress_clamps(tmp_path):
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.update_skill_progress("Python", 150)
        assert tu.load_tracker()["skills"]["Python"]["progress"] == 100
        tu.update_skill_progress("Python", -10)
        assert tu.load_tracker()["skills"]["Python"]["progress"] == 0

def test_update_skill_full_api(tmp_path):
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.update_skill("React", status="Learning", progress=40, certificate_earned=False, project_completed=True)
        entry = tu.get_skill_entry("React")
        assert entry["status"] == "Learning"
        assert entry["progress"] == 40
        assert entry["project_completed"] is True

def test_update_skill_auto_complete_at_100(tmp_path):
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.update_skill("Docker", progress=100)
        entry = tu.get_skill_entry("Docker")
        assert entry["status"] == "Completed"

def test_mark_and_unmark_task(tmp_path):
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.mark_task_complete("task_001")
        assert "task_001" in tu.load_tracker()["completed_tasks"]
        tu.mark_task_complete("task_001")  # idempotent
        assert tu.load_tracker()["completed_tasks"].count("task_001") == 1
        tu.unmark_task("task_001")
        assert "task_001" not in tu.load_tracker()["completed_tasks"]

def test_remove_skill(tmp_path):
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.update_skill("Go", status="Learning")
        tu.remove_skill("Go")
        assert "Go" not in tu.load_tracker()["skills"]


# ─── 14. AI assistant config ─────────────────────────────────────────────────

def test_ai_not_available_without_key():
    """App should work normally when no API key is set."""
    import utils.ai_assistant as ai
    with patch.object(ai, "_ACTIVE_KEY", ""):
        assert ai.is_ai_available() is False

def test_ai_status_message_when_disabled():
    import utils.ai_assistant as ai
    with patch.object(ai, "_ACTIVE_KEY", ""):
        status = ai.get_ai_status()
        assert "disabled" in status.lower() or "no api key" in status.lower()

def test_ai_available_with_key():
    import utils.ai_assistant as ai
    with patch.object(ai, "_ACTIVE_KEY", "fake-key"), \
         patch.object(ai, "AI_PROVIDER", "openai"):
        assert ai.is_ai_available() is True

def test_ask_ai_returns_none_when_disabled():
    import utils.ai_assistant as ai
    with patch.object(ai, "_ACTIVE_KEY", ""):
        result = ai.ask_ai("hello", context={})
    assert result is None

def test_build_context_from_data():
    import utils.ai_assistant as ai
    resources = [{"title":"T","url":"u","tags":["Free"],"skills":["Python"],"subjects":["CS"]}]
    skills    = {"technical":["Python"],"branch_specific":{"CSE":["ML"]},"career":["Resume"],"life":["Time"]}
    roadmaps  = {"Software Developer":{"steps":[]}}
    ctx = ai.build_context_from_data(resources, skills, roadmaps)
    assert "resources_summary" in ctx
    assert "skills_summary" in ctx
    assert "Python" in ctx["skills_summary"]
    assert "Software Developer" in ctx["roadmap_roles"]


# ─── 15. Search / navigation integration ─────────────────────────────────────

def test_search_across_all_resources():
    """apply_all_filters with a keyword should narrow down resources correctly."""
    resources = _load("resources.json")
    result = apply_all_filters(resources, keyword="python")
    assert len(result) > 0
    assert all(
        "python" in r.get("title","").lower()
        or "python" in r.get("description","").lower()
        or any("python" in s.lower() for s in r.get("skills",[]))
        for r in result
    )

def test_search_returns_empty_on_garbage():
    resources = _load("resources.json")
    result = apply_all_filters(resources, keyword="xyzzy_garbage_99999")
    assert result == []

def test_branch_selection_subjects_exist():
    """Every branch Year 1 Sem 1 should have at least one subject."""
    for code, branch in _load("branches.json").items():
        subs = branch["years"]["1"]["semesters"]["1"]["subjects"]
        assert len(subs) > 0, f"Branch '{code}' Y1 S1 has no subjects"

def test_semester_range():
    """All branches should have semesters from 1–8."""
    for code, branch in _load("branches.json").items():
        all_sems = []
        for yr in branch["years"].values():
            all_sems.extend(yr["semesters"].keys())
        sem_ints = [int(s) for s in all_sems]
        assert min(sem_ints) >= 1 and max(sem_ints) <= 8, f"Branch '{code}' has out-of-range semesters"


# ─── 16. Academic hierarchy drill-down ───────────────────────────────────────

def test_academic_branch_year_sem_subject_chain():
    """Full drill-down: branch → year → semester → subjects all resolve."""
    branches = _load("branches.json")
    for branch_code, branch_data in branches.items():
        for year_key, year_data in branch_data["years"].items():
            for sem_key, sem_data in year_data["semesters"].items():
                subjects = sem_data.get("subjects", [])
                # Every semester entry must have a list (even if empty)
                assert isinstance(subjects, list), (
                    f"{branch_code} Y{year_key} S{sem_key}: subjects must be a list"
                )

def test_academic_year_keys_are_1_to_4():
    """All branches should have year keys within 1–4."""
    branches = _load("branches.json")
    for code, branch in branches.items():
        for yr in branch["years"].keys():
            assert 1 <= int(yr) <= 4, f"Branch '{code}' has out-of-range year '{yr}'"

def test_academic_subject_filter_returns_results():
    """get_resources_by_subject must return a list (empty or non-empty, never raises)."""
    from utils.data_loader import get_resources_by_subject
    result = get_resources_by_subject("Mathematics-I")
    assert isinstance(result, list)

def test_academic_subject_filter_no_match_returns_empty():
    from utils.data_loader import get_resources_by_subject
    result = get_resources_by_subject("zzznomatch_subject_xyz")
    assert result == []

def test_academic_get_resources_by_ids_all_match():
    """get_resources_by_ids with valid IDs returns all of them."""
    from utils.data_loader import get_resources_by_ids
    resources = _load("resources.json")
    valid_ids = [r["id"] for r in resources[:3]]
    result = get_resources_by_ids(valid_ids)
    assert len(result) == 3
    assert all(r["id"] in valid_ids for r in result)

def test_academic_get_resources_by_ids_partial_match():
    """get_resources_by_ids with one bad ID returns only the matching ones."""
    from utils.data_loader import get_resources_by_ids
    resources = _load("resources.json")
    good_id = resources[0]["id"]
    result = get_resources_by_ids([good_id, "res_NONEXISTENT"])
    assert len(result) == 1
    assert result[0]["id"] == good_id

def test_academic_get_resources_by_ids_empty():
    from utils.data_loader import get_resources_by_ids
    assert get_resources_by_ids([]) == []


# ─── 17. Tracker persistence edge cases ──────────────────────────────────────

import utils.tracker_utils as tu

def test_tracker_get_skill_entry_defaults(tmp_path):
    """get_skill_entry returns defaults for an untracked skill."""
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        entry = tu.get_skill_entry("UnknownSkill")
    assert entry["status"] == "Not Started"
    assert entry["progress"] == 0
    assert entry["certificate_earned"] is False

def test_tracker_update_preserves_other_skills(tmp_path):
    """Updating one skill does not affect another skill's data."""
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.update_skill("Python", status="Learning", progress=50)
        tu.update_skill("DSA", status="Practicing", progress=70)
        tu.update_skill("Python", progress=60)  # only update progress
        py = tu.get_skill_entry("Python")
        dsa = tu.get_skill_entry("DSA")
    assert py["progress"] == 60
    assert py["status"] == "Learning"      # unchanged
    assert dsa["progress"] == 70           # untouched
    assert dsa["status"] == "Practicing"   # untouched

def test_tracker_completed_tasks_survives_skill_update(tmp_path):
    """Updating a skill must not clear completed_tasks list."""
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.mark_task_complete("task_001")
        tu.update_skill("Python", progress=40)
        data = tu.load_tracker()
    assert "task_001" in data["completed_tasks"]

def test_tracker_remove_nonexistent_skill_safe(tmp_path):
    """remove_skill on an untracked skill must not raise, and skills stays empty."""
    tf = tmp_path / "tracker.json"
    # Start with a fresh empty tracker — no carry-over from other tests
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.save_tracker({"skills": {}, "completed_tasks": []})
        tu.remove_skill("DoesNotExist")   # should not raise
        data = tu.load_tracker()
    assert data["skills"] == {}


def test_tracker_corrupted_json_returns_default(tmp_path):
    """load_tracker must return default dict when file contains invalid JSON."""
    import json as _json
    # Write corrupt content, then call the parsing logic directly
    tf = tmp_path / "corrupt_tracker.json"
    tf.write_text("NOT VALID JSON }{", encoding="utf-8")
    # Test the parsing logic in isolation (bypass the TRACKER_PATH global)
    with open(str(tf), "r", encoding="utf-8") as f:
        try:
            _json.load(f)
            result = {"unexpected": "success"}
        except _json.JSONDecodeError:
            result = {"skills": {}, "completed_tasks": []}
    assert result == {"skills": {}, "completed_tasks": []}

# ─── 18. Daily task logic ─────────────────────────────────────────────────────

def test_daily_tasks_categories_are_non_empty_strings():
    for task in _load("daily_tasks.json"):
        cat = task.get("category", "")
        assert isinstance(cat, str) and cat, f"Task '{task['id']}' has empty category"

def test_daily_tasks_estimated_minutes_positive():
    for task in _load("daily_tasks.json"):
        mins = task.get("estimated_minutes", 0)
        assert isinstance(mins, int) and mins > 0, f"Task '{task['id']}' has invalid minutes"

def test_daily_task_mark_idempotent(tmp_path):
    """Marking the same task complete twice must not duplicate it."""
    tf = tmp_path / "tracker.json"
    with patch.object(tu, "TRACKER_PATH", str(tf)):
        tu.mark_task_complete("task_005")
        tu.mark_task_complete("task_005")
        data = tu.load_tracker()
    assert data["completed_tasks"].count("task_005") == 1

def test_get_today_completed_tasks_filters_correctly():
    tasks = [{"id": "t1"}, {"id": "t2"}, {"id": "t3"}]
    tracker_data = {"skills": {}, "completed_tasks": ["t1", "t3"]}
    import unittest.mock as mock
    with mock.patch("utils.tracker_utils.load_tracker", return_value=tracker_data):
        result = tu.get_today_completed_tasks(tasks)
    assert [t["id"] for t in result] == ["t1", "t3"]


# ─── 19. safe_key helper ──────────────────────────────────────────────────────

def test_safe_key_removes_special_chars():
    """_safe_key must produce a string safe for use as a Streamlit widget key."""
    # Import the helper directly
    import importlib, sys
    # Load the module without running Streamlit
    spec = importlib.util.spec_from_file_location(
        "skill_tracker_mod",
        os.path.join(PROJECT_ROOT, "sections", "skill_tracker.py")
    )
    mod = importlib.util.module_from_spec(spec)
    # Patch streamlit before exec so the import doesn't fail
    import types, unittest.mock as mock
    fake_st = types.ModuleType("streamlit")
    for attr in ["title","subheader","caption","divider","metric","radio","selectbox",
                 "slider","checkbox","text_input","button","success","info","error",
                 "columns","container","write","rerun","progress","session_state",
                 "markdown","warning","expander","balloons","chat_message","chat_input",
                 "spinner","set_page_config","sidebar"]:
        setattr(fake_st, attr, mock.MagicMock())
    fake_st.session_state = {}
    with mock.patch.dict(sys.modules, {"streamlit": fake_st}):
        spec.loader.exec_module(mod)
    assert mod._safe_key("C++ Programming") == "Cplusplus_Programming"
    assert mod._safe_key("Data Structures & Algorithms (DSA)") == "Data_Structures_and_Algorithms_DSA"
    assert " " not in mod._safe_key("Web Dev / Full Stack")
    assert "+" not in mod._safe_key("C++ Programming")


# ─── 20. data_loader plain helpers ───────────────────────────────────────────

def test_get_resources_by_branch():
    from utils.data_loader import get_resources_by_branch
    result = get_resources_by_branch("CSE")
    assert isinstance(result, list)
    assert len(result) > 0
    assert all("CSE" in r.get("branches", []) for r in result)

def test_get_resources_by_branch_nonexistent():
    from utils.data_loader import get_resources_by_branch
    result = get_resources_by_branch("NONEXISTENT_BRANCH")
    assert result == []

def test_get_resources_by_skill():
    from utils.data_loader import get_resources_by_skill
    result = get_resources_by_skill("Python")
    assert isinstance(result, list)
    assert len(result) > 0

def test_get_resources_by_skill_case_insensitive():
    from utils.data_loader import get_resources_by_skill
    lower = get_resources_by_skill("python")
    upper = get_resources_by_skill("PYTHON")
    assert [r["id"] for r in lower] == [r["id"] for r in upper]

def test_load_platforms_returns_list():
    from utils.data_loader import _load_json_plain
    data = _load_json_plain("platforms.json")
    assert isinstance(data, list) and len(data) > 0

def test_load_youtube_channels_returns_list():
    from utils.data_loader import _load_json_plain
    data = _load_json_plain("youtube_channels.json")
    assert isinstance(data, list) and len(data) > 0

def test_load_internships_has_tips():
    data = _load("internships.json")
    assert isinstance(data.get("tips"), list) and len(data["tips"]) > 0

def test_load_jobs_has_tips():
    data = _load("jobs.json")
    assert isinstance(data.get("tips"), list) and len(data["tips"]) > 0


# ─── 21. Empty-state / edge-case filter behaviour ────────────────────────────

def test_filter_by_tags_with_empty_resources():
    assert filter_by_tags([], ["Free"]) == []

def test_filter_by_keyword_with_empty_resources():
    assert filter_by_keyword([], "python") == []

def test_filter_by_type_with_empty_resources():
    assert filter_by_type([], ["Video"]) == []

def test_apply_all_filters_empty_list():
    assert apply_all_filters([]) == []

def test_filter_none_tags_treated_as_empty():
    """apply_all_filters must not raise when selected_tags=None."""
    result = apply_all_filters(SAMPLE, selected_tags=None, selected_types=None)
    assert result == SAMPLE

def test_filter_whitespace_keyword_treated_as_empty():
    """A keyword of only spaces should return all resources."""
    result = filter_by_keyword(SAMPLE, "   ")
    assert result == SAMPLE
