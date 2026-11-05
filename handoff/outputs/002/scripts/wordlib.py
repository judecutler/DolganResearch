"""Shared helpers for handoff 002 (stdlib only). Aligns tiers by (start,end) timeline index per speaker."""
import os, pickle, bisect, re, collections
HOME = os.environ['HOME']
WORD_TIERS = ['tx','mb','mp','ge','gg','gr','mc','ps','SyF','SeR','IST','Top','Foc','BOR','BOR-Phon','BOR-Morph','CS','ExLocPoss']
def load(c):
    return pickle.load(open(f'{HOME}/scratch/002/{c}.pkl', 'rb'))['data']
def utterance_index(tiers_of_spk):
    """sorted list of (start_idx, end_idx, ref_text, fe_text) from ref + fe tiers of one speaker"""
    ref = tiers_of_spk.get('ref', []); fe = tiers_of_spk.get('fe', [])
    femap = {(e[0], e[1]): e[4] for e in fe}
    out = []
    for e in ref:
        out.append((e[0], e[1], e[4], femap.get((e[0], e[1]), '')))
    out.sort()
    return out
def words(d):
    """yield dict per tx event: fields from aligned tiers (exact (start,end) match), plus utterance"""
    by_spk = collections.defaultdict(lambda: collections.defaultdict(list))
    for t in d['tiers']:
        by_spk[t['speaker']][t['category']] = t['events']
    for spk, cats in by_spk.items():
        look = {cat: {(e[0], e[1]): e[4] for e in evs} for cat, evs in cats.items() if cat != 'tx'}
        # events may repeat (same span) -> keep list for those categories
        utt = utterance_index(cats); starts = [u[0] for u in utt]
        for i, e in enumerate(cats.get('tx', [])):
            row = {'spk': spk, 'i': i, 'span': (e[0], e[1]), 'ids': (e[2], e[3]), 'tx': e[4]}
            for cat in WORD_TIERS[1:]:
                row[cat] = look.get(cat, {}).get((e[0], e[1]))
            k = bisect.bisect_right(starts, e[0]) - 1
            if k >= 0 and utt[k][0] <= e[0] < utt[k][1] + 0 or (k >= 0 and e[0] >= utt[k][0] and e[1] <= utt[k][1]):
                row['ref'] = utt[k][2]; row['fe'] = utt[k][3]
            else:
                row['ref'] = None; row['fe'] = None
            yield row
SEP = re.compile(r'[-=]')
def morphs(s): return SEP.split(s) if s else []
