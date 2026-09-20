"""
Phase 2.5 Part 2: Skills enrichment
- Add more skill aliases to new YouTube resources so substring matching catches them
- Add resources for remaining 37 zero-resource skills
"""
import json

resources = json.load(open('data/resources.json', encoding='utf-8'))

# ─── Enrich existing resources with additional skill name aliases ──────────────
skill_enrichments = {
    # res_253: Python
    "res_253": {"skills": ["Python Programming", "Object-Oriented Programming (OOP)",
                            "Python for Data Science", "Python for Bioinformatics"]},
    # res_255: JS
    "res_255": {"skills": ["JavaScript (Frontend)", "HTML & CSS", "Frontend Development",
                            "Full Stack Development"]},
    # res_262: Architecture -> also covers Compiler Design (same low-level CS)
    "res_262": {"skills": ["Computer Architecture", "Compiler Design",
                            "Theory of Computation"]},
    # res_263: Git -> Open Source, Technical Blogging
    "res_263": {"skills": ["Git & GitHub", "Open Source Contribution",
                            "Open Source Development", "Technical Blogging & Portfolio Building",
                            "Software Engineering"]},
    # res_264: Statistics -> covers many data skills
    "res_264": {"skills": ["Statistics for Data Science", "Data Analysis",
                            "Machine Learning", "Probability"]},
    # res_265: ML -> covers Advanced ML, Data Science, Feature Engineering
    "res_265": {"skills": ["Machine Learning", "Python for Data Science",
                            "Data Analysis", "Advanced Machine Learning",
                            "Data Science & Analytics", "Machine Learning Basics",
                            "Kaggle & Competitive ML", "Feature Engineering"]},
    # res_266: Deep Learning -> covers many AI skills
    "res_266": {"skills": ["Deep Learning", "Machine Learning",
                            "Deep Learning & Neural Networks", "Deep Learning Architectures",
                            "Neural Networks", "Computer Vision",
                            "Reinforcement Learning", "Generative AI",
                            "Generative AI & LLMs", "AI Research Methods",
                            "Advanced Machine Learning", "Explainable AI (XAI)",
                            "Explainable AI", "Natural Language Processing (NLP)",
                            "Time Series Analysis", "Time Series Forecasting"]},
    # res_267: NLP
    "res_267": {"skills": ["Natural Language Processing (NLP)", "Machine Learning",
                            "Natural Language Processing"]},
    # res_268: Data Viz -> also covers tableau/power bi context
    "res_268": {"skills": ["Data Visualization", "Python for Data Science",
                            "Data Analysis", "Data Engineering",
                            "Data Engineering & Pipelines"]},
    # res_269: MLOps -> covers related
    "res_269": {"skills": ["MLOps", "MLOps & Model Deployment",
                            "Docker & Kubernetes", "Data Engineering",
                            "Data Engineering & Pipelines"]},
    # res_270: AWS -> covers Cloud related
    "res_270": {"skills": ["AWS", "Cloud Computing", "Cloud Computing (AWS/GCP/Azure)",
                            "Cloud Infrastructure", "Microsoft Azure",
                            "Google Cloud Platform"]},
    # res_272: Docker/K8s
    "res_272": {"skills": ["Docker & Kubernetes", "DevOps & CI/CD",
                            "Cloud Computing", "Microservices Architecture",
                            "Distributed Systems"]},
    # res_273: DevOps
    "res_273": {"skills": ["DevOps & CI/CD", "Cloud Computing",
                            "Monitoring & Observability", "Terraform / Infrastructure as Code",
                            "CI/CD", "Virtualization", "Information Security Management"]},
    # res_274: Ethical hacking
    "res_274": {"skills": ["Cybersecurity Fundamentals", "Ethical Security Concepts",
                            "Penetration Testing", "Network Security",
                            "Security Awareness", "Cybersecurity"]},
    # res_275: Web Security
    "res_275": {"skills": ["Web Security", "Application Security",
                            "DevSecOps", "Cybersecurity Fundamentals",
                            "Security Awareness", "Information Security Management"]},
    # res_276: UI/UX
    "res_276": {"skills": ["UI/UX Design", "Figma", "UX Research",
                            "Graphic Design"]},
    # res_277: Canva / Design
    "res_277": {"skills": ["Canva", "Graphic Design", "Content Creation",
                            "Digital Marketing", "SEO"]},
    # res_279: Public Speaking
    "res_279": {"skills": ["Public Speaking", "Presentation Skills",
                            "Communication — Verbal", "Non-verbal Communication",
                            "Group Discussion Skills"]},
    # res_281: EQ
    "res_281": {"skills": ["Emotional Intelligence", "Active Listening",
                            "Teamwork & Collaboration", "Conflict Resolution",
                            "Leadership Basics"]},
    # res_282: Productivity
    "res_282": {"skills": ["Time Management", "Productivity Tools (Notion, Trello)",
                            "Discipline & Consistency", "Habit Building",
                            "Resilience & Mental Health", "Stress Management",
                            "Growth Mindset", "Learning How to Learn"]},
    # res_283: Resume
    "res_283": {"skills": ["Resume & CV Writing", "LinkedIn Profile Optimization",
                            "Personal Branding Online", "Internship Search Strategies",
                            "Career Planning", "Technical Blogging & Portfolio Building",
                            "Professional Networking"]},
    # res_284: Critical Thinking
    "res_284": {"skills": ["Critical Thinking", "Decision Making",
                            "Problem Solving", "Creativity"]},
    # res_285: Entrepreneurship
    "res_285": {"skills": ["Entrepreneurship & Startups", "Entrepreneurship Mindset",
                            "Basic Sales & Persuasion", "Decision Making",
                            "Negotiation", "Freelancing Basics",
                            "Higher Studies Planning (MS/MBA)"]},
    # res_286: MATLAB
    "res_286": {"skills": ["MATLAB/Simulink", "MATLAB for Mechanical",
                            "MATLAB/Simulink for EEE", "Control Systems Engineering"]},
    # res_287: Arduino
    "res_287": {"skills": ["Arduino & Raspberry Pi",
                            "Embedded Systems & Microcontrollers",
                            "IoT & Sensor Networks", "Industrial IoT",
                            "Industrial Automation", "Sensor Calibration & Metrology"]},
    # res_288: VLSI
    "res_288": {"skills": ["VLSI Design", "Verilog / VHDL (HDL)",
                            "Digital Electronics", "FPGA Design",
                            "Digital Signal Processing"]},
    # res_289: Control Systems
    "res_289": {"skills": ["Control Systems Engineering", "Process Control Design",
                            "MATLAB/Simulink for EEE", "PLC & SCADA Programming",
                            "SCADA & PLC Programming"]},
    # res_290: Structural
    "res_290": {"skills": ["STAAD Pro / ETABS Structural Analysis",
                            "Structural Engineering", "Civil Engineering",
                            "Site Safety & Quality Management",
                            "Geotechnical Analysis Software",
                            "Construction Management Software",
                            "GIS & Remote Sensing", "Revit & BIM",
                            "AutoCAD for Civil Engineering"]},
    # res_291: Thermodynamics
    "res_291": {"skills": ["Thermodynamic Simulations", "Mechanical Engineering",
                            "Chemical Engineering", "Fluid Mechanics",
                            "Mass Transfer Operations", "Process Design & Optimization",
                            "Chemical Reaction Engineering", "Process Safety & HAZOP",
                            "Environmental Compliance"]},
    # res_292: Robotics
    "res_292": {"skills": ["Robotics & Automation", "Mechanical Engineering",
                            "Embedded Systems & Microcontrollers",
                            "Operations Research for Engineering",
                            "Product Design & Development",
                            "3D Printing & Additive Manufacturing",
                            "CAD with AutoCAD / SolidWorks",
                            "CAM & CNC Programming",
                            "Finite Element Analysis (Ansys)"]},
    # res_293: Aspen Plus
    "res_293": {"skills": ["Aspen Plus Process Simulation",
                            "Process Design & Optimization"]},
    # res_294: AutoCAD Civil
    "res_294": {"skills": ["AutoCAD for Civil Engineering",
                            "Revit & BIM", "GIS & Remote Sensing",
                            "Construction Management Software"]},
    # res_295: Bioinformatics
    "res_295": {"skills": ["Bioinformatics Tools (BLAST, NCBI)",
                            "Python for Bioinformatics",
                            "Genomics & Proteomics",
                            "Computational Drug Discovery",
                            "Molecular Biology Techniques",
                            "Genetic Engineering Techniques",
                            "Downstream Processing",
                            "Laboratory Information Systems"]},
    # res_296: R / Biostatistics
    "res_296": {"skills": ["Biostatistics & R",
                            "Statistics for Data Science", "Data Analysis"]},
    # res_297: SolidWorks
    "res_297": {"skills": ["CAD with AutoCAD / SolidWorks",
                            "CAM & CNC Programming",
                            "Product Design & Development",
                            "3D Printing & Additive Manufacturing",
                            "Non-Destructive Testing (NDT)"]},
    # res_298: FEA Ansys
    "res_298": {"skills": ["Finite Element Analysis (Ansys)",
                            "Thermodynamic Simulations",
                            "Product Design & Development"]},
    # res_299: SEO/Digital Marketing
    "res_299": {"skills": ["SEO", "Digital Marketing", "Content Creation"]},
    # res_300: GIS
    "res_300": {"skills": ["GIS & Remote Sensing",
                            "Geotechnical Analysis Software",
                            "Civil Engineering",
                            "Construction Management Software",
                            "Revit & BIM"]},
    # res_301: PLC
    "res_301": {"skills": ["PLC & SCADA Programming",
                            "SCADA & PLC Programming",
                            "Industrial Automation",
                            "Control Systems Engineering",
                            "Industrial IoT"]},
    # res_302: LabVIEW
    "res_302": {"skills": ["LabVIEW & Virtual Instrumentation",
                            "Industrial Automation",
                            "Sensor Calibration & Metrology",
                            "Industrial IoT"]},
    # res_303: Communication
    "res_303": {"skills": ["Communication — Verbal",
                            "Communication — Written",
                            "Professional Email Writing",
                            "Non-verbal Communication",
                            "Group Discussion Skills",
                            "HR Interview & Behavioural Questions",
                            "Presentation Skills"]},
    # res_304: Digital Literacy
    "res_304": {"skills": ["Digital Literacy",
                            "AI Literacy for Professionals",
                            "Professional Networking"]},
    # res_305: Professional Networking
    "res_305": {"skills": ["Professional Networking",
                            "Personal Branding Online",
                            "LinkedIn Profile Optimization"]},
    # res_306: Express.js
    "res_306": {"skills": ["Express.js", "Node.js",
                            "Backend Development", "REST APIs",
                            "Full Stack Development", "Web Application Development",
                            "API Development & Integration"]},
    # res_307: Flask
    "res_307": {"skills": ["Flask", "Python Programming",
                            "Backend Development", "REST APIs",
                            "Full Stack Development"]},
    # res_308: GCP
    "res_308": {"skills": ["Google Cloud Platform", "Cloud Computing",
                            "Cloud Infrastructure", "Microsoft Azure",
                            "Cloud Computing (AWS/GCP/Azure)"]},
    # res_309: Prompt Engineering
    "res_309": {"skills": ["Prompt Engineering", "Generative AI",
                            "AI Agents", "Generative AI & LLMs",
                            "Responsible AI", "Responsible AI & AI Ethics",
                            "AI Literacy for Professionals", "AI Research Methods"]},
    # res_310: Statistics
    "res_310": {"skills": ["Statistics for Data Science", "Mathematics",
                            "Probability"]},
}

