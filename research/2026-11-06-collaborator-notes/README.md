# Collaborator notes and height replacement

Research update: November 6, 2026. The published manuscript remains Version 4 with 4,973 total variables. This collection does not announce a new polynomial or a completed new proof of integer definability.

The supplied notes isolate a pole-parity assertion, give explicit local denominator-clearing constructions, and reformulate the paired-point problem. Their use of the von Känel–Kret height estimate can be replaced by the existing five-contact proof in Version 4. The replacement preserves exponent 24 and the five-contact structure. It inherits the source qualifications of that existing proof.

The project uses the collective agentic notes from Stefan Baranczuk, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry. Supplied documents retain their separate printed authorship and provenance.

## Reading order

1. Read [the height replacement](height-replacement.md) for the exact substitution, constants, dependency chain, and remaining arithmetic input.
2. Read [the comparison](comparison.md) for useful ideas, duplicates, and unsuccessful shortcuts.
3. Read the supplied [pole-parity equivalence note](supplied/paper_equivalence.pdf) and [arithmetic-input note](supplied/proof_optimization.pdf). They are unchanged originals. Their original height sections are superseded for the adapted argument by the replacement note, not silently edited.
4. For the separate reduced-precision route, read the supplied [reduced-input article](supplied/two-proofs-reduced-inputs-v3.pdf) and its [TeX](supplied/two-proofs-reduced-inputs-v3.tex). Apply the same height replacement; its other assumptions remain.
5. Read the [lower-bound note](supplied/lower-bounds-existential-integers.pdf), [TeX](supplied/lower-bounds-existential-integers.tex), and [contact explanation](supplied/contacts-explained.pdf) as separate research. The stronger lower bounds have not received a complete independent audit here.

## Status by topic

| Topic | Current disposition |
| --- | --- |
| Replacement of von Känel–Kret | Exact reduction to the existing Version 4 five-contact height proof; no new external theorem required |
| Parity predicate P | Still the unproved input of the collaborator's standalone route; this update does not re-audit or replace our restricted-converse proof |
| Paired-point reformulation | Algebra checked independently; existence of the required points is not a consequence of that calculation |
| Generator enlargement and quadratic Lucas equations | Potential precision tradeoff, with no compiled or counted improved quartic |
| 82- and 100-witness constructions | Previously supplied high-degree constructions; not new quartic records |
| Lower bounds | Supplied arguments retained for review, not all independently accepted |
| Released polynomial | Unchanged Version 4, 4,973 total variables, degree four, 72,925 monomials |

## Received repository audit

The [Fable audit record](fable-repository-audit.md) preserves the reported finite successes and arithmetic review limits. The [source-status clarification](source-status.md) explains the frozen generator-era label and the current acceptance record. The Lean target remains the approved original huge-polynomial target; it is not a quartic formalization.

## Provenance and reproducibility

[SUPPLIED_SOURCES.json](SUPPLIED_SOURCES.json) records hashes of every copied source. [ARCHIVE_CATALOGUE.json](ARCHIVE_CATALOGUE.json) records the supplied ZIP's central directory and which entries were selected. Unselected files were not republished. The two separately supplied PDFs were described as notes from Sohail Farhangi's collaborator; this collection does not infer a named author from that description. Each supplied document retains its own printed date and credits.

[DEPENDENCIES.json](DEPENDENCIES.json) pins the Version 4 manuscript and the relevant existing review records. [ALGEBRA_CHECKS.json](ALGEBRA_CHECKS.json) records the narrow algebra checks from the initial comparison. Run:

```sh
python -E -B research/2026-11-06-collaborator-notes/check_replacement.py
```

This checks source hashes, the contact convention, elementary identities and the numerical bounds used in the substitution. It is not a checker for the modularity theorem or the full arithmetic proof.

The raw supplied ZIP is identified by hash but is not nested in this collection. Selected mathematical sources are included; prompts, conversation transcripts, credentials, and redundant executable archives are excluded. Original documents retain their authorship and terms; the repository license does not relicense them.
