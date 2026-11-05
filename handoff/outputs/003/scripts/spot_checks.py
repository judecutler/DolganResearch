"""Handoff 003 step 4: independent spot checks of the derived tables against the .exb / .coma files.
Run from the repo root:  python3 -I handoff/outputs/003/scripts/spot_checks.py [--verbose]
Stdlib only. Reads data/derived and data/raw. Writes only ids and pass/fail to stdout (no corpus text),
except with --verbose, which also prints words for debugging (do not commit that output).
Does not import anything from shared/ or case_change/: everything is re-derived here."""
import sys, os, csv, re, random, bisect, collections
import xml.etree.ElementTree as ET
SEED = 20261105
VERBOSE = '--verbose' in sys.argv
ROOT = os.getcwd()
CASES = {'ACC': 'ACC', 'ACC.INDF': 'ACC', 'DAT/LOC': 'DAT/LOC', 'ABL': 'ABL', 'INSTR': 'INS', 'INS': 'INS', 'GEN': 'GEN', 'PART': 'PART',
         'COMP': 'COMP', 'ALL': 'ALL', 'LAT': 'LAT', 'PROL': 'PROL', 'VOC': 'VOC', 'COM1': 'COM', 'COM2': 'COM', 'COM3': 'COM', 'COM4': 'COM'}
def rd(path): return list(csv.DictReader(open(path, encoding='utf-8')))
_cache = {}
UREF = {c: {r['utt_id']: r['ref'].strip() for r in csv.DictReader(open(f'data/derived/{c}/utterances.csv', encoding='utf-8'))} for c in ('dolgan', 'evenki')}
def exb(corpus, text_id):
    key = (corpus, text_id)
    if key in _cache: return _cache[key]
    base = os.path.join(ROOT, 'data/raw', 'dolgan-2.0' if corpus == 'dolgan' else 'evenki-2.0')
    g = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)) and os.path.isdir(os.path.join(base, d, text_id))][0]
    root = ET.parse(os.path.join(base, g, text_id, text_id + '.exb')).getroot()
    idx = {t.get('id'): i for i, t in enumerate(root.iter('tli'))}
    tiers = collections.defaultdict(lambda: collections.defaultdict(list))   # speaker -> category -> events
    for t in root.iter('tier'):
        for e in t.iter('event'):
            tiers[t.get('speaker')][t.get('category')].append((idx.get(e.get('start'), -1), idx.get(e.get('end'), -1), e.text or ''))
    utts = collections.defaultdict(list)   # full ref label (as in the .exb ref tier) -> [(speaker, span, text)]
    for spk, cats in tiers.items():
        for s, e, txt in cats.get('ref', []):
            utts[txt.strip()].append((spk, (s, e), txt))
    _cache[key] = (tiers, utts); return _cache[key]
def words_of(corpus, text_id, utt_no):
    """return list of dict(span, speaker, tx, mb, mp, ge, ps, SyF, IST) for utterance number utt_no"""
    tiers, utts = exb(corpus, text_id)
    ref = UREF[corpus].get(f'{text_id}#{utt_no:03d}')
    hits = utts.get(ref, []) if ref else []
    if len(hits) != 1: return None, f'{len(hits)} ref events match utterance {utt_no}'
    spk, (rs, re_), _ = hits[0]
    cats = tiers[spk]
    look = {c: {(s, e): t for s, e, t in evs} for c, evs in cats.items()}
    out = []
    for s, e, tx in cats.get('tx', []):
        if s >= rs and e <= re_:
            w = {'span': (s, e), 'speaker': spk, 'tx': tx.strip()}
            for c in ('mb', 'mp', 'ge', 'ps', 'SyF', 'IST'): w[c] = (look.get(c, {}).get((s, e)) or '').strip()
            out.append(w)
    return out, spk
def parse_tid(tid):
    m = re.fullmatch(r'(.+)#(\d+)\.w(\d+)', tid); return m.group(1), int(m.group(2)), int(m.group(3))
def morphs(x): return re.split(r'[-=]', x) if x else []
def my_case(ge):
    if not ge: return ''
    if re.search(r'\.\[NOM\]$', ge): return 'NOM'
    for g in reversed(morphs(ge)):
        for part in [g] + g.split('.'):
            if part in CASES: return CASES[part]
        if re.search(r'(^|\.)ACC(\.|$)', g): return 'ACC'
    return ''
results = []
def rec(group, tid, ok, note=''): results.append((group, tid, ok, note))
rng = random.Random(SEED)
toks = {c: {r['token_id']: r for r in rd(f'data/derived/{c}/tokens.csv')} for c in ('dolgan', 'evenki')}
def my_word(corpus, tid):
    text, u, w = parse_tid(tid); ws, spk = words_of(corpus, text, u)
    if ws is None or not (1 <= w <= len(ws)): return None, spk
    return ws[w - 1], spk
