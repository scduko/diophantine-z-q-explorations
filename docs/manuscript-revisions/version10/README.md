# Version 10: response to Issue 2

This revision addresses all nine points in [manvirjaswal's review](https://github.com/elliotglazer/diophantine-z-q/issues/2). It changes explanations, source applications and attribution. Every polynomial specification and coefficient file is unchanged from Version 9.

The [historical follow-up](../../audit-history/issue2/README.md) distinguishes arguments already present in earlier research from explanations newly incorporated into this edition. In particular, the full valuation proof predates this revision; "missing" below refers to the printed derivation, not the entire research record.

| Point | Revision |
| --- | --- |
| 1 | Credit Mazur's 1992 conjectures and projection observation; explicitly include Conjecture 2. |
| 2 | Add a general determinant-specialization lemma and prove the required generic dimensions before applying the central calibration. |
| 3 | Distinguish OpenAI's Turing-completeness result from the many-one completeness deduced here. |
| 4 | Check Kato's published 1999 prime-two hypotheses and compare its full-cochain convention with the 2004 j-star convention. |
| 5 | Print the conjugation and a dictionary for all saved templates and composition recipes. |
| 6 | Give the missing valuation inequalities and trace contradiction. |
| 7 | Add local OpenAI attribution, both converse preprints and exact source-section provenance. |
| 8 | Add the Robinson, Poonen and Koenigsmann history. |
| 9 | Explain why the no-seed congruence applies outside the coefficient filter. |

[Detailed dispositions](responses.json), [source pins and access limitations](sources.json), and [new applications and conventions](new-applications.json) record the review. The Kato comparison includes the local maps and actual retained class, rather than citing a theorem in a different cohomology convention. The coefficient-filter calculation already existed in Appendix G; the revision makes its scope explicit at the consumer.

The [revision manifest](revision.json) reconstructs Version 10 from Version 9 by exact ordered replacements. The current inventory records every citation and reference, rebinds the Version 9 application sites, and identifies changed sites and the relevant issue items. Earlier inventory files retain their historical meaning; a changed application is not labeled unchanged.

```sh
python -B docs/manuscript-revisions/version10/check.py
python -B docs/manuscript-revisions/version10/check_valuation.py
python -B scripts/check_construction.py --report build/construction-checks.json
```

The first two commands check document bindings and bounded regression cases. They do not decide the mathematical truth of the arguments. The source review is internal AI review of these nine points, not an independent verification of the whole manuscript or a completed formal proof. No new unpublished arithmetic theorem is assumed. Mazur's 1992 publisher metadata was verified but its full scan was inaccessible; the relevant conjectures and projection observation were read in the published 1995 update. Poonen's checked source is the corrected author version, not a comparison against final published typesetting.

The [current TeX](../../../manuscripts/quartic_v10.tex) and [PDF](../../../manuscripts/quartic_v10.pdf) contain the corrections. Version 9 remains available as the exact historical baseline.
