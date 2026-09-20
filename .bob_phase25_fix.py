"""
Phase 2.5 Fix Script
====================
Step 1: Add skills field to youtube_channels.json entries
Step 2: Add YouTube-tagged resources for skills with no YouTube coverage
Step 3: Add learning resources for skills with zero resources
"""
import json

# ─────────────────────────────────────────────────────────────────
# STEP 1: Add skills mappings to youtube_channels.json
# ─────────────────────────────────────────────────────────────────

CHANNEL_SKILLS = {
    "yt_001": {  # freeCodeCamp
        "skills": ["Python Programming", "JavaScript (Frontend)", "HTML & CSS", "React",
                   "Node.js", "Data Structures & Algorithms (DSA)", "C Programming",
                   "SQL", "Data Analysis", "Machine Learning", "Docker & Kubernetes",
                   "Backend Development", "Full Stack Development", "Git & GitHub",
                   "Computer Networks", "Linux & Command Line", "Bash / Shell Scripting",
                   "TypeScript", "Django", "Flask", "FastAPI", "Express.js"]
    },
    "yt_002": {  # CodeWithHarry
        "skills": ["Python Programming", "C Programming", "C++ Programming", "JavaScript (Frontend)",
                   "HTML & CSS", "Java Programming", "SQL", "Web Security", "Django",
                   "Backend Development", "Full Stack Development", "Data Structures & Algorithms (DSA)"]
    },
    "yt_003": {  # Apna College
        "skills": ["Java Programming", "C++ Programming", "Data Structures & Algorithms (DSA)",
                   "Python Programming", "SQL", "Object-Oriented Programming (OOP)", "GATE / GRE Preparation"]
    },
    "yt_004": {  # Traversy Media
        "skills": ["HTML & CSS", "JavaScript (Frontend)", "React", "Node.js", "Express.js",
                   "Full Stack Development", "Backend Development", "REST APIs",
                   "TypeScript", "Next.js", "Flutter", "Mobile Development"]
    },
    "yt_005": {  # The Net Ninja
        "skills": ["JavaScript (Frontend)", "React", "Vue", "Django", "Node.js",
                   "HTML & CSS", "TypeScript", "Flutter", "Firebase", "Next.js",
                   "GraphQL", "Full Stack Development", "Mobile Development"]
    },
    "yt_006": {  # Programming with Mosh
        "skills": ["Python Programming", "JavaScript (Frontend)", "React", "SQL",
                   "C++ Programming", "Java Programming", "Node.js", "HTML & CSS",
                   "Object-Oriented Programming (OOP)", "Data Structures & Algorithms (DSA)"]
    },
    "yt_007": {  # The Coding Train
        "skills": ["JavaScript (Frontend)", "Python Programming", "Algorithms",
                   "Machine Learning", "Creativity", "Problem Solving"]
    },
    "yt_008": {  # Neso Academy
        "skills": ["Computer Networks", "Digital Electronics", "C Programming",
                   "Operating Systems", "Database Management Systems (DBMS)",
                   "Computer Architecture", "Communication Systems",
                   "Signals & Systems", "GATE / GRE Preparation",
                   "Electronic Circuits", "Embedded Systems & Microcontrollers"]
    },
    "yt_009": {  # Gate Smashers
        "skills": ["Operating Systems", "Database Management Systems (DBMS)",
                   "Computer Networks", "Theory of Computation", "Compiler Design",
                   "Data Structures & Algorithms (DSA)", "GATE / GRE Preparation",
                   "Software Engineering", "Computer Architecture"]
    },
    "yt_010": {  # Jenny's Lectures
        "skills": ["Algorithms", "Data Structures & Algorithms (DSA)", "C Programming",
                   "Python Programming", "Operating Systems", "GATE / GRE Preparation",
                   "Computer Architecture", "Software Engineering"]
    },
    "yt_011": {  # Abdul Bari
        "skills": ["Data Structures & Algorithms (DSA)", "Algorithms",
                   "GATE / GRE Preparation", "Compiler Design", "Theory of Computation"]
    },
    "yt_012": {  # Striver / takeUforward
        "skills": ["Data Structures & Algorithms (DSA)", "Competitive Programming Strategy",
                   "Technical Interview Preparation", "Java Programming",
                   "System Design", "Problem Solving"]
    },
    "yt_013": {  # Kunal Kushwaha
        "skills": ["Data Structures & Algorithms (DSA)", "Java Programming",
                   "Open Source Contribution", "Git & GitHub",
                   "Technical Interview Preparation", "Problem Solving"]
    },
    "yt_014": {  # Two Minute Papers
        "skills": ["Machine Learning", "Deep Learning", "Generative AI",
                   "AI Research Methods", "Reinforcement Learning", "Computer Vision",
                   "Natural Language Processing (NLP)", "Explainable AI (XAI)"]
    },
    "yt_015": {  # Computerphile
        "skills": ["Computer Networks", "Operating Systems", "Cybersecurity Fundamentals",
                   "Algorithms", "Machine Learning", "Natural Language Processing (NLP)",
                   "Web Security", "Cryptography", "AI Literacy for Professionals"]
    },
    "yt_016": {  # AI Explained
        "skills": ["Generative AI", "AI Literacy for Professionals", "Machine Learning",
                   "Deep Learning", "AI Agents", "Responsible AI", "Prompt Engineering"]
    },
    "yt_017": {  # Matt Wolfe
        "skills": ["Generative AI", "AI Literacy for Professionals", "Content Creation",
                   "Prompt Engineering", "AI Agents", "Digital Marketing"]
    },
    "yt_018": {  # Ali Abdaal
        "skills": ["Productivity Tools (Notion, Trello)", "Time Management", "Learning How to Learn",
                   "Habit Building", "Personal Branding Online", "Freelancing Basics",
                   "Technical Blogging & Portfolio Building", "Discipline & Consistency",
                   "Growth Mindset", "Career Planning"]
    },
    "yt_019": {  # Thomas Frank
        "skills": ["Productivity Tools (Notion, Trello)", "Time Management",
                   "Learning How to Learn", "Habit Building", "Discipline & Consistency",
                   "Study Skills"]
    },
    "yt_020": {  # Ankur Warikoo
        "skills": ["Career Planning", "Financial Literacy", "Entrepreneurship & Startups",
                   "Personal Branding Online", "Internship Search Strategies",
                   "Resume & CV Writing", "LinkedIn Profile Optimization",
                   "Freelancing Basics", "Decision Making", "Leadership Basics",
                   "Entrepreneurship Mindset"]
    },
    "yt_021": {  # The Art of Improvement
        "skills": ["Decision Making", "Habit Building", "Critical Thinking",
                   "Growth Mindset", "Emotional Intelligence", "Resilience & Mental Health",
                   "Problem Solving", "Productivity Tools (Notion, Trello)"]
    },
    "yt_022": {  # Improvement Pill
        "skills": ["Habit Building", "Discipline & Consistency", "Time Management",
                   "Stress Management", "Growth Mindset", "Resilience & Mental Health"]
    },
    "yt_023": {  # Alex Hormozi
        "skills": ["Entrepreneurship & Startups", "Basic Sales & Persuasion",
                   "Entrepreneurship Mindset", "Negotiation", "Personal Branding Online",
                   "Leadership Basics", "Content Creation"]
    },
    "yt_024": {  # Valuetainment
        "skills": ["Entrepreneurship & Startups", "Entrepreneurship Mindset",
                   "Leadership Basics", "Basic Sales & Persuasion",
                   "Decision Making", "Career Planning"]
    },
    "yt_025": {  # Stanford GSB
        "skills": ["Entrepreneurship & Startups", "Leadership Basics",
                   "Higher Studies Planning (MS/MBA)", "Decision Making",
                   "Product Management", "Entrepreneurship Mindset"]
    },
    "yt_026": {  # Harvard Business Review
        "skills": ["Leadership Basics", "Teamwork & Collaboration",
                   "Decision Making", "Emotional Intelligence",
                   "Professional Networking", "Entrepreneurship & Startups"]
    },
    "yt_027": {  # TED
        "skills": ["Public Speaking", "Presentation Skills", "Critical Thinking",
                   "Leadership Basics", "Creativity", "Communication — Verbal",
                   "AI Literacy for Professionals", "Emotional Intelligence"]
    },
    "yt_028": {  # TED-Ed
        "skills": ["Critical Thinking", "Learning How to Learn", "Problem Solving",
                   "Creativity", "Communication — Verbal", "AI Literacy for Professionals"]
    },
    "yt_029": {  # Big Think
        "skills": ["Critical Thinking", "Decision Making", "Creativity",
                   "Leadership Basics", "AI Literacy for Professionals",
                   "Emotional Intelligence", "Growth Mindset"]
    },
    "yt_030": {  # Charisma on Command
        "skills": ["Communication — Verbal", "Public Speaking", "Active Listening",
                   "Presentation Skills", "Non-verbal Communication",
                   "Emotional Intelligence", "Teamwork & Collaboration"]
    },
    "yt_031": {  # Kurzgesagt
        "skills": ["Critical Thinking", "AI Literacy for Professionals",
                   "Environmental Engineering", "Problem Solving"]
    },
    "yt_032": {  # Veritasium
        "skills": ["Statistics for Data Science", "Mathematics", "Physics",
                   "Critical Thinking", "Problem Solving", "Learning How to Learn"]
    },
    "yt_033": {  # Mark Rober
        "skills": ["Problem Solving", "Creativity", "Engineering Design",
                   "Product Design & Development"]
    },
    "yt_034": {  # SmarterEveryDay
        "skills": ["Problem Solving", "Mechanical Engineering",
                   "Thermodynamic Simulations", "Physics", "Engineering Design"]
    },
    "yt_035": {  # CrashCourse
        "skills": ["Statistics for Data Science", "Computer Architecture",
                   "Software Engineering", "Critical Thinking",
                   "AI Literacy for Professionals", "Learning How to Learn"]
    },
    "yt_036": {  # Numberphile
        "skills": ["Mathematics", "Statistics for Data Science",
                   "Algorithms", "Cryptography"]
    },
    "yt_037": {  # 3Blue1Brown
        "skills": ["Mathematics", "Statistics for Data Science",
                   "Machine Learning", "Deep Learning", "Linear Algebra",
                   "Neural Networks", "Python for Data Science"]
    },
    "yt_038": {  # Sentdex
        "skills": ["Python Programming", "Machine Learning", "Deep Learning",
                   "Python for Data Science", "Data Analysis",
                   "Natural Language Processing (NLP)", "Computer Vision"]
    },
    "yt_039": {  # TechWorld with Nana
        "skills": ["Docker & Kubernetes", "DevOps & CI/CD", "Cloud Computing",
                   "Terraform / Infrastructure as Code", "Monitoring & Observability",
                   "Git & GitHub", "Linux & Command Line", "Kubernetes"]
    },
    "yt_040": {  # NetworkChuck
        "skills": ["Computer Networks", "Cybersecurity Fundamentals", "Linux & Command Line",
                   "Ethical Security Concepts", "Network Security",
                   "Penetration Testing", "Bash / Shell Scripting", "Security Awareness"]
    },
    "yt_041": {  # John Hammond
        "skills": ["Penetration Testing", "Cybersecurity Fundamentals",
                   "Web Security", "Application Security",
                   "Ethical Security Concepts", "Network Security"]
    },
    "yt_042": {  # David Bombal
        "skills": ["Computer Networks", "Cybersecurity Fundamentals", "Network Security",
                   "Linux & Command Line", "Ethical Security Concepts",
                   "DevSecOps", "Penetration Testing"]
    },
    "yt_043": {  # Hussein Nasser
        "skills": ["System Design", "Backend Development", "Database Management Systems (DBMS)",
                   "Computer Networks", "REST APIs", "Node.js",
                   "Distributed Systems", "Microservices Architecture"]
    },
    "yt_044": {  # Gaurav Sen
        "skills": ["System Design", "System Design (Advanced)", "Data Structures & Algorithms (DSA)",
                   "Distributed Systems", "Microservices Architecture",
                   "Technical Interview Preparation", "Backend Development"]
    },
    "yt_045": {  # ByteByteGo
        "skills": ["System Design", "System Design (Advanced)", "Backend Development",
                   "Database Management Systems (DBMS)", "Distributed Systems",
                   "REST APIs", "Cloud Computing", "Microservices Architecture"]
    },
    "yt_046": {  # Fireship
        "skills": ["JavaScript (Frontend)", "TypeScript", "React", "Node.js",
                   "Docker & Kubernetes", "Cloud Computing", "Next.js",
                   "Flutter", "Firebase", "Full Stack Development",
                   "Web Security", "DevOps & CI/CD"]
    },
    "yt_047": {  # Corey Schafer
        "skills": ["Python Programming", "Django", "Flask", "Object-Oriented Programming (OOP)",
                   "SQL", "Git & GitHub", "Data Analysis",
                   "Python for Data Science", "Debugging"]
    },
    "yt_048": {  # Andrej Karpathy
        "skills": ["Deep Learning", "Machine Learning", "Neural Networks",
                   "Generative AI", "AI Research Methods",
                   "Python Programming", "Natural Language Processing (NLP)"]
    },
    "yt_049": {  # Yannic Kilcher
        "skills": ["Deep Learning", "Machine Learning", "Reinforcement Learning",
                   "Natural Language Processing (NLP)", "Generative AI",
                   "AI Research Methods", "Explainable AI (XAI)"]
    },
    "yt_050": {  # Abhishek Thakur
        "skills": ["Machine Learning", "Deep Learning", "Python for Data Science",
                   "Kaggle & Competitive ML", "Natural Language Processing (NLP)",
                   "Computer Vision", "Feature Engineering"]
    },
    "yt_051": {  # NPTEL Official
        "skills": ["Computer Networks", "Operating Systems", "Database Management Systems (DBMS)",
                   "Digital Electronics", "Communication Systems", "Thermodynamics",
                   "Fluid Mechanics", "Control Systems Engineering",
                   "GATE / GRE Preparation", "Software Engineering",
                   "Electrical Machines", "Environmental Engineering",
                   "Chemical Engineering", "Structural Engineering",
                   "Materials Science"]
    },
    "yt_052": {  # MIT OCW
        "skills": ["Algorithms", "Computer Architecture", "Software Engineering",
                   "Machine Learning", "Deep Learning", "Statistics for Data Science",
                   "Mathematics", "Linear Algebra", "Data Structures & Algorithms (DSA)",
                   "Computer Networks", "Operating Systems", "Chemistry",
                   "Physics"]
    },
    "yt_053": {  # Lesics
        "skills": ["Mechanical Engineering", "Electrical Machines",
                   "Thermodynamic Simulations", "Robotics & Automation",
                   "Renewable Energy Systems", "IC Engines",
                   "Control Systems Engineering", "Power Electronics"]
    },
    "yt_054": {  # The Efficient Engineer
        "skills": ["Mechanical Engineering", "Structural Engineering",
                   "Thermodynamics", "Materials Science", "Fluid Mechanics",
                   "Finite Element Analysis (Ansys)", "Product Design & Development",
                   "Civil Engineering", "Engineering Design"]
    },
    "yt_055": {  # All About Electronics
        "skills": ["Electronic Circuits", "Communication Systems",
                   "Embedded Systems & Microcontrollers", "Digital Electronics",
                   "PCB Design", "VLSI Design", "Signals & Systems",
                   "Analog Electronics", "IoT & Sensor Networks"]
    },
    "yt_056": {  # Graham Stephan
        "skills": ["Financial Literacy", "Entrepreneurship & Startups",
                   "Entrepreneurship Mindset", "Basic Sales & Persuasion"]
    },
    "yt_057": {  # CA Rachana Ranade
        "skills": ["Financial Literacy", "Entrepreneurship & Startups"]
    },
    "yt_058": {  # Internshala
        "skills": ["Internship Search Strategies", "Resume & CV Writing",
                   "LinkedIn Profile Optimization", "Technical Interview Preparation",
                   "HR Interview & Behavioural Questions", "Career Planning",
                   "Personal Branding Online"]
    },
    "yt_059": {  # Josh Talks
        "skills": ["Entrepreneurship & Startups", "Career Planning",
                   "Entrepreneurship Mindset", "Leadership Basics",
                   "Resilience & Mental Health", "Growth Mindset"]
    },
    "yt_060": {  # Simon Sinek
        "skills": ["Leadership Basics", "Communication — Verbal",
                   "Teamwork & Collaboration", "Emotional Intelligence",
                   "Public Speaking", "Professional Networking",
                   "Entrepreneurship Mindset"]
    },
}

