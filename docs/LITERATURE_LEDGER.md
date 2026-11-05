# Literature ledger

Verification records for every claim in this repo that something is unstudied. Built from two independent passes: a literature map, then a second pass whose only job was to falsify each gap. Full notes are in [`docs/background/`](background). Where the passes disagreed, the second pass wins.

**Statuses:** FILLED (done, cite it), PARTIAL (some of it done), OPEN-VERIFIED (no falsifier found in the searches listed), UNVERIFIED (could not check).
"OPEN-VERIFIED" means *no falsifier found in the searches run*. It is not proof.

Last full check: 2026-11-04. Re-check dates go in the table at the bottom.

## Study A: evidentiality in Dolgan, compared with Evenki

**Status: OPEN-VERIFIED for a dedicated or quantitative study of Dolgan. Evenki and Sakha side NOT YET MAPPED.**

Searches: 7 queries in English, Russian and German (including `evidentiality Dolgan`, `эвиденциальность долганский язык`, `Dolganisch Evidentialität`, and Sakha and Evenki variants). No article, thesis or talk on Dolgan evidentiality turned up.

| Closest work | What it covers | Why it does not fill the gap |
|---|---|---|
| Däbritz (2022), *A Grammar of Dolgan*, Brill, §6.6 "Evidentiality" | Description of the evidential forms | Descriptive, from corpus examples; no frequencies or comparison. **We have not read §6.6.** |
| Däbritz (2023), "Dolgan", *Journal of Endangered Languages* 13(23): 177–199 | Short description: inferential `-DA4K`+AGR.POSS, postterminal `-BI4T`, evidential particle *äbit* | No Evenki or Sakha comparison, no frequency data. Full text: https://dergipark.org.tr/tr/download/article-file/3631398 |
| Efremov (2010), "Means of expressing indirect evidentiality in the Sakha language", *Siberian Journal of Philology* 1: 152–156 | Sakha only | Does not cover Dolgan. https://www.philology.nsc.ru/journals/spj_en/article.php?id=390 |
| Greed (2018), "From perfect to narrative tense", *Studies in Language* | Even | Cites Sakha, not Dolgan. https://ouci.dntb.gov.ua/works/4O35dAN4 |
| Sheifer (Dartmouth), work in progress: "Epistemic and agent-oriented modality in Dolgan and Yakut" | Adjacent: epistemic modality | Unpublished, and not evidentiality as such. https://faculty-directory.dartmouth.edu/karina-sheifer |
| Habitual `-AːččI` chapter, TSL 136 (Benjamins, 2026) | Habitual | Different category. **Do not pursue the habitual.** |

**Manual checks still owed**
1. Read Däbritz (2022) §6.6 and Däbritz (2023) on evidentiality, so the paper starts from what they already state.
2. **Map the Evenki and Sakha evidentiality literature.** Not done. Required before claiming a comparison gap. (WP10, web Claude.)
3. Pakendorf and Stapert (2020, Oxford Guide to the Transeurasian Languages, 430–445) may mention Sakha or Dolgan evidentials. The HAL copy was blocked and not read.
4. Read Stapert (2013) chapters, which could not be opened. Contents unknown.
5. Watch Sheifer's modality project.
6. Email the INEL team (inel@uni-hamburg.de) and Däbritz about work in press.

## Study B: case change across speaker generations in Dolgan

**Status: PARTIAL overall. The apparent-time test is OPEN-VERIFIED with moderate confidence (it was lightly checked).**

Searches: 7 queries in the verification pass (English and Russian), plus three in the first pass. Included `Sheifer Bolshakova Dolgan direct object marking`, `дифференцированное маркирование объекта долганский`, `долганский язык вторичная предикация творительный дательный падеж`, `Dolgan apparent time case change instrumental dative younger speakers corpus`.

