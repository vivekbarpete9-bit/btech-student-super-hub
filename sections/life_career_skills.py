"""
pages/life_career_skills.py
---------------------------
Life & Career Skills — A curated guide to soft skills, communication,
personal development, and career readiness.
"""

import streamlit as st
from components.section_header import section_header

LIFE_SKILLS = {
    "💬 Communication": {
        "desc": "The single most important skill in every career.",
        "skills": [
            ("Verbal Communication", "Speak clearly, confidently and concisely. Practise summarising ideas in 30 seconds."),
            ("Written Communication", "Clear emails, reports, and messages. Short sentences. Active voice. Structured paragraphs."),
            ("Non-verbal Communication", "Body language, eye contact, and posture convey as much as words."),
            ("Active Listening", "Listen to understand, not to reply. Ask follow-up questions."),
            ("Public Speaking", "Join Toastmasters, practise on YouTube, or speak at college events."),
        ],
        "resources": [
            ("TED Talks", "https://www.ted.com/"),
            ("Charisma on Command (YouTube)", "https://www.youtube.com/@CharismaOnCommand"),
            ("NPTEL Soft Skills", "https://nptel.ac.in/courses/109/104/109104093/"),
        ]
    },
    "🤝 People & Leadership": {
        "desc": "How you work with others determines how far you go.",
        "skills": [
            ("Emotional Intelligence (EQ)", "Understand and manage your own emotions. Empathise with others."),
            ("Networking", "Building genuine relationships — not collecting contacts."),
            ("Teamwork & Collaboration", "Collaborate effectively, contribute your fair share, support teammates."),
            ("Leadership Basics", "Influence without authority. Take ownership. Develop others."),
            ("Conflict Resolution", "Address disagreements constructively — focus on issues, not people."),
        ],
        "resources": [
            ("Big Think (YouTube)", "https://www.youtube.com/@bigthink"),
            ("HBR Leadership Articles", "https://hbr.org/topic/subject/leadership"),
        ]
    },
    "🧠 Thinking Skills": {
        "desc": "How you approach problems sets you apart.",
        "skills": [
            ("Critical Thinking", "Question assumptions. Evaluate evidence. Avoid logical fallacies."),
            ("Problem Solving", "Break problems into parts. Generate options. Pick the best path."),
            ("Decision Making", "Use frameworks: pros/cons, 10/10/10, first principles."),
            ("Creativity", "Combine ideas from different domains. Embrace curiosity."),
        ],
        "resources": [
            ("TED-Ed (YouTube)", "https://www.youtube.com/@TEDEd"),
        ]
    },
    "⚡ Self Management": {
        "desc": "Managing yourself is the foundation of managing everything else.",
        "skills": [
            ("Time Management", "Time-block your calendar. Protect deep work time. Use the Pomodoro technique."),
            ("Discipline & Consistency", "Small daily habits compound. Show up even when you don't feel like it."),
            ("Habit Building", "Use habit stacking and environment design to make good habits automatic."),
            ("Resilience & Mental Health", "Build emotional robustness. Rest is productive. Seek help when needed."),
            ("Learning How to Learn", "Spaced repetition, active recall, the Feynman technique."),
            ("Productivity Tools", "Notion, Obsidian, Trello, Google Calendar — pick one and master it."),
        ],
        "resources": [
            ("Ali Abdaal (YouTube)", "https://www.youtube.com/@aliabdaal"),
            ("Thomas Frank (YouTube)", "https://www.youtube.com/@Thomasfrank"),
            ("Ankur Warikoo (YouTube)", "https://www.youtube.com/@warikoo"),
        ]
    },
    "💼 Career Skills": {
        "desc": "Skills that directly influence your job search and career growth.",
        "skills": [
            ("Resume Building", "1 page. Bullet points with impact (what you did + result). Use ATS-friendly format."),
            ("LinkedIn / Online Presence", "Professional photo, clear headline, skills, and 3+ recommendations."),
            ("Personal Branding", "What do you want to be known for? Be consistent across platforms."),
            ("Interview Skills", "STAR method for behavioral questions. Practice DSA and system design for tech."),
            ("Professional Email", "Short. Clear subject. One ask per email. Reply within 24 hours."),
            ("Digital Literacy", "Spreadsheets, presentations, collaboration tools — non-negotiable."),
            ("AI Literacy", "Know what AI tools can and can't do. Use them to amplify your work, not replace thinking."),
            ("Presentation Skills", "Tell a story. Know your audience. Fewer slides, more impact."),
        ],
        "resources": [
            ("Internshala Resume Guide", "https://trainings.internshala.com/resume-writing-training/"),
            ("LinkedIn Learning", "https://www.linkedin.com/learning/"),
            ("IBM SkillsBuild", "https://skillsbuild.org/"),
        ]
    },
    "💰 Business & Finance": {
        "desc": "Basic business literacy for engineers entering the workforce.",
        "skills": [
            ("Financial Literacy", "Understand salary, tax (Form 16), savings, SIP investing, emergency fund."),
            ("Basic Sales & Persuasion", "Ethical persuasion: understand needs, offer value, be honest about limitations."),
            ("Negotiation", "Know your value. Research market rates. Ask — the worst they can say is no."),
            ("Entrepreneurship Mindset", "Customer obsession, bias for action, learning from failure."),
        ],
        "resources": [
            ("Ankur Warikoo (Financial Literacy)", "https://www.youtube.com/@warikoo"),
            ("Alex Hormozi (Business)", "https://www.youtube.com/@AlexHormozi"),
            ("Stanford GSB (YouTube)", "https://www.youtube.com/@stanfordgsb"),
        ]
    },
}


def show() -> None:
    section_header("Life & Career Skills", "The skills that determine how far you go — beyond your technical degree.", "🌱")

    st.info(
        "💡 **Note:** These skills are not taught in most B.Tech programmes — but they are "
        "evaluated in every interview, workplace and leadership role. "
        "Start building them now."
    )

    st.divider()

    category_names = list(LIFE_SKILLS.keys())
    tabs = st.tabs(category_names)

    for tab, cat_name in zip(tabs, category_names):
        with tab:
            cat_data = LIFE_SKILLS[cat_name]
            st.caption(cat_data["desc"])

            for skill_name, tip in cat_data["skills"]:
                with st.container(border=True):
                    st.markdown(f"**{skill_name}**")
                    st.caption(tip)

            if cat_data.get("resources"):
                st.markdown("**📚 Resources to improve:**")
                for name, url in cat_data["resources"]:
                    st.markdown(f"- [{name}]({url})")
