import sys, os, re, collections, pickle, json
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W, coma_lib
OUT = f'{W.HOME}/scratch/002/out'
def fe_ok(fe):
    if not fe: return False
    body = fe.strip()[1:]
    return not re.search(r'\b[A-ZА-ЯЁ][a-zа-яё]+', body.replace(' I ', ' ')) and len(body) < 90
def tx_ok(tx): return not re.search(r'[A-ZА-ЯЁ]', tx.strip()) and len(tx.strip()) < 30
res = {}
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    # Q4: first utterance (in a flk text) with >=10 fully-annotated consecutive words, no capitals
    q4 = None
    for rel, d in sorted(D.items()):
        if not rel.startswith('flk'): continue
        rows = list(W.words(d)); run = []
        for r in rows:
            full = all(r.get(k) and r[k].strip() for k in ('tx', 'mb', 'mp', 'ge', 'mc', 'ps')) and tx_ok(r['tx'])
            if full and (not run or r['ref'] == run[-1]['ref']): run.append(r)
            else: run = [r] if full else []
            if len(run) == 10: q4 = (rel.split('/')[1], run); break
        if q4: break
    res[c + '_q4'] = {'text': q4[0], 'rows': [[r['ids'][0], r['ids'][1], r['tx'].strip(), r['mb'], r['mp'], r['ge'], r['mc'], r['ps']] for r in q4[1]]}
    b1 = pickle.load(open(f'{OUT}/{c}_b1.pkl', 'rb'))
    # distinct-ish examples: take first 5 whose word isn't a repeat
    def pick(lst, n=5, key=lambda x: x[1]):
        seen, out = set(), []
        for x in lst:
            if key(x) in seen: continue
            seen.add(key(x)); out.append(x)
            if len(out) == n: break
        return out
    res[c + '_O'] = pick(b1['syf_ex']['O']); res[c + '_S'] = pick(b1['syf_ex']['S'])
    res[c + '_obj'] = pick([x for x in b1['obj_ex']], 5, key=lambda x: x[1])
    res[c + '_St'] = pick([x for x in b1['st_ex'] if fe_ok(x[5])], 5, key=lambda x: x[1])
    res[c + '_evid'] = [(r[0].split('_')[0] + '..', r[2], r[3], r[4], r[5], r[6], r[7]) for r in b1['ev_rows'] if tx_ok(r[2]) and fe_ok(r[7])][:12]
json.dump(res, open(f'{OUT}/excerpts.json', 'w'), ensure_ascii=False, indent=1)
for k, v in res.items():
    print('####', k)
    if k.endswith('_q4'):
        print(' text', v['text']); [print('  ', x) for x in v['rows']]
    else:
        for x in (v if isinstance(v, list) else []): print('  ', x)
