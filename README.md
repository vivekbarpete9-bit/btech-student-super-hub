# B.Tech Student Super-Hub

A beginner-friendly Streamlit web app that helps B.Tech students navigate academics,
skills, career resources, internships, jobs, and more — all in one place.

## Features
- **Academic Hub**: Browse resources by Branch → Year → Semester → Subject → Resources
- **Skills Hub**: Technical, branch-specific, career and life skills
- **Learning Resources**: Tag-filtered resource browser with platforms and YouTube channels
- **Coding & Practice Hub**: LeetCode, HackerRank, CodeChef, Codeforces and more
- **Project Hub**: Project ideas (beginner to advanced), build tools, hackathons
- **Courses & Certificates**: Free and paid courses with certifications
- **Internship Hub**: India and global internship platforms with tips
- **Jobs Hub**: Job platforms India and global with prep checklist
- **Career Roadmaps**: Step-by-step paths for 22+ roles
- **Personal Skill Tracker**: Track your learning progress
- **Daily Skill Tasks**: Daily micro-tasks to build skills consistently
- **Life & Career Skills**: Soft skills, finance, communication
- **AI Assistant**: Personalised advice powered by OpenAI or Groq (optional)
- **Global Search**: Find any resource across the entire hub

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

### Enabling the AI Assistant (optional)

```bash
# Copy the example env file
cp .env.example .env
# Edit .env and fill in your API key (OpenAI or Groq)

# Linux/macOS
export OPENAI_API_KEY="sk-..."
streamlit run app.py

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
streamlit run app.py
```

## Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```
betch-student-super-hub/
├── app.py                   # Entry point & sidebar navigation
├── requirements.txt
├── README.md
├── .env.example             # Template for AI assistant API key
├── sections/                # One file per page/section
│   ├── dashboard.py
│   ├── academic_hub.py
│   ├── skills_hub.py
│   ├── learning_resources.py
│   ├── coding_practice.py
│   ├── project_hub.py
│   ├── courses_certificates.py
│   ├── internship_hub.py
│   ├── jobs_hub.py
│   ├── career_roadmaps.py
│   ├── skill_tracker.py
│   ├── daily_tasks.py
│   ├── life_career_skills.py
│   ├── ai_assistant.py
│   └── search.py
├── components/              # Reusable UI widgets
│   ├── resource_card.py
│   ├── tag_filter.py
│   ├── section_header.py
│   └── progress_bar.py
├── data/                    # All static content (edit these to add resources)
│   ├── branches.json        # 10 branches × 4 years × 2 semesters × subjects
│   ├── resources.json       # 156 verified learning resources
│   ├── skills.json          # Technical, branch-specific, career and life skills
│   ├── roadmaps.json        # 22 career roadmaps
│   ├── daily_tasks.json     # Daily skill tasks
│   ├── platforms.json       # 53 learning platforms
│   ├── youtube_channels.json # 39 YouTube channels
│   ├── internships.json     # India & global internship platforms
│   ├── jobs.json            # India & global job platforms
│   └── tracker.json         # User's personal progress (auto-created)
├── utils/
│   ├── data_loader.py
│   ├── filters.py
│   ├── tracker_utils.py
│   └── ai_assistant.py
└── tests/
    └── test_data.py         # 146 tests
```

## Adding Resources

Open `data/resources.json` and add a new entry following the existing schema.
The resource will automatically appear in every relevant section (Academic Hub,
Skills Hub, Career Roadmaps, Search) based on its `subjects`, `skills`, and `branches` fields.

## Supported Branches

| Code | Branch |
|------|--------|
| CSE | Computer Science & Engineering |
| IT | Information Technology |
| AI_DS | AI & Data Science |
| ECE | Electronics & Communication Engineering |
| EEE | Electrical & Electronics Engineering |
| ME | Mechanical Engineering |
| CE | Civil Engineering |
| CHEM | Chemical Engineering |
| BT | Biotechnology |
| EI | Electronics & Instrumentation Engineering |

## Phase Roadmap

- **Phase 1 (complete):** Academic completeness — all branches Y1–Y4, common subjects (EVS, Constitution, Ethics, Workshop), branch-specific subjects, 156 verified resources with full mapping
- **Phase 2 (planned):** Skills/YouTube additions, Hackathons & Events page, About section, missing roadmap resources
- **Phase 3 (planned):** UI/UX redesign — cyber/futuristic theme, dark mode, animated dashboard
- **Phase 4 (planned):** AI Assistant enhancements — dotenv integration, streaming responses, Gemini/Ollama support
