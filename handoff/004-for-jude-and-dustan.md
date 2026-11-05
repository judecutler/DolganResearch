# 004: Decisions, reading and one email (for Jude and Dustan)

- **From:** web Claude
- **To:** Jude, Dustan
- **Status:** needs-human
- **Created:** 2026-11-05
- **Depends on:** none (do it while desktop Claude runs 003)

## Goal
Handoff 002 changed several assumptions in the plans. Some of the fixes are decisions only you can make. Some need a source that web Claude cannot read. This task lists them in priority order. Each item says why it matters.

## 1. Confirm or change seven decisions (10 minutes)
Read D-016 to D-023 in `docs/DECISIONS.md`. In the "By" column, write your name next to each one you accept. Change the ones you don't accept. Most important:
- **D-017.** Keep the GitHub repo **private** while it holds corpus sentences, because speakers' names occur inside the transcripts.
- **D-020.** Study A codes every word the corpus already tags as evidential (89 Dolgan, 29 Evenki), plus a **sample** of the ambiguous forms (`TAK` glossed `COND1`, `PST2`). Exhaustive coding would be about 3,000 items.
- **D-023.** The speaker table keeps **sex** as a covariate. CLAUDE.md rule 9 lists only speaker ID and birth year, so this needs your yes or no.

## 2. Update `evidentiality/PLAN.md` (you own it; 20 minutes)
Web Claude does not edit your folder. What 002 found, to fold in:
- The corpus glosses the particle `eːt` as `EVID` (53 tokens). This is probably the copula *äbit* grammaticalised as a particle, but that is **unverified**. Check Däbritz (2022) §6.6.
- `INFER` (36 tokens) is the morph `TAK`. The same morph is glossed `COND1` 555 times. Whether a given `TAK` is inferential is therefore an annotator's call, and that is what your codebook's `is_evidential_use` column decides.
- `-BIt` in your notes is `BIT` in the data, glossed `PST2` (2,415) and `PTCP.PST` (714). Whether `PST2` is Däbritz's "postterminal" is **unconfirmed** (D-022).
- Evenki has only 29 `EVID` tokens (on `-rkə`) and no `INFER`. A Dolgan/Evenki comparison will need Evenki forms beyond the tagged ones. Which forms those are is D-007, and it needs the Evenki literature.
- The codebook dropdowns come from `shared/config/evid_codebook.json`. When you change the codebook, change that file too, or ask web Claude.

## 3. Read two sources (each is the input for a decision)
- **Däbritz (2022), *A Grammar of Dolgan*, §6.6 (evidentiality) and the tense chapter.** Settles D-022 (is `PST2` the postterminal?) and whether `eːt` is the evidential particle. Check whether the book is open access (a Zenodo record was found earlier, unverified).
- **Siegl (2015)** on Dolgan secondary predication, the source of the dative-to-instrumental claim. Study B1 cannot run without a way to recognise a secondary predicate, and the corpus has no tag for one (D-021). Note the examples and criteria Siegl uses. Web Claude turns them into a candidate filter.

## 4. Send one email to the INEL team (draft below; edit freely)
Four questions only they can answer cleanly. Send it from your own address.

> To: inel@uni-hamburg.de
> Subject: Questions about the INEL Dolgan Corpus 2.0 metadata and counts
>
> Dear INEL team,
>
> We are two linguists at UC Berkeley starting a study of Dolgan with the INEL Dolgan Corpus 2.0 and the INEL Evenki Corpus 2.0. Thank you for making them available. While preparing the data we ran into four questions that we could not resolve from the documentation:
>
> 1. Counts. The documentation gives 14,193 utterances and 97,625 tokens for Dolgan 2.0. Counting the files, we get 14,076 `ref` events (14,078 `HIAT:u` in the .exs files) and 97,652 `tx` events (97,757 `HIAT:w`). Which counting rule do the documented figures use? (For Evenki 2.0, the `# INEL:w` and `ref` counts match the website exactly.)
> 2. Anabar. The documentation says Anabar Dolgan is not included, but the .coma marks three texts (AnKA_2009_Games_nar, AnKA_2009_Story_nar, ChAPa_NN1_2009_Taboo_nar) and two speakers with the dialect "Anabar". Which is correct?
> 3. Terminology. Is the label PST2 (morph BIT) the form that Däbritz (2022, 2023) calls the postterminal? Is the particle glossed EVID (eːt) the grammaticalised copula form äbit?
> 4. Annotation coverage. SyF and SeR are filled in for 50 of the 136 Dolgan texts. Were these texts chosen by some criterion (for example, a particular collection or project), or is coverage simply incomplete? This matters for us because we want to compare speakers born in different decades.
>
> With best regards,
> Jude [surname] and Dustan [surname]

## 5. After desktop Claude finishes 003: the pilot (Gate 2)
Open `data/derived/workbooks/pilot_sheet_A.xlsx` (Jude) and `pilot_sheet_B.xlsx` (Dustan) on Jude's computer. They hold the same 40 items. Code them **separately**, without talking about them, using the dropdowns in the yellow columns. Then ask any Claude session to run:
`python3 shared/workbook.py merge data/derived/workbooks/pilot_key.csv <A.xlsx> <B.xlsx> data/derived/workbooks/pilot`
It reports values outside the codebook and the agreement for each column. Discuss every disagreement and revise the codebook. That is Gate 2.

---

## Results
*(Jude or Dustan fills in)*

- **Decisions confirmed or changed:**
- **evidentiality/PLAN.md updated:** yes / no
- **What Däbritz §6.6 says about PST2 and eːt:**
- **What Siegl (2015) uses to identify secondary predicates:**
- **Email sent (date), reply (date and summary):**
