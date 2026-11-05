import sys, os, collections, re, pickle
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    slots = collections.Counter(); misalign = collections.Counter(); forms = collections.defaultdict(collections.Counter)
    for rel, d in D.items():
        for r in W.words(d):
            mp, ge, mc, mb = r['mp'], r['ge'], r['mc'], r['mb']
            if not (mp and ge and mc and mp.strip()): continue
            mps, ges, mcs = W.morphs(mp.strip()), W.morphs(ge.strip()), mc.strip().split('-')
            if len(mps) != len(mcs): misalign['mc_vs_mp_differ'] += 1; 
            else: misalign['mc_vs_mp_equal'] += 1
            for i, m in enumerate(mps):
                if len(mcs) == len(mps): slots[mcs[i]] += 1
                if re.fullmatch(r'(?i)(bit|dak|bit.*|dak.*)', m) or re.search(r'(?i)^(BIt|DAK|BIT|dAK)$', m):
                    forms[m][(ges[i] if i < len(ges) else '?', mcs[i] if len(mcs) == len(mps) else '?')] += 1
    print('=====', c, dict(misalign))
    print(' mc slot names (top 60):', slots.most_common(60))
    print(' mp morphs that look like BIt/DAK:', {k: dict(v) for k, v in forms.items()})
