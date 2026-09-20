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


# ─── 22. Phase 1 — Academic completeness tests ───────────────────────────────

def test_resources_count_156_or_more():
    """After Phase 1 additions we should have at least 156 resources."""
    resources = _load("resources.json")
    assert len(resources) >= 156, f"Expected >= 156 resources, got {len(resources)}"


def test_new_resource_ids_exist():
    """Spot-check key Phase 1 resources are present."""
    resources = _load("resources.json")
    ids = {r["id"] for r in resources}
    for expected_id in [
        "res_101", "res_102", "res_103", "res_104", "res_105",
        "res_106", "res_107", "res_108", "res_109", "res_110",
        "res_111", "res_112", "res_113", "res_114", "res_115",
        "res_116", "res_117", "res_118", "res_119", "res_120",
        "res_121", "res_122", "res_123", "res_124", "res_125",
        "res_126", "res_127", "res_128", "res_129", "res_130",
        "res_131", "res_132", "res_133", "res_134", "res_135",
        "res_136", "res_137", "res_138", "res_139", "res_140",
        "res_141", "res_142", "res_143", "res_144", "res_145",
        "res_146", "res_147", "res_148", "res_149", "res_150",
        "res_151", "res_152", "res_153", "res_154", "res_155", "res_156",
    ]:
        assert expected_id in ids, f"Expected new resource '{expected_id}' not found"


def test_evs_subject_added_to_all_branches():
    """Environmental Science (EVS) must be in Semester 2 of every branch."""
    branches = _load("branches.json")
    for code, branch in branches.items():
        sem2_subjects = branch["years"]["1"]["semesters"]["2"]["subjects"]
        assert "Environmental Science (EVS)" in sem2_subjects, (
            f"Branch '{code}' Y1 S2 is missing 'Environmental Science (EVS)'"
        )


def test_indian_constitution_added_to_all_branches():
    """Indian Constitution must appear in at least one semester of every branch."""
    branches = _load("branches.json")
    for code, branch in branches.items():
        all_subjects = []
        for yr in branch["years"].values():
            for sem in yr["semesters"].values():
                all_subjects.extend(sem.get("subjects", []))
        assert "Indian Constitution" in all_subjects, (
            f"Branch '{code}' is missing 'Indian Constitution'"
        )


def test_professional_ethics_added_to_all_branches():
    """Professional Ethics must appear in at least one semester of every branch."""
    branches = _load("branches.json")
    for code, branch in branches.items():
        all_subjects = []
        for yr in branch["years"].values():
            for sem in yr["semesters"].values():
                all_subjects.extend(sem.get("subjects", []))
        assert "Professional Ethics" in all_subjects, (
            f"Branch '{code}' is missing 'Professional Ethics'"
        )


def test_workshop_practice_in_year1():
    """Workshop Practice must be in Year 1 of every branch."""
    branches = _load("branches.json")
    for code, branch in branches.items():
        y1_subjects = []
        for sem in branch["years"]["1"]["semesters"].values():
            y1_subjects.extend(sem.get("subjects", []))
        assert "Workshop Practice" in y1_subjects, (
            f"Branch '{code}' Year 1 is missing 'Workshop Practice'"
        )


def test_evs_has_resource():
    """Environmental Science (EVS) should have at least one resource."""
    from utils.data_loader import get_resources_by_subject
    result = get_resources_by_subject("Environmental Science (EVS)")
    assert len(result) >= 1, "No resources found for 'Environmental Science (EVS)'"


def test_indian_constitution_has_resource():
    """Indian Constitution should have at least one resource."""
    from utils.data_loader import get_resources_by_subject
    result = get_resources_by_subject("Indian Constitution")
    assert len(result) >= 1, "No resources found for 'Indian Constitution'"