# Also enrich some earlier resources that have generic skill names
early_enrichments = {
    # res_012: Kaggle (ML)
    "res_012": {"skills_to_add": ["Machine Learning Basics", "Kaggle & Competitive ML",
                                   "Data Science & Analytics", "Feature Engineering",
                                   "Advanced Machine Learning"]},
    # res_001: Mathematics (NPTEL)
    "res_001": {"skills_to_add": ["Statistics for Data Science", "Mathematics"]},
    # res_019: Python (freeCodeCamp)
    "res_019": {"skills_to_add": ["Python Programming", "Data Science & Analytics",
                                   "Python for Bioinformatics"]},
    # res_161: Kotlin
    "res_161": {"skills_to_add": ["Kotlin", "Android Development",
                                   "Mobile App Development", "Mobile Development"]},
    # res_168: Flutter
    "res_168": {"skills_to_add": ["Flutter", "Mobile Development",
                                   "Mobile App Development", "Dart"]},
    # res_162: React
    "res_162": {"skills_to_add": ["React", "JavaScript (Frontend)",
                                   "Frontend Development"]},
    # res_163: Next.js
    "res_163": {"skills_to_add": ["Next.js", "React", "Full Stack Development"]},
    # res_164: Node.js
    "res_164": {"skills_to_add": ["Node.js", "Backend Development",
                                   "Full Stack Development", "API Development & Integration"]},
    # res_165: Django
    "res_165": {"skills_to_add": ["Django", "Python Programming",
                                   "Backend Development", "Full Stack Development"]},
    # res_166: FastAPI
    "res_166": {"skills_to_add": ["FastAPI", "REST APIs",
                                   "Backend Development", "API Development & Integration"]},
    # res_167: GraphQL
    "res_167": {"skills_to_add": ["GraphQL", "REST APIs",
                                   "API Development & Integration"]},
    # res_170: Terraform
    "res_170": {"skills_to_add": ["Terraform / Infrastructure as Code",
                                   "DevOps & CI/CD", "Cloud Computing"]},
    # res_171: Prometheus/Grafana
    "res_171": {"skills_to_add": ["Monitoring & Observability", "DevOps & CI/CD"]},
    # res_172: RL
    "res_172": {"skills_to_add": ["Reinforcement Learning"]},
    # res_173: XAI
    "res_173": {"skills_to_add": ["Explainable AI (XAI)", "Explainable AI",
                                   "Responsible AI", "Responsible AI & AI Ethics"]},
    # res_174: Time Series
    "res_174": {"skills_to_add": ["Time Series Analysis", "Time Series Forecasting"]},
    # res_175: Pen Testing (TryHackMe)
    "res_175": {"skills_to_add": ["Penetration Testing", "Cybersecurity Fundamentals",
                                   "Ethical Security Concepts"]},
    # res_176: OWASP
    "res_176": {"skills_to_add": ["Web Security", "Application Security",
                                   "DevSecOps", "Security Awareness"]},
    # res_177: Figma
    "res_177": {"skills_to_add": ["Figma", "UI/UX Design"]},
    # res_178: Google UX
    "res_178": {"skills_to_add": ["UI/UX Design", "Figma", "Graphic Design"]},
    # res_179: Canva
    "res_179": {"skills_to_add": ["Canva", "Graphic Design", "Content Creation"]},
    # res_180: DaVinci
    "res_180": {"skills_to_add": ["Video Editing", "Content Creation"]},
    # res_181: Digital Marketing
    "res_181": {"skills_to_add": ["Digital Marketing", "SEO", "Content Creation"]},
    # res_182: Resume
    "res_182": {"skills_to_add": ["Resume & CV Writing"]},
    # res_183: LinkedIn
    "res_183": {"skills_to_add": ["LinkedIn Profile Optimization",
                                   "Personal Branding Online"]},
    # res_184: Technical Interview
    "res_184": {"skills_to_add": ["Technical Interview Preparation"]},
    # res_185: GATE
    "res_185": {"skills_to_add": ["GATE / GRE Preparation"]},
    # res_186: GRE
    "res_186": {"skills_to_add": ["GATE / GRE Preparation",
                                   "Higher Studies Planning (MS/MBA)"]},
    # res_187: Freelancing
    "res_187": {"skills_to_add": ["Freelancing Basics"]},
    # res_188: YC Startup
    "res_188": {"skills_to_add": ["Entrepreneurship & Startups",
                                   "Entrepreneurship Mindset"]},
    # res_189: Presentation
    "res_189": {"skills_to_add": ["Presentation Skills", "Public Speaking"]},
    # res_190: AI Literacy
    "res_190": {"skills_to_add": ["AI Literacy for Professionals", "Digital Literacy"]},
    # res_191: Professional Email
    "res_191": {"skills_to_add": ["Professional Email Writing",
                                   "Communication — Written"]},
    # res_192: Active Listening
    "res_192": {"skills_to_add": ["Active Listening", "Communication — Verbal"]},
    # res_193: EQ
    "res_193": {"skills_to_add": ["Emotional Intelligence", "Leadership Basics",
                                   "Teamwork & Collaboration"]},
    # res_194: Leadership
    "res_194": {"skills_to_add": ["Leadership Basics", "Teamwork & Collaboration",
                                   "Conflict Resolution"]},
    # res_195: Critical Thinking
    "res_195": {"skills_to_add": ["Critical Thinking", "Decision Making",
                                   "Problem Solving"]},
    # res_196: Time Management
    "res_196": {"skills_to_add": ["Time Management",
                                   "Productivity Tools (Notion, Trello)"]},
    # res_197: Financial Literacy
    "res_197": {"skills_to_add": ["Financial Literacy"]},
    # res_198: Learning to Learn
    "res_198": {"skills_to_add": ["Learning How to Learn", "Habit Building",
                                   "Growth Mindset"]},
    # res_199: Negotiation
    "res_199": {"skills_to_add": ["Negotiation"]},
    # res_200: Software Testing
    "res_200": {"skills_to_add": ["Software Testing", "Debugging"]},
    # res_201: REST API
    "res_201": {"skills_to_add": ["REST APIs", "Backend Development",
                                   "API Development & Integration"]},
    # res_202: Python for DS (IBM)
    "res_202": {"skills_to_add": ["Python for Data Science", "Data Analysis",
                                   "Data Science & Analytics"]},
    # res_203: Debugging (MIT)
    "res_203": {"skills_to_add": ["Debugging", "Software Testing",
                                   "Linux & Command Line"]},
    # res_204: OOP
    "res_204": {"skills_to_add": ["Object-Oriented Programming (OOP)",
                                   "Java Programming"]},
    # res_205: Personal Branding
    "res_205": {"skills_to_add": ["Personal Branding Online"]},
    # res_206: HR Interview
    "res_206": {"skills_to_add": ["HR Interview & Behavioural Questions",
                                   "Technical Interview Preparation",
                                   "Group Discussion Skills"]},
    # res_207: Group Discussion
    "res_207": {"skills_to_add": ["Group Discussion Skills",
                                   "Communication — Verbal"]},
    # res_208: Agile
    "res_208": {"skills_to_add": ["Agile / Scrum Basics", "Agile & Scrum",
                                   "Software Engineering"]},
    # res_209: Open Source
    "res_209": {"skills_to_add": ["Open Source Contribution",
                                   "Open Source Development",
                                   "Technical Blogging & Portfolio Building",
                                   "Git & GitHub"]},
    # res_210: Competitive Programming
    "res_210": {"skills_to_add": ["Competitive Programming Strategy"]},
    # res_230: Linux Foundation
    "res_230": {"skills_to_add": ["Linux & Command Line",
                                   "Bash / Shell Scripting",
                                   "Operating Systems",
                                   "Network Administration",
                                   "Database Administration"]},
    # res_231: AI Research Methods
    "res_231": {"skills_to_add": ["AI Research Methods", "Machine Learning",
                                   "Advanced Machine Learning"]},
    # res_232: Python ML Google Codelabs
    "res_232": {"skills_to_add": ["Machine Learning", "Python for Data Science",
                                   "Computer Vision"]},
    # res_233: PyTorch
    "res_233": {"skills_to_add": ["Deep Learning",
                                   "Deep Learning & Neural Networks",
                                   "Deep Learning Architectures",
                                   "Machine Learning"]},
    # res_234: DeepLearning.AI LLMs
    "res_234": {"skills_to_add": ["Generative AI", "AI Agents",
                                   "Prompt Engineering", "Generative AI & LLMs",
                                   "Responsible AI", "Responsible AI & AI Ethics",
                                   "AI Research Methods", "AI Literacy for Professionals"]},
    # res_238: MLflow
    "res_238": {"skills_to_add": ["MLOps", "MLOps & Model Deployment"]},
    # res_239: AWS Security
    "res_239": {"skills_to_add": ["Application Security",
                                   "Cybersecurity Fundamentals",
                                   "Information Security Management"]},
    # res_240: DevSecOps
    "res_240": {"skills_to_add": ["DevSecOps", "Application Security",
                                   "Information Security Management"]},
    # res_241: PCB KiCad
    "res_241": {"skills_to_add": ["PCB Design", "Embedded Systems & Microcontrollers",
                                   "Digital Electronics"]},
    # res_242: Internship Search
    "res_242": {"skills_to_add": ["Internship Search Strategies",
                                   "Career Planning"]},
    # res_243: Higher Studies
    "res_243": {"skills_to_add": ["Higher Studies Planning (MS/MBA)",
                                   "GATE / GRE Preparation"]},
    # res_244: Technical Blogging
    "res_244": {"skills_to_add": ["Technical Blogging & Portfolio Building",
                                   "Personal Branding Online",
                                   "Open Source Development"]},
    # res_245: Public Speaking (Toastmasters)
    "res_245": {"skills_to_add": ["Public Speaking", "Presentation Skills",
                                   "Group Discussion Skills"]},
    # res_246: Conflict Resolution
    "res_246": {"skills_to_add": ["Conflict Resolution", "Teamwork & Collaboration",
                                   "Negotiation"]},
    # res_247: Creativity
    "res_247": {"skills_to_add": ["Creativity", "Problem Solving"]},
    # res_248: Habit Building
    "res_248": {"skills_to_add": ["Habit Building", "Discipline & Consistency",
                                   "Growth Mindset"]},
    # res_249: Resilience (Yale)
    "res_249": {"skills_to_add": ["Resilience & Mental Health",
                                   "Stress Management", "Growth Mindset"]},
    # res_250: Sales
    "res_250": {"skills_to_add": ["Basic Sales & Persuasion", "Negotiation",
                                   "Entrepreneurship Mindset"]},
    # res_251: Growth Mindset
    "res_251": {"skills_to_add": ["Growth Mindset", "Learning How to Learn",
                                   "Resilience & Mental Health"]},
    # res_252: Stress Management NPTEL
    "res_252": {"skills_to_add": ["Stress Management", "Resilience & Mental Health"]},
}

