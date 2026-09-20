import json

resources = json.load(open('data/resources.json', encoding='utf-8'))
skills_data = json.load(open('data/skills.json', encoding='utf-8'))
channels = json.load(open('data/youtube_channels.json', encoding='utf-8'))
roadmaps = json.load(open('data/roadmaps.json', encoding='utf-8'))
branches = json.load(open('data/branches.json', encoding='utf-8'))

total_branches = len(branches)
total_subs = 0
sems_with_resources = 0
sems_total = 0
for bname, bdata in branches.items():
    for yrname, yrdata in bdata.get('years', {}).items():
        for semname, semdata in yrdata.get('semesters', {}).items():
            total_subs += len(semdata.get('subjects', []))
            sems_total += 1
            if semdata.get('resource_ids'):
                sems_with_resources += 1

total_steps = sum(len(v.get('steps', [])) for v in roadmaps.values())
filled_steps = sum(1 for v in roadmaps.values() for s in v.get('steps', []) if s.get('resource_ids'))
empty_steps = [(rmap, s['step'], s['title']) for rmap, v in roadmaps.items() for s in v.get('steps', []) if not s.get('resource_ids')]

yt_categories = sorted(set(c['category'] for c in channels))

print("=== PHASE 2 SECOND GAP AUDIT ===\n")
print(f"Branches: {total_branches}")
print(f"Total subjects (sum across all branches): {total_subs}")
print(f"Semesters with resources: {sems_with_resources}/{sems_total}")
print(f"Resources total: {len(resources)}")
print()
print("Skills breakdown:")
for cat, skills in skills_data.items():
    print(f"  {cat}: {len(skills)}")
print(f"  TOTAL: {sum(len(v) for v in skills_data.values())}")
print()
print(f"YouTube channels: {len(channels)} in {len(yt_categories)} categories")
for cat in yt_categories:
    count = sum(1 for c in channels if c['category'] == cat)
    print(f"  {cat}: {count}")
print()
print(f"Career roadmaps: {len(roadmaps)}")
print(f"Roadmap steps filled: {filled_steps}/{total_steps}")
if empty_steps:
    print("  Still empty:")
    for rmap, step, title in empty_steps:
        print(f"    {rmap} step {step}: {title}")
else:
    print("  All roadmap steps have resources ✓")

# Resource URL duplicates check
urls = [r['url'] for r in resources]
url_dupes = [u for u in set(urls) if urls.count(u) > 1]
print()
print(f"Duplicate resource URLs: {len(url_dupes)}")
if url_dupes:
    for u in url_dupes:
        print(f"  {u}")

# ID uniqueness
ids = [r['id'] for r in resources]
id_dupes = [i for i in set(ids) if ids.count(i) > 1]
print(f"Duplicate resource IDs: {len(id_dupes)}")

# Tags check
from utils.filters import VALID_TAGS, VALID_TYPES
bad_tags = [(r['id'], t) for r in resources for t in r.get('tags', []) if t not in VALID_TAGS]
bad_types = [(r['id'], r.get('type')) for r in resources if r.get('type') not in VALID_TYPES]
print(f"Resources with invalid tags: {len(bad_tags)}")
print(f"Resources with invalid types: {len(bad_types)}")

print("\n=== SUMMARY ===")
print(f"Phase 2 complete: {filled_steps == total_steps and not url_dupes and not id_dupes and not bad_tags and not bad_types}")
