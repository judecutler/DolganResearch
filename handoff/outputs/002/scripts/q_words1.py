import sys, os, collections, re
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    chars = {t: collections.Counter() for t in ('mb', 'mp', 'ge')}
    tot = collections.Counter(); ex = {}
    for rel, d in D.items():
        for r in W.words(d):
            tot['tx_words'] += 1
            for t in ('mb', 'mp', 'ge'):
                v = r[t]
                if v is None: continue
                for ch in v:
                    if not ch.isalnum(): chars[t][ch] += 1
            for t in ('mb','mp','ge','mc','ps'):
                if r[t] is None: tot['no_'+t] += 1
                elif not r[t].strip(): tot['empty_'+t] += 1
            if r['ref'] is None: tot['no_utterance'] += 1
    print('=====', c, dict(tot))
    for t in ('mb', 'mp', 'ge'): print(' ', t, 'non-alphanumeric characters:', chars[t].most_common(25))
