"""Handoff 006 step 5: spot checks of the regenerated tables against the .exb files.
Run from the repo root:  python3 -I handoff/outputs/006/scripts/spot_checks_006.py > handoff/outputs/006/spot_checks.md
Stdlib only; does not import shared/ or case_change/. Prints ids, labels, pass/fail; no corpus sentences.
Words are re-derived from the .exb: utterance = the ref event whose text equals utterances.csv `ref` (same speaker);
its words are that speaker's tx events inside the ref span, in file order; wNN = ordinal. Each .exb is parsed once."""
import os, re, csv, random, collections, time, sys
import xml.etree.ElementTree as ET
SEED = 20261106
T0 = time.time()
ROOT = os.getcwd()
def rd(p): return list(csv.DictReader(open(p, encoding='utf-8')))
_dirs = {}
def exb_path(corpus, text_id):
    base = os.path.join(ROOT, 'data/raw', corpus + '-2.0')
    if corpus not in _dirs:
        m = {}
        for g in os.listdir(base):
            if os.path.isdir(os.path.join(base, g)):
                for t in os.listdir(os.path.join(base, g)): m[t] = os.path.join(base, g, t, t + '.exb')
        _dirs[corpus] = m
    return _dirs[corpus][text_id]
_cache = {}
def exb(corpus, text_id):
    k = (corpus, text_id)
    if k not in _cache:
        root = ET.parse(exb_path(corpus, text_id)).getroot()
        idx = {t.get('id'): i for i, t in enumerate(root.iter('tli'))}
        tiers = collections.defaultdict(lambda: collections.defaultdict(list))
        for t in root.iter('tier'):
            for e in t.iter('event'):
                tiers[t.get('speaker')][t.get('category')].append((idx[e.get('start')], idx[e.get('end')], (e.text or '').strip()))
        refs = collections.defaultdict(list)
        for spk, cats in tiers.items():
            for s, e, txt in cats.get('ref', []): refs[(spk, txt)].append((s, e))
        _cache[k] = (tiers, refs)
    return _cache[k]
UTT = {c: {u['utt_id']: u for u in rd(f'data/derived/{c}/utterances.csv')} for c in ('dolgan', 'evenki')}
def parse_tid(tid):
    m = re.fullmatch(r'(.+)#(\d+)\.w(\d+)', tid); return m.group(1) + '#' + m.group(2), int(m.group(3))
def words_of(corpus, utt_id):
    u = UTT[corpus].get(utt_id)
    if not u: return None, 'utterance not in utterances.csv'
    tiers, refs = exb(corpus, u['text_id']); spk = u['speaker_id']
    hits = refs.get((spk, u['ref'].strip()), [])
    if len(hits) != 1: return None, f'{len(hits)} ref events match'
    rs, re_ = hits[0]; cats = tiers[spk]
    look = {c: {(s, e): v for s, e, v in evs} for c, evs in cats.items()}
    out = []
    for s, e, tx in cats.get('tx', []):
        if s >= rs and e <= re_:
            w = {'tx': tx}
            for c in ('ge', 'ps', 'SyF'): w[c] = look.get(c, {}).get((s, e), '')
            out.append(w)
    return out, spk
def word(corpus, tid):
    uid, n = parse_tid(tid); ws, info = words_of(corpus, uid)
    if ws is None or not 1 <= n <= len(ws): return None, info if ws is None else 'ordinal out of range'
    return ws[n - 1], ''
morphs = lambda g: [m for m in re.split(r'[-=]', g) if m] if g else []
comps = lambda m: [c.strip('[]()') for c in m.split('.') if c.strip('[]()')]
def stem(ge): ms = morphs(ge); return ms[0].split('.')[0].strip('[]') if ms else ''
def is_cop(w): return w['ps'] in ('cop', 'aux') or stem(w['ge']) in ('be', 'become') or bool(re.search(r'(^|[:\s])cop|cop($|[\s.])', w['SyF']))
rng = random.Random(SEED)
res = []
def rec(g, tid, ok, note): res.append((g, tid, ok, note))
tok = {c: {r['token_id']: r for r in rd(f'data/derived/{c}/tokens.csv')} for c in ('dolgan', 'evenki')}
VERB = ('v', 'aux', 'cop')
# (1) object predicate
objs = rd('data/derived/dolgan/objects.csv')
TID = 'ElBK_KuNS_2004_Storytellers_conv#135.w03'
o = [r for r in objs if r['token_id'] == TID]
if not o: rec('object predicate', TID, None, 'object row absent from objects.csv')
for r in o:
    p = r['pred_token_id']
    if not p: rec('object predicate', TID, True, 'pred_token_id empty')
    else:
        ps = tok['dolgan'].get(p, {}).get('ps', '(token missing)'); w, info = word('dolgan', p)
        eps = w['ps'] if w else '(not found: ' + info + ')'
        rec('object predicate', TID, ps in VERB and eps in VERB, f'pred `{p}`: tokens.csv ps={ps!r}, .exb ps={eps!r}')
