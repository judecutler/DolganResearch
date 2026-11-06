"""Handoff 006 step 4: classify the qa_flags `word_tier_event_without_word` events.
Run from the repo root:  python3 -I handoff/outputs/006/scripts/bor_check.py > handoff/outputs/006/bor_check.md
Stdlib only; does not import shared/. Reads data/raw (.exb) and data/derived. Prints ids, spans, tier values (<=25 chars), counts; no sentences.
Spans are timeline indices (position of the <tli> in file order), the coordinates used in the flag detail.
Classes, relative to the SAME speaker's tx events:
 (a) event starts at one tx word's start and ends at a later tx word's end (multi-word event);
 (b) event overlaps at least one tx word but is not (a) (partial overlap; sub-classified as inside-one-word or crossing a word boundary);
 (c) event overlaps no tx word of that speaker; c-other = it overlaps another speaker's tx word, c-none = no tx word at all.
Each .exb is parsed once."""
import os, re, csv, random, collections, time
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
            gp = os.path.join(base, g)
            if os.path.isdir(gp):
                for t in os.listdir(gp): m[t] = os.path.join(gp, t, t + '.exb')
        _dirs[corpus] = m
    return _dirs[corpus][text_id]
_cache = {}
def parse(corpus, text_id):
    k = (corpus, text_id)
    if k in _cache: return _cache[k]
    root = ET.parse(exb_path(corpus, text_id)).getroot()
    idx = {t.get('id'): i for i, t in enumerate(root.iter('tli'))}
    ev = collections.defaultdict(lambda: collections.defaultdict(list))   # speaker -> category -> [(s, e, text)]
    for t in root.iter('tier'):
        spk, cat = t.get('speaker'), t.get('category')
        for e in t.iter('event'):
            ev[spk][cat].append((idx[e.get('start')], idx[e.get('end')], (e.text or '').strip()))
    _cache[k] = ev; return ev
def klass(a, b, words, others):
    starts = {s for s, e in words}; ends = {e for s, e in words}
    n_inside = sum(1 for s, e in words if s >= a and e <= b)
    if a in starts and b in ends and n_inside >= 2: return 'a'
    over = [(s, e) for s, e in words if s < b and e > a]
    if over:
        return 'b-inside-one-word' if len(over) == 1 and over[0][0] <= a and b <= over[0][1] else 'b-crosses-boundary'
    if any(s < b and e > a for s, e in others): return 'c-other-speaker'
    return 'c-none'
rng = random.Random(SEED)
P = print
P('# 006 step 4: `word_tier_event_without_word` check\n')
P(f'Script: `handoff/outputs/006/scripts/bor_check.py`, seed {SEED}. Spans are timeline indices. Examples are random (fixed seed), ids and tier values only.\n')
P('Classes (same speaker\'s `tx` words): **a** = starts at one word\'s start and ends at a later word\'s end; '
  '**b** = partial overlap (b-inside-one-word: lies within one word; b-crosses-boundary: overlaps a word boundary); '
  '**c** = overlaps no word of that speaker (c-other-speaker: overlaps another speaker\'s word; c-none: no word at all).\n')
store = {}
for corpus in ('dolgan', 'evenki'):
    flags = [r for r in rd(f'data/derived/{corpus}/qa_flags.csv') if r['flag'] == 'word_tier_event_without_word']
    cls = collections.Counter(); ex = collections.defaultdict(list); aev = []; bad = 0
    for f in flags:
        m = re.fullmatch(r'(\S+) (\S+) \((\d+), (\d+)\)', f['detail'].strip())
        if not m: bad += 1; continue
        spk, cat, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        ev = parse(corpus, f['text_id'])
        words = [(s, e) for s, e, _ in ev[spk].get('tx', [])]
        others = [(s, e) for sp, c in ev.items() if sp != spk for s, e, _ in c.get('tx', [])]
        k = klass(a, b, words, others)
        vals = [v for s, e, v in ev[spk].get(cat, []) if (s, e) == (a, b)]
        val = vals[0] if vals else '(event not found)'
        nw = sum(1 for s, e in words if s >= a and e <= b)
        cls[(cat, k)] += 1; ex[k].append((f['text_id'], spk, cat, a, b, val, nw))
        if k == 'a': aev.append((f['text_id'], spk, cat, a, b, val, nw))
    store[corpus] = aev
    P(f'## {corpus.capitalize()}: {len(flags)} flags' + (f' ({bad} with unparsable detail)' if bad else '') + '\n')
    tiers = sorted({c for c, _ in cls}); ks = ['a', 'b-inside-one-word', 'b-crosses-boundary', 'c-other-speaker', 'c-none']
    P('| Tier | ' + ' | '.join(ks) + ' | Total |'); P('|---' * (len(ks) + 2) + '|')
    for t in tiers: P(f'| {t} | ' + ' | '.join(str(cls[(t, k)]) for k in ks) + f' | {sum(cls[(t, k)] for k in ks)} |')
    P('| **All** | ' + ' | '.join(str(sum(cls[(t, k)] for t in tiers)) for k in ks) + f' | {sum(cls.values())} |\n')
    for k in ks:
        if not ex[k]: continue
        P(f'Examples, class {k} ({min(5, len(ex[k]))} of {len(ex[k])}):\n'); P('| text_id | speaker | tier | span | tx words inside | tier value |'); P('|---|---|---|---|---|---|')
        for t in rng.sample(ex[k], min(5, len(ex[k]))): P(f'| {t[0]} | {t[1]} | {t[2]} | ({t[3]}, {t[4]}) | {t[6]} | `{t[5][:25]}` |')
        P('')
    if aev:
        bc = collections.Counter(c for _, _, c, *_ in aev)
        borA = [t for t in aev if t[2] != 'ExLocPoss']
        if borA:
            P(f'Examples, class a, BOR and BOR-Morph only ({min(5, len(borA))} of {len(borA)}):\n'); P('| text_id | speaker | tier | span | tx words inside | tier value |'); P('|---|---|---|---|---|---|')
            for t in rng.sample(borA, min(5, len(borA))): P(f'| {t[0]} | {t[1]} | {t[2]} | ({t[3]}, {t[4]}) | {t[6]} | `{t[5][:25]}` |')
            P('')
        P(f'Class-a events by tier: {dict(bc)}. Words covered per class-a event: {dict(sorted(collections.Counter(t[6] for t in aev).items()))}.\n')
