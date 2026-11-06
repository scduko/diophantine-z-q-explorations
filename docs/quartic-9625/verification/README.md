# Version 3 release checks

[REPRODUCTION.json](REPRODUCTION.json) records successful frozen-certificate
replay and clean reproduction of the selected 9,625-variable polynomial.
The package manifest is
`eb4b2ae93f932d96919d8779f937b7eec47163c8cf8909d1b66a55b1fdc08559`.
The [individual logs and finite-test reports](reproduction-logs/) accompany
that receipt. The regenerated source, residuals, variable map, weights and
expanded table agree with the frozen package. The regenerated certificate
agrees after removal of its elapsed-time field, and both certificates pass
complete replay.

This reproduction was the successful first stage of private validation run
42230959046 at commit `f9251d63c8167f9113b57b2dc840c67902eb68ed`.
The subsequent inventory command in that job omitted its required `--repo`
argument. That command was corrected separately; the reproduction receipt
does not claim that the entire earlier job passed.

The corrected inventory command, its 14 negative tests, all 57 handoff tests,
the final PDF build and rendering passed in run 42231309342 at commit
`9e57b1cf5540fb3fa77e132cb5da4a7df50bbf9c`.
[PDF_BUILD.json](PDF_BUILD.json) binds the final 192-page PDF to the TeX
source; [PDF_VISUAL.json](PDF_VISUAL.json) records the page inspection.
The final display-only correction changed two rendered pages, which were
inspected again. The other reviewed page images are byte-identical.

The handoff check also compares the original certificate with the included
[regenerated certificate](regenerated-certificate.jsonl.gz). Their 1,249
records agree after removing only the last record's elapsed-time field.
[CERTIFICATE_COMPARISON.json](CERTIFICATE_COMPARISON.json) records an
independent comparison. The final handoff suite has 65 negative cases;
[HANDOFF_TESTS.json](HANDOFF_TESTS.json) and the
[review addendum](reviews/handoff-certificate-comparison.md) cover this check.

[Review records](reviews/) distinguish the arithmetic source review,
package review, inventory review and handoff review. The finite programs
do not prove the arithmetic source theorem or complete the separate Lean
formalization. The manuscript and current theorem inventory state the
mathematical dependencies and their source-version qualifications.
