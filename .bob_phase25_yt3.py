import json

resources = json.load(open('data/resources.json', encoding='utf-8'))
existing_urls = {r['url'] for r in resources}
existing_ids = {r['id'] for r in resources}

new_yt = [
    {
        'id': 'res_360',
        'title': 'ARM Cortex-M Tutorial – Phil Salmony (YouTube)',
        'url': 'https://www.youtube.com/playlist?list=PLXSyc11qLa1a4Tqbz228dPZfMrs-KRpzA',
        'type': 'Video',
        'tags': ['Free', 'YouTube', 'Intermediate', 'Global'],
        'subjects': ['ARM Architecture', 'Embedded Systems'],
        'skills': ['ARM Cortex Programming', 'Embedded Systems & Microcontrollers',
                   'Microprocessors & Microcontrollers'],
        'branches': ['ECE', 'EI'],
        'description': 'Phil Salmony ARM Cortex-M series — registers, memory map, interrupts, CMSIS, FreeRTOS on STM32.'
    },
    {
        'id': 'res_361',
        'title': 'Six Sigma Green Belt – LSSGB (YouTube)',
        'url': 'https://www.youtube.com/watch?v=FWvgMoVomE0',
        'type': 'Video',
        'tags': ['Free', 'YouTube', 'Intermediate', 'Global'],
        'subjects': ['Six Sigma', 'Quality Management'],
        'skills': ['Six Sigma for Process Industries', 'Quality Control'],
        'branches': ['CHEM', 'ME'],
        'description': 'Six Sigma fundamentals — DMAIC process, control charts, statistical process control, and Lean tools explained.'
    },
    {
        'id': 'res_362',
        'title': 'LabVIEW for Beginners – NI Tutorial (YouTube)',
        'url': 'https://www.youtube.com/watch?v=Iyu65HDTPMU',
        'type': 'Video',
        'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
        'subjects': ['LabVIEW', 'Virtual Instrumentation'],
        'skills': ['LabVIEW & Virtual Instrumentation', 'Industrial Automation',
                   'Sensor Calibration & Metrology'],
        'branches': ['EI', 'ECE'],
        'description': 'National Instruments LabVIEW intro on YouTube — data flow programming, VI creation, DAQ and signal analysis.'
    },
    {
        'id': 'res_363',
        'title': 'Biomedical Instrumentation – NPTEL (YouTube)',
        'url': 'https://www.youtube.com/playlist?list=PLbRMhDVUMngfRvJ5_06LIHFtqJEH0lFCT',
        'type': 'Video',
        'tags': ['Free', 'YouTube', 'Intermediate', 'India', 'Government'],
        'subjects': ['Biomedical Instrumentation'],
        'skills': ['Biomedical Instrumentation', 'Sensor Calibration & Metrology'],
        'branches': ['EI', 'ECE'],
        'description': 'NPTEL biomedical instrumentation YouTube playlist — biosignals, ECG, EEG, patient monitoring and medical imaging.'
    },
    {
        'id': 'res_364',
        'title': 'Aspen Plus Introduction – LearnChemE (YouTube)',
        'url': 'https://www.youtube.com/playlist?list=PLZCl1u1EjO_tQ1hGJUcVh5lTGQ0WkMaV1',
        'type': 'Video',
        'tags': ['Free', 'YouTube', 'Beginner', 'Global'],
        'subjects': ['Aspen Plus Simulation', 'Chemical Process Simulation'],
        'skills': ['Aspen Plus Process Simulation', 'Process Design & Optimization',
                   'Chemical Engineering'],
        'branches': ['CHEM'],
        'description': 'LearnChemE Aspen Plus YouTube tutorials — flash separators, distillation, reactors and process simulation basics.'
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