# ---- (1) objects: 10 Dolgan rows
obj = rd('data/derived/dolgan/objects.csv'); pick = rng.sample(obj, 10)
for r in pick:
    tid = r['token_id']; t = toks['dolgan'][tid]; w, spk = my_word('dolgan', tid)
    if w is None: rec('objects', tid, False, 'word not found in .exb: ' + str(spk)); continue
    bad = []
    if w['tx'] != t['tx'].strip(): bad.append('tx differs')
    if w['ge'] != t['ge'].strip(): bad.append('ge differs')
    if w['SyF'] != t['SyF'].strip(): bad.append('SyF differs')
    if r['syf'] not in w['SyF'].split(' ') and r['syf'] not in w['SyF']: bad.append('objects.syf not in .exb SyF')
    if not re.search(r':O$', r['syf'].strip()) : bad.append('syf does not end :O')
    if w['speaker'] != r['speaker_id'] or w['speaker'] != t['speaker_id']: bad.append('speaker differs')
    if my_case(w['ge']) != (r['case'] or '') : bad.append(f"case: pipeline '{r['case']}' vs mine '{my_case(w['ge'])}' (ge labels only: {[m for m in morphs(w['ge']) if m.isupper() or '.' in m][:4] if True else ''})")
    note = ''
    if r['pred_token_id']:
        ptext, pu, pw = parse_tid(r['pred_token_id']); pw_ = my_word('dolgan', r['pred_token_id'])[0]
        if ptext != parse_tid(tid)[0] or pu != parse_tid(tid)[1]: bad.append('pred not in same utterance')
        elif pw_ is None: bad.append('pred word not found')
        else:
            if pw_['ps'] == 'v': note = 'pred ps=v'
            elif pw_['ps'] in ('cop', 'aux'): note = f"pred ps={pw_['ps']} (copula/auxiliary, not a lexical verb)"
            else: bad.append(f"pred ps={pw_['ps']!r} is not a verb")
    else:
        ws, _ = words_of('dolgan', *parse_tid(tid)[:2]); has = [x for x in ws if x['ps'] in ('v', 'cop', 'aux')]
        if has: bad.append('pred empty but utterance has a verb/cop/aux word')
        else: note = 'no predicate, and none in utterance'
    rec('objects', tid, not bad, '; '.join(bad) or note)
# ---- (2) evid candidates: 5 tier-1 + 5 tier-2 Dolgan, 3 Evenki
def rule_ok(rule, w, tx_parts):
    mps = morphs(w['mp']); ges = ' '.join(morphs(w['ge']))
    if rule == 'ge_EVID': return 'EVID' in w['ge']
    if rule == 'ge_INFER': return 'INFER' in w['ge']
    if rule == 'IST_quot': return 'quot' in w['IST']
    if rule == 'mp_BIT': return 'BIT' in mps
    if rule == 'mp_TAK_not_INFER': return 'TAK' in mps and 'INFER' not in w['ge']
    if rule == 'copula_BIT': return 'BIT' in mps and w['ps'] == 'cop'
    if rule == 'particle_buollaga': return w['mp'].startswith('bu͡ollag')
    if rule == 'evenki_PRF': return any(re.fullmatch(r'PRF(\d)?', c) for g in morphs(w['ge']) for c in g.split('.'))
    return None
def check_evid(corpus, rows, group):
    for r in rows:
        tid = r['token_id']; w, spk = my_word(corpus, tid)
        if w is None: rec(group, tid, False, 'word not found: ' + str(spk)); continue
        bad = []
        if w['tx'] != r['tx'].strip(): bad.append('tx differs')
        if w['ge'] != r['ge'].strip(): bad.append('ge differs')
        if w['speaker'] != r['speaker_id']: bad.append('speaker differs')
        for rule in r['rules'].split():
            ok = rule_ok(rule, w, None)
            if ok is None: bad.append(f'unknown rule {rule}')
            elif not ok: bad.append(f'rule {rule} not satisfied by the .exb word')
        if r['target_morph'] and r['target_morph'] not in morphs(w['mp']): bad.append('target_morph not in mp')
        ws, _ = words_of(corpus, *parse_tid(tid)[:2]); mine = ' '.join(x['tx'] for x in ws)
        ctx = re.sub(r'\s+', ' ', r['context'].replace('[[', '').replace(']]', '')).strip()
        if ctx != re.sub(r'\s+', ' ', mine).strip(): bad.append('context is not the utterance text')
        if '[[' + w['tx'] + ']]' not in r['context']: bad.append('target not marked in context')
        rec(group, tid, not bad, '; '.join(bad) or 'rules: ' + r['rules'])