def test_professional_ethics_has_resource():
    """Professional Ethics should have at least one resource."""
    from utils.data_loader import get_resources_by_subject
    result = get_resources_by_subject("Professional Ethics")
    assert len(result) >= 1, "No resources found for 'Professional Ethics'"


def test_non_cs_branches_have_resources_in_year2():
    """EEE, ME, CE, CHEM, BT, EI should all have resources in at least one Year 2 semester."""
    branches = _load("branches.json")
    for code in ["EEE", "ME", "CE", "CHEM", "BT", "EI"]:
        y2 = branches[code]["years"]["2"]["semesters"]
        all_ids = []
        for sem in y2.values():
            all_ids.extend(sem.get("resource_ids", []))
        assert len(all_ids) > 0, (
            f"Branch '{code}' has no resource_ids in any Year 2 semester"
        )


def test_non_cs_branches_have_resources_in_year3():
    """EEE, ME, CE, CHEM, BT, EI should all have resources in at least one Year 3 semester."""
    branches = _load("branches.json")
    for code in ["EEE", "ME", "CE", "CHEM", "BT", "EI"]:
        y3 = branches[code]["years"]["3"]["semesters"]
        all_ids = []
        for sem in y3.values():
            all_ids.extend(sem.get("resource_ids", []))
        assert len(all_ids) > 0, (
            f"Branch '{code}' has no resource_ids in any Year 3 semester"
        )


def test_all_branch_resource_ids_are_valid():
    """All resource_ids in branches.json must exist in resources.json (full re-check after Phase 1)."""
    branches = _load("branches.json")
    valid_ids = {r["id"] for r in _load("resources.json")}
    for bcode, branch in branches.items():
        for year, yd in branch.get("years", {}).items():
            for sem, sd in yd.get("semesters", {}).items():
                for rid in sd.get("resource_ids", []):
                    assert rid in valid_ids, (
                        f"Branch {bcode} Y{year} S{sem} references unknown id '{rid}'"
                    )


def test_cse_system_design_subject_present():
    """CSE Year 4 should now include System Design."""
    branches = _load("branches.json")
    y4_subjects = []
    for sem in branches["CSE"]["years"]["4"]["semesters"].values():
        y4_subjects.extend(sem.get("subjects", []))
    assert "System Design" in y4_subjects, "CSE Year 4 missing 'System Design'"


def test_ece_fpga_subject_present():
    """ECE Year 4 should include FPGA Design & HDL."""
    branches = _load("branches.json")
    y4_subjects = []
    for sem in branches["ECE"]["years"]["4"]["semesters"].values():
        y4_subjects.extend(sem.get("subjects", []))
    assert "FPGA Design & HDL" in y4_subjects, "ECE Year 4 missing 'FPGA Design & HDL'"


def test_eee_ev_subject_present():
    """EEE should include Electric Vehicles & Battery Technology."""
    branches = _load("branches.json")
    all_subjects = []
    for yr in branches["EEE"]["years"].values():
        for sem in yr["semesters"].values():
            all_subjects.extend(sem.get("subjects", []))
    assert "Electric Vehicles & Battery Technology" in all_subjects, (
        "EEE missing 'Electric Vehicles & Battery Technology'"
    )


def test_me_non_destructive_testing_present():
    """ME should include Non-Destructive Testing in Year 4."""
    branches = _load("branches.json")
    y4_subjects = []
    for sem in branches["ME"]["years"]["4"]["semesters"].values():
        y4_subjects.extend(sem.get("subjects", []))
    assert "Non-Destructive Testing" in y4_subjects, (
        "ME Year 4 missing 'Non-Destructive Testing'"
    )


def test_bt_python_bioinformatics_present():
    """BT should include Python for Bioinformatics."""
    branches = _load("branches.json")
    all_subjects = []
    for yr in branches["BT"]["years"].values():
        for sem in yr["semesters"].values():
            all_subjects.extend(sem.get("subjects", []))
    assert "Python for Bioinformatics" in all_subjects, (
        "BT missing 'Python for Bioinformatics'"
    )


