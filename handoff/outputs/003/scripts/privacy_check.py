"""Privacy check for reports (prints only counts/line numbers, never the matched text).
python3 -I handoff/outputs/003/scripts/privacy_check.py reports/qa_report.md reports/gate0_feasibility.md reports/power_b2.md"""
import sys, re, glob, xml.etree.ElementTree as ET
names = set()
for cm in glob.glob('data/raw/*/*.coma'):
    for s in ET.parse(cm).getroot().iter('Speaker'):
        for tag in ('Pseudo', 'Name', 'FirstName', 'LastName', 'Surname', 'Given'):
            v = (s.findtext(tag) or '').strip()
            if len(v) > 2: names.add(v)
        for k in s.iter('Key'):
            if k.get('Name', '').lower().startswith(('1 ', '2 ', '3 ')) and k.text and len(k.text.strip()) > 2 and 'name' in k.get('Name', '').lower(): names.add(k.text.strip())
print('name-like values checked:', len(names))
for p in sys.argv[1:]:
    txt = open(p, encoding='utf-8').read(); lines = txt.split('\n'); bad = {}
    for n in names:
        hit = [i + 1 for i, l in enumerate(lines) if re.search(r'\b' + re.escape(n) + r'\b', l)]
        if hit: bad.setdefault('name', []).extend(hit)
    full = [i + 1 for i, l in enumerate(lines) if re.search(r'\b(1[89]|20)\d\d[-./](0?[1-9]|1[0-2])[-./](0?[1-9]|[12]\d|3[01])\b', l) or re.search(r'\b(0?[1-9]|[12]\d|3[01])[-./](0?[1-9]|1[0-2])[-./](1[89]|20)\d\d\b', l)]
    if full: bad['full_date'] = full
    ipa = [i + 1 for i, l in enumerate(lines) if re.search(r'[ɐ-ʯЀ-ӿʰ-˿]', l)]
    if ipa: bad['ipa_or_cyrillic'] = ipa
    quoted = [i + 1 for i, l in enumerate(lines) if re.search(r'\[\[|“|«', l)]
    if quoted: bad['quote_markers'] = quoted
    print(p, 'OK' if not bad else 'FLAGGED', {k: sorted(set(v))[:15] for k, v in bad.items()})
