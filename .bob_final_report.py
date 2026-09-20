"""Final Phase 2.5 Gap Report"""
import json

resources = json.load(open('data/resources.json', encoding='utf-8'))
channels = json.load(open('data/youtube_channels.json', encoding='utf-8'))
skills_data = json.load(open('data/skills.json', encoding='utf-8'))
branches = json.load(open('data/branches.json', encoding='utf-8'))
roadmaps = json.load(open('data/roadmaps.json', encoding='utf-8'))

def get_yt(s):
    sl = s.lower()
    return [r for r in resources if 'YouTube' in r.get('tags',[]) and any(sl in sk.lower() for sk in r.get('skills',[]))]

def get_res(s):
    sl = s.lower()
    return [r for r in resources if any(sl in sk.lower() for sk in r.get('skills',[]))]

all_skills = {}
for cat, items in skills_data.items():
    if isinstance(items, list):
        for s in items: all_skills[s] = cat
    elif isinstance(items, dict):
        for b, bs in items.items():
            for s in bs: all_skills[s] = f'branch/{b}'

# Subjects
all_subjects = set()
for bname, bdata in branches.items():
    for yr, yrdata in bdata.get('years',{}).items():
        for sem, semdata in yrdata.get('semesters',{}).items():
            for subj in semdata.get('subjects',[]):
                all_subjects.add(subj)

subj_with_res = {s for s in all_subjects if any(s in r.get('subjects',[]) for r in resources)}
lab_subjects = {s for s in all_subjects if any(x in s.lower() for x in ['lab','project','internship','elective','mini project'])}
theory_subjects = all_subjects - lab_subjects
theory_with_res = subj_with_res & theory_subjects
theory_without_res = theory_subjects - subj_with_res

# Roadmaps
all_steps = 0
filled_steps = 0
for rmap, rdata in roadmaps.items():
    for s in rdata.get('steps',[]):
        all_steps += 1
        if s.get('resource_ids'): filled_steps += 1

skills_with_res = [s for s in all_skills if get_res(s)]
skills_without_res = [s for s in all_skills if not get_res(s)]
skills_with_yt = [s for s in all_skills if get_yt(s)]
skills_without_yt = [s for s in all_skills if not get_yt(s)]

yt_tagged = [r for r in resources if 'YouTube' in r.get('tags',[])]
yt_skill_mappings = sum(len(r.get('skills',[])) for r in yt_tagged)

print('=== PHASE 2.5 FINAL GAP REPORT ===')
print()
print('--- ACADEMIC SUBJECTS ---')
print(f'Total unique subjects: {len(all_subjects)}')
print(f'Theory subjects: {len(theory_subjects)}')
print(f'Theory subjects WITH direct resource mapping: {len(theory_with_res)}')
print(f'Theory subjects WITHOUT direct resource mapping: {len(theory_without_res)}')
print(f'Lab/Project/Elective subjects (intentional gap): {len(lab_subjects)}')
print()
print('--- SKILLS ---')
print(f'Total skills: {len(all_skills)}')
print(f'Skills WITH learning resources: {len(skills_with_res)}')
print(f'Skills WITHOUT learning resources: {len(skills_without_res)}')
if skills_without_res:
    for s in skills_without_res: print(f'  NO-RES: {s}')
print(f'Skills WITH YouTube resources: {len(skills_with_yt)}')
print(f'Skills WITHOUT YouTube resources: {len(skills_without_yt)}')
if skills_without_yt:
    for s in skills_without_yt: print(f'  NO-YT: {s}')
print()
print('--- YOUTUBE ---')
print(f'YouTube channels (youtube_channels.json): {len(channels)}')
print(f'Channels with skills field: {sum(1 for c in channels if c.get("skills"))}')
print(f'YouTube-tagged resources (resources.json): {len(yt_tagged)}')
print(f'Total YouTube-to-skill mappings: {yt_skill_mappings}')
print()
print('--- ROADMAPS ---')
print(f'Career roadmaps: {len(roadmaps)}')
print(f'Steps filled: {filled_steps}/{all_steps}')
print()
print('--- FILES ---')
print('data/resources.json', len(resources), 'resources')
print('data/youtube_channels.json', len(channels), 'channels')
print('data/skills.json', sum(len(v) for v in skills_data.values()), 'skills')
print('data/roadmaps.json', len(roadmaps), 'roadmaps')
print()
print('--- DATA QUALITY ---')
ids = [r['id'] for r in resources]
urls = [r['url'] for r in resources]
print('ID dupes:', len([i for i in set(ids) if ids.count(i)>1]))
print('URL dupes:', len([u for u in set(urls) if urls.count(u)>1]))
from utils.filters import VALID_TAGS, VALID_TYPES
bad_t = [(r['id'],t) for r in resources for t in r.get('tags',[]) if t not in VALID_TAGS]
bad_ty = [r['id'] for r in resources if r.get('type') not in VALID_TYPES]
print('Bad tags:', len(bad_t))
print('Bad types:', len(bad_ty))