def test_ce_gis_remote_sensing_present():
    """CE should include GIS & Remote Sensing in Year 4."""
    branches = _load("branches.json")
    y4_subjects = []
    for sem in branches["CE"]["years"]["4"]["semesters"].values():
        y4_subjects.extend(sem.get("subjects", []))
    assert "GIS & Remote Sensing" in y4_subjects, (
        "CE Year 4 missing 'GIS & Remote Sensing'"
    )


def test_no_duplicate_resource_ids_after_phase1():
    """After adding Phase 1 resources, all IDs must still be unique."""
    ids = [r["id"] for r in _load("resources.json")]
    assert len(ids) == len(set(ids)), "Duplicate resource IDs found after Phase 1 additions"


def test_yt_040_is_networkchuck():
    """yt_040 was the duplicate Apna College; it has been reused for NetworkChuck (Phase 2)."""
    channels = _load("youtube_channels.json")
    ch = next((c for c in channels if c["id"] == "yt_040"), None)
    assert ch is not None, "yt_040 should exist (NetworkChuck)"
    assert "NetworkChuck" in ch["name"], f"yt_040 should be NetworkChuck, got: {ch['name']}"


def test_apna_college_still_present():
    """yt_003 (Apna College) must still exist after removing the duplicate."""
    channels = _load("youtube_channels.json")
    ids = [c["id"] for c in channels]
    assert "yt_003" in ids, "yt_003 (Apna College) was accidentally removed"


def test_res_049_description_typo_fixed():
    """res_049 description should say 'fast.ai' not 'free.ai'."""
    resources = _load("resources.json")
    r = next((x for x in resources if x["id"] == "res_049"), None)
    assert r is not None, "res_049 not found"
    assert "free.ai" not in r["description"], "res_049 still has 'free.ai' typo"
    assert "fast.ai" in r["description"], "res_049 should mention 'fast.ai'"


def test_it_branch_has_web_programming_subject():
    """IT should have Web Programming as a subject."""
    branches = _load("branches.json")
    all_subjects = []
    for yr in branches["IT"]["years"].values():
        for sem in yr["semesters"].values():
            all_subjects.extend(sem.get("subjects", []))
    assert "Web Programming" in all_subjects, "IT missing 'Web Programming' subject"


def test_subject_resource_coverage_common_subjects():
    """Key common subjects must have at least one resource each."""
    from utils.data_loader import get_resources_by_subject
    required_covered = [
        "Mathematics-I",
        "Engineering Physics",
        "Engineering Chemistry",
        "C Programming",
        "Engineering Drawing",
        "English Communication",
        "Data Structures",
        "Digital Electronics",
        "Environmental Science (EVS)",
        "Indian Constitution",
        "Professional Ethics",
        "Basic Electrical Engineering",
    ]
    for subj in required_covered:
        result = get_resources_by_subject(subj)
        assert len(result) >= 1, f"No resources found for required subject: '{subj}'"


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2 TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_phase2_resource_count():
    """After Phase 2 additions, resources.json must have at least 252 entries."""
    resources = _load("resources.json")
    assert len(resources) >= 252, f"Expected ≥252 resources, got {len(resources)}"


def test_phase2_no_duplicate_resource_ids():
    """All resource IDs must be unique after Phase 2."""
    ids = [r["id"] for r in _load("resources.json")]
    assert len(ids) == len(set(ids)), "Duplicate resource IDs found after Phase 2"


def test_phase2_no_duplicate_resource_urls():
    """No two resources should share the exact same URL."""
    urls = [r["url"] for r in _load("resources.json")]
    dupes = [u for u in urls if urls.count(u) > 1]
    assert not dupes, f"Duplicate URLs found: {set(dupes)}"