| Closest work | What it covers | Why it does not fill the gap |
|---|---|---|
| Siegl (2015), "Three Nganasan–Evenki/Dolgan morphosyntactic parallels and their implications", *Linguistica Uralica* 51(4): 258–277 | Asserts a 20th-century shift in Dolgan secondary predication from dative to instrumental under Russian influence | Asserts, but as far as the full text shows does not test it quantitatively. **We have not verified what data he used.** Full text: https://digar.ee/arhiiv/en/download/230696 |
| Sheifer and Bolshakova (2023), "Contact-induced patterns in direct object marking in Dolgan", workshop slides | Dolgan and Sakha binary and ternary object marking; ternary strategy in more contexts in Dolgan than Sakha | Slides, qualitative, three languages. No published version found. Sheifer's profile lists the paper as work in progress. https://blogs.helsinki.fi/language-diversification-and-spread-north/files/2023/09/Sheifer-DOM-in-DLG.pdf |
| Däbritz (2022, §4.2 Case; 2023) | Threefold object marking: nominative, accusative, partitive. Partitive `+DA4` is a reanalysed locative. | Reports no variation between speakers and does not discuss secondary predicates. |
| Siegl, "Der Partitiv im Taimyr Dolganischen", *Journal de la Société Finno-Ougrienne* (year not resolved) | Partitive case | Descriptive; field data plus a 48,000-word written sample |
| Baker and Vinokurova (2010), *NLLT*, and "Rethinking structural case: Partitive case in Sakha" | Sakha formal analysis | Sakha only. https://link.springer.com/article/10.1007/s11049-010-9105-1 ; https://openpolar.no/Record/ftdatacite:10.5281%2Fzenodo.4680300 |
| Pakendorf and Stapert (2020) | Contact-induced loss of Turkic genitive and locative; new partitive | Overview chapter; not read in full |

**Rule:** do not pitch "differential object marking in Dolgan" as new. Pitch the age comparison.

**Manual checks still owed**
1. Read Siegl (2015) in full: what exactly is claimed, on what data. (WP10.)
2. One more Russian query on secondary predication and one Google Scholar "cited by" on Siegl (2015). Cited-by data was not obtainable in the first pass.
3. Contact Sheifer, or check for publication, before submitting.
4. Resolve the year of Siegl's partitive paper.
5. Read Stapert (2013).

## Backup angles (parked)

| Angle | Status | Why parked |
|---|---|---|
| Russian loanword integration in Dolgan vs Evenki | PARTIAL | A 2019 plenary talk by Wagner-Nagy and Arkhipov, "Russian borrowings in languages of Central Siberia: observations from corpora" (Moscow, 27 Oct 2019), covers proportions of borrowings, a Dolgan comparison across periods, noun plural marking and verb adaptation in Selkup, Kamas, Dolgan and Nganasan. Evenki is not in it. Däbritz (2023) already states that Russian verbs take `-LAː` and nouns are not integrated. INEL glossing of Russian items is reported inconsistent (Stoynova 2024). |
| Computational Dolgan morphology | PARTIAL | A stub Apertium transducer exists (`apertium/apertium-dlg`, about 72 lexicon entries, last push 2021). Dolgan is in the Wav2Gloss Fieldwork set. A usable analyser is open. |
| Selkup aspect-suffix productivity across dialects | OPEN-VERIFIED (moderate) | Separate project. See `docs/background/frontier-report-all-languages.md` |

## Already covered. Do not repeat
Negation (Siegl 2020), predicative possession (Däbritz 2018), first-person imperative (Däbritz 2019), placeholders (Däbritz 2018), habitual (TSL 136, 2026), partitive (Siegl), *naada* (Siegl 2020, 2021), *barı* "all" (Siegl 2018), information structure and focus position (Däbritz 2020, 2021, 2023), Evenki lexical copies in Dolgan (Hayırsever 2023), Russian loan phonetics (K. Stachowski 2010), rounding-harmony acoustics (Gopal et al., in progress), Anabar sociolinguistics (Grenoble et al. 2024).

## Must-cite list (provisional)
Däbritz (2022; 2023); Siegl (2015); Pakendorf and Stapert (2020); Stapert (2013); Sheifer and Bolshakova (2023); Baker and Vinokurova (2010); the INEL corpus citations (Däbritz, Kudryakova and Stapert for Dolgan; Däbritz, Gusev and Stoynova for Evenki); DoReCo Dolgan (Däbritz, Kudryakova, Stapert and Arkhipov 2024; DOI 10.34847/nkl.f09eikq3) if used.

## Sources that could not be reached
Glottolog bibliography for Dolgan (blocked); Stapert (2013) chapters (blocked, chapter titles unseen); Google Scholar "cited by" (unavailable); a possible review of the Däbritz grammar on journal.fi (bot protection); the HAL copy of Pakendorf and Stapert (2020).
Resolved in this session: ISTINA record 261724568 is the Wagner-Nagy and Arkhipov 2019 talk above; record 261725820 is the catalogue entry for the INEL Dolgan corpus and contains no analysis.

## Checks log
| Date | Who | What | Result |
|---|---|---|---|
| 2026-11-04 | web Claude | Initial map and independent falsification pass | as above |
| 2026-11-04 | Jude | ISTINA records opened in a browser | resolved (see above) |