# Apply full replacements
res_map = {r['id']: r for r in resources}

for rid, update in skill_enrichments.items():
    if rid in res_map:
        res_map[rid]['skills'] = update['skills']

# Apply additions
for rid, update in early_enrichments.items():
    if rid in res_map:
        current = res_map[rid].get('skills', [])
        to_add = update.get('skills_to_add', [])
        res_map[rid]['skills'] = current + [s for s in to_add if s not in current]

# Write back
with open('data/resources.json', 'w', encoding='utf-8') as f:
    json.dump(list(res_map.values()), f, indent=2, ensure_ascii=False)

print(f"Enrichment done: {len(skill_enrichments)} full replacements, {len(early_enrichments)} additions")
print(f"Total resources: {len(res_map)}")

# ── Add remaining missing resources ──────────────────────────────────────────
resources = json.load(open('data/resources.json', encoding='utf-8'))
existing_ids = {r['id'] for r in resources}
existing_urls = {r['url'] for r in resources}

extra_resources = [
  {
    "id": "res_311",
    "title": "React Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=bMknfKXIFA8",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["React", "Frontend Development"],
    "skills": ["React", "JavaScript (Frontend)", "Frontend Development",
               "Full Stack Development", "Next.js"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp 12-hour React course — hooks, components, state, Router, and full project builds."
  },
  {
    "id": "res_312",
    "title": "Node.js & Express.js Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=Oe421EPjeBE",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Node.js", "Express.js", "Backend Development"],
    "skills": ["Node.js", "Express.js", "Backend Development",
               "REST APIs", "Full Stack Development",
               "API Development & Integration", "Web Application Development"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp 8-hour Node.js & Express course — REST APIs, middleware, auth, and MongoDB integration."
  },
  {
    "id": "res_313",
    "title": "Flutter Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=VPvVD8t02U8",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Flutter", "Mobile Development"],
    "skills": ["Flutter", "Mobile Development", "Mobile App Development", "Dart"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp Flutter tutorial — widgets, state management, navigation, and cross-platform app building."
  },
  {
    "id": "res_314",
    "title": "Go Programming for Beginners – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=un6ZyFkqFKo",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Go Programming"],
    "skills": ["Go (Golang)", "Backend Development"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp Go (Golang) tutorial — syntax, goroutines, channels, REST APIs and microservices."
  },
  {
    "id": "res_315",
    "title": "Kotlin Crash Course – Traversy Media (YouTube)",
    "url": "https://www.youtube.com/watch?v=5flXf8nuq60",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Kotlin Programming"],
    "skills": ["Kotlin", "Android Development", "Mobile App Development"],
    "branches": ["CSE", "IT"],
    "description": "Traversy Media Kotlin crash course — syntax, OOP, null safety, coroutines and Android basics."
  },
  {
    "id": "res_316",
    "title": "Swift for Beginners – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=comQ1-x2a1Q",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Swift Programming", "iOS Development"],
    "skills": ["Swift", "Mobile Development", "Mobile App Development"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp Swift programming tutorial — variables, OOP, optionals, SwiftUI, and iOS app basics."
  },
  {
    "id": "res_317",
    "title": "Rust Programming – No Boilerplate (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLZaoyhMXgBzoM9bfb5pyUOT3zjnaDdSEP",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Rust Programming"],
    "skills": ["Rust", "Systems Programming"],
    "branches": ["CSE"],
    "description": "No Boilerplate's Rust playlist — ownership, borrowing, lifetimes, error handling and async Rust."
  },
  {
    "id": "res_318",
    "title": "Android Development Full Course – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=fis26HvvDII",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Android Development", "Kotlin Programming"],
    "skills": ["Android Development", "Kotlin", "Mobile App Development",
               "Mobile Development"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp Android development course — Kotlin, Jetpack Compose, ViewModels, Room and navigation."
  },
  {
    "id": "res_319",
    "title": "Microsoft Azure Fundamentals – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=NKEFWyqJ5XA",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Microsoft Azure", "Cloud Computing"],
    "skills": ["Microsoft Azure", "Cloud Computing",
               "Cloud Computing (AWS/GCP/Azure)", "Cloud Infrastructure"],
    "branches": ["CSE", "IT"],
    "description": "freeCodeCamp AZ-900 prep — Azure services, security, governance, pricing and support overview."
  },
  {
    "id": "res_320",
    "title": "Competitive Programming – Errichto (YouTube)",
    "url": "https://www.youtube.com/c/Errichto",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Competitive Programming", "Algorithms"],
    "skills": ["Competitive Programming Strategy",
               "Data Structures & Algorithms (DSA)", "Problem Solving"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Errichto teaches competitive programming — segment trees, DP, graphs, contest strategies and live coding."
  },
  {
    "id": "res_321",
    "title": "GraphQL Tutorial – Traversy Media (YouTube)",
    "url": "https://www.youtube.com/watch?v=Y0lDGjwRYKw",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["GraphQL"],
    "skills": ["GraphQL", "REST APIs", "API Development & Integration",
               "Backend Development"],
    "branches": ["CSE", "IT"],
    "description": "Traversy Media GraphQL crash course — schemas, queries, mutations, resolvers and Apollo."
  },
  {
    "id": "res_322",
    "title": "Next.js Full Course – Traversy Media (YouTube)",
    "url": "https://www.youtube.com/watch?v=mTz0GXj8NN0",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Next.js", "Full Stack Development"],
    "skills": ["Next.js", "React", "Full Stack Development",
               "Backend Development"],
    "branches": ["CSE", "IT"],
    "description": "Traversy Media Next.js crash course — pages, routing, SSR, SSG, API routes and deployment."
  },
  {
    "id": "res_323",
    "title": "System Design Interview – Gaurav Sen (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLMCXHnjXnTnvo6alSjVkgxV-VH6EPyvoX",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["System Design"],
    "skills": ["System Design", "System Design (Advanced)",
               "Distributed Systems", "Microservices Architecture",
               "Backend Development"],
    "branches": ["CSE", "IT"],
    "description": "Gaurav Sen system design interview playlist — scalability, caching, databases, load balancing and real-world designs."
  },
  {
    "id": "res_324",
    "title": "Computer Vision – sentdex (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLQVvvaa0QuDdttJXlLtAJxJetJcqmqlQq",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Computer Vision", "Deep Learning"],
    "skills": ["Computer Vision", "Deep Learning", "Machine Learning",
               "Python Programming", "Neural Networks"],
    "branches": ["CSE", "AI_DS"],
    "description": "Sentdex OpenCV and computer vision playlist — image processing, object detection, face recognition and neural networks."
  },
  {
    "id": "res_325",
    "title": "Reinforcement Learning – Hugging Face Course (YouTube/Free)",
    "url": "https://huggingface.co/learn/deep-rl-course/unit0/introduction",
    "type": "Course",
    "tags": ["Free", "Certificate", "Intermediate", "Global"],
    "subjects": ["Reinforcement Learning"],
    "skills": ["Reinforcement Learning", "Deep Learning", "Machine Learning"],
    "branches": ["CSE", "AI_DS"],
    "description": "Hugging Face free deep RL course — Q-learning, policy gradient, PPO, and hands-on game environments."
  },
  {
    "id": "res_326",
    "title": "GATE / Higher Studies Planning – Gate Smashers Full Playlist",
    "url": "https://www.youtube.com/@GateSmashers",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["GATE Preparation", "Higher Studies"],
    "skills": ["GATE / GRE Preparation", "Higher Studies Planning (MS/MBA)",
               "Technical Interview Preparation"],
    "branches": ["CSE", "IT", "ECE", "EEE", "ME", "CE"],
    "description": "Gate Smashers complete GATE CS preparation — all core subjects with PYQ analysis and mock strategies."
  },
  {
    "id": "res_327",
    "title": "DSP Fundamentals – Neso Academy (YouTube Playlist)",
    "url": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRhG6s3jYIU48CqsT5cyiDTO",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "India"],
    "subjects": ["Digital Signal Processing"],
    "skills": ["Digital Signal Processing", "Communication Systems",
               "RF & Wireless Communication"],
    "branches": ["ECE", "EEE", "EI"],
    "description": "Neso Academy DSP playlist — discrete signals, DFT, FFT, FIR/IIR filters, Z-transform and spectrum analysis."
  },
  {
    "id": "res_328",
    "title": "Power Electronics – NPTEL (YouTube)",
    "url": "https://www.youtube.com/playlist?list=PLbRMhDVUMngf-peFloB7kyiA40PUkGRoZ",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "India", "Government"],
    "subjects": ["Power Electronics"],
    "skills": ["Power Electronics", "Electrical Machines",
               "Power Systems Analysis", "Renewable Energy Systems",
               "Electric Vehicles & Battery Technology", "Smart Grid",
               "High Voltage Engineering", "Energy Auditing & Management"],
    "branches": ["EEE"],
    "description": "NPTEL power electronics lectures — converters, inverters, DC-DC circuits, motor drives and renewable energy."
  },
  {
    "id": "res_329",
    "title": "Responsible AI & Ethics – Google Responsible AI Practices (Free)",
    "url": "https://ai.google/responsibility/responsible-ai-practices/",
    "type": "Reference",
    "tags": ["Free", "Official", "Beginner", "Global"],
    "subjects": ["Responsible AI & Ethics", "AI Ethics"],
    "skills": ["Responsible AI", "Responsible AI & AI Ethics",
               "AI Literacy for Professionals"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Google's free Responsible AI practices guide — fairness, transparency, privacy, security and accountability."
  },
  {
    "id": "res_330",
    "title": "Blockchain Fundamentals – Coursera (Princeton)",
    "url": "https://www.coursera.org/learn/cryptocurrency",
    "type": "Course",
    "tags": ["Free", "Certificate", "Intermediate", "Global"],
    "subjects": ["Blockchain Technology"],
    "skills": ["Blockchain Basics", "Cybersecurity Fundamentals",
               "Cryptography"],
    "branches": ["CSE", "IT"],
    "description": "Princeton Bitcoin and Cryptocurrency Technologies course — blockchain, mining, smart contracts and DeFi."
  },
  {
    "id": "res_331",
    "title": "Mass Transfer Operations – NPTEL (IIT Madras)",
    "url": "https://nptel.ac.in/courses/103/106/103106113/",
    "type": "Course",
    "tags": ["Free", "Government", "Certificate", "Intermediate", "India"],
    "subjects": ["Mass Transfer Operations"],
    "skills": ["Mass Transfer Operations", "Chemical Engineering",
               "Process Design & Optimization"],
    "branches": ["CHEM"],
    "description": "NPTEL mass transfer operations — absorption, extraction, distillation, drying and leaching."
  },
  {
    "id": "res_332",
    "title": "Chemical Reaction Engineering – NPTEL (IIT Bombay)",
    "url": "https://nptel.ac.in/courses/103/102/103102044/",
    "type": "Course",
    "tags": ["Free", "Government", "Certificate", "Intermediate", "India"],
    "subjects": ["Chemical Reaction Engineering"],
    "skills": ["Chemical Reaction Engineering", "Chemical Engineering",
               "Process Design & Optimization"],
    "branches": ["CHEM"],
    "description": "NPTEL chemical reaction engineering — reactor design, kinetics, CSTR, PFR, and non-ideal reactors."
  },
  {
    "id": "res_333",
    "title": "Process Safety & HAZOP – AIChE Free Resources",
    "url": "https://www.aiche.org/resources/publications/cep/process-safety",
    "type": "Reference",
    "tags": ["Free", "Official", "Intermediate", "Global"],
    "subjects": ["Process Safety", "HAZOP"],
    "skills": ["Process Safety & HAZOP", "Environmental Compliance",
               "Chemical Engineering"],
    "branches": ["CHEM"],
    "description": "AIChE Chemical Engineering Progress resources on process safety — HAZOP, LOPA, PSM and risk analysis."
  },
  {
    "id": "res_334",
    "title": "Operations Research – NPTEL (IIT Bombay)",
    "url": "https://nptel.ac.in/courses/110/101/110101081/",
    "type": "Course",
    "tags": ["Free", "Government", "Certificate", "Intermediate", "India"],
    "subjects": ["Operations Research"],
    "skills": ["Operations Research for Engineering",
               "Mechanical Engineering"],
    "branches": ["ME", "CE", "CHEM"],
    "description": "IIT Bombay NPTEL operations research — linear programming, transportation, assignment, queuing and inventory."
  },
  {
    "id": "res_335",
    "title": "Electric Vehicles – NPTEL (IIT Kharagpur)",
    "url": "https://nptel.ac.in/courses/108/105/108105227/",
    "type": "Course",
    "tags": ["Free", "Government", "Certificate", "Intermediate", "India"],
    "subjects": ["Electric Vehicles", "Battery Technology"],
    "skills": ["Electric Vehicles & Battery Technology",
               "Power Electronics", "Renewable Energy Systems",
               "Electrical Machines", "Smart Grid"],
    "branches": ["EEE", "ME"],
    "description": "NPTEL EV fundamentals — battery chemistry, BMS, motor drives, charging infrastructure and EV design."
  },
  {
    "id": "res_336",
    "title": "Django REST Framework – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=c708Nf0cHrs",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["Django", "REST APIs", "Backend Development"],
    "skills": ["Django", "REST APIs", "Backend Development",
               "Python Programming", "Full Stack Development",
               "API Development & Integration", "Web Application Development"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "freeCodeCamp Django REST Framework course — serializers, viewsets, authentication, and API building."
  },
  {
    "id": "res_337",
    "title": "Flask REST API Tutorial – Traversy Media (YouTube)",
    "url": "https://www.youtube.com/watch?v=GMppyAPbLYk",
    "type": "Video",
    "tags": ["Free", "YouTube", "Beginner", "Global"],
    "subjects": ["Flask", "REST APIs", "Backend Development"],
    "skills": ["Flask", "REST APIs", "Backend Development",
               "Python Programming", "API Development & Integration",
               "Full Stack Development"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "Traversy Media Flask REST API tutorial — routes, authentication, SQLAlchemy, JWT and deployment."
  },
  {
    "id": "res_338",
    "title": "FastAPI Full Tutorial – freeCodeCamp (YouTube)",
    "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA",
    "type": "Video",
    "tags": ["Free", "YouTube", "Intermediate", "Global"],
    "subjects": ["FastAPI", "REST APIs", "Backend Development"],
    "skills": ["FastAPI", "REST APIs", "Backend Development",
               "Python Programming", "API Development & Integration",
               "Web Application Development"],
    "branches": ["CSE", "IT", "AI_DS"],
    "description": "freeCodeCamp FastAPI tutorial — async endpoints, Pydantic, OAuth2, SQLAlchemy and API documentation."
  },
  {
    "id": "res_339",
    "title": "IT Service Management (ITSM) – ITIL v4 Foundation (Axelos Free)",
    "url": "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation",
    "type": "Reference",
    "tags": ["Free", "Official", "Intermediate", "Global"],
    "subjects": ["IT Service Management"],
    "skills": ["IT Service Management (ITSM)", "Enterprise Architecture",
               "Information Security Management", "Network Administration",
               "Database Administration", "Web Application Development",
               "API Development & Integration", "Virtualization"],
    "branches": ["IT"],
    "description": "ITIL v4 Foundation official guide — service management, incident, change and problem management practices."
  },
  {
    "id": "res_340",
    "title": "Network Administration – Cisco Networking Academy (Free Courses)",
    "url": "https://www.netacad.com/courses/networking",
    "type": "Course",
    "tags": ["Free", "Official", "Certificate", "Beginner", "Global"],
    "subjects": ["Computer Networks", "Network Administration"],
    "skills": ["Network Administration", "Computer Networks",
               "Cybersecurity Fundamentals", "Database Administration",
               "Cloud Infrastructure", "Information Security Management"],
    "branches": ["CSE", "IT", "ECE"],
    "description": "Cisco NetAcad free networking courses — CCNA prep, IP routing, switching, wireless and security fundamentals."
  },
  {
    "id": "res_341",
    "title": "ARM Cortex-M Programming – Udemy (Free Preview + ARM Learn)",
    "url": "https://developer.arm.com/documentation/den0013/d/",
    "type": "Notes",
    "tags": ["Free", "Official", "Intermediate", "Global"],
    "subjects": ["ARM Architecture", "Embedded Systems"],
    "skills": ["ARM Cortex Programming",
               "Embedded Systems & Microcontrollers",
               "Microprocessors & Microcontrollers"],
    "branches": ["ECE", "EI"],
    "description": "ARM official Cortex-M documentation — architecture, instruction set, memory model, exception handling and CMSIS."
  },
  {
    "id": "res_342",
    "title": "RF & Wireless Communications – NPTEL (IIT Kanpur)",
    "url": "https://nptel.ac.in/courses/117/104/117104099/",
    "type": "Course",
    "tags": ["Free", "Government", "Certificate", "Intermediate", "India"],
    "subjects": ["RF Engineering", "Wireless Communications"],
    "skills": ["RF & Wireless Communication", "Communication Systems",
               "Information Theory & Coding"],
    "branches": ["ECE"],
    "description": "NPTEL RF and wireless communications — transmission lines, antennas, propagation, modulation and 5G basics."
  },
  {
    "id": "res_343",
    "title": "Downstream Bioprocessing – NPTEL (IIT Delhi)",
    "url": "https://nptel.ac.in/courses/102/102/102102082/",
    "type": "Course",
    "tags": ["Free", "Government", "Certificate", "Intermediate", "India"],
    "subjects": ["Downstream Processing", "Bioprocessing"],
    "skills": ["Downstream Processing", "Industrial Biotechnology",
               "Genetic Engineering Techniques",
               "Molecular Biology Techniques",
               "Laboratory Information Systems"],
    "branches": ["BT"],
    "description": "NPTEL downstream bioprocessing — cell disruption, centrifugation, chromatography, filtration and bioseparation."
  },
]

added = 0
for nr in extra_resources:
    if nr['id'] not in existing_ids and nr['url'] not in existing_urls:
        resources.append(nr)
        existing_ids.add(nr['id'])
        existing_urls.add(nr['url'])
        added += 1
    else:
        print(f"SKIP: {nr['id']}")

with open('data/resources.json', 'w', encoding='utf-8') as f:
    json.dump(resources, f, indent=2, ensure_ascii=False)

print(f"Added {added} extra resources. Total: {len(resources)}")
