# Audit integration and historical claims

This protocol addresses the failure exposed by Issue 2: valid arguments in the research record were compressed or omitted in the manuscript, then some omissions were incorrectly described as newly repaired mathematical gaps. It cannot guarantee mathematical correctness. It makes the required evidence and remaining uncertainty visible.

## Before responding to an objection

1. Freeze the reviewed manuscript and the proposed revision by commit or SHA-256. Identify the exact claim, its inputs, and the passage that uses it.
2. Search the source inventory, earlier proof packets, corrections, and reviews. Read the actual relevant arguments. A PASS label or a source filename is not evidence that the implication was checked.
3. Classify the historical result separately from the manuscript result. The historical result is one of: prior justification found, prior inputs found but their connecting argument needs work, genuinely new argument required, attribution/history only, or unresolved. The manuscript result is: incorporated, partly incorporated, or pending. Do not call an objection a new gap merely because the printed explanation is incomplete.
4. Record what was searched, the exact evidence that supports the classification, and what was not established. Finding one prior justification does not show that every previous audit checked it independently. Failing to find a proof is not proof that none existed.

## Before marking a repair incorporated

Trace the source statement, hypotheses and conventions through the actual application to its consumer. Check the carrier, field, prime, integral versus rational coefficients, local conditions, maps, normalizations, quantifiers and relevant exceptional cases. Include the connecting argument at the application site or an explicit reference to the exact lemma that supplies it. Check both locations after editing.

For a substantive repair, obtain review by someone other than its author before describing it as independently accepted. If such review has not happened, record that limitation. Repeated reviews by the same agent are not independent reviews. For this Issue 2 historical follow-up the assessment is internal source comparison, not new independent whole-proof validation.

Update the evidence register and run its structural checker. A changed manuscript hash or excerpt must invalidate the old binding until the change is reviewed. Do not relabel all historical sites as current without comparing them. Link the exact release in any public reply, state the scope of the checks, and distinguish a document repair from a change to the polynomial or theorem.

## Release and reporting rules

- Every tracked finding needs its historical disposition, manuscript disposition, supporting evidence, and consuming passage.
- Keep unresolved items open and describe them explicitly. Do not infer global completeness from the number of completed reviews.
- A green CI result verifies only what the named checker implements. It does not certify an informal proof, establish priority, or check the truth of an external theorem.
- Preserve dated source packets and correction notes. Do not rewrite old verdicts to make the history look consistent.
- Before claiming an objection newly discovered a gap, read the historical evidence again. If earlier reporting was inaccurate, correct it explicitly.

The first register is [Issue 2](issue2/README.md). Its checker binds all nine dispositions to the exact Version 10 source and response list, checks their application passages and evidence files, and rejects unresolved historical claims marked incorporated. It also checks that the paper build still selects the bound manuscript, so merely advancing the builder to a new edition cannot silently inherit this acceptance. It does not decide whether the prose actually proves the mathematics. Future editions must retain the historical register and supply a newly reviewed binding for the current edition.
