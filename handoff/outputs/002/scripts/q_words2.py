import sys, os, collections, re
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    nomb = collections.Counter(); ex = collections.defaultdict(list); pct = collections.Counter()
    for rel, d in D.items():
        for r in W.words(d):
            tx = r['tx'].strip()
            if r['mb'] is None: nomb[re.sub(r'\w', 'w', tx)[:12]] += 1; 
            ge = r['ge'] or ''
            if '%' in ge: pct[ge if len(ge) < 12 else 'long:' + re.sub(r'[^%\-. ]', 'x', ge)[:20]] += 1
            def keep(key, cond):
                if cond and len(ex[key]) < 3 and not re.search(r'[A-ZА-Я][a-zа-я]+', r['tx']): ex[key].append((rel.split('/')[0], r['tx'].strip(), r['mb'], r['mp'], r['ge']))
            mb = r['mb'] or ''; mp = r['mp'] or ''
            keep('clitic=', '=' in mb)
            keep('zero[]in_mp', '[' in mp)
            keep('colon_in_mb', ':' in mb)
            keep('slash_in_ge', '/' in ge)
            keep('pct_in_ge', '%' in ge)
            keep('underscore_ge', '_' in ge)
    print('=====', c)
    print(' tx of words with no mb (shape: w=letter):', nomb.most_common(8))
    print(' ge values containing %:', pct.most_common(10))
    for k, v in ex.items():
        print(' ', k)
        for x in v: print('    ', x)