nonv = collections.Counter(tok['dolgan'].get(r['pred_token_id'], {}).get('ps', '(missing)') for r in objs if r['pred_token_id'] and tok['dolgan'].get(r['pred_token_id'], {}).get('ps') not in VERB)
n_pred = sum(1 for r in objs if r['pred_token_id']); n_empty = len(objs) - n_pred
# (2) copula_next
b1 = [r for r in rd('data/derived/dolgan/b1_candidates.csv') if 'copula_next' in r['rules'].split()]
by_utt = collections.defaultdict(list)
for t in tok['dolgan'].values(): by_utt[t['utt_id']].append(t)
for r in rng.sample(b1, 5):
    tid = r['token_id']; uid, n = parse_tid(tid); bad = []
    ws, info = words_of('dolgan', uid)
    if ws is None: rec('b1 copula_next', tid, False, info); continue
    seq = sorted(by_utt[uid], key=lambda t: int(t['idx']))
    if [t['tx'].strip() for t in seq] != [w['tx'] for w in ws] or [t['ps'] for t in seq] != [w['ps'] for w in ws]: bad.append('tokens.csv order/tx/ps differs from .exb')
    after = ws[n:]; j = next((k for k, w in enumerate(after) if is_cop(w)), None)
    if j is None: bad.append('no copula/aux/be word after target'); note = ''
    else:
        between = [w['ps'] for w in after[:j] if w['ps'] == 'v']
        if between: bad.append(f'{len(between)} ps=v word(s) between target and copula')
        if after[j]['ge'] != r['next_verb']: bad.append(f"next_verb {r['next_verb']!r} != first copula gloss {after[j]['ge']!r}")
        note = f"copula at +{j + 1} (ps={after[j]['ps']}, stem gloss {stem(after[j]['ge'])!r}), ps=v between: {len(between)}"
    rec('b1 copula_next', tid, not bad, '; '.join(bad) or note)
# (3) Evenki PRF rules
ev = rd('data/derived/evenki/evid_candidates.csv')
for rule in ('evenki_PTCP_PRF', 'evenki_PRF'):
    pool = [r for r in ev if rule in r['rules'].split()]
    for r in rng.sample(pool, 3):
        tid = r['token_id']; w, info = word('evenki', tid); bad = []
        if w is None: rec(rule, tid, False, info); continue
        if w['tx'] != r['tx'].strip(): bad.append('tx differs from .exb')
        if w['ge'] != r['ge'].strip(): bad.append('ge differs from .exb')
        cs = [comps(m) for m in morphs(w['ge'])]
        ptcp_prf = any('PTCP' in c and 'PRF' in c for c in cs); prf = any('PRF' in c for c in cs)
        lab = [m for m in morphs(w['ge']) if 'PRF' in m]
        if rule == 'evenki_PTCP_PRF' and not ptcp_prf: bad.append('no morph with PTCP and PRF together')
        if rule == 'evenki_PRF' and (not prf or ptcp_prf): bad.append('PRF missing or participle present')
        rec(rule, tid, not bad, '; '.join(bad) or 'PRF morph gloss: ' + ', '.join(f'`{x}`' for x in lab))
P = print
P('# 006 step 5: spot checks\n')
P(f'Script: `handoff/outputs/006/scripts/spot_checks_006.py`, seed **{SEED}** (one `random.Random`, used in order: 5 copula_next rows, 3 evenki_PTCP_PRF, 3 evenki_PRF). Words re-derived from the .exb files.\n')
P('| Check | Token id | Result | Note |'); P('|---|---|---|---|')
for g, tid, ok, note in res: P(f"| {g} | `{tid}` | {'pass' if ok else ('n/a' if ok is None else 'FAIL')} | {note} |")
P('')
P(f'Dolgan objects: {len(objs)}; with pred_token_id {n_pred}, empty {n_empty}. pred_token_ids whose tokens.csv ps is not v/aux/cop: **{sum(nonv.values())}**' + (f' {dict(nonv)}' if nonv else '') + '.\n')
c = collections.Counter((g, ok) for g, _, ok, _ in res)
P('Summary: ' + '; '.join(f"{g}: {c[(g, True)]} pass, {c[(g, False)]} fail" for g in dict.fromkeys(g for g, *_ in res)) + '.')
print(f'run time {time.time() - T0:.1f} s', file=sys.stderr)