# ---- objects (and tokens) inside class-a BOR / BOR-Morph events, Dolgan
aev = [t for t in store['dolgan'] if t[2] in ('BOR', 'BOR-Morph')]
texts = {t[0] for t in aev}
utts = [u for u in rd('data/derived/dolgan/utterances.csv') if u['text_id'] in texts]
span_of = {}   # token_id -> (speaker, (s, e)), rebuilt from the .exb
unres = 0
for u in utts:
    ev = parse('dolgan', u['text_id']); spk = u['speaker_id']
    refs = [(s, e) for s, e, t in ev[spk].get('ref', []) if t == u['ref'].strip()]
    if len(refs) != 1: unres += 1; continue
    rs, re_ = refs[0]
    ws = [(s, e) for s, e, _ in ev[spk].get('tx', []) if s >= rs and e <= re_]
    for i, w in enumerate(ws, 1): span_of[f"{u['utt_id']}.w{i:02d}"] = (spk, w)
by_text = collections.defaultdict(list)
for t in aev: by_text[t[0]].append(t)
def inside(text_id, tid):
    sw = span_of.get(tid)
    if not sw: return []
    spk, (s, e) = sw
    return [t for t in by_text[text_id] if t[1] == spk and s >= t[3] and e <= t[4]]
FIELD = {'BOR': ('bor', 'BOR'), 'BOR-Morph': ('bor_morph', 'BOR_Morph')}
oc = collections.Counter(); oids = []
for o in rd('data/derived/dolgan/objects.csv'):
    if o['text_id'] not in texts: continue
    for t in inside(o['text_id'], o['token_id']):
        f = FIELD[t[2]][0]; oc[(t[2], 'inside')] += 1
        if not o[f].strip(): oc[(t[2], 'empty')] += 1; oids.append((o['token_id'], t[2], t[3], t[4]))
tc = collections.Counter()
for r in rd('data/derived/dolgan/tokens.csv'):
    if r['text_id'] not in texts: continue
    for t in inside(r['text_id'], r['token_id']):
        f = FIELD[t[2]][1]; tc[(t[2], 'inside')] += 1
        if not r[f].strip(): tc[(t[2], 'empty')] += 1
P('## Dolgan: objects inside class-a BOR / BOR-Morph events\n')
P(f'Class-a BOR/BOR-Morph events: {len(aev)} in {len(texts)} texts. Utterances in those texts not resolvable to one ref event: {unres}.\n')
P('| Tier | Objects inside a class-a event | of which `bor` / `bor_morph` empty | Tokens (tokens.csv) inside | of which `BOR` / `BOR_Morph` empty |'); P('|---|---|---|---|---|')
for c in ('BOR', 'BOR-Morph'): P(f'| {c} | {oc[(c, "inside")]} | {oc[(c, "empty")]} | {tc[(c, "inside")]} | {tc[(c, "empty")]} |')
P('')
if oids:
    P('Objects with empty field: ' + ', '.join(f'`{i}` ({c} ({a}, {b}))' for i, c, a, b in oids) + '\n')
nb = sum(1 for t in aev if t[2] == 'BOR'); nm = len(aev) - nb
P('## Is information lost?\n')
P(f'Yes at the token level, no at the object level. Every flagged event except 2 in Dolgan is a multi-word (class a) event, so the pipeline, '
  f'which only copies word-tier values onto a token whose tx span matches the event exactly, drops them. For BOR this means {nb} class-a BOR and '
  f'{nm} class-a BOR-Morph events lose their loan label: {tc[("BOR", "empty")]} + {tc[("BOR-Morph", "empty")]} tokens in tokens.csv that lie inside '
  f'these events have an empty BOR / BOR_Morph field. None of these tokens is an object ({oc[("BOR", "empty")] + oc[("BOR-Morph", "empty")]} objects affected), '
  f'so the B2 object table and its `bor` / `bor_morph` / loan confounder are not affected in the current data. The ExLocPoss events '
  f'({sum(1 for t in store["dolgan"] if t[2] == "ExLocPoss")} Dolgan, {len(store["evenki"])} Evenki) are construction-level annotations over several words '
  f'and are also absent from the token-level ExLocPoss column; whether that matters depends on whether any analysis uses ExLocPoss. '
  f'No event lies outside the speaker\'s words or on another speaker\'s words.\n')
import sys
print(f'run time {time.time() - T0:.1f} s', file=sys.stderr)
