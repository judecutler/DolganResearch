"""Stage 1 for handoff 002: parse every .exb of a corpus into a compact pickle.
Usage: python3 -I parse_all.py CORPUS_DIR OUT_PICKLE
Stdlib only. Reads only; never modifies the corpus."""
import sys, os, pickle, glob, time
import xml.etree.ElementTree as ET

def parse_exb(path):
    root = ET.parse(path).getroot()
    tli_ids = [t.get('id') for t in root.iter('tli')]
    idx = {t: i for i, t in enumerate(tli_ids)}
    speakers = [s.get('id') for s in root.iter('speaker')]
    tiers = []
    for t in root.iter('tier'):
        evs = []
        for e in t.iter('event'):
            evs.append((idx.get(e.get('start'), -1), idx.get(e.get('end'), -1), e.get('start'), e.get('end'), e.text or ''))
        tiers.append({'id': t.get('id'), 'speaker': t.get('speaker'), 'category': t.get('category'),
                      'type': t.get('type'), 'display': t.get('display-name'), 'events': evs})
    return {'speakers': speakers, 'n_tli': len(tli_ids), 'tiers': tiers,
            'tli_dup': len(tli_ids) - len(set(tli_ids))}

if __name__ == '__main__':
    corpus, out = sys.argv[1], sys.argv[2]
    files = sorted(glob.glob(os.path.join(corpus, '*', '*', '*.exb')))
    data, errors = {}, []
    t0 = time.time()
    for f in files:
        rel = os.path.relpath(f, corpus)
        try:
            d = parse_exb(f); d['genre'] = rel.split(os.sep)[0]; d['size'] = os.path.getsize(f)
            data[rel] = d
        except Exception as ex:
            errors.append((rel, repr(ex)))
    pickle.dump({'data': data, 'errors': errors}, open(out, 'wb'))
    print(len(files), 'files,', len(data), 'parsed,', len(errors), 'errors,', round(time.time() - t0, 1), 's')
    for e in errors[:10]: print('ERR', e)
