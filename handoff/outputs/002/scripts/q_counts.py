import sys, pickle, collections, os, glob, re
import xml.etree.ElementTree as ET
home = os.environ['HOME']
PUNCT = re.compile(r'^[\W_]+$', re.U)
for c, root in (('dolgan', 'd'), ('evenki', 'e')):
    D = pickle.load(open(f'{home}/scratch/002/{c}.pkl', 'rb'))['data']
    base = f'{home}/scratch/x/{root}'
    tot = collections.Counter(); spk = set(); spk_by_file = []
    exs_w = exs_u = exs_sc = 0
    for rel, d in D.items():
        tot['transcripts'] += 1
        spk.update(d['speakers']); spk_by_file.append(len(d['speakers']))
        for t in d['tiers']:
            cat = t['category']
            if cat == 'tx':
                for e in t['events']:
                    tot['tx_events'] += 1
                    txt = e[4].strip()
                    if txt: tot['tx_nonempty'] += 1
                    if txt and PUNCT.match(txt): tot['tx_punct_only'] += 1
                    tot['tx_ws_tokens'] += len(txt.split())
            elif cat == 'ref': tot['ref_events'] += len(t['events'])
            elif cat == 'fe': tot['fe_events'] += len(t['events']); tot['fe_nonempty'] += sum(1 for e in t['events'] if e[4].strip())
            elif cat == 'mb': tot['mb_events'] += len(t['events']); tot['mb_nonempty'] += sum(1 for e in t['events'] if e[4].strip())
        exs = glob.glob(os.path.join(base, os.path.dirname(rel), '*.exs'))
        assert len(exs) == 1, rel
        r = ET.parse(exs[0]).getroot()
        for ts in r.iter('ts'):
            n = ts.get('n')
            if n == 'HIAT:w': tot['exs_HIAT_w'] += 1
            elif n == 'HIAT:u': tot['exs_HIAT_u'] += 1
            elif n == 'sc': tot['exs_sc'] += 1
    print('=====', c)
    for k, v in sorted(tot.items()): print(f'  {k:16s} {v}')
    print('  distinct speaker ids in .exb speakertables:', len(spk), '| speakers per transcript mean', round(sum(spk_by_file)/len(spk_by_file),2))
