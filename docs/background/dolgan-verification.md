# Dolgan paper angles: second-checker verification (Nov 2026)

Method: about 45 searches and fetches, aimed at falsifying the four gaps in `dolgan.md`. I also inspected GitHub directly. GitHub was the only scholarly or code host reachable by curl through the proxy.

**Unreachable sources:**
- Blocked outright (403 or not on the allowlist): the Leiden handle and DSpace pages, brill.com, aclanthology.org, OpenAlex, Semantic Scholar, Crossref and unimorph.github.io.
- Loaded but needed JavaScript: istina.msu.ru.
- Behind Anubis bot protection: journal.fi/finjol and hal.univ-lyon2.fr.
- No Google Scholar "cited-by" counts could be obtained. Citing works were approximated by search only.

Verdicts:

| Angle | Verdict |
|---|---|
| 1. Russian loan integration, Dolgan vs Evenki | **STILL UNVERIFIED, leaning OPEN** (blocked by Stapert 2013 and the two ISTINA records) |
| 2. Evidentiality corpus study | **OPEN-VERIFIED** for a dedicated or quantitative study |
| 3. DOM / case change across generations | **PARTIAL** (Sheifer's DOM work is in progress and unpublished; the apparent-time test is OPEN) |
| 4. Computational morphology | **PARTIAL** (an Apertium stub exists; no usable analyzer) |

---

## Angle 1: Morphological integration of Russian borrowings, Dolgan vs Evenki

### Takeaway
No published study was found that compares how Russian material is morphologically integrated in Dolgan and in Evenki. None uses the INEL BOR-Morph/CS tiers either. Two things block an OPEN verdict:
- The chapter titles of Stapert 2013 chapters 2–10 could not be read; only the file list was visible.
- The ISTINA records 261724568 and 261725820 could not be identified, because istina.msu.ru renders only with JavaScript.

There is also a new caveat. Däbritz already states the basic integration facts descriptively (see the second finding).

### Cited Findings
- **Stapert 2013, table of contents.** The Leiden repository lists 10 chapters, but only "Chapter 1 Introduction" has a title. Chapters 2–10 are untitled file entries. The abstract mentions "contact-induced change… Tungusic and Turkic influences" and correlates contact patterns with genetic admixture. It does not mention Russian or code-switching. Five different Leiden item pages were fetched and none exposed chapter titles. — [item 2940584](https://scholarlypublications.universiteitleiden.nl/access/item%3A2940584/view); [item 2940598](https://scholarlypublications.universiteitleiden.nl/access/item%3A2940598/view); [item 2940600](https://scholarlypublications.universiteitleiden.nl/access/item%3A2940600/view). The handle hdl.handle.net/1887/21798 and openaccess.leidenuniv.nl redirect to Primo, which was not fetched.
- **Däbritz 2023 (JEL sketch)** already makes these points:
  - "Russian copied verbs are suffixed without exception with the verbaliser {-LA4ː}."
  - Russian nominals are not morphologically integrated in this speaker's variety.
  - "code copies often cannot be clearly distinguished from spontaneous code-switches."
  - Russian phonotactic adaptation is treated in Däbritz 2022, Ch. 11.2.2.
  - Source: [Däbritz 2023 full text](https://dergipark.org.tr/tr/download/article-file/3631398)
  - This is descriptive and based on one speaker, but it sets the baseline any paper must cite.
- **Däbritz 2022** has §11.2 "Loanwords" inside Ch. 11 "Lexicon". There is no separate contact or code-switching chapter. — [TOC via sack.de](https://www.sack.de/daebritz-a-grammar-of-dolgan/9789004516236)
- **The INEL publications page** lists no publication on code-switching. Its Russian-loan-morphology items concern Kamas (Arkhipov 2023), and Nanai and Ulcha (Oskolskaya & Stoynova 2024). None concerns Dolgan. — [INEL publications](https://www.slm.uni-hamburg.de/inel/aktivitaeten/publikationen.html)
- **INEL conference talks on Dolgan** cover phonetics, tense, possessives and the corpus. None covers borrowing or code-switching. — [INEL talks](https://www.slm.uni-hamburg.de/en/inel/aktivitaeten/konferenzbeitraege.html)
- **Oskolskaya & Stoynova 2024**, "Two similar languages borrow verbs in different ways" (ALP 20.2), covers Nanai and Ulcha. Evenki appears only on an areal map, and Dolgan is not mentioned. — [ALP PDF](https://alp.iling.spb.ru/static/alp_XX_2/05.pdf)
- **Oskolskaya & Stoynova 2013**, "The la-form: Russian verbs in Nanai speech" (JEFUL), does not mention Dolgan. It is a methodological model, since Nanai *-la* parallels Dolgan {-LAː}. — [JEFUL](https://ojs.utlib.ee/index.php/jeful/article/download/jeful.2013.4.2.05/10219/15025)
- **Stoynova 2024**, roundtable "Переключение кодов в устных корпусах малых языков" (RNC20):
  - It describes the INEL code-switching tags RUS:ext, RUS:int.ins and RUS:int.alt.
  - It notes inconsistent glossing of Russian items in INEL, which is a data-quality risk for Angle 1.
  - It does not mention Dolgan.
  - Source: [PDF](https://ruslang.ru/sites/default/files/doc/ruscorpora2024/roundtable_contact/Stoynova-roundtable_RNC20.pdf)
- **Stoynova 2023 (SLE)**, "Reconstructing a pre-Soviet contact with Russian: Barhahan Evenki": the Evenki side only, with code-switching attested about 14 times. It is not a systematic noun/verb integration study and does not mention Dolgan. — [slides](https://blogs.helsinki.fi/language-diversification-and-spread-north/files/2023/09/EvenkiRUSContact_shared.pdf)
- **The 2021 book of abstracts** of "Indigenous languages of Russia in contact with Russian II" covers about 20 languages, Evenki among them, but not Dolgan. — [HSE PDF](https://publications.hse.ru/pubs/share/direct/523116431.pdf)
- **Kashkin 2023**, a survey of language-contact research in Russia, mentions Dolgan only as a Taymyr population. It cites no Dolgan–Russian contact work. — [PDF](https://ruslang.ru/sites/default/files/doc/kashkin/2023/Kashkin-2023-kontakty_napravlenija.pdf)
- **Other loanword work, all lexical, etymological or phonetic:**
  - K. Stachowski 2012, "Word-final consonant clusters in Russian loanwords in Dolgan" (Gülensoy Festschrift, pp. 283–294). — [Avesis](https://avesis.istanbul.edu.tr/yayin/7411b285-adbd-4ae2-8ad0-426df3c4e31d/turk-mogol-arastirmalari-prof-dr-tuncer-gulensoy-armagani)
  - Piispanen 2023, "New Dolgan etymologies", *Turkic Languages* 27(2). — [Harrassowitz](https://tl.harrassowitz-library.com/article/TL/2023/2/4)
  - Nazmutdinova 2018, "Aboriginal and borrowed lexical strata in Dolgan" (*Northern Russian Dialects* 17). — [IL RAN](https://nrd.iling.spb.ru/en/node/117)
- **Stapert's Leiden publication list** has only three items: the 2013 thesis, the INEL corpus, and Pakendorf & Stapert 2020. No separate code-switching paper is listed. — [Leiden](https://www.universiteitleiden.nl/en/staffmembers/eugenie-stapert/publications)
- **The ISTINA records** (presentation 261724568, article 261725820) keep surfacing for searches on "Dolgan Russian code-switching / borrowed verbs" and "Arkhipov INEL borrowing". The title and author could not be extracted: the fetch returned only "Для работы с сайтом включите JavaScript". A search on the ID numbers returned nothing relevant. Article 344774839 surfaced as well and was likewise unreadable.

### Queries run (Angle 1)
1. `Stapert 2013 "Contact-induced change in Dolgan" chapters Russian`
2. `долганский язык переключение кодов русский` (RU)
3. `Stoynova Russian borrowings Siberian languages Dolgan Evenki INEL corpus`
4. `Arkhipov INEL borrowing annotation Russian loanwords Evenki Selkup Dolgan`
5. `istina.msu.ru долганский русский переключение кодов глаголы заимствованные` (RU)
6. `Dolgan Russian code-switching borrowed verbs Stoynova OR Oskolskaya OR Kashkin`
7. `Russische Lehnwörter Dolganisch Morphologie Integration` (DE)
8. `LOT 336 Stapert Dolgan dissertation pdf lotpublications`
9. `Dolgan Russian code-switching corpus talk 2024 OR 2025`
10. `"261725820" OR "261724568" istina`
11. `долганско-русское двуязычие переключение кодов корпус INEL статья` (RU)
12. `Dolgan "Russian verbs" verbalizer -LAː borrowing code-switching Taimyr Turkic`
13. `"Russian verbs in Dolgan" OR "русские глаголы в долганском"` (RU)
14. `Eugénie Stapert Dolgan Russian code-switching OR "mixed" OR borrowing article`
15. `переключение кодов в речи долган Таймыр русский язык доклад Ломоносов` (RU)

### Inferences
- The ISTINA hits co-occur with "Arkhipov" and with "borrowed verbs". The likeliest candidate is an MSU or HSE-linked talk and article on Russian verbs or code-switching in Dolgan, possibly from the Hamburg/Moscow INEL circle. This is unconfirmed, and it is the single biggest falsification risk.
- Even if the ISTINA item covers Dolgan alone, a quantitative two-recipient comparison (Dolgan vs Evenki) would still be novel. The angle should be framed as comparative and tier-based, not as "first study of Russian loans in Dolgan".
- Two facts to state upfront: Däbritz says {-LAː} is obligatory for Russian verbs, and Russian nouns are not integrated. The paper should test these on corpus data across speakers.

### Must-do before claiming OPEN
- Open ISTINA 261724568 and 261725820 in a JS-enabled browser.
- Open the Stapert 2013 front-matter PDF (item 03) for the TOC.

---

## Angle 2: Evidentiality in Dolgan (corpus study, compared with Evenki)

### Takeaway
**OPEN-VERIFIED** for a dedicated or quantitative study. The only coverage is descriptive: Däbritz 2022 §6.6 "Evidentiality", and a paragraph in Däbritz 2023. No article, thesis or talk on Dolgan evidentiality turned up in English, Russian or German. The Sakha evidentiality literature I found does not cover Dolgan.

### Cited Findings
- **Däbritz 2022 grammar**: §6.6 Evidentiality, inside Ch. 6 "Verbal Inflectional Morphology". — [sack.de TOC](https://www.sack.de/daebritz-a-grammar-of-dolgan/9789004516236)
- **Däbritz 2023** describes the evidential system as "relatively simple compared to surrounding Siberian languages":
  - The one dedicated inferential is {-DA4K}+AGR.POSS (grammar p. 296).
  - The postterminal {-BI4T} also expresses evidentiality.
  - The copula's 3SG postterminal *äbit* has become an evidential particle.
  - It makes no Evenki or Sakha comparison and reports no frequency data.
  - Source: [Däbritz 2023](https://dergipark.org.tr/tr/download/article-file/3631398)
- **Efremov 2010**, "Means of expressing indirect evidentiality in the Sakha language" (*Siberian Journal of Philology* 1: 152–156), is about Sakha only. — [SPJ](https://www.philology.nsc.ru/journals/spj_en/article.php?id=390)
- **Greed 2018**, "From perfect to narrative tense" (*Studies in Language*), is about Even. It cites Sakha but not Dolgan. — [OUCI](https://ouci.dntb.gov.ua/works/4O35dAN4)
- **Other searches**:
  - The Russian searches returned only general Dolgan pages, such as Wikipedia and the SFU ethnic-identity book.
  - The German search returned nothing on Dolgan.
  - The English search surfaced only Däbritz 2023 and Sheifer's DOM slides.
- **Sheifer's work-in-progress list** includes "Epistemic and agent-oriented modality in Dolgan and Yakut". This is adjacent (epistemic modality) but not evidentiality as such, and it is unpublished. — [Dartmouth profile](https://faculty-directory.dartmouth.edu/karina-sheifer)

### Queries run (Angle 2)
1. `evidentiality Dolgan`
2. `эвиденциальность долганский язык` (RU)
3. `долганский язык косвенная засвидетельствованность` (RU)
4. `Sakha Yakut evidentiality ebit indirective Pakendorf OR Petrova OR Vinokurova`
5. `Dolganisch Evidentialität Indirektivität` (DE)
6. `Evenki evidentiality corpus INEL non-witnessed Dolgan comparison`
7. `"Grammar of Dolgan" Däbritz review evidentiality chapter …`

### Inferences
- The risk is moderate. Sheifer's epistemic-modality project may encroach on this angle, so a paper should stress corpus frequency, genre and generation, and the Evenki comparison.
- The Pakendorf & Stapert 2020 Oxford chapter (HAL PDF blocked by Anubis) may briefly mention Sakha/Dolgan evidentials. It was not checked.

---

## Angle 3: DOM / case-marking change across speaker generations

### Takeaway
**PARTIAL.**
- **DOM in Dolgan** has been described: Däbritz 2023 and 2022 (§4.2 Case) describe a three-way nominative / accusative / partitive pattern, and Siegl covers the partitive.
- **Sheifer & Bolshakova** remain unpublished. Sheifer's Dartmouth profile lists "Contact-induced patterns in direct object marking in Dolgan" under Works in Progress.
- **Apparent-time change**, whether Siegl's dative-to-instrumental shift in secondary predicates or DOM change by birth cohort, has no published test that I could find. That sub-angle is OPEN.

### Cited Findings
- **Sheifer's Dartmouth profile** lists under "Works in Progress": "Contact-induced patterns in direct object marking in Dolgan", "Epistemic and agent-oriented modality in Dolgan and Yakut", and "Polyfunctionality of the pronoun kihi in Dolgan and Yakut". None is among her published items. — [Dartmouth](https://faculty-directory.dartmouth.edu/karina-sheifer)
- **The 2023 workshop slides** remain the only public version. — [slides](https://blogs.helsinki.fi/language-diversification-and-spread-north/files/2023/09/Sheifer-DOM-in-DLG.pdf)
- **Däbritz 2023**:
  - It describes "threefold differential object marking: nominative vs accusative vs partitive". Specificity drives nominative vs accusative; the partitive goes with imperative and prospective, i.e. actions not completed at the moment of speech.
  - The partitive {+DA4} is a reanalysed locative.
  - It reports **no** cross-speaker variation in object marking.
  - It does **not** discuss secondary predicates.
  - Source: [Däbritz 2023](https://dergipark.org.tr/tr/download/article-file/3631398)
- **Siegl 2015** remains the only source of the dative-to-instrumental claim. A search for its citing works found only Siegl's own partitive paper, Däbritz 2023 and Stapert-related pages. No follow-up test appeared. — [CEEOL](https://www.ceeol.com/search/article-detail?id=304362); [digar](https://digar.ee/arhiiv/en/download/230696)
- **Russian searches** on DOM and on secondary predication with the instrumental or dative returned no Dolgan items.

### Queries run (Angle 3)
1. `Sheifer Bolshakova Dolgan direct object marking`
2. `дифференцированное маркирование объекта долганский` (RU)
3. `Dolgan accusative unmarked object partitive Evenki influence Sakha DOM 2024 OR 2025`
4. `долганский язык вторичная предикация творительный дательный падеж` (RU)
5. `Dolgan apparent time case change instrumental dative younger speakers corpus`
6. `Kirill Sheifer Dolgan Sakha Evenki object marking paper 2024 2025`
7. `Siegl "Three Nganasan-Evenki/Dolgan morphosyntactic parallels" cited`

### Inferences
- Do not pitch "DOM in Dolgan" as new. Sheifer & Bolshakova's paper is presumably forthcoming. Pitch instead an apparent-time quantitative test using INEL speaker birth years:
  - Siegl's dative-to-instrumental claim for secondary predicates
  - the three-way DOM by TAM context
- Contact Sheifer, or watch for her publication, before submitting.

---

## Angle 4: Computational morphology for Dolgan

### Takeaway
**PARTIAL.**
- **Apertium**: a Dolgan morphological transducer *exists* as `apertium/apertium-dlg`, but it is a toy stub. Its lexc file is 251 lines with about 72 entry lines, and its twol file is 36 lines. The repository was created in 2016, has had only maintenance commits since, and the last push was 2021-07-19.
- **GiellaLT**: no `lang-dlg` was found by GitHub search. `lang-evn` exists.
- **UniMorph**: there is no `unimorph/dlg`, but `unimorph/sah` exists.
- **Wav2Gloss**: Dolgan (INEL, 11.64h training data) is one of the languages in the Fieldwork dataset. That paper reports only aggregate glossing results, with Dolgan-specific figures given only for transcription.
- **Verdict**: a usable FST analyzer or a benchmarked Dolgan glosser is OPEN. "Neural glossing of Dolgan" is partly occupied by the Wav2Gloss/Fieldwork data.

### Cited Findings
- **apertium/apertium-dlg** (GitHub API: created 2018-03-08 per GitHub, earliest commit 2016-10-10 by K. B. Unhammer, last pushed 2021-07-19, size 26 KB):
  - The README template claims "Morphological analysis of dlg".
  - The lexc has lexica for Nouns, Verbs, cases, possessives and clitics, but only about 72 entries in total.
  - Source: [github.com/apertium/apertium-dlg](https://github.com/apertium/apertium-dlg). Inspected by clone.
- **Related Apertium Sakha resources**: apertium-sah (last pushed 2022), apertium-kaz-sah and apertium-sah-eng.
- **GitHub repository search** ("dolgan", 61 results) shows that apart from apertium-dlg the hits are surname or project noise. Other searches returned nothing relevant: "dolgan language" and "dolgan morphology" gave 0, and searching giellalt for dlg gave 0. INEL-related repos are for Evenki only (`stakannn/INEL-evenki-corpus-processing`, a Whisper Evenki fine-tune).
- **Wav2Gloss** (ACL 2024): Table 1 has "dolg1241 | Dolgan (Däbritz et al., 2022) | BY-NC-SA | 11.64 | 1.23". Dolgan is named among "the highest-resource languages" in the transcription analysis. — [arXiv 2403.13169](https://arxiv.org/html/2403.13169v2)
- **ACL Anthology and UniMorph sites** could not be reached directly (proxy 403). Web searches for "Dolgan morphological analyzer finite-state OR automatic glossing" and the Russian equivalent returned nothing Dolgan-specific.

### Queries run (Angle 4)
1. GitHub API: `dolgan`
2. GitHub API: `dolgan language`
3. GitHub API: `dolgan morphology`
4. GitHub API: `lang-dlg`
5. GitHub API: `dlg fst`
6. GitHub API: `org:giellalt lang-dlg`
7. GitHub API: `org:unimorph dlg`
8. GitHub API: `INEL corpus`
9. `Dolgan morphological analyzer finite-state OR automatic glossing`
10. `долганский язык морфологический анализатор автоматическая разметка корпус` (RU)
11. `Wav2Gloss Fieldwork dataset DoReCo languages Dolgan interlinear glossing`

### Inferences
- Do not claim "no Dolgan analyzer exists". Say instead that only an Apertium stub of about 70 entries exists. A paper could build a GiellaLT/Apertium FST bootstrapped from INEL glosses and the apertium-sah lexicon, and evaluate it against INEL.
- The "affix productivity / morphotactics" angle from `dolgan.md` is unaffected by these findings and still has no direct competitor.

---

## Däbritz 2022 table of contents and citing works

### Takeaway
The grammar has 574 pages and 14 chapters. These sections are relevant to the angles:
- evidentiality: §6.6
- case: §4.2
- possession: §4.3
- clause chaining: §9.1
- loanwords: §11.2
- derivation: Ch. 12

There is no stand-alone chapter on language contact, code-switching or DOM. DOM falls under §4.2 Case and Ch. 8 Clausal Syntax.

### Cited Findings
- **Full TOC**:
  - 1 Introduction (§1.6 Material and Data)
  - 2 Phonology and Phonetics
  - 3 Word Classes
  - 4 Nominal Inflectional Morphology (4.1 Number, 4.2 Case, 4.3 Possession, 4.4 Predicate Forms of Nominals)
  - 5 Pronominal Inflectional Morphology
  - 6 Verbal Inflectional Morphology (6.3 Non-finite, 6.4 Tense-Aspect, 6.5 Mood/Modality/Illocution, 6.6 Evidentiality)
  - 7 Non-clausal Syntax
  - 8 Clausal Syntax—Simple Clauses (8.5 Negation)
  - 9 Complex Clauses (9.1 Clause Chaining, 9.2 Coordination, 9.3 Subordination)
  - 10 Discourse Organization
  - 11 Lexicon (11.1 Semantic Fields, 11.2 Loanwords)
  - 12 Derivational Processes
  - 13 Sample Texts
  - 14 References
  - Source: [sack.de](https://www.sack.de/daebritz-a-grammar-of-dolgan/9789004516236)
- **Citing works.** Scholar cited-by counts were not obtainable. Items found by search that cite Däbritz 2022:
  - Däbritz 2023 (JEL)
  - Golovatskaya et al. 2026 (*Philology. Theory & Practice*)
  - the Wav2Gloss Fieldwork dataset (which cites the INEL corpus, Däbritz et al. 2022)
  - the TSL 136 habitual chapter (2026), which probably cites it but was not checked
  - Sheifer's slides (2023)
- **A FinJoL review** surfaced on journal.fi (article 153018). It is probably a review of the grammar, but it was blocked by Anubis and is unverified.

---

## Inferences (cross-angle)
- **Strongest angle: 1**, provided the ISTINA item proves to be Dolgan-only or descriptive. Its novelty is a two-recipient comparison using matched tiers, with the Nanai/Ulcha strategy-contrast framework of Oskolskaya & Stoynova as the template.
- **Cleanest verified angle: 2** (evidentiality corpus study). Watch Sheifer's "epistemic modality in Dolgan and Yakut".
- **Angle 3** must be narrowed to an apparent-time test to avoid Sheifer & Bolshakova.
- **Angle 4** must acknowledge the apertium-dlg stub and the Wav2Gloss inclusion.
- **Data-quality caveat** for any INEL Russian-material study: Stoynova (2024) reports inconsistent glossing of Russian items across INEL corpora. Clitics are segmented differently, and some Russian items are glossed while others are not.