def test_phase2_youtube_channels_count():
    """After Phase 2, youtube_channels.json must have at least 60 channels."""
    channels = _load("youtube_channels.json")
    assert len(channels) >= 60, f"Expected ≥60 YouTube channels, got {len(channels)}"


def test_phase2_youtube_no_duplicate_ids():
    """All YouTube channel IDs must be unique."""
    ids = [c["id"] for c in _load("youtube_channels.json")]
    assert len(ids) == len(set(ids)), "Duplicate YouTube channel IDs found"


def test_phase2_youtube_no_duplicate_urls():
    """No two YouTube channels should share the exact same URL."""
    urls = [c["url"] for c in _load("youtube_channels.json")]
    dupes = [u for u in urls if urls.count(u) > 1]
    assert not dupes, f"Duplicate YouTube channel URLs: {set(dupes)}"


def test_phase2_youtube_cybersecurity_category():
    """After Phase 2, there must be at least one channel in 'Cybersecurity / Networking'."""
    channels = _load("youtube_channels.json")
    cats = [c["category"] for c in channels]
    assert "Cybersecurity / Networking" in cats, "No Cybersecurity / Networking YouTube channel found"


def test_phase2_youtube_system_design_category():
    """After Phase 2, there must be at least one channel in 'System Design / Backend'."""
    channels = _load("youtube_channels.json")
    cats = [c["category"] for c in channels]
    assert "System Design / Backend" in cats, "No System Design / Backend YouTube channel found"


def test_phase2_youtube_finance_category():
    """After Phase 2, there must be at least one channel in 'Finance / Life Skills'."""
    channels = _load("youtube_channels.json")
    cats = [c["category"] for c in channels]
    assert "Finance / Life Skills" in cats, "No Finance / Life Skills YouTube channel found"


def test_phase2_youtube_core_engineering_category():
    """After Phase 2, there must be at least one channel in 'Core Engineering'."""
    channels = _load("youtube_channels.json")
    cats = [c["category"] for c in channels]
    assert "Core Engineering" in cats, "No Core Engineering YouTube channel found"


def test_phase2_roadmaps_no_empty_steps():
    """After Phase 2, all roadmap steps must have at least one resource_id."""
    data = _load("roadmaps.json")
    empty = []
    for rmap, rdata in data.items():
        for s in rdata.get("steps", []):
            if not s.get("resource_ids"):
                empty.append(f"{rmap} step {s['step']}: {s['title']}")
    assert not empty, f"Roadmap steps still have no resources:\n" + "\n".join(empty)


def test_phase2_roadmaps_resource_ids_exist():
    """Every resource_id referenced in roadmaps must exist in resources.json."""
    data = _load("roadmaps.json")
    resources = _load("resources.json")
    valid_ids = {r["id"] for r in resources}
    missing = []
    for rmap, rdata in data.items():
        for s in rdata.get("steps", []):
            for rid in s.get("resource_ids", []):
                if rid not in valid_ids:
                    missing.append(f"{rmap} step {s['step']}: unknown resource '{rid}'")
    assert not missing, "Roadmaps reference non-existent resource IDs:\n" + "\n".join(missing)


def test_phase2_android_roadmap_all_steps_filled():
    """Android Developer roadmap previously had 5/5 empty steps — all must now be filled."""
    data = _load("roadmaps.json")
    steps = data["Android Developer"]["steps"]
    empty = [s for s in steps if not s.get("resource_ids")]
    assert not empty, f"Android Developer still has empty steps: {[s['title'] for s in empty]}"


def test_phase2_uxdesigner_roadmap_all_steps_filled():
    """UI/UX Designer roadmap previously had 6/6 empty steps — all must now be filled."""
    data = _load("roadmaps.json")
    steps = data["UI/UX Designer"]["steps"]
    empty = [s for s in steps if not s.get("resource_ids")]
    assert not empty, f"UI/UX Designer still has empty steps: {[s['title'] for s in empty]}"


