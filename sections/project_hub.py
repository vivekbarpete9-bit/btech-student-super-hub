"""
pages/project_hub.py
--------------------
Project Hub — Resources for finding project ideas, building, and deploying.
"""

import streamlit as st
from components.section_header import section_header

PROJECT_RESOURCES = [
    {"name": "GitHub", "url": "https://github.com/", "tags": ["Free","Projects","Global"], "desc": "Host code, collaborate, contribute to open source."},
    {"name": "GitLab", "url": "https://gitlab.com/", "tags": ["Free","Projects","Global"], "desc": "Git hosting with built-in CI/CD — great for DevOps projects."},
    {"name": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions", "tags": ["Free","Projects","Practice","Global"], "desc": "Real-world data science projects and competitions."},
    {"name": "Devpost", "url": "https://devpost.com/", "tags": ["Free","Projects","Global"], "desc": "Find hackathons and showcase completed projects."},
    {"name": "Major League Hacking (MLH)", "url": "https://mlh.io/", "tags": ["Free","Projects","Global"], "desc": "Official student hackathon league — beginner-friendly events."},
    {"name": "Unstop Hackathons", "url": "https://unstop.com/hackathons", "tags": ["Free","Projects","India"], "desc": "India's largest hackathon and competition platform."},
    {"name": "GitHub Student Pack", "url": "https://education.github.com/pack", "tags": ["Free","Projects","Global"], "desc": "Free tools for students: GitHub Pro, JetBrains, DigitalOcean credits."},
    {"name": "Vercel (Deploy)", "url": "https://vercel.com/", "tags": ["Free","Projects","Global"], "desc": "Deploy web apps instantly — great for frontend and full-stack projects."},
    {"name": "Netlify (Deploy)", "url": "https://www.netlify.com/", "tags": ["Free","Projects","Global"], "desc": "Free static site and serverless function hosting."},
    {"name": "Render (Deploy)", "url": "https://render.com/", "tags": ["Free","Projects","Global"], "desc": "Deploy full-stack apps, APIs, and databases for free."},
    {"name": "GitHub Explore (Ideas)", "url": "https://github.com/explore", "tags": ["Free","Projects","Global"], "desc": "Discover trending repos and get project inspiration."},
    {"name": "roadmap.sh Projects", "url": "https://roadmap.sh/projects", "tags": ["Free","Projects","Global"], "desc": "Structured project ideas with beginner to advanced levels."},
    {"name": "awesome-for-beginners", "url": "https://github.com/MunGell/awesome-for-beginners", "tags": ["Free","Projects","Global"], "desc": "Open-source repos that welcome first-time contributors."},
    {"name": "Read the Docs", "url": "https://readthedocs.org/", "tags": ["Free","Projects","Global"], "desc": "Free documentation hosting for open-source projects."},
    {"name": "Shields.io", "url": "https://shields.io/", "tags": ["Free","Projects","Global"], "desc": "Add professional badges to your GitHub README."},
]

CATEGORIES = {
    "🌱 Beginner": ["Build a personal portfolio website", "Create a to-do list app", "Number guessing game (Python)", "Simple calculator", "Weather app using a free API", "Student grade calculator"],
    "🔧 Intermediate": ["Blog with user authentication", "REST API with Flask or Express", "E-commerce product page", "Chat app with WebSockets", "URL shortener", "Book/Movie review app"],
    "🔥 Advanced": ["Full-stack MERN/PERN application", "Real-time collaborative editor", "ML-powered recommendation engine", "Microservices with Docker & Kubernetes", "DevOps CI/CD pipeline"],
    "🌐 Web": ["Portfolio site", "Weather dashboard", "Quiz app", "Job board clone", "Blog CMS"],
    "📱 App": ["Habit tracker (Android/Flutter)", "Expense tracker", "Flashcard study app", "Notes app with sync"],
    "🤖 AI / Data": ["Sentiment analysis tool", "Image classifier", "Chatbot with LangChain", "Stock price predictor", "Kaggle competition submission"],
    "🔌 IoT": ["Smart home automation (Arduino/ESP32)", "Weather station with sensors", "Plant watering system"],
    "🔒 Cybersecurity": ["Password strength checker", "Port scanner (Python)", "Basic firewall rule simulator"],
    "🏗️ Engineering": ["Structural load calculator (Civil)", "Signal processing demo (ECE)", "Chemical process simulation (Chem)", "CNC path visualiser (ME)"],
}


def show() -> None:
    section_header("Project Hub", "Find ideas, tools, and platforms to build your engineering portfolio.", "🚀")

    tabs = st.tabs(["💡 Project Ideas", "🛠️ Build & Deploy Tools", "🤝 Open Source & Hackathons"])

    with tabs[0]:
        st.subheader("Project Ideas by Category")
        st.caption("Pick a level or domain — build it, put it on GitHub, and share the link in job applications.")
        for cat, ideas in CATEGORIES.items():
            with st.expander(cat):
                for idea in ideas:
                    st.markdown(f"• {idea}")

    with tabs[1]:
        st.subheader("Build & Deploy Resources")
        col1, col2 = st.columns(2)
        for i, res in enumerate(PROJECT_RESOURCES):
            with (col1 if i % 2 == 0 else col2):
                with st.container(border=True):
                    st.markdown(f"**[{res['name']}]({res['url']})**")
                    st.caption(res["desc"])
                    st.markdown(" ".join(f"`{t}`" for t in res["tags"]))

    with tabs[2]:
        st.subheader("Open Source & Hackathons")
        st.markdown("""
**Why contribute to open source?**
- Real code review from experienced developers.
- Visible commits on your GitHub profile.
- Networking with developers worldwide.
- Many internships and jobs ask about OSS contributions.

**How to start:**
1. Search [awesome-for-beginners](https://github.com/MunGell/awesome-for-beginners) for projects that welcome new contributors.
2. Read the `CONTRIBUTING.md` file before making a PR.
3. Start with documentation fixes or small bug reports.
4. Join a [Major League Hacking](https://mlh.io/) hackathon — they're beginner-friendly.
5. [Devpost](https://devpost.com/) has remote hackathons with prizes — great for your resume.
        """)
