# QA differences (handoff 003, step 3)

`reports/qa_report.md`: **no row is non-MATCH.** All of the pipeline's counts equal the counts measured in handoff 002 (Dolgan and Evenki), so there are no two-number differences, example words or "which side is right" to report.

Exit code of `run_all.py`: 0.

## QA flags raised by the pipeline (not count mismatches)

| Flag | Count | What I found |
|---|---|---|
| `morph_gloss_mismatch` | 2 | Tokens `AkNN_KuNS_200212_LifeHandicraft_conv#123.w12` and `#123.w15`: the mb morpheme is the postposition (`kɨtta`, `gɨtta`) with gloss `with`, and mp and gloss have different shapes. 002 reported 0 mismatches with its own rule; the pipeline's rule is stricter or differs. Only these 2 tokens in the corpus. |
| `speaker_not_in_coma` | 3 | Speaker ids `DCh`, `ES`, `SE` appear in transcripts but not in the .coma. They are speakers without birth data, so they cannot be in the birth-year analyses. |
| `word_tier_event_without_word` | 1,282 | Events on a word-level tier (the sample I looked at is a BOR tier) that have no matching `tx` word. Spread over many texts (top 5 texts: 67, 45, 38, 36, 35 flags). The pipeline ignores these events; I did not check whether information is lost. |

Objects: 1,307 under 002's rule and 1,307 under the pipeline's rule.