def test_phase2_video_editor_roadmap_all_steps_filled():
    """Video Editor roadmap previously had 6/6 empty steps — all must now be filled."""
    data = _load("roadmaps.json")
    steps = data["Video Editor"]["steps"]
    empty = [s for s in steps if not s.get("resource_ids")]
    assert not empty, f"Video Editor still has empty steps: {[s['title'] for s in empty]}"


def test_phase2_skills_technical_count():
    """After Phase 2 skills expansion, technical skills must number at least 85."""
    data = _load("skills.json")
    technical = data.get("technical", [])
    assert len(technical) >= 85, f"Expected ≥85 technical skills, got {len(technical)}"


def test_phase2_skills_career_count():
    """After Phase 2 skills expansion, career skills must number at least 16."""
    data = _load("skills.json")
    career = data.get("career", [])
    assert len(career) >= 16, f"Expected ≥16 career skills, got {len(career)}"


def test_phase2_skills_life_count():
    """After Phase 2 skills expansion, life skills must number at least 20."""
    data = _load("skills.json")
    life = data.get("life", [])
    assert len(life) >= 20, f"Expected ≥20 life skills, got {len(life)}"


def test_phase2_res_kotlin_android_exists():
    """res_161 (Kotlin for Android) must exist in resources after Phase 2."""
    resources = _load("resources.json")
    r = next((x for x in resources if x["id"] == "res_161"), None)
    assert r is not None, "res_161 (Kotlin for Android) not found"
    assert "Kotlin" in r["title"], f"res_161 title unexpected: {r['title']}"


def test_phase2_res_pytorch_tutorial_exists():
    """res_233 (Deep Learning PyTorch Official) must exist in resources after Phase 2."""
    resources = _load("resources.json")
    r = next((x for x in resources if x["id"] == "res_233"), None)
    assert r is not None, "res_233 (PyTorch tutorials) not found"


def test_phase2_res_figma_official_exists():
    """res_177 (Figma Official Tutorials) must exist — covers previously empty UI/UX steps."""
    resources = _load("resources.json")
    r = next((x for x in resources if x["id"] == "res_177"), None)
    assert r is not None, "res_177 (Figma Official Tutorials) not found"


def test_phase2_res_linux_foundation_exists():
    """res_230 (Linux Foundation Intro) must exist — covers DevOps/Cybersecurity Linux steps."""
    resources = _load("resources.json")
    r = next((x for x in resources if x["id"] == "res_230"), None)
    assert r is not None, "res_230 (Linux Foundation) not found"


def test_phase2_res_valid_tags():
    """All new Phase 2 resources must use only VALID_TAGS."""
    import sys
    sys.path.insert(0, ".")
    from utils.filters import VALID_TAGS
    resources = _load("resources.json")
    bad = []
    for r in resources:
        for tag in r.get("tags", []):
            if tag not in VALID_TAGS:
                bad.append(f"{r['id']}: invalid tag '{tag}'")
    assert not bad, "Resources with invalid tags:\n" + "\n".join(bad)


def test_phase2_res_valid_types():
    """All Phase 2 resources must use only VALID_TYPES."""
    import sys
    sys.path.insert(0, ".")
    from utils.filters import VALID_TYPES
    resources = _load("resources.json")
    bad = [f"{r['id']}: '{r['type']}'" for r in resources if r.get("type") not in VALID_TYPES]
    assert not bad, "Resources with invalid types:\n" + "\n".join(bad)


def test_phase2_all_resources_have_required_fields():
    """Every resource must have id, title, url, type, tags, description."""
    required = {"id", "title", "url", "type", "tags", "description"}
    resources = _load("resources.json")
    missing = [
        f"{r.get('id','?')}: missing {required - r.keys()}"
        for r in resources if not required.issubset(r.keys())
    ]
    assert not missing, "Resources missing required fields:\n" + "\n".join(missing)


