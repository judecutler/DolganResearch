"""Handoff 002 part B1: EVID/INFER (Q18), tense/mood slots (Q18), SyF/SeR (Q9,Q10), objects (Q19)."""
import sys, os, csv, re, collections, pickle
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
LOCAL = f'{W.HOME}/mnt/DolganResearch/data/derived/002'   # git-ignored, local only
CASE_EXPL = re.compile(r'^(ACC(\.INDF|\.INDEF)?|DAT/LOC|DAT|LOC|ABL\d?|ALL|LAT\d?|INSTR|INS|COM\d?|PROL|GEN|PART|COMP|VOC)$')
def has_name(tx): return bool(re.search(r'[A-ZА-ЯЁ]', tx.strip()[:1])) or bool(re.search(r'\s[A-ZА-ЯЁ]', ' ' + tx.strip()))
SAFE = lambda r: not has_name(r['tx']) and not (r['fe'] and re.search(r'\b[A-Z][a-z]+', (r['fe'] or '')[1:]) and False)
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    ev_rows = []; slot_lab = collections.defaultdict(collections.Counter); slot_ex = collections.defaultdict(lambda: collections.defaultdict(list))
    evid_mp = collections.Counter()
    syf = collections.Counter(); syf_ex = {'O': [], 'S': []}; ser_roles = collections.Counter(); ser_forms = collections.Counter(); st_ex = []
    obj = collections.Counter(); obj_ex = []
    n_syf_word = 0
    for rel, d in sorted(D.items()):
        tid = rel.split('/')[1]
        # SyF / SeR from all events
        for t in d['tiers']:
            if t['category'] == 'SeR':
                for e in t['events']:
                    v = e[4].strip()
                    if not v: continue
                    form, _, role = v.rpartition(':')
                    if not form: form, role = v, '(no colon)'
                    ser_roles[role] += 1; ser_forms[form] += 1
            if t['category'] == 'SyF':
                for e in t['events']:
                    if e[4].strip(): syf[e[4].strip().rsplit(':', 1)[-1]] += 1
        for r in W.words(d):
            mb, mp, ge, mc = r['mb'], r['mp'], r['ge'], r['mc']
            # --- EVID / INFER
            if ge and re.search(r'EVID|INFER', ge):
                ev_rows.append([tid, r['spk'], r['tx'].strip(), mb, mp, ge, mc, r['fe']])
                if mp and ge:
                    mps, ges = W.morphs(mp.strip()), W.morphs(ge.strip())
                    if len(mps) == len(ges):
                        for m, g in zip(mps, ges):
                            if re.search(r'EVID|INFER', g): evid_mp[(m, g)] += 1
            # --- tense/mood slots through mc (only where mc aligns with mp)
            if mp and ge and mc and mp.strip():
                mps, ges, mcs, mbs = W.morphs(mp.strip()), W.morphs(ge.strip()), mc.strip().split('-'), W.morphs((mb or '').strip())
                if len(mps) == len(mcs) == len(ges):
                    for i, s in enumerate(mcs):
                        base = s.replace('[', '').replace(']', '')
                        if re.search(r'(tense|mood)', base) and not base.startswith('v:(') and '(' not in base:
                            slot = base.split('.')[0]
                            lab = ges[i]; slot_lab[slot][lab] += 1
                            if len(slot_ex[slot][lab]) < 3 and SAFE(r) and i < len(mbs): slot_ex[slot][lab].append(mbs[i] + ' / ' + mps[i])
            # --- SyF O/S word-aligned and SeR St
            sy = (r['SyF'] or '').strip()
            if sy:
                n_syf_word += 1
                last = sy.rsplit(':', 1)[-1]
                for k in ('O', 'S'):
                    if sy.endswith(':' + k) and len(syf_ex[k]) < 60 and SAFE(r): syf_ex[k].append((tid, r['tx'].strip(), mb, ge, mc, sy))
                if sy.endswith(':O'):
                    labs = W.morphs((ge or '').strip())
                    expl = [g for g in labs if CASE_EXPL.match(g.split('.[')[0])] if ge else []
                    zero_nom = bool(ge and re.search(r'\.\[NOM\]$', ge.strip()))
                    k = 'O_word'; obj[k] += 1
                    kind = 'explicit_case:' + (re.sub(r'\d', '', expl[-1]) if expl else '') if expl and not zero_nom else ('zero_NOM_bracket' if zero_nom else ('no_ge' if not ge else 'other_no_case_label'))
                    obj[kind] += 1
                    if (zero_nom or kind == 'other_no_case_label') and len(obj_ex) < 80 and SAFE(r): obj_ex.append((tid, r['tx'].strip(), mb, mp, ge, mc, sy))
            se = (r['SeR'] or '').strip()
            if se.endswith(':St') and len(st_ex) < 60 and SAFE(r): st_ex.append((tid, r['tx'].strip(), mb, ge, se, r['fe']))
    # ---- write local full lists
    with open(f'{LOCAL}/evid_infer_tokens_{c}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['text_id', 'speaker_id', 'tx', 'mb', 'mp', 'ge', 'mc', 'free_translation_en']); w.writerows(ev_rows)
    print('=====', c)
    print(' EVID/INFER tokens:', len(ev_rows), '| by (mp morph, ge label):', evid_mp.most_common(12))
    for slot in sorted(slot_lab, key=lambda s: -sum(slot_lab[s].values())):
        print(f'  slot {slot}: total {sum(slot_lab[slot].values())}; top5:', [(l, n, slot_ex[slot][l]) for l, n in slot_lab[slot].most_common(5)])
    print(' SyF last-part counts (top 12):', syf.most_common(12), '| SyF events aligned to a word:', n_syf_word)
    print(' SeR roles (all):', ser_roles.most_common())
    print(' SeR forms top5:', ser_forms.most_common(5))
    print(' objects (:O on a word):', dict(obj))
    pickle.dump({'syf_ex': syf_ex, 'obj_ex': obj_ex, 'st_ex': st_ex, 'ev_rows': ev_rows}, open(f'{W.HOME}/scratch/002/out/{c}_b1.pkl', 'wb'))
