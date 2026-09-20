import json

data = json.load(open('data/roadmaps.json'))

# Mapping of roadmap -> step number -> resource_ids to ADD (merged with existing)
fixes = {
    "Frontend Developer": {
        3: ["res_162"],        # React Official Tutorial
        5: ["res_203"],        # MIT Missing Semester (tools/debugging)
    },
    "Backend Developer": {
        3: ["res_166", "res_201"],   # FastAPI tutorial + REST API Udemy
    },
    "Full Stack Developer": {
        2: ["res_162", "res_163"],   # React + Next.js
    },
    "Android Developer": {
        1: ["res_161"],              # Kotlin for Android (Official)
        2: ["res_161"],              # Android Fundamentals — same Google resource
        3: ["res_161"],              # Jetpack Compose — same Kotlin/Android resource
        4: ["res_164"],              # Node.js / networking basics
        5: ["res_209"],              # GitHub Open Source Guides (publishing / releasing)
    },
    "AI Engineer": {
        3: ["res_233"],              # Deep Learning — PyTorch Official
        4: ["res_234"],              # LLMs & Generative AI — DeepLearning.AI
    },
    "ML Engineer": {
        3: ["res_233"],              # Deep Learning — PyTorch Official
        4: ["res_202"],              # Python for Data Science / pipelines — IBM Coursera
    },
    "Data Scientist": {
        5: ["res_236", "res_237"],   # Power BI + Tableau
    },
    "Data Analyst": {
        1: ["res_235"],              # Excel — Microsoft Official
        4: ["res_236", "res_237"],   # Power BI + Tableau
        5: ["res_174"],              # Time Series / statistics — Kaggle Learn
    },
    "Data Engineer": {
        4: ["res_238"],              # MLflow (experiment tracking / orchestration context)
        5: ["res_202"],              # Python for Data Science — IBM (data modelling)
    },
    "Cloud Engineer": {
        3: ["res_170"],              # Terraform — HashiCorp Official
        5: ["res_239"],              # AWS Well-Architected Security
    },
    "DevOps Engineer": {
        1: ["res_230"],              # Linux Foundation Intro
    },
    "Cybersecurity": {
        2: ["res_230"],              # Linux Foundation Intro
        3: ["res_176"],              # OWASP Top 10 (security concepts)
        4: ["res_175"],              # TryHackMe Jr Penetration Tester
        5: ["res_176"],              # OWASP Top 10 (web security)
        6: ["res_185"],              # NPTEL GATE / cert prep (closest cert-prep resource)
    },
    "MLOps Engineer": {
        3: ["res_238"],              # MLflow Official Docs
        5: ["res_171"],              # Prometheus & Grafana Monitoring
    },
    "UI/UX Designer": {
        1: ["res_178"],              # Google UX Design Certificate
        2: ["res_177"],              # Figma Official Tutorials
        3: ["res_178"],              # Google UX Design Certificate covers UX Research
        4: ["res_177"],              # Figma prototyping / interaction
        5: ["res_178"],              # Google UX Design covers accessibility
        6: ["res_244"],              # Technical Blogging / portfolio (Dev.to)
    },
    "Product Designer": {
        1: ["res_178"],              # Google UX Design Certificate
        2: ["res_177"],              # Figma Official Tutorials
        3: ["res_188"],              # YC Startup School (product thinking)
        4: ["res_208"],              # Agile & Scrum — Scrum Alliance
        5: ["res_244"],              # Dev.to / portfolio building
    },
    "Technical Writer": {
        4: ["res_166"],              # FastAPI (API documentation context)
        5: ["res_244"],              # Dev.to / Hashnode portfolio
    },
    "Game Developer": {
        2: ["res_157"],              # C++ full course (Unity uses C#, closest available)
        3: ["res_157"],              # C++ / programming — build 2D game context
        4: ["res_157"],              # 3D fundamentals — programming foundation
        5: ["res_209"],              # GitHub guides — publishing / release
    },
    "Product Manager": {
        1: ["res_188"],              # YC Startup School (product thinking)
        2: ["res_207"],              # Group Discussion / user research skills
        3: ["res_208"],              # Agile & Scrum (prioritisation frameworks context)
        4: ["res_208"],              # Agile & Scrum
    },
    "Graphic Designer": {
        1: ["res_178"],              # Google UX Design (design principles)
        2: ["res_179"],              # Canva Design School
        3: ["res_179"],              # Canva (branding)
        4: ["res_179"],              # Canva (digital vs print)
        5: ["res_244"],              # Dev.to / portfolio
    },
    "Video Editor": {
        1: ["res_180"],              # DaVinci Resolve (storytelling / editing context)
        2: ["res_180"],              # DaVinci Resolve Official Tutorials
        3: ["res_180"],              # DaVinci Resolve (colour grading)
        4: ["res_180"],              # DaVinci Resolve (audio)
        5: ["res_180"],              # DaVinci Resolve Fusion (motion graphics)
        6: ["res_244"],              # Dev.to / portfolio / YouTube channel
    },
    "Entrepreneur": {
        1: ["res_188"],              # YC Startup School (problem discovery)
        3: ["res_188"],              # YC Startup School (validate & iterate)
        4: ["res_181", "res_250"],   # Google Digital Marketing + Sales course
        6: ["res_188"],              # YC Startup School (network / support)
    },
    "GATE / Higher Studies": {
        5: ["res_185", "res_186"],   # NPTEL GATE + Khan Academy GRE
    },
}

# Apply fixes
for roadmap_name, step_fixes in fixes.items():
    if roadmap_name not in data:
        print(f"WARNING: roadmap '{roadmap_name}' not found")
        continue
    steps = data[roadmap_name]["steps"]
    for step_num, new_ids in step_fixes.items():
        step = next((s for s in steps if s["step"] == step_num), None)
        if step is None:
            print(f"WARNING: step {step_num} not found in '{roadmap_name}'")
            continue
        existing = step.get("resource_ids", [])
        merged = existing + [i for i in new_ids if i not in existing]
        step["resource_ids"] = merged

with open('data/roadmaps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Verify
empty_count = 0
for rmap, rdata in data.items():
    for s in rdata.get("steps", []):
        if not s.get("resource_ids"):
            empty_count += 1
            print(f"Still empty: {rmap} step {s['step']}: {s['title']}")

print(f"\nDone. Remaining empty steps: {empty_count}")
