import sys, os, re, collections, pickle, json, csv
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W, coma_lib
OUT = f'{W.HOME}/scratch/002/out'
def tx_ok(tx): return not any(ch.isupper() for ch in tx) and len(tx.strip()) < 30
def fe_ok(fe):
    if not fe: return False
    body = fe.strip()[1:]
    return not re.search(r'\b[A-ZА-ЯЁ][a-zа-яё]+', body.replace(' I ', ' ')) and len(body) < 90
CASES = {'ACC','DAT','LOC','ABL','ALL','LAT','INS','INSTR','COM','PROL','GEN','PART','COMP','VOC'}
res = {}
# ---------- Q17: case counts at morph-label level
REQ = ['NOM','ACC','ACC.INDEF','ACC.INDF','PART','DAT','DAT/LOC','LOC','ABL','ALL','LAT','INSTR','INS','COM','PROL','GEN','COMP']
for c in ('dolgan','evenki'):
    cen = pickle.load(open(f'{OUT}/{c}_census.pkl','rb'))['census']
    t = {}
    for lab in REQ: t[lab] = cen.get(lab, 0)
    zero_nom = sum(n for g, n in cen.items() if g.endswith('.[NOM]') or g == '[NOM]')
    # numbered variants
    var = {k: sum(n for g, n in cen.items() if re.fullmatch(k + r'\d+', g)) for k in ('COM','LAT','ABL','ALL','INS','PROL','GEN','ACC')}
    comb = {k: sum(n for g, n in cen.items() if g != k and re.search(r'(?<![A-Z0-9])' + k + r'(?![A-Z0-9])', g) and not g.endswith('.[NOM]')) for k in ('ACC','DAT/LOC','LAT','ABL','COM')}
    print('##', c, 'Q17 exact-label counts:', {k: v for k, v in t.items()}, '| zero NOM ".[NOM]" (labels ending in it):', zero_nom, '| numbered variants:', {k: v for k, v in var.items() if v}, '| inside longer labels (e.g. PRO.1SG.ACC):', comb)
# ---------- Q19 improved
for c in ('dolgan','evenki'):
    D = W.load(c); obj = collections.Counter(); ex = []
    for rel, d in sorted(D.items()):
        tid = rel.split('/')[1]
        for r in W.words(d):
            sy = (r['SyF'] or '').strip()
            if not sy.endswith(':O'): continue
            ge = (r['ge'] or '').strip(); obj['O words'] += 1
            if not ge: obj['no ge'] += 1; continue
            labs = W.morphs(ge); last = labs[-1]
            comps = set(re.split(r'[.\[\]/]', ' '.join(labs).replace(' ', '.')))
            if re.search(r'\.\[NOM\]$', ge): k = 'zero-marked nominative (ge ends .[NOM])'
            elif 'ACC' in comps: k = 'accusative (ACC, ACC.INDF or inside a PRO label)'
            elif comps & (CASES - {'ACC'}): k = 'other explicit case (' + ','.join(sorted(comps & CASES)) + ')'
            elif last.startswith('RFL'): k = 'reflexive-possessive suffix, no case label'
            else: k = 'no case label (other)'
            obj[k] += 1
            if k.startswith('zero') and tx_ok(r['tx']) and len(ex) < 40: ex.append((tid, r['tx'].strip(), r['mb'], r['mp'], ge, r['mc'], sy))
    print('##', c, 'Q19', dict(obj))
    seen=set(); pick=[]
    for x in ex:
        if x[1] in seen: continue
        seen.add(x[1]); pick.append(x)
        if len(pick)==5: break
    res[c+'_zero_nom_obj']=pick
# ---------- Q13/Q14 from coma (Dolgan)
sp, co = coma_lib.load(f'{W.HOME}/scratch/x/d/dolgan.coma')
D = W.load('dolgan'); names = {rel.split('/')[1]: rel for rel in D}
cls = collections.Counter()
for n, v in co.items():
    if n not in names: continue
    pub = v.get('2 Published in','') not in ('','...'); arch = v.get('1a Archive (sound)','')
    tdnt = 'TDNT' in arch; yr = v.get('2b Date of recording','')[:4]
    yb = 'year<=1999' if yr.isdigit() and int(yr) <= 1999 else ('2000-2006' if yr.isdigit() and int(yr) <= 2006 else ('2007-2010' if yr.isdigit() and int(yr) <= 2010 else ('2017' if yr=='2017' else 'other')))
    cls[('published-in value' if pub else 'no Published-in') , ('archive=TDNT' if tdnt else 'archive other/blank'), yb] += 1
print('## Q13 dolgan (exb-bearing 136) combos [Published in?, Archive, rec-year bucket]:'); [print('   ', k, n) for k, n in sorted(cls.items(), key=lambda x: -x[1])]
an_txt = [n for n, v in co.items() if v.get('3 Dialect') == 'Anabar']
an_sp = [s for s, v in sp.items() if v.get('2 Dialect') == 'Anabar']
inexb = set(); [inexb.update(d['speakers']) for d in D.values()]
print('## Q14 Anabar texts:', an_txt, '| in exb:', [n in names for n in an_txt], '| Anabar speakers (ids):', an_sp, '| of those present in an .exb:', [s in inexb for s in an_sp])
# Evenki Q15
spE, coE = coma_lib.load(f'{W.HOME}/scratch/x/e/evenki.coma')
print('## Q15 evenki: speakers', len(spE), '| DOB "...":', sum(1 for v in spE.values() if v.get('4 Date of birth')=='...'), '| sex unknown:', sum(1 for v in spE.values() if v['_sex']=='unknown'))
# fix excerpts
ex = json.load(open(f'{OUT}/excerpts.json'))
ex.update(res)
json.dump(ex, open(f'{OUT}/excerpts.json','w'), ensure_ascii=False, indent=1)
