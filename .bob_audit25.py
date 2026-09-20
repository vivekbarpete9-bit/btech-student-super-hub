"""
Phase 2.5 Complete Audit Script
Checks every skill for: learning resource, YouTube resource (in resources.json with YouTube tag)
"""
import json, sys
sys.path.insert(0, '.')

resources = json.load(open('data/resources.json', encoding='utf-8'))
skills_data = json.load(open('data/skills.json', encoding='utf-8'))
channels = json.load(open('data/youtube_channels.json', encoding='utf-8'))
branches = json.load(open('data/branches.json', encoding='utf-8'))
roadmaps = json.load(open('data/roadmaps.json', encoding='utf-8'))

# Build skill->resources mapping (case-insensitive)
def get_res_for_skill(skill):
    sl = skill.lower()
    return [r for r in resources if any(sl in s.lower() for s in r.get('skills', []))]

def get_yt_for_skill(skill):
    return [r for r in get_res_for_skill(skill) if 'YouTube' in r.get('tags', [])]

# All skills flat list
all_skills = {}
for cat, items in skills_data.items():
    if isinstance(items, list):
        for s in items:
            all_skills[s] = cat
    elif isinstance(items, dict):
        for branch, bskills in items.items():
            for s in bskills:
                all_skills[s] = f"branch_specific/{branch}"

print(f"Total skills: {len(all_skills)}")
print(f"Total resources: {len(resources)}")
print(f"YouTube-tagged resources: {len([r for r in resources if 'YouTube' in r.get('tags',[])])}")
print(f"YouTube channels (separate file): {len(channels)}")
print()

# Skills with NO resources at all
no_res = []
no_yt = []
has_res = []
has_yt = []

for skill, cat in sorted(all_skills.items()):
    res_list = get_res_for_skill(skill)
    yt_list = get_yt_for_skill(skill)
    if not res_list:
        no_res.append((skill, cat))
    else:
        has_res.append((skill, cat))
    if not yt_list:
        no_yt.append((skill, cat))
    else:
        has_yt.append((skill, cat))

print(f"Skills WITH learning resources: {len(has_res)}")
print(f"Skills WITHOUT learning resources: {len(no_res)}")
print(f"Skills WITH YouTube resources: {len(has_yt)}")
print(f"Skills WITHOUT YouTube resources: {len(no_yt)}")
print()

print("=== SKILLS WITHOUT ANY LEARNING RESOURCE ===")
for s, c in no_res:
    print(f"  [{c}] {s}")

print()
print("=== SKILLS WITHOUT YOUTUBE RESOURCES ===")
for s, c in no_yt:
    print(f"  [{c}] {s}")

# Subject audit
print()
print("=== SUBJECTS (from branches.json) ===")
all_subjects = set()
for bname, bdata in branches.items():
    for yr, yrdata in bdata.get('years', {}).items():
        for sem, semdata in yrdata.get('semesters', {}).items():
            for subj in semdata.get('subjects', []):
                all_subjects.add(subj)

subjects_with_res = set()
subjects_without_res = set()
for subj in sorted(all_subjects):
    res_list = [r for r in resources if subj in r.get('subjects', [])]
    if res_list:
        subjects_with_res.add(subj)
    else:
        subjects_without_res.add(subj)

print(f"Total unique subjects: {len(all_subjects)}")
print(f"Subjects with direct resource mapping: {len(subjects_with_res)}")
print(f"Subjects without direct resource mapping: {len(subjects_without_res)}")
print()
print("Subjects without direct resource mapping:")
for s in sorted(subjects_without_res):
    print(f"  {s}")
