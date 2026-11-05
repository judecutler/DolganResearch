import sys, os, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import coma_lib
home = os.environ['HOME']
def pat(v): return re.sub(r'[A-Za-zА-Яа-я]', 'a', re.sub(r'\d', 'd', v)) if v else '(empty)'
for c, f in (('dolgan', 'd/dolgan.coma'), ('evenki', 'e/evenki.coma')):
    sp, co = coma_lib.load(f'{home}/scratch/x/{f}')
    print('=====', c, 'speakers', len(sp), 'communications', len(co))
    print('known/sex/pseudo samples:', collections.Counter(v['_known'] for v in sp.values()), collections.Counter(v['_sex'] for v in sp.values()))
    dob = [v.get('4 Date of birth', '') for v in sp.values()]
    print('DOB non-empty:', sum(1 for x in dob if x), 'of', len(dob))
    print('DOB patterns:', collections.Counter(pat(x) for x in dob).most_common())
    print('DOB non-numeric examples (textual):', sorted(set(x for x in dob if x and re.search(r'[^\d\-./]', x)))[:15])
    dod = [v.get('5 Date of death', '') for v in sp.values()]
    print('DOD non-empty', sum(1 for x in dod if x))
    print('speaker-level region/dialect/country/L1:')
    for k in ('2 Region', '3 Country', '2 Dialect', '3 Dialect', '2 Dialectal group', '1 First language'):
        vals = [v.get(k) for v in sp.values() if k in v]
        if vals: print('  ', k, collections.Counter(vals).most_common(10))
    print('COMMUNICATION fields:')
    for k in ('1 Genre', '3 Dialect', '3a Dialectal group', '3b Dialect', 'Region', 'Country', '2 Source type', '6 Has audio', '1a Archive (sound)', '1a Archive'):
        vals = [v.get(k) for v in co.values() if k in v]
        if vals: print('  ', k, len(vals), 'with value', sum(1 for x in vals if x), collections.Counter(vals).most_common(14))
    for k in ('2b Date of recording',):
        vals = [v.get(k, '') for v in co.values()]
        print('  ', k, 'non-empty', sum(1 for x in vals if x), 'of', len(vals), 'patterns', collections.Counter(pat(x) for x in vals).most_common())
    pubs = [v.get('2 Published in', v.get('3a Published in', '')) for v in co.values()]
    print('  Published in: non-empty', sum(1 for x in pubs if x), 'distinct', len(set(pubs)), collections.Counter(pubs).most_common(6))
