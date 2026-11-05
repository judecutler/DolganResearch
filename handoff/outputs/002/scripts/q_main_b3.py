import sys, os, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    utt = collections.defaultdict(lambda: [0, 0]); texts = collections.Counter(); ex = []
    for rel, d in sorted(D.items()):
        tid = rel.split('/')[1]
        for r in W.words(d):
            tx = r['tx'].strip()
            if r['mb'] is None and not re.fullmatch(r'[\W_]+', tx) and not tx.startswith('((') and not re.fullmatch(r'\(.*-\)', tx):
                utt[(tid, r['spk'], r['ref'])][0] += 1; texts[tid] += 1
                if len(ex) < 6 and not re.search(r'[A-ZА-ЯЁ]', tx[:1]) and r['i'] > 40: ex.append((tid.split('_')[0] + '..', tx, (r['fe'] or '')[:70]))
            if r['mb'] is not None: utt[(tid, r['spk'], r['ref'])][1] += 1
    whole = sum(1 for k, v in utt.items() if v[0] and not v[1]); part = sum(1 for k, v in utt.items() if v[0] and v[1])
    print('=====', c, '| utterances where ALL words lack mb:', whole, '| utterances with SOME words lacking mb:', part, '| texts affected:', len(texts), 'of', len(D))
    print(' top texts by count (counts only):', [n for _, n in texts.most_common(8)])
    print(' examples (text prefix, tx word, free translation en):'); [print('   ', e) for e in ex]
