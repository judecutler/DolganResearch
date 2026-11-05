"""Handoff 002 part B2: Q4 sample alignment, Q21 oddities. Read-only inspection."""
import sys, os, re, collections, pickle
sys.path.insert(0, os.path.dirname(__file__))
import wordlib as W
CYR = re.compile(r'[А-Яа-яЁё]'); LAT = re.compile(r'[A-Za-z]')
for c in ('dolgan', 'evenki'):
    D = W.load(c)
    odd = collections.Counter(); notext_gloss = []; pct = collections.Counter(); nomb_kind = collections.Counter()
    sample = None; empty_tiers = collections.Counter(); dupspan = 0; dup_tier_ids = 0
    for rel, d in sorted(D.items()):
        tid = rel.split('/')[1]
        if d['tli_dup']: odd['files_with_duplicate_timeline_ids'] += 1
        ids = [t['id'] for t in d['tiers']]
        if len(ids) != len(set(ids)): dup_tier_ids += 1
        ge_ne = 0
        for t in d['tiers']:
            if not t['events']: empty_tiers[t['category']] += 1
            elif not any(e[4].strip() for e in t['events']): empty_tiers['allblank:' + t['category']] += 1
            spans = [(e[0], e[1]) for e in t['events']]
            if t['category'] in ('tx', 'mb', 'mp', 'ge') and len(spans) != len(set(spans)): dupspan += 1
            for e in t['events']:
                x = e[4]
                if '�' in x: odd['replacement_char_events'] += 1
                if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', x): odd['control_char_events'] += 1
                if t['category'] == 'tx':
                    if CYR.search(x): odd['tx_events_with_cyrillic'] += 1
                    if CYR.search(x) and LAT.search(x): odd['tx_events_mixing_cyrillic_and_latin'] += 1
                if t['category'] in ('mb', 'mp') and CYR.search(x): odd[t['category'] + '_events_with_cyrillic'] += 1
                if t['category'] in ('ge',):
                    if x.strip() == '%%': pct['ge_exactly_%%'] += 1
                    if x.strip() == '%': pct['ge_exactly_%'] += 1
                    if '%%' in x: pct['ge_events_containing_%%'] += 1
                    if re.search(r'(^|[-=.])%(?!%)', x): pct['ge_events_with_single_%_prefix'] += 1
                    if x.strip(): ge_ne += 1
                if t['category'] in ('mb', 'mp', 'tx') and '%' in x: pct['%_in_' + t['category']] += 1
        if ge_ne == 0: notext_gloss.append(tid)
        for r in W.words(d):
            if r['mb'] is None:
                tx = r['tx'].strip()
                k = 'punctuation_only' if re.fullmatch(r'[\W_]+', tx) else 'non-speech (( ))' if tx.startswith('((') else 'truncated (xx-)' if re.fullmatch(r'\(.*-\)', tx) else 'other'
                nomb_kind[k] += 1
            if sample is None and r['fe'] and all(r.get(k) for k in ('mb', 'mp', 'ge', 'mc', 'ps')) and False: pass
    print('=====', c)
    print(' odd:', dict(odd)); print(' %:', dict(pct)); print(' tiers with no events / all blank (by category):', dict(empty_tiers))
    print(' texts with no non-empty ge event:', len(notext_gloss)); print(' files with duplicate tier ids:', dup_tier_ids, '| tiers (tx/mb/mp/ge) with repeated spans:', dupspan)
    print(' tx words without an mb event, by kind:', dict(nomb_kind))
