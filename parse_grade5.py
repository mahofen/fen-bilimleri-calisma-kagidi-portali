import re

with open('grade5_outcomes.txt', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.split('='*50)
outcomes_dict = {}

for entry in entries:
    if not entry.strip():
        continue
    unit_m = re.search(r'UNIT:\s*(.*?)\n', entry)
    subj_m = re.search(r'SUBJECT:\s*(.*?)\n', entry)
    unit = unit_m.group(1).strip() if unit_m else ''
    subj = subj_m.group(1).strip() if subj_m else ''
    
    outcomes_s = re.search(r'OUTCOMES:\n(.*?)\nPROCESS:', entry, re.DOTALL)
    process_s = re.search(r'PROCESS:\n(.*)', entry, re.DOTALL)
    
    if outcomes_s and process_s:
        raw_o = outcomes_s.group(1).strip()
        raw_p = process_s.group(1).strip()
        
        matches = list(re.finditer(r'(FB\.5\.\d+\.\d+)\.\s*(.*?)(?=(?:FB\.5\.\d+\.\d+\.)|\Z)', raw_o, re.DOTALL))
        for m in matches:
            code = m.group(1)
            desc = m.group(2).strip()
            full_out = code + '. ' + desc
            if code not in outcomes_dict:
                p_match = re.search(re.escape(code) + r'\.(.*?)(?=(?:FB\.5\.\d+\.\d+\.)|\Z)', raw_p, re.DOTALL)
                proc_text = p_match.group(1).strip() if p_match else ''
                outcomes_dict[code] = {
                    'unit': unit,
                    'subject': subj,
                    'outcome': full_out,
                    'process': proc_text
                }

with open('parsed_5th_grade.txt', 'w', encoding='utf-8') as out_f:
    out_f.write(f'Total Unique Outcomes: {len(outcomes_dict)}\n\n')
    for k, v in outcomes_dict.items():
        out_f.write(f'=== {k} ===\n')
        out_f.write(f"UNIT: {v['unit']}\n")
        out_f.write(f"SUBJECT: {v['subject']}\n")
        out_f.write(f"OUTCOME: {v['outcome']}\n")
        out_f.write(f"PROCESS:\n{v['process']}\n\n")

print('Saved successfully. Total:', len(outcomes_dict))
