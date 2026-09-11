# B.Tech Student Super-Hub

A beginner-friendly Streamlit web app that helps B.Tech students navigate academics,
skills, career resources, internships, jobs, and more — all in one place.

## Features
- Academic Hub: Browse resources by Branch → Year → Semester → Subject
- Skills Hub: Technical, branch-specific, career and life skills
- Learning Resources: Tag-filtered resource browser
- Coding & Practice Hub, Project Hub, Courses & Certificates
- Internship Hub, Jobs Hub, Career Roadmaps
- Personal Skill Tracker, Daily Skill Tasks
- Global Search with tag filters

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

## Run Tests

```bash
pytest tests/
```

## Project Structure

```
betch-student-super-hub/
├── app.py                  # Entry point & sidebar navigation
├── requirements.txt
├── README.md
├── pages/                  # One file per section
│   ├── dashboard.py
│   ├── academic_hub.py
│   ├── skills_hub.py
│   └── search.py
├── components/             # Reusable UI widgets
│   ├── resource_card.py
│   ├── tag_filter.py
│   ├── section_header.py
│   └── progress_bar.py
├── data/                   # All static content (edit these to add resources)
│   ├── branches.json
│   ├── resources.json
│   ├── skills.json
│   ├── roadmaps.json
│   ├── daily_tasks.json
│   └── tracker.json
└── utils/
    ├── data_loader.py
    ├── filters.py
    └── tracker_utils.py
```

## Adding Resources
Open `data/resources.json` and add a new entry following the existing schema.
The resource will automatically appear in every relevant section.

## Phase Roadmap
- **Phase 1 (current):** Foundation — data layer, shared components, Academic Hub, Skills Hub, Search
- **Phase 2:** Learning Resources, Coding Hub, Project Hub, Courses, Internships, Jobs
- **Phase 3:** Career Roadmaps, Skill Tracker, Daily Tasks, Life & Career Skills
- **Phase 4 (future):** AI Assistant integration
