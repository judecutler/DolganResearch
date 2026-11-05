import sys, pickle, collections, os
home = os.environ['HOME']
for c in ('dolgan', 'evenki'):
    D = pickle.load(open(f'{home}/scratch/002/{c}.pkl', 'rb'))['data']
    print('=========', c, len(D), 'files')
    cat_files = collections.Counter(); cat_type = collections.defaultdict(collections.Counter)
    per_file_tiers = collections.Counter()
    spk_tiers = collections.Counter()
    for rel, d in D.items():
        cats = set()
        for t in d['tiers']:
            cats.add(t['category']); cat_type[t['category']][t['type']] += 1
        for k in cats: cat_files[k] += 1
        per_file_tiers[len(d['tiers'])] += 1
        spk_tiers[len(d['speakers'])] += 1
        # is display-name == category-SPK ?
    print('categories (files containing it) / types:')
    for k, n in sorted(cat_files.items(), key=lambda x: -x[1]):
        print(f'  {k:12s} {n:4d}  types={dict(cat_type[k])}')
    print('speakers per file distribution:', dict(sorted(spk_tiers.items())))
    # tiers with no speaker attribute?
    nos = sum(1 for d in D.values() for t in d['tiers'] if not t['speaker'])
    print('tiers without speaker attr:', nos)
    # display-name pattern check
    bad = collections.Counter()
    for d in D.values():
        for t in d['tiers']:
            if t['display'] != f"{t['category']}-{t['speaker']}": bad[(t['category'], t['display'] == t['id'])] += 1
    print('display != category-speaker:', dict(bad) if bad else 'none')
    # per genre one file: tiers list for the first file of each genre
    gen = {}
    for rel, d in D.items(): gen.setdefault(d['genre'], rel)
    for g, rel in sorted(gen.items()):
        d = D[rel]; sp = d['speakers'][0]
        print(' genre', g, '| tiers for first speaker:', [(t['category'], t['type']) for t in d['tiers'] if t['speaker'] == sp])