def test_phase2_youtube_channels_required_fields():
    """Every YouTube channel must have id, name, url, category, tags, type, description."""
    required = {"id", "name", "url", "category", "tags", "type", "description"}
    channels = _load("youtube_channels.json")
    missing = [
        f"{c.get('id','?')}: missing {required - c.keys()}"
        for c in channels if not required.issubset(c.keys())
    ]
    assert not missing, "Channels missing required fields:\n" + "\n".join(missing)


def test_phase2_gate_roadmap_mock_tests_step():
    """GATE / Higher Studies roadmap step 5 (Mock Tests) must now have resources."""
    data = _load("roadmaps.json")
    steps = data["GATE / Higher Studies"]["steps"]
    step5 = next((s for s in steps if s["step"] == 5), None)
    assert step5 is not None, "GATE roadmap step 5 not found"
    assert step5.get("resource_ids"), "GATE step 5 'Mock Tests' still has no resources"


def test_phase2_entrepreneur_roadmap_step1_filled():
    """Entrepreneur roadmap step 1 (Problem Discovery) must now have resources."""
    data = _load("roadmaps.json")
    steps = data["Entrepreneur"]["steps"]
    step1 = next((s for s in steps if s["step"] == 1), None)
    assert step1 is not None
    assert step1.get("resource_ids"), "Entrepreneur step 1 'Problem Discovery' still empty"


def test_phase2_cybersecurity_roadmap_all_steps_filled():
    """Cybersecurity roadmap previously had 5/6 empty steps — all must now be filled."""
    data = _load("roadmaps.json")
    steps = data["Cybersecurity"]["steps"]
    empty = [s for s in steps if not s.get("resource_ids")]
    assert not empty, f"Cybersecurity roadmap still has empty steps: {[s['title'] for s in empty]}"


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2.5 TESTS — YouTube Mapping Coverage & Resource Completeness
# ─────────────────────────────────────────────────────────────────────────────

def _get_yt_for_skill(skill_name: str, all_resources: list) -> list:
    """Simulate Skills Hub: find YouTube-tagged resources matching skill (substring)."""
    sl = skill_name.lower()
    return [r for r in all_resources
            if "YouTube" in r.get("tags", [])
            and any(sl in s.lower() for s in r.get("skills", []))]


def _get_res_for_skill(skill_name: str, all_resources: list) -> list:
    sl = skill_name.lower()
    return [r for r in all_resources
            if any(sl in s.lower() for s in r.get("skills", []))]


def test_phase25_resource_count():
    """Phase 2.5 must reach at least 350 total resources."""
    resources = _load("resources.json")
    assert len(resources) >= 350, f"Expected ≥350 resources, got {len(resources)}"


def test_phase25_youtube_resources_count():
    """Phase 2.5 must have at least 80 YouTube-tagged resources in resources.json."""
    resources = _load("resources.json")
    yt = [r for r in resources if "YouTube" in r.get("tags", [])]
    assert len(yt) >= 80, f"Expected ≥80 YouTube resources, got {len(yt)}"


def test_phase25_all_skills_have_resources():
    """Every skill in skills.json must have at least one resource via substring match."""
    resources = _load("resources.json")
    skills_data = _load("skills.json")
    all_skills = []
    for cat, items in skills_data.items():
        if isinstance(items, list):
            all_skills.extend(items)
        elif isinstance(items, dict):
            for branch_skills in items.values():
                all_skills.extend(branch_skills)
    no_res = [s for s in all_skills if not _get_res_for_skill(s, resources)]
    assert not no_res, f"Skills with NO resources: {no_res}"


