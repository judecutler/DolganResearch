"""Handoff 002, part A: tier coverage (Q7), morph/gloss alignment (Q6), gloss census (Q16)."""
import sys, os, csv, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
OUT = f'{W.HOME}/scratch/002/out'
OPT = ['SyF', 'SeR', 'IST', 'Top', 'Foc', 'BOR', 'BOR-Phon', 'BOR-Morph', 'CS', 'ExLocPoss']
LOWER = re.compile(r'[a-zа-яё]')
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    # ---------- Q7 coverage
    rows = []
    for rel, d in sorted(D.items()):
        tid = rel.split('/')[1]
        cats = collections.defaultdict(lambda: [0, 0, False])   # events, nonempty, present
        for t in d['tiers']:
            x = cats[t['category']]; x[2] = True; x[0] += len(t['events']); x[1] += sum(1 for e in t['events'] if e[4].strip())
        nw = sum(len(t['events']) for t in d['tiers'] if t['category'] == 'tx')
        row = {'text_id': tid, 'genre': d['genre'], 'n_speakers': len(d['speakers']), 'n_tx_events': nw}
        for k in OPT:
            row[k + '_present'] = int(cats[k][2]); row[k + '_nonempty_events'] = cats[k][1]
        rows.append(row)
    with open(f'{OUT}/tier_coverage_{c}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('=====', c, 'coverage rows', len(rows))
    for k in OPT:
        print(f'  {k:10s} present in {sum(r[k+"_present"] for r in rows):4d} texts | non-empty in {sum(1 for r in rows if r[k+"_nonempty_events"]>0):4d} texts | events {sum(r[k+"_nonempty_events"] for r in rows)}')
    # ---------- Q6 + Q16
    eq = collections.Counter(); mism = []; per_text = collections.defaultdict(collections.Counter)
    census = collections.Counter(); census_files = collections.defaultdict(set)
    atomic = collections.Counter()
    for rel, d in sorted(D.items()):
        tid = rel.split('/')[1]
        for r in W.words(d):
            mb, ge = r['mb'], r['ge']
            if mb is not None and ge is not None and mb.strip() and ge.strip():
                a, b = len(W.morphs(mb.strip())), len(W.morphs(ge.strip()))
                k = 'equal' if a == b else 'differ'
                eq[k] += 1; per_text[tid][k] += 1
                if a != b and len(mism) < 400: mism.append((tid, r['tx'].strip(), mb.strip(), r['mp'], ge.strip(), a, b))
            if ge and ge.strip():
                for g in W.morphs(ge.strip()):
                    census[g] += 1; census_files[g].add(tid)
                    typ = 'stem_or_word' if LOWER.search(g) else 'grammatical'
                    if typ == 'grammatical':
                        for p in re.split(r'[.\[\]/]', g):
                            if p: atomic[p] += 1
    print('  mb-vs-ge morph counts: equal', eq['equal'], 'differ', eq['differ'], 'ratio differ %.2f%%' % (100 * eq['differ'] / max(1, sum(eq.values()))))
    # a single text: the largest by words
    big = max(per_text.items(), key=lambda kv: sum(kv[1].values()))
    print('  single text', 'largest by aligned words:', big[0] if False else '(id withheld)', dict(big[1]))
    import pickle; pickle.dump({'mism': mism, 'per_text': dict(per_text)}, open(f'{OUT}/{c}_q6.pkl', 'wb'))
    with open(f'{OUT}/gloss_census_{c}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['label', 'type', 'count', 'n_texts'])
        items = sorted(census.items(), key=lambda kv: (LOWER.search(kv[0]) is not None, -kv[1], kv[0]))
        for g, n in items: w.writerow([g, 'stem_or_word' if LOWER.search(g) else 'grammatical', n, len(census_files[g])])
    n_gram = sum(1 for g in census if not LOWER.search(g)); n_stem = len(census) - n_gram
    print('  census: distinct labels', len(census), '| grammatical', n_gram, '| stem/word', n_stem, '| tokens', sum(census.values()))
    print('  size of census csv', os.path.getsize(f'{OUT}/gloss_census_{c}.csv'), 'bytes')
    print('  top 70 atomic grammatical labels:', atomic.most_common(70))
    pickle.dump({'atomic': atomic, 'census': census}, open(f'{OUT}/{c}_census.pkl', 'wb'))
