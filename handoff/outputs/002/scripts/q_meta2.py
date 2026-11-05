import sys, os, re, collections, pickle
sys.path.insert(0, os.path.dirname(__file__))
import coma_lib
home = os.environ['HOME']
def fmt(v):
    if not v: return '(empty)'
    return re.sub(r'\d', 'D', v)
for c, f, pk in (('dolgan', 'd/dolgan.coma', 'dolgan'), ('evenki', 'e/evenki.coma', 'evenki')):
    sp, co = coma_lib.load(f'{home}/scratch/x/{f}')
    D = pickle.load(open(f'{home}/scratch/002/{pk}.pkl', 'rb'))['data']
    names = {os.path.dirname(rel).split('/')[-1]: rel for rel in D}
    with_exb = {n: v for n, v in co.items() if n in names}
    print('=====', c, 'coma communications', len(co), '| with an .exb folder:', len(with_exb), '| without:', len(co) - len(with_exb), '| exb folders not in coma:', len([n for n in names if n not in co]))
    # speakers
    in_exb = set(); tx_spk = set(); nonempty_tx = collections.Counter()
    for rel, d in D.items():
        in_exb.update(d['speakers'])
        for t in d['tiers']:
            if t['category'] == 'tx' and any(e[4].strip() for e in t['events']): tx_spk.add(t['speaker'])
    print('speaker ids: coma', len(sp), '| in .exb speakertables', len(in_exb), '| with non-empty tx tier', len(tx_spk), '| ids in exb but not in coma:', len(in_exb - set(sp)), '| coma speakers not in any exb:', len(set(sp) - in_exb))
    # speakers listed in "4 Speakers" of communications with exb
    listed = set()
    for n, v in with_exb.items():
        for s in re.split(r'[,;]\s*', v.get('4 Speakers', '')):
            if s: listed.add(s)
    print('distinct values in "4 Speakers" of exb-bearing communications:', len(listed), 'sample format:', list(listed)[:3])
    # DOB formats for speakers in exb (ids)
    for label, ids in (('all coma speakers', set(sp)), ('speakers in .exb', in_exb & set(sp))):
        dob = [sp[i].get('4 Date of birth', '') for i in ids]
        print(f'DOB [{label}] n={len(dob)}: with a value (not empty and not "..."):', sum(1 for x in dob if x and x != '...'), '| unknown ("..."):', sum(1 for x in dob if x == '...'), '| empty:', sum(1 for x in dob if not x))
        print('   formats:', collections.Counter(fmt(x) for x in dob).most_common())
    print('textual DOB values (non-digit text):', sorted(set(sp[i].get('4 Date of birth', '') for i in sp if re.search(r'[A-Za-z]|\(', sp[i].get('4 Date of birth', '')))))
    # communications: with exb
    for k in ('2b Date of recording', '1 Genre', '3 Dialect', '3a Dialectal group', '3b Dialect'):
        vals = [v.get(k) for v in with_exb.values() if k in v]
        if not vals: continue
        if k.startswith('2b'):
            print(f'[{k}] among exb-bearing: n={len(vals)}, formats', collections.Counter(fmt(x) for x in vals).most_common())
            yrs = collections.Counter(x[:4] for x in vals if re.match(r'\d{4}', x)); print('   by first 4 digits:', sorted(yrs.items()))
        else:
            print(f'[{k}] among exb-bearing: n={len(vals)} with value (not "..."): {sum(1 for x in vals if x and x != "...")}', collections.Counter(vals).most_common())
    # Anabar anywhere
    hits = []
    for n, v in co.items():
        for k, x in v.items():
            if isinstance(x, str) and re.search('anabar', x, re.I): hits.append((n in names, k, x[:60]))
    sp_hits = [(k, x[:60]) for v in sp.values() for k, x in v.items() if isinstance(x, str) and re.search('anabar', x, re.I)]
    print('Anabar mentions in communications (has_exb, field, value):', collections.Counter((h[0], h[1], h[2]) for h in hits).most_common(8))
    print('Anabar mentions in speaker records (field, value):', collections.Counter(sp_hits).most_common(8))
    # coma-reported counts
    for key in ('# HIAT:w', '# HIAT:u', '# INEL:w', '# INEL:u', '# e', '# sc', '# HIAT:ip', '# INEL:ip'):
        vs = []
        for v in with_exb.values():
            if key in v and re.fullmatch(r'\d+', v[key]): vs.append(int(v[key]))
        if vs: print(f'coma sum of "{key}" over {len(vs)} exb-bearing communications:', sum(vs))