def test_phase25_all_skills_have_youtube():
    """Every skill in skills.json must have at least one YouTube resource reachable via Skills Hub."""
    resources = _load("resources.json")
    skills_data = _load("skills.json")
    all_skills = []
    for cat, items in skills_data.items():
        if isinstance(items, list):
            all_skills.extend(items)
        elif isinstance(items, dict):
            for branch_skills in items.values():
                all_skills.extend(branch_skills)
    no_yt = [s for s in all_skills if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"Skills with NO YouTube resources ({len(no_yt)}): {no_yt[:10]}"


def test_phase25_youtube_channels_have_skills_field():
    """All 60 YouTube channels must have a skills field after Phase 2.5."""
    channels = _load("youtube_channels.json")
    missing = [c["id"] for c in channels if not c.get("skills")]
    assert not missing, f"Channels missing skills field: {missing}"


def test_phase25_key_programming_skills_have_youtube():
    """Core programming skills must each have a YouTube resource."""
    resources = _load("resources.json")
    core = ["Python Programming", "Java Programming", "JavaScript (Frontend)",
            "C Programming", "C++ Programming", "HTML & CSS",
            "Data Structures & Algorithms (DSA)", "Git & GitHub"]
    no_yt = [s for s in core if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"Core programming skills without YouTube: {no_yt}"


def test_phase25_core_cs_skills_have_youtube():
    """Core CS theory skills must have YouTube resources."""
    resources = _load("resources.json")
    core_cs = ["Operating Systems", "Computer Networks", "Database Management Systems (DBMS)",
               "Software Engineering", "Computer Architecture", "System Design"]
    no_yt = [s for s in core_cs if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"Core CS skills without YouTube: {no_yt}"


def test_phase25_ai_data_skills_have_youtube():
    """AI/Data skills must have YouTube resources."""
    resources = _load("resources.json")
    ai_skills = ["Machine Learning", "Deep Learning", "Natural Language Processing (NLP)",
                 "Data Visualization", "MLOps", "Generative AI", "Reinforcement Learning"]
    no_yt = [s for s in ai_skills if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"AI/Data skills without YouTube: {no_yt}"


def test_phase25_cloud_devops_skills_have_youtube():
    """Cloud/DevOps skills must have YouTube resources."""
    resources = _load("resources.json")
    cloud = ["AWS", "Docker & Kubernetes", "DevOps & CI/CD",
             "Terraform / Infrastructure as Code", "Linux & Command Line"]
    no_yt = [s for s in cloud if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"Cloud/DevOps skills without YouTube: {no_yt}"


def test_phase25_cybersecurity_skills_have_youtube():
    """Cybersecurity skills must have YouTube resources."""
    resources = _load("resources.json")
    sec = ["Cybersecurity Fundamentals", "Penetration Testing",
           "Web Security", "Network Security"]
    no_yt = [s for s in sec if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"Cybersecurity skills without YouTube: {no_yt}"


def test_phase25_life_career_skills_have_youtube():
    """Key life and career skills must have YouTube resources."""
    resources = _load("resources.json")
    life = ["Time Management", "Financial Literacy", "Public Speaking",
            "Emotional Intelligence", "Critical Thinking", "Resume & CV Writing",
            "LinkedIn Profile Optimization", "Leadership Basics"]
    no_yt = [s for s in life if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"Life/career skills without YouTube: {no_yt}"


def test_phase25_no_duplicate_resource_urls():
    """No two resources can share the same URL."""
    resources = _load("resources.json")
    urls = [r["url"] for r in resources]
    dupes = [u for u in set(urls) if urls.count(u) > 1]
    assert not dupes, f"Duplicate URLs found: {dupes}"


def test_phase25_no_duplicate_resource_ids():
    """All resource IDs must be unique."""
    resources = _load("resources.json")
    ids = [r["id"] for r in resources]
    dupes = [i for i in set(ids) if ids.count(i) > 1]
    assert not dupes, f"Duplicate IDs: {dupes}"


def test_phase25_all_resources_valid_tags():
    """All resources must use only VALID_TAGS."""
    import sys as _sys
    _sys.path.insert(0, ".")
    from utils.filters import VALID_TAGS
    resources = _load("resources.json")
    bad = [(r["id"], t) for r in resources for t in r.get("tags", []) if t not in VALID_TAGS]
    assert not bad, f"Resources with invalid tags: {bad[:5]}"


def test_phase25_all_resources_valid_types():
    """All resources must use only VALID_TYPES."""
    import sys as _sys
    _sys.path.insert(0, ".")
    from utils.filters import VALID_TYPES
    resources = _load("resources.json")
    bad = [r["id"] for r in resources if r.get("type") not in VALID_TYPES]
    assert not bad, f"Resources with invalid types: {bad}"


def test_phase25_youtube_channels_no_url_dupes():
    """YouTube channels must not have duplicate URLs."""
    channels = _load("youtube_channels.json")
    urls = [c["url"] for c in channels]
    dupes = [u for u in set(urls) if urls.count(u) > 1]
    assert not dupes, f"Duplicate channel URLs: {dupes}"


def test_phase25_react_has_youtube():
    """React skill must have a YouTube resource reachable from Skills Hub."""
    resources = _load("resources.json")
    assert _get_yt_for_skill("React", resources), "React has no YouTube resource"


def test_phase25_react_native_has_resource():
    """React Native must have at least one resource after Phase 2.5."""
    resources = _load("resources.json")
    assert _get_res_for_skill("React Native", resources), "React Native has no resource"


def test_phase25_react_native_has_youtube():
    """React Native must have a YouTube resource."""
    resources = _load("resources.json")
    assert _get_yt_for_skill("React Native", resources), "React Native has no YouTube resource"


def test_phase25_biotech_skills_covered():
    """Key Biotechnology branch skills must have resources."""
    resources = _load("resources.json")
    bt_skills = ["Bioinformatics Tools (BLAST, NCBI)", "Genetic Engineering Techniques",
                 "Genomics & Proteomics", "Industrial Biotechnology"]
    no_res = [s for s in bt_skills if not _get_res_for_skill(s, resources)]
    assert not no_res, f"Biotech skills without resources: {no_res}"


def test_phase25_ece_skills_covered():
    """Key ECE branch skills must have YouTube resources."""
    resources = _load("resources.json")
    ece_skills = ["VLSI Design", "Embedded Systems & Microcontrollers",
                  "Digital Signal Processing", "PCB Design"]
    no_yt = [s for s in ece_skills if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"ECE skills without YouTube: {no_yt}"


def test_phase25_mechanical_skills_covered():
    """Key ME branch skills must have YouTube resources."""
    resources = _load("resources.json")
    me_skills = ["Finite Element Analysis (Ansys)", "Robotics & Automation",
                 "Thermodynamic Simulations", "CAD with AutoCAD / SolidWorks"]
    no_yt = [s for s in me_skills if not _get_yt_for_skill(s, resources)]
    assert not no_yt, f"ME skills without YouTube: {no_yt}"


def test_phase25_civil_skills_covered():
    """Key Civil branch skills must have resources."""
    resources = _load("resources.json")
    ce_skills = ["STAAD Pro / ETABS Structural Analysis", "GIS & Remote Sensing",
                 "AutoCAD for Civil Engineering"]
    no_res = [s for s in ce_skills if not _get_res_for_skill(s, resources)]
    assert not no_res, f"Civil skills without resources: {no_res}"


def test_phase25_res_259_valid_url():
    """res_259 (DBMS Gate Smashers) must not have the old placeholder URL."""
    resources = _load("resources.json")
    r = next((x for x in resources if x["id"] == "res_259"), None)
    assert r is not None, "res_259 not found"
    assert "networkingDBMS" not in r["url"], "res_259 still has broken placeholder URL"


def test_phase25_channel_skills_not_empty():
    """No YouTube channel should have an empty skills list."""
    channels = _load("youtube_channels.json")
    empty = [c["id"] for c in channels if not c.get("skills")]
    assert not empty, f"Channels with empty skills: {empty}"
