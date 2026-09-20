import json

resources = json.load(open('data/resources.json', encoding='utf-8'))
existing_urls = {r['url'] for r in resources}
existing_ids = {r['id'] for r in resources}

new_yt = [
  {
    'id': 'res_352',
    'title': 'AI Agents & Prompt Engineering – Sam Witteveen (YouTube)',
    'url': 'https://www.youtube.com/c/samwitteveenai',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Intermediate', 'Global'],
    'subjects': ['Generative AI', 'AI Agents', 'Prompt Engineering'],
    'skills': ['AI Agents', 'Prompt Engineering', 'Generative AI',
               'AI Literacy for Professionals', 'Generative AI & LLMs',
               'Responsible AI', 'Responsible AI & AI Ethics'],
    'branches': ['CSE', 'IT', 'AI_DS'],
    'description': 'Sam Witteveen builds LangChain, AutoGen and RAG applications — practical AI agent and prompt engineering tutorials.'
  },
  {
    'id': 'res_353',
    'title': 'AI Literacy – Crash Course AI (YouTube)',
    'url': 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtO65LeD2p4_Sb5XQ51par_b',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
    'subjects': ['AI Literacy', 'Introduction to AI'],
    'skills': ['AI Literacy for Professionals', 'Digital Literacy',
               'Responsible AI', 'Machine Learning'],
    'branches': ['CSE', 'IT', 'AI_DS', 'ECE', 'EEE', 'ME', 'CE', 'CHEM', 'BT', 'EI'],
    'description': 'PBS Crash Course AI series — what is AI, machine learning, ethics, bias, privacy and societal impact.'
  },
  {
    'id': 'res_354',
    'title': 'Debugging & Profiling – freeCodeCamp (YouTube)',
    'url': 'https://www.youtube.com/watch?v=l8ze3V_dtjE',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Intermediate', 'Global'],
    'subjects': ['Debugging', 'Software Engineering'],
    'skills': ['Debugging', 'Software Testing', 'Python Programming'],
    'branches': ['CSE', 'IT', 'AI_DS'],
    'description': 'freeCodeCamp debugging tutorial — breakpoints, stack traces, pdb, Chrome DevTools and systematic debugging.'
  },
  {
    'id': 'res_355',
    'title': 'Technical Writing for Engineers (YouTube)',
    'url': 'https://www.youtube.com/watch?v=_HKGcT3RpbU',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
    'subjects': ['Written Communication', 'Professional Writing'],
    'skills': ['Communication — Written', 'Professional Email Writing',
               'Technical Blogging & Portfolio Building'],
    'branches': ['CSE', 'IT', 'AI_DS', 'ECE', 'EEE', 'ME', 'CE', 'CHEM', 'BT', 'EI'],
    'description': 'Technical writing tips for engineers — professional emails, reports, documentation and workplace communication.'
  },
  {
    'id': 'res_356',
    'title': 'HR Interview Prep – Internshala (YouTube)',
    'url': 'https://www.youtube.com/watch?v=YUkFsT5gIwE',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Beginner', 'India'],
    'subjects': ['HR Interview', 'Job Interview Preparation'],
    'skills': ['HR Interview & Behavioural Questions', 'Technical Interview Preparation',
               'Communication — Verbal', 'Professional Email Writing'],
    'branches': ['CSE', 'IT', 'AI_DS', 'ECE', 'EEE', 'ME', 'CE', 'CHEM', 'BT', 'EI'],
    'description': 'Internshala guide to HR interview questions — STAR method, common questions, salary negotiation tips.'
  },
  {
    'id': 'res_357',
    'title': 'Digital Literacy – Google Digital Wellbeing (YouTube)',
    'url': 'https://www.youtube.com/watch?v=OOSryToGjOY',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
    'subjects': ['Digital Literacy'],
    'skills': ['Digital Literacy', 'AI Literacy for Professionals', 'Security Awareness'],
    'branches': ['CSE', 'IT', 'AI_DS', 'ECE', 'EEE', 'ME', 'CE', 'CHEM', 'BT', 'EI'],
    'description': "Google's digital literacy series covering online safety, data privacy, misinformation and digital wellbeing."
  },
  {
    'id': 'res_358',
    'title': 'Bioinformatics – StatQuest (YouTube)',
    'url': 'https://www.youtube.com/c/joshstarmer',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
    'subjects': ['Bioinformatics', 'Statistics'],
    'skills': ['Bioinformatics Tools (BLAST, NCBI)', 'Biostatistics & R',
               'Genomics & Proteomics', 'Computational Drug Discovery',
               'Molecular Biology Techniques', 'Genetic Engineering Techniques',
               'Downstream Processing', 'Laboratory Information Systems'],
    'branches': ['BT', 'AI_DS'],
    'description': 'StatQuest visual explanations of bioinformatics — RNA-seq, PCA, statistical tests used in genomics research.'
  },
  {
    'id': 'res_359',
    'title': 'Network Admin – David Bombal (YouTube)',
    'url': 'https://www.youtube.com/watch?v=n2D1o-aM-2s',
    'type': 'Video',
    'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
    'subjects': ['Computer Networks', 'Network Administration'],
    'skills': ['Network Administration', 'Computer Networks',
               'Database Administration', 'IT Service Management (ITSM)',
               'Enterprise Architecture', 'Virtualization',
               'Information Security Management'],
    'branches': ['CSE', 'IT', 'ECE'],
    'description': 'David Bombal CCNA prep and network admin — routing, switching, VLANs, Cisco IOS and enterprise networking.'
  },
]

added = 0
for nr in new_yt:
    if nr['id'] not in existing_ids and nr['url'] not in existing_urls:
        resources.append(nr)
        existing_ids.add(nr['id'])
        existing_urls.add(nr['url'])
        added += 1
    else:
        print('SKIP:', nr['id'])

with open('data/resources.json', 'w', encoding='utf-8') as f:
    json.dump(resources, f, indent=2, ensure_ascii=False)
print(f'Added {added}. Total: {len(resources)}')
