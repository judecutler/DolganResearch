import xml.etree.ElementTree as ET
def load(path):
    r = ET.parse(path).getroot()
    sp = {}
    for s in r.iter('Speaker'):
        sig = (s.findtext('Sigle') or '').strip()
        d = {k.get('Name'): (k.text or '').strip() for k in s.iter('Key')}
        d['_sex'] = (s.findtext('Sex') or '').strip(); d['_known'] = (s.findtext('KnownHuman') or '').strip()
        d['_pseudo'] = (s.findtext('Pseudo') or '').strip()
        sp[sig] = d
    co = {}
    for c in r.iter('Communication'):
        d = {}
        for k in c.iter('Key'):
            d.setdefault(k.get('Name'), (k.text or '').strip())
        d['_tr'] = [(t.findtext('Name') or '', t.findtext('Filename') or '') for t in c.iter('Transcription')]
        d['_files'] = [(f.findtext('Filename') or '') for f in c.iter('File')]
        d['_langs'] = [(l.findtext('LanguageCode') or l.text or '') for l in c.iter('Language')]
        co[c.get('Name')] = d
    return sp, co
