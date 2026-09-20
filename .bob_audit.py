import json

with open('data/skills.json') as f:
    skills = json.load(f)
with open('data/resources.json') as f:
    resources = json.load(f)
with open('data/youtube_channels.json') as f:
    channels = json.load(f)
with open('data/roadmaps.json') as f:
    roadmaps = json.load(f)
with open('data/branches.json') as f:
    branches = json.load(f)

tech = skills.get('technical', [])
branch_specific = skills.get('branch_specific', {})
career = skills.get('career', [])
life = skills.get('life', [])

all_branch_skills = []
for blist in branch_specific.values():
    all_branch_skills.extend(blist)

total_skills = len(tech) + len(career) + len(life) + len(all_branch_skills)
print(f'=== SKILLS ===')
print(f'Technical: {len(tech)}, Branch-specific: {len(all_branch_skills)}, Career: {len(career)}, Life: {len(life)}, Total: {total_skills}')

print(f'\n=== RESOURCES ===')
print(f'Total: {len(resources)}')
type_counts = {}
for r in resources:
    t = r.get('type','?')
    type_counts[t] = type_counts.get(t, 0) + 1
print('Types:', dict(sorted(type_counts.items())))

# Map skills covered by resources
skills_covered_by_res = set()
for r in resources:
    for s in r.get('skills', []):
        skills_covered_by_res.add(s.lower().strip())

print('\n=== TECHNICAL SKILLS WITHOUT RESOURCES ===')
missing_tech = []
for s in tech:
    sl = s.lower()
    # partial match OK
    if not any(sl in covered or covered in sl for covered in skills_covered_by_res):
        missing_tech.append(s)
print(f'Count: {len(missing_tech)}')
for s in missing_tech:
    print(f'  - {s}')

print('\n=== CAREER SKILLS WITHOUT RESOURCES ===')
missing_career = []
for s in career:
    sl = s.lower()
    if not any(sl in covered or covered in sl for covered in skills_covered_by_res):
        missing_career.append(s)
print(f'Count: {len(missing_career)}')
for s in missing_career:
    print(f'  - {s}')

print('\n=== LIFE SKILLS WITHOUT RESOURCES ===')
missing_life = []
for s in life:
    sl = s.lower()
    if not any(sl in covered or covered in sl for covered in skills_covered_by_res):
        missing_life.append(s)
print(f'Count: {len(missing_life)}')
for s in missing_life:
    print(f'  - {s}')

print('\n=== YOUTUBE CHANNELS ===')
print(f'Total: {len(channels)}')
cats = {}
for c in channels:
    cat = c.get('category','?')
    cats[cat] = cats.get(cat,0)+1
print('Categories:', dict(sorted(cats.items())))
# Check for duplicate URLs
urls = [c.get('url','') for c in channels]
dup_urls = [u for u in set(urls) if urls.count(u) > 1]
if dup_urls:
    print(f'DUPLICATE URLs: {dup_urls}')

print('\n=== ROADMAP RESOURCE GAPS ===')
valid_res_ids = {r['id'] for r in resources}
for role, rm in roadmaps.items():
    empty = [s for s in rm.get('steps',[]) if not s.get('resource_ids')]
    if empty:
        print(f'  {role}: {len(empty)}/{len(rm.get("steps",[]))} steps empty: {[s["title"] for s in empty]}')

print('\n=== DUPLICATE RESOURCE CHECK ===')
ids = [r['id'] for r in resources]
dup_ids = [i for i in set(ids) if ids.count(i)>1]
res_urls = [r.get('url','') for r in resources]
dup_urls_res = [u for u in set(res_urls) if res_urls.count(u)>1 and u]
print(f'Duplicate IDs: {dup_ids}')
print(f'Duplicate URLs: {len(dup_urls_res)}')
for u in dup_urls_res[:10]:
    print(f'  {u}')

print('\n=== ACADEMIC SUBJECTS COVERAGE ===')
all_subjects = set()
for branch in branches.values():
    for year in branch['years'].values():
        for sem in year['semesters'].values():
            for s in sem['subjects']:
                all_subjects.add(s)

subjects_covered = set()
for r in resources:
    for s in r.get('subjects', []):
        subjects_covered.add(s)

skip = ['Lab', 'Project Phase', 'Elective-', 'Internship', 'Mini Project']
real_subs = [s for s in all_subjects if not any(p in s for p in skip)]
covered_real = [s for s in real_subs if s in subjects_covered]
uncovered_real = [s for s in real_subs if s not in subjects_covered]
print(f'Total unique subjects: {len(all_subjects)}')
print(f'Substantive (non-lab/project): {len(real_subs)}')
print(f'Covered: {len(covered_real)}, Uncovered: {len(uncovered_real)}')
print('UNCOVERED:')
for s in sorted(uncovered_real):
    print(f'  - {s}')