ev = rd('data/derived/dolgan/evid_candidates.csv')
check_evid('dolgan', rng.sample([r for r in ev if r['tier'] == '1'], 5), 'evid tier 1 (Dolgan)')
check_evid('dolgan', rng.sample([r for r in ev if r['tier'] == '2'], 5), 'evid tier 2 (Dolgan)')
check_evid('evenki', rng.sample(rd('data/derived/evenki/evid_candidates.csv'), 3), 'evid (Evenki)')
# ---- (3) b1 candidates: 5 random Dolgan rows
b1 = rd('data/derived/dolgan/b1_candidates.csv')
for r in rng.sample(b1, 5):
    tid = r['token_id']; w, spk = my_word('dolgan', tid)
    if w is None: rec('b1', tid, False, 'word not found: ' + str(spk)); continue
    bad = []
    if w['tx'] != r['tx'].strip(): bad.append('tx differs')
    if w['ge'] and my_case(w['ge']) != r['case']: bad.append(f"case: pipeline '{r['case']}' vs mine '{my_case(w['ge'])}'")
    ws, _ = words_of('dolgan', *parse_tid(tid)[:2]); i = parse_tid(tid)[2]
    after = ws[i:]; nxt = [x for x in after if x['ps'] in ('cop', 'aux')]; lexv_between = []
    note = 'rules: ' + r['rules']
    if r['next_verb']:
        mine = nxt[0]['ge'] if nxt else ''
        if mine != r['next_verb']: bad.append('next_verb differs from the next cop/aux word in the utterance')
        else: note += '; next_verb = next cop/aux word, %d word(s) after the target, %d lexical verb(s) in between' % (ws.index(nxt[0]) + 1 - i, sum(1 for x in ws[i:ws.index(nxt[0])] if x['ps'] == 'v'))
    else:
        note += '; next_verb empty'
        if 'copula_next' in r['rules'].split(): bad.append('rule copula_next but next_verb empty')
    rec('b1', tid, not bad, '; '.join(bad) or note)
# ---- (4) multi-speaker text: 5 utterances
texts = rd('data/derived/dolgan/texts.csv')
cols = list(texts[0].keys()); ncol = 'n_speakers'
multi = [t for t in texts if t[ncol].isdigit() and int(t[ncol]) > 1]
ttext = rng.choice(multi)['text_id']
utts_csv = [u for u in rd('data/derived/dolgan/utterances.csv') if u['text_id'] == ttext]
by_utt = collections.defaultdict(list)
for t in toks['dolgan'].values():
    if t['text_id'] == ttext: by_utt[t['utt_id']].append(t)
for u in rng.sample(utts_csv, 5):
    uid = u['utt_id']; num = int(uid.split('#')[1]); ws, spk = words_of('dolgan', ttext, num)
    mine = ws if ws is not None else []
    got = sorted(by_utt[uid], key=lambda t: int(t['idx']))
    bad = []
    if ws is None: bad.append(str(spk))
    else:
        if len(got) != len(mine): bad.append(f'word count: pipeline {len(got)} vs .exb {len(mine)}')
        if any(t['speaker_id'] != spk for t in got): bad.append('a word has a different speaker than the utterance')
        if u['speaker_id'] != spk: bad.append('utterance speaker differs')
        if [t['tx'].strip() for t in got] != [x['tx'] for x in mine]: bad.append('word order or text differs')
    rec('multi-speaker utterances', uid, not bad, '; '.join(bad) or f'{len(mine)} words, speaker {spk}')
multi_text_note = ttext
# ---- (5) speakers: 5 rows with in_coma = 1
def coma_dob(corpus, sid):
    path = os.path.join(ROOT, 'data/raw', 'dolgan-2.0/dolgan.coma' if corpus == 'dolgan' else 'evenki-2.0/evenki.coma')
    root = ET.parse(path).getroot()
    for s in root.iter('Speaker'):
        if (s.findtext('Sigle') or '').strip() == sid:
            for k in s.iter('Key'):
                if k.get('Name') == '4 Date of birth': return (k.text or '').strip()
sp = [r for r in rd('data/derived/dolgan/speakers.csv') if r['in_coma'] == '1']
for r in rng.sample(sp, 5):
    raw = coma_dob('dolgan', r['speaker_id']); lo = hi = ''
    m = re.fullmatch(r'(\d{4})', raw); m2 = re.fullmatch(r'(\d{4})/(\d{4})', raw); m3 = re.fullmatch(r'(\d{4})\.\d\d\.\d\d\.?', raw); m4 = re.fullmatch(r'(\d{3})0s(?: \(\?\))?', raw)
    if m: lo = hi = m.group(1)
    elif m2: lo, hi = m2.group(1), m2.group(2)
    elif m3: lo = hi = m3.group(1)
    elif m4: lo, hi = m4.group(1) + '0', m4.group(1) + '9'
    fmt = re.sub(r'\d', 'D', raw)
    ok = (str(r['birth_lo']) == lo and str(r['birth_hi']) == hi)
    rec('speakers', r['speaker_id'], ok, f"coma format {fmt!r}; pipeline {r['birth_lo'] or '-'}..{r['birth_hi'] or '-'}; mine {lo or '-'}..{hi or '-'}")
# ---- report
print(f'seed {SEED}; multi-speaker text used: {multi_text_note}')
tot = collections.Counter()
for g, tid, ok, note in results:
    tot[(g, ok)] += 1
print('\n| Group | Checked | Pass | Fail |\n|---|---|---|---|')
groups = list(dict.fromkeys(g for g, *_ in results))
for g in groups: print(f"| {g} | {tot[(g, True)] + tot[(g, False)]} | {tot[(g, True)]} | {tot[(g, False)]} |")
print('\n| Group | Id | Result | Note |\n|---|---|---|---|')
for g, tid, ok, note in results: print(f"| {g} | `{tid}` | {'pass' if ok else 'FAIL'} | {note} |")