# Load and update channels
channels = json.load(open('data/youtube_channels.json', encoding='utf-8'))
updated = 0
for ch in channels:
    cid = ch['id']
    if cid in CHANNEL_SKILLS:
        ch['skills'] = CHANNEL_SKILLS[cid]['skills']
        updated += 1
with open('data/youtube_channels.json', 'w', encoding='utf-8') as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)
print(f"Step 1 done: {updated}/{len(channels)} channels now have skills field")

# ─────────────────────────────────────────────────────────────────
# STEP 2 & 3: Add YouTube-tagged resources for skills with no YouTube coverage
#             AND learning resources for skills with zero resources
# ─────────────────────────────────────────────────────────────────

existing = json.load(open('data/resources.json', encoding='utf-8'))
existing_ids = {r['id'] for r in existing}
existing_urls = {r['url'] for r in existing}

new_resources = [
  # ── PROGRAMMING ──────────────────────────────────────────────────────────
  {
    "id": "res_253",
    "title": "Python Tutorial for Beginners – Programming with Mosh (YouTube)",
    "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Python Programming", "Object-Oriented Programming"],
    "skills": ["Python Programming", "Object-Oriented Programming (OOP)"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Programming with Mosh 6-hour Python tutorial — variables, OOP, modules, and projects."
  },
  {
    "id": "res_254",
    "title": "Java Full Course – Bro Code (YouTube)",
    "url": "https://www.youtube.com/watch?v=xk4_1vDrzzo",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Java Programming", "Object-Oriented Programming (Java)"],
    "skills": ["Java Programming", "Object-Oriented Programming (OOP)"],
    "branches": ["CSE", "IT"],
    "description": "Comprehensive 12-hour Java course covering OOP, data structures, and Java fundamentals."
  },
  {
    "id": "res_255",
    "title": "JavaScript Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=jS4aFq5-91M",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["JavaScript", "Frontend Development"],
    "skills": ["JavaScript (Frontend)", "HTML & CSS", "Frontend Development"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp 7-hour JavaScript full course covering ES6, DOM, async/await, and projects."
  },
  {
    "id": "res_256",
    "title": "HTML & CSS Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=mU6anWqZJcc",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["HTML & CSS", "Web Development", "Frontend Development"],
    "skills": ["HTML & CSS", "Frontend Development", "JavaScript (Frontend)"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp complete HTML & CSS course — structure, styling, flexbox, grid, and responsive design."
  },
  {
    "id": "res_257",
    "title": "Bash Scripting Tutorial – NetworkChuck (YouTube)",
    "url": "https://www.youtube.com/watch?v=SPwyp2NG-bE",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Linux Administration", "Bash Scripting"],
    "skills": ["Bash / Shell Scripting", "Linux & Command Line"],
    "branches": ["CSE", "IT"],
    "description": "NetworkChuck beginner-friendly bash scripting tutorial — variables, loops, functions, and automation."
  },
  # ── CORE CS ───────────────────────────────────────────────────────────────
  {
    "id": "res_258",
    "title": "Operating Systems – Gate Smashers (YouTube Playlist)",
    "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Operating Systems"],
    "skills": ["Operating Systems"],
    "branches": ["CSE", "IT"],
    "description": "Gate Smashers full OS playlist — processes, threads, memory management, scheduling, and file systems."
  },
  {
    "id": "res_259",
    "title": "DBMS Full Course – Gate Smashers (YouTube Playlist)",
    "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiFAN6I8CuViBuCdJnetworkingDBMS",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Database Management Systems", "SQL"],
    "skills": ["Database Management Systems (DBMS)", "SQL"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Gate Smashers DBMS playlist — ER model, normalization, transactions, SQL, and query optimization."
  },
  {
    "id": "res_260",
    "title": "Computer Networks – Gate Smashers (YouTube Playlist)",
    "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiGCN6C5MJEXPaO5KMmO9oi3",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Computer Networks"],
    "skills": ["Computer Networks", "Network Security"],
    "branches": ["CSE", "IT", "ECE"],
    "description": "Gate Smashers full Computer Networks playlist — OSI model, TCP/IP, routing, subnetting, and security."
  },
  {
    "id": "res_261",
    "title": "Software Engineering – Jenny's Lectures (YouTube Playlist)",
    "url": "https://www.youtube.com/playlist?list=PLdo5W4Nhv31bb8LtNA3dX6NDRH7EZiEEE",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Software Engineering"],
    "skills": ["Software Engineering", "Software Testing", "Agile / Scrum Basics"],
    "branches": ["CSE", "IT"],
    "description": "Jenny's Lectures software engineering playlist — SDLC models, requirements, testing, and project management."
  },
  {
    "id": "res_262",
    "title": "Computer Architecture & Organization – Neso Academy (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRgLLlzdgiTUKULKJPYc0A4q",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Computer Organization & Architecture"],
    "skills": ["Computer Architecture"],
    "branches": ["CSE", "IT", "ECE"],
    "description": "Neso Academy complete computer architecture playlist — number systems, logic, CPU, memory, and pipelining."
  },
  {
    "id": "res_263",
    "title": "Git & GitHub Tutorial – Kevin Stratvert (YouTube)",
    "url": "https://www.youtube.com/watch?v=tRZGeaHPoaw",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Version Control (Git)", "Software Engineering"],
    "skills": ["Git & GitHub", "Open Source Contribution", "Software Engineering"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Comprehensive Git & GitHub tutorial — commits, branches, pull requests, and collaboration workflows."
  },
  # ── DATA SCIENCE / AI ───────────────────────────────────────────────────────
  {
    "id": "res_264",
    "title": "Statistics for Data Science – StatQuest (YouTube)",
    "url": "https://www.youtube.com/c/joshstarmer",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Statistics", "Data Analysis"],
    "skills": ["Statistics for Data Science", "Data Analysis", "Machine Learning"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "StatQuest explains statistics, machine learning, and data analysis visually — loved by beginners worldwide."
  },
  {
    "id": "res_265",
    "title": "Machine Learning Course – Sentdex (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3RVRfAQKRBIUqMvzK",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Machine Learning", "Python for Data Science"],
    "skills": ["Machine Learning", "Python for Data Science", "Data Analysis"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Sentdex practical machine learning with Python — scikit-learn, regression, classification, and clustering."
  },
  {
    "id": "res_266",
    "title": "Deep Learning with PyTorch – Andrej Karpathy (YouTube)",
    "url": "https://www.youtube.com/watch?v=VMj-3S1tku0",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Deep Learning", "Neural Networks"],
    "skills": ["Deep Learning", "Machine Learning", "Python Programming",
               "Deep Learning & Neural Networks", "Deep Learning Architectures"],
    "branches": ["CSE", "AI_DS"],
    "description": "Andrej Karpathy builds a neural network from scratch — micrograd, makemore, GPT — best deep learning intro on YouTube."
  },
  {
    "id": "res_267",
    "title": "NLP with Python – Sentdex (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Natural Language Processing"],
    "skills": ["Natural Language Processing (NLP)", "Machine Learning", "Python Programming"],
    "branches": ["CSE", "AI_DS"],
    "description": "Sentdex NLP playlist with NLTK — tokenization, sentiment analysis, text classification, and word vectors."
  },
  {
    "id": "res_268",
    "title": "Data Visualization with Python – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=GPVsHOlRBBI",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Data Visualization"],
    "skills": ["Data Visualization", "Python for Data Science", "Data Analysis"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "freeCodeCamp data visualization course — Matplotlib, Seaborn, Plotly and effective chart design."
  },
  {
    "id": "res_269",
    "title": "MLOps Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=Ly3Dor8HZUA",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["MLOps", "AI Deployment"],
    "skills": ["MLOps", "MLOps & Model Deployment", "Docker & Kubernetes", "Data Engineering"],
    "branches": ["CSE", "AI_DS"],
    "description": "freeCodeCamp MLOps course — CI/CD for ML, model packaging, deployment, monitoring with MLflow and DVC."
  },
  # ── CLOUD / DEVOPS ────────────────────────────────────────────────────────
  {
    "id": "res_270",
    "title": "AWS for Beginners – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=ulprqHHWlng",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Cloud Computing", "AWS"],
    "skills": ["AWS", "Cloud Computing", "Cloud Computing (AWS/GCP/Azure)", "Cloud Infrastructure"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp AWS cloud practitioner prep — EC2, S3, RDS, VPC, IAM and core AWS services."
  },
  {
    "id": "res_271",
    "title": "Docker Tutorial for Beginners – TechWorld with Nana (YouTube)",
    "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Docker", "DevOps"],
    "skills": ["Docker & Kubernetes", "DevOps & CI/CD", "Cloud Computing"],
    "branches": ["CSE", "IT"],
    "description": "TechWorld with Nana complete Docker tutorial — containers, images, Dockerfile, Docker Compose."
  },
  {
    "id": "res_272",
    "title": "Kubernetes Course – TechWorld with Nana (YouTube)",
    "url": "https://www.youtube.com/watch?v=X48VuDVv0do",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Kubernetes", "DevOps"],
    "skills": ["Docker & Kubernetes", "DevOps & CI/CD", "Cloud Computing"],
    "branches": ["CSE", "IT"],
    "description": "TechWorld with Nana Kubernetes complete course — pods, deployments, services, ingress, Helm."
  },
  {
    "id": "res_273",
    "title": "DevOps Roadmap — TechWorld with Nana (YouTube)",
    "url": "https://www.youtube.com/watch?v=9pZ2xmsSDdo",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["DevOps"],
    "skills": ["DevOps & CI/CD", "Cloud Computing", "Monitoring & Observability",
               "Terraform / Infrastructure as Code", "CI/CD"],
    "branches": ["CSE", "IT"],
    "description": "TechWorld with Nana DevOps roadmap overview — CI/CD, containers, cloud, monitoring, and IaC."
  },
  # ── CYBERSECURITY ─────────────────────────────────────────────────────────
  {
    "id": "res_274",
    "title": "Ethical Hacking Full Course – NetworkChuck (YouTube)",
    "url": "https://www.youtube.com/watch?v=3Kq1MIfTWCE",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Cybersecurity", "Ethical Hacking"],
    "skills": ["Cybersecurity Fundamentals", "Ethical Security Concepts",
               "Penetration Testing", "Network Security", "Security Awareness"],
    "branches": ["CSE", "IT"],
    "description": "NetworkChuck beginner ethical hacking course — Linux, networking, Kali Linux, and vulnerability scanning."
  },
  {
    "id": "res_275",
    "title": "Web Security & OWASP – Computerphile (YouTube Playlist)",
    "url": "https://www.youtube.com/playlist?list=PLzH6n4zXuckpKAj1_88VS-8Z6yn9zX_P6",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Web Security", "Application Security"],
    "skills": ["Web Security", "Application Security", "DevSecOps",
               "Cybersecurity Fundamentals", "Security Awareness"],
    "branches": ["CSE", "IT"],
    "description": "Computerphile web security playlist — SQL injection, XSS, CSRF, session hijacking explained clearly."
  },
  # ── DESIGN / CREATIVE ─────────────────────────────────────────────────────
  {
    "id": "res_276",
    "title": "UI/UX Design Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=c9Wg6Cb_YlU",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["UI/UX Design"],
    "skills": ["UI/UX Design", "Figma", "UX Research"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp UI/UX design course — design principles, Figma, user research, and prototyping."
  },
  {
    "id": "res_277",
    "title": "Canva Tutorial for Beginners – Design School (YouTube)",
    "url": "https://www.youtube.com/watch?v=X_9Zjt0rGAA",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Graphic Design", "Content Creation"],
    "skills": ["Canva", "Graphic Design", "Content Creation", "Digital Marketing"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Canva beginner tutorial — creating social media graphics, presentations, logos, and brand content."
  },
  {
    "id": "res_278",
    "title": "Video Editing for Beginners – DaVinci Resolve (YouTube)",
    "url": "https://www.youtube.com/watch?v=63Ln33O4p4c",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Video Editing"],
    "skills": ["Video Editing", "Content Creation"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Beginner DaVinci Resolve tutorial — importing footage, cutting, transitions, colour, and export."
  },
  # ── CAREER / LIFE SKILLS ──────────────────────────────────────────────────
  {
    "id": "res_279",
    "title": "Public Speaking Tips – TED Masterclass Clips (YouTube)",
    "url": "https://www.youtube.com/watch?v=i0a_oq6EMDI",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Public Speaking", "Communication"],
    "skills": ["Public Speaking", "Presentation Skills", "Communication — Verbal"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "TED's tips on public speaking — structure, openings, body language, and overcoming nerves."
  },
  {
    "id": "res_280",
    "title": "Financial Literacy for Students – CA Rachana Ranade (YouTube)",
    "url": "https://www.youtube.com/watch?v=HsTTVlMhBU4",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Financial Literacy"],
    "skills": ["Financial Literacy"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "CA Rachana Ranade explains SIP, mutual funds, tax, insurance and budgeting for Indian students."
  },
  {
    "id": "res_281",
    "title": "Emotional Intelligence – Charisma on Command (YouTube)",
    "url": "https://www.youtube.com/watch?v=D6_xHzZc_fs",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Emotional Intelligence"],
    "skills": ["Emotional Intelligence", "Active Listening", "Teamwork & Collaboration"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Charisma on Command videos on emotional intelligence — empathy, self-awareness, and social dynamics."
  },
  {
    "id": "res_282",
    "title": "Time Management & Productivity – Ali Abdaal (YouTube)",
    "url": "https://www.youtube.com/watch?v=iDbdXTMnOmE",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Time Management", "Productivity"],
    "skills": ["Time Management", "Productivity Tools (Notion, Trello)",
               "Discipline & Consistency", "Habit Building"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Ali Abdaal's time management system — deep work, task batching, Notion, and avoiding procrastination."
  },
  {
    "id": "res_283",
    "title": "Resume & LinkedIn Tips – Internshala (YouTube)",
    "url": "https://www.youtube.com/watch?v=y8YH0Qbu5h4",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Resume & CV Writing", "LinkedIn Profile Optimization"],
    "skills": ["Resume & CV Writing", "LinkedIn Profile Optimization",
               "Personal Branding Online", "Internship Search Strategies"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Internshala guide to writing ATS-friendly resumes and optimizing LinkedIn profiles for Indian students."
  },
  {
    "id": "res_284",
    "title": "Critical Thinking & Problem Solving – TED-Ed (YouTube)",
    "url": "https://www.youtube.com/watch?v=dItUGF8GdTw",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Critical Thinking"],
    "skills": ["Critical Thinking", "Decision Making", "Problem Solving", "Creativity"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "TED-Ed collection on critical thinking, logical fallacies, and structured problem-solving approaches."
  },
  {
    "id": "res_285",
    "title": "Entrepreneurship & Startups – YC Startup School (YouTube)",
    "url": "https://www.youtube.com/c/ycombinator",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Entrepreneurship & Startups"],
    "skills": ["Entrepreneurship & Startups", "Entrepreneurship Mindset",
               "Basic Sales & Persuasion", "Decision Making"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Y Combinator's startup school YouTube channel — fundraising, product, growth, and founder advice."
  },
  # ── BRANCH-SPECIFIC SKILLS WITHOUT RESOURCES ─────────────────────────────
  {
    "id": "res_286",
    "title": "MATLAB for Engineers – MathWorks Official (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLn8PRpmsu08oBSjfGe8WIMN-2_rwWFSgr",
    "type": "Video",
    "tags": ["Free", "YouTube", "Official", "Beginner", "Global"],
    "subjects": ["MATLAB", "Simulation Lab (MATLAB)"],
    "skills": ["MATLAB/Simulink", "MATLAB for Mechanical", "MATLAB/Simulink for EEE",
               "Control Systems Engineering"],
    "branches": ["ECE", "EEE", "ME", "EI"],
    "description": "Official MathWorks MATLAB tutorials — scripting, matrices, plotting, Simulink, and engineering applications."
  },
  {
    "id": "res_287",
    "title": "Arduino Tutorial – Paul McWhorter (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLGs0VKk2DiYw-L-RibttcvK-WBZm8WLEP",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Embedded Systems", "Arduino & Raspberry Pi"],
    "skills": ["Arduino & Raspberry Pi", "Embedded Systems & Microcontrollers", "IoT & Sensor Networks"],
    "branches": ["ECE", "EI", "EEE"],
    "description": "Comprehensive 200+ video Arduino series from basics to sensors, motors, displays, and IoT projects."
  },
  {
    "id": "res_288",
    "title": "VLSI Design – NPTEL (IIT Bombay YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLbRMhDVUMngeMrJ-OruMqPLuBe3S8z4hN",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India", "Government"],
    "subjects": ["VLSI Design"],
    "skills": ["VLSI Design", "Verilog / VHDL (HDL)", "Digital Electronics", "FPGA Design"],
    "branches": ["ECE"],
    "description": "IIT Bombay NPTEL VLSI design lectures — CMOS, logic synthesis, Verilog, and chip design flow."
  },
  {
    "id": "res_289",
    "title": "Control Systems – Brian Douglas (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLUMWjy5jgHK1NC52DXXrriwihVrYZKqjk",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Control Systems", "Process Control"],
    "skills": ["Control Systems Engineering", "Process Control Design",
               "MATLAB/Simulink for EEE", "PLC & SCADA Programming"],
    "branches": ["EEE", "ECE", "EI", "CHEM"],
    "description": "Brian Douglas engineering control systems series — Bode plots, PID, root locus, and state space."
  },
  {
    "id": "res_290",
    "title": "Structural Analysis – The Efficient Engineer (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLCnfkbz9LCXJxRDSJdpUNSmq7kMFuAhXe",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Structural Analysis", "Structural Engineering"],
    "skills": ["STAAD Pro / ETABS Structural Analysis", "Structural Engineering",
               "Civil Engineering", "Site Safety & Quality Management"],
    "branches": ["CE"],
    "description": "The Efficient Engineer structural analysis series — beams, trusses, frames, and deflection methods."
  },
  {
    "id": "res_291",
    "title": "Thermodynamics – The Efficient Engineer (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLCnfkbz9LCXJyiN4sBOdL-qCn0MkpW8iP",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Thermodynamics", "Thermodynamic Simulations"],
    "skills": ["Thermodynamic Simulations", "Mechanical Engineering",
               "Chemical Engineering", "Fluid Mechanics"],
    "branches": ["ME", "CHEM"],
    "description": "The Efficient Engineer thermodynamics series — laws, cycles, entropy, heat engines, and refrigeration."
  },
  {
    "id": "res_292",
    "title": "Robotics – MIT OpenCourseWare (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLkx8KyIQkMfXyKku6DstXjB8-j5UF5xoN",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Robotics", "Automation"],
    "skills": ["Robotics & Automation", "Mechanical Engineering", "Embedded Systems & Microcontrollers"],
    "branches": ["ME", "ECE", "EI"],
    "description": "MIT OCW robotics lectures — kinematics, dynamics, motion planning, and robot programming."
  },
  # ── MISSING LEARNING RESOURCES (non-YouTube) for zero-resource skills ────
  {
    "id": "res_293",
    "title": "Aspen Plus for Chemical Engineering – Coursera (UC Boulder)",
    "url": "https://www.coursera.org/learn/aspenplus",
    "type": "Course",
    "tags": ["Free", "Certificate", "Intermediate", "Global"],
    "subjects": ["Aspen Plus Simulation", "Chemical Process Simulation"],
    "skills": ["Aspen Plus Process Simulation", "Process Design & Optimization"],
    "branches": ["CHEM"],
    "description": "Coursera course on process simulation with Aspen Plus — steady-state simulation of distillation, reactors and heat exchangers."
  },
  {
    "id": "res_294",
    "title": "AutoCAD for Civil Engineering – Autodesk Official (Free Trial + Docs)",
    "url": "https://www.autodesk.com/certification/learn/catalog/category/12",
    "type": "Course",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["AutoCAD", "Civil Drafting"],
    "skills": ["AutoCAD for Civil Engineering", "Revit & BIM", "GIS & Remote Sensing"],
    "branches": ["CE"],
    "description": "Autodesk official AutoCAD and Revit learning paths — 2D drafting, 3D modelling, BIM workflows for civil engineers."
  },
  {
    "id": "res_295",
    "title": "Bioinformatics Algorithms – UCSD (Coursera)",
    "url": "https://www.coursera.org/specializations/bioinformatics",
    "type": "Course",
    "tags": ["Free", "Certificate", "Intermediate", "Global"],
    "subjects": ["Bioinformatics"],
    "skills": ["Bioinformatics Tools (BLAST, NCBI)", "Python for Bioinformatics",
               "Genomics & Proteomics", "Computational Drug Discovery"],
    "branches": ["BT", "AI_DS"],
    "description": "UCSD Bioinformatics Specialization on Coursera — DNA sequencing, genome assembly, alignment algorithms and BLAST."
  },
  {
    "id": "res_296",
    "title": "R Programming for Statistics – DataCamp Free Intro",
    "url": "https://www.datacamp.com/courses/free-introduction-to-r",
    "type": "Course",
    "tags": ["Free", "Beginner", "Global"],
    "subjects": ["Statistics", "Bioinformatics"],
    "skills": ["Biostatistics & R", "Statistics for Data Science", "Data Analysis"],
    "branches": ["BT", "AI_DS", "CSE"],
    "description": "Free DataCamp R intro — vectors, matrices, data frames, and statistical analysis basics."
  },
  {
    "id": "res_297",
    "title": "CAD/CAM with SolidWorks – SolidWorks Official eLearning",
    "url": "https://www.solidworks.com/sw/education/student-software-3d-mcad.htm",
    "type": "Course",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["CAD/CAM", "Product Design"],
    "skills": ["CAD with AutoCAD / SolidWorks", "CAM & CNC Programming",
               "Product Design & Development", "3D Printing & Additive Manufacturing"],
    "branches": ["ME"],
    "description": "SolidWorks student free access and official eLearning — part modelling, assemblies, drawings, and simulation."
  },
  {
    "id": "res_298",
    "title": "FEA with Ansys – Ansys Official Free Courses",
    "url": "https://courses.ansys.com/",
    "type": "Course",
    "tags": ["Free", "Official", "Intermediate", "Global"],
    "subjects": ["Finite Element Analysis"],
    "skills": ["Finite Element Analysis (Ansys)", "Thermodynamic Simulations",
               "Product Design & Development"],
    "branches": ["ME", "CE"],
    "description": "Ansys official free online courses for FEA, CFD, and structural simulation — beginner to advanced."
  },
  {
    "id": "res_299",
    "title": "Digital Marketing & SEO – Google Skillshop",
    "url": "https://skillshop.docebosaas.com/learn",
    "type": "Course",
    "tags": ["Free", "Official", "Certificate", "Beginner", "Global"],
    "subjects": ["Digital Marketing", "SEO"],
    "skills": ["SEO", "Digital Marketing", "Content Creation"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Google Skillshop free certifications — Google Ads, Analytics, SEO, and digital marketing fundamentals."
  },
  {
    "id": "res_300",
    "title": "GIS & Remote Sensing – ESRI ArcGIS Free Training",
    "url": "https://www.esri.com/training/catalog/search/",
    "type": "Course",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["GIS & Remote Sensing", "Geotechnical Analysis"],
    "skills": ["GIS & Remote Sensing", "Geotechnical Analysis Software",
               "Civil Engineering"],
    "branches": ["CE"],
    "description": "ESRI free ArcGIS training — spatial analysis, mapping, remote sensing, and GIS fundamentals for civil engineers."
  },
  {
    "id": "res_301",
    "title": "PLC Programming (Siemens TIA Portal) – RealPars (Free Lessons)",
    "url": "https://realpars.com/plc-programming-examples/",
    "type": "Course",
    "tags": ["Free", "Beginner", "Global"],
    "subjects": ["PLC Programming", "Industrial Automation"],
    "skills": ["PLC & SCADA Programming", "SCADA & PLC Programming",
               "Industrial Automation", "Control Systems Engineering"],
    "branches": ["EEE", "EI"],
    "description": "RealPars free PLC programming lessons — ladder logic, structured text, Siemens TIA Portal and industrial automation."
  },
  {
    "id": "res_302",
    "title": "LabVIEW Core 1 – NI Official (Free Intro)",
    "url": "https://www.ni.com/en/shop/services/education/self-paced-online-courses-for-labview.html",
    "type": "Course",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["LabVIEW", "Virtual Instrumentation"],
    "skills": ["LabVIEW & Virtual Instrumentation", "Industrial Automation", "Sensor Calibration & Metrology"],
    "branches": ["EI"],
    "description": "National Instruments official LabVIEW intro — data flow programming, DAQ, signal processing and virtual instruments."
  },
  {
    "id": "res_303",
    "title": "Communication Skills – Coursera (Georgia Tech)",
    "url": "https://www.coursera.org/learn/technical-communication",
    "type": "Course",
    "tags": ["Free", "Certificate", "Beginner", "Global"],
    "subjects": ["Communication Skills", "Professional Communication"],
    "skills": ["Communication — Verbal", "Communication — Written",
               "Professional Email Writing", "Non-verbal Communication"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Georgia Tech technical communication course — writing, presentations, oral communication and professional style."
  },
  {
    "id": "res_304",
    "title": "Digital Literacy – Google Digital Garage (Core)",
    "url": "https://learndigital.withgoogle.com/digitalgarage/course/digital-skills-for-the-future",
    "type": "Course",
    "tags": ["Free", "Certificate", "Beginner", "Global"],
    "subjects": ["Digital Literacy"],
    "skills": ["Digital Literacy", "AI Literacy for Professionals",
               "Professional Networking"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Google's free digital skills course — internet safety, online tools, digital communication and career skills."
  },
  {
    "id": "res_305",
    "title": "Professional Networking – LinkedIn Official Guide",
    "url": "https://www.linkedin.com/learning/paths/improve-your-networking",
    "type": "Course",
    "tags": ["Paid", "Certificate", "Beginner", "Global"],
    "subjects": ["Professional Networking"],
    "skills": ["Professional Networking", "Personal Branding Online",
               "LinkedIn Profile Optimization"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "LinkedIn Learning networking path — building relationships, informational interviews, and online presence."
  },
  {
    "id": "res_306",
    "title": "Express.js Official Guide",
    "url": "https://expressjs.com/en/guide/routing.html",
    "type": "Notes",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["Express.js", "Node.js", "Backend Development"],
    "skills": ["Express.js", "Node.js", "Backend Development", "REST APIs"],
    "branches": ["CSE", "IT"],
    "description": "Official Express.js guide — routing, middleware, error handling, database integration and API design."
  },
  {
    "id": "res_307",
    "title": "Flask Official Documentation Tutorial",
    "url": "https://flask.palletsprojects.com/en/stable/tutorial/",
    "type": "Notes",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["Flask", "Backend Development"],
    "skills": ["Flask", "Python Programming", "Backend Development", "REST APIs"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Official Flask tutorial — building a blog app with routing, templates, databases, and testing."
  },
  {
    "id": "res_308",
    "title": "Google Cloud Fundamentals – Google Cloud Skills Boost (Free)",
    "url": "https://www.cloudskillsboost.google/paths/11",
    "type": "Course",
    "tags": ["Free", "Official", "Certificate", "Beginner", "Global"],
    "subjects": ["Cloud Computing", "Google Cloud Platform"],
    "skills": ["Google Cloud Platform", "Cloud Computing", "Cloud Infrastructure"],
    "branches": ["CSE", "IT"],
    "description": "Google Cloud's free learning path — GCP fundamentals, compute, storage, networking and ML services."
  },
  {
    "id": "res_309",
    "title": "Prompt Engineering Guide – DAIR.AI (Free Online)",
    "url": "https://www.promptingguide.ai/",
    "type": "Notes",
    "tags": ["Free", "Beginner", "Global"],
    "subjects": ["Generative AI", "Prompt Engineering"],
    "skills": ["Prompt Engineering", "Generative AI", "AI Agents"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Comprehensive free prompt engineering guide — techniques, zero-shot, few-shot, chain-of-thought, and advanced prompting."
  },
  {
    "id": "res_310",
    "title": "Statistics – Khan Academy (Complete)",
    "url": "https://www.khanacademy.org/math/statistics-probability",
    "type": "Course",
    "tags": ["Free", "Beginner", "Global"],
    "subjects": ["Statistics", "Probability"],
    "skills": ["Statistics for Data Science", "Mathematics"],
    "branches": ["CSE", "IT", "AI_DS", "ECE", "EEE", "ME", "CE", "CHEM", "BT", "EI"],
    "description": "Khan Academy complete statistics and probability course — distributions, hypothesis testing, regression and inference."
  },
]

# Filter out any entries with duplicate URLs
all_resources = existing.copy()
added = 0
skipped_url = 0
skipped_id = 0

existing_urls_set = {r['url'] for r in existing}
existing_ids_set = {r['id'] for r in existing}

for nr in new_resources:
    if nr['id'] in existing_ids_set:
        skipped_id += 1
        print(f"  SKIP (dup ID): {nr['id']}")
        continue
    if nr['url'] in existing_urls_set:
        skipped_url += 1
        print(f"  SKIP (dup URL): {nr['id']} {nr['url'][:60]}")
        continue
    all_resources.append(nr)
    existing_urls_set.add(nr['url'])
    existing_ids_set.add(nr['id'])
    added += 1

with open('data/resources.json', 'w', encoding='utf-8') as f:
    json.dump(all_resources, f, indent=2, ensure_ascii=False)

print(f"\nStep 2/3 done: {added} resources added ({skipped_url} URL dupes skipped, {skipped_id} ID dupes skipped)")
print(f"Total resources: {len(all_resources)}")
