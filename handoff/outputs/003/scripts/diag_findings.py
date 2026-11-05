"""Handoff 003 diagnostics (ids and counts only). Run from repo root: python3 -I handoff/outputs/003/scripts/diag_findings.py"""
import csv, collections
def rd(p): return list(csv.DictReader(open(p, encoding='utf-8')))
T = {r['token_id']: r for r in rd('data/derived/dolgan/tokens.csv')}
objs = rd('data/derived/dolgan/objects.csv')
print('objects', len(objs), 'with pred', sum(1 for o in objs if o['pred_token_id']))
c = collections.Counter(T[o['pred_token_id']]['ps'] for o in objs if o['pred_token_id'])
print('pred ps counts', c.most_common())
by = collections.defaultdict(list)
for t in T.values(): by[t['utt_id']].append(t)
b1 = rd('data/derived/dolgan/b1_candidates.csv')
print('b1', len(b1), collections.Counter(r['rules'] for r in b1).most_common())
n = k = 0
for r in b1:
    if 'copula_next' not in r['rules'].split(): continue
    ws = sorted(by[r['token_id'].split('.w')[0]], key=lambda t: int(t['idx'])); i = int(r['token_id'].split('.w')[1])
    cop = [j for j, t in enumerate(ws) if j >= i and t['ps'] in ('cop', 'aux')]
    if not cop: continue
    n += 1
    if any(t['ps'] == 'v' for t in ws[i:cop[0]]): k += 1
print('copula_next rows', n, 'with a lexical v between target and copula/aux:', k)
fl = rd('data/derived/dolgan/qa_flags.csv'); print('flag cols', list(fl[0].keys()))
print(collections.Counter(f.get('flag') or f.get('kind') for f in fl))
for f in fl:
    if (f.get('flag') or f.get('kind')) in ('morph_gloss_mismatch', 'speaker_not_in_coma'):
        print({k: v for k, v in f.items() if k in ('flag', 'kind', 'token_id', 'speaker_id', 'detail', 'text_id')}, T.get(f.get('token_id'), {}).get('mp'), '|', T.get(f.get('token_id'), {}).get('ge'))
w = [f for f in fl if (f.get('flag') or f.get('kind')) == 'word_tier_event_without_word']
print('word_tier_event_without_word by text (top5):', collections.Counter(f.get('text_id') for f in w).most_common(5))
print('sample', {k: v[:60] for k, v in w[0].items()})
