"""
Phase 2.5 Cleanup Script
- Fix res_259 broken DBMS URL
- Enrich res_015 and res_045 skills fields
- Enrich res_258, res_260 playlist URLs
"""
import json

resources = json.load(open('data/resources.json', encoding='utf-8'))

fixes = {
    # res_015: Docker/Kubernetes (was skills=['Docker','Kubernetes','DevOps'])
    "res_015": {
        "skills": ["Docker & Kubernetes", "DevOps & CI/CD", "Cloud Computing",
                   "Docker", "Kubernetes", "DevOps"]
    },
    # res_045: HTML/CSS (was skills=['HTML','CSS','Frontend Development'])
    "res_045": {
        "skills": ["HTML & CSS", "Frontend Development", "JavaScript (Frontend)",
                   "HTML", "CSS"]
    },
    # res_259: Fix broken placeholder DBMS URL -> use actual Gate Smashers DBMS playlist
    "res_259": {
        "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiFAN6I8CuViBuCdJn2GtXKE",
        "title": "DBMS Full Course – Gate Smashers (YouTube Playlist)",
        "skills": ["Database Management Systems (DBMS)", "SQL"],
        "description": "Gate Smashers complete DBMS playlist — ER model, normalization, transactions, SQL, indexing and query optimization."
    },
    # res_258: OS playlist URL
    "res_258": {
        "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p",
        "skills": ["Operating Systems"],
        "description": "Gate Smashers full OS playlist — processes, threads, memory management, scheduling, deadlocks, and file systems."
    },
    # res_260: Computer Networks playlist URL
    "res_260": {
        "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiGCN6C5MJEXPaO5KMmO9oi3",
        "skills": ["Computer Networks", "Network Security"],
        "description": "Gate Smashers full Computer Networks playlist — OSI model, TCP/IP, routing, subnetting, and network security."
    },
}

updated = 0
for r in resources:
    if r['id'] in fixes:
        for k, v in fixes[r['id']].items():
            r[k] = v
        updated += 1

with open('data/resources.json', 'w', encoding='utf-8') as f:
    json.dump(resources, f, indent=2, ensure_ascii=False)

print(f"Cleanup done: {updated} resources updated")

# Verify
resources2 = json.load(open('data/resources.json', encoding='utf-8'))
urls = [r['url'] for r in resources2]
dupes = [u for u in set(urls) if urls.count(u) > 1]
ids = [r['id'] for r in resources2]
id_dupes = [i for i in set(ids) if ids.count(i) > 1]
print(f"Total resources: {len(resources2)}")
print(f"URL dupes: {dupes}")
print(f"ID dupes: {id_dupes}")
