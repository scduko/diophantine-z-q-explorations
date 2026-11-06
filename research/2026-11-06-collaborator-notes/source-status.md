# Current source status and frozen generator labels

The source selected by Version 4 is `target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-4a82d9a8dc1b`. The [current inventory](../../docs/quartic-4973/README.md) and [release evidence](../../docs/quartic-4973-validation/RELEASE_EVIDENCE.json) identify its acceptance, finite replay and remaining source qualifications.

The phrase `EXPLORATORY SOURCE` in the frozen [source entry](../../quartics/quartic-4973/source-entry.json) is a generator-era metadata value, not the latest acceptance decision. The phrase following it, that arithmetic acceptance is outside the algebraic checker, remains correct. A passing checker establishes the exact algebraic transformations and expansion; it does not prove the arithmetic characterization of the source.

The current source-entry SHA-256 is `39af6e354ce265a7954c2fbae53373862a89f81114e6c24c56eb9ff3020d9857`. Changing even this descriptive field would change the pinned artifact. The literal field is preserved in the research update so existing independent replay and hash comparisons remain valid. This clarification supersedes the old label for readers; replacing it in generated artifacts is deferred to a regeneration that also updates and validates all dependent pins.

The received [Fable audit summary](fable-repository-audit.md) records the label finding and distinguishes reported finite checks from arithmetic review limits.
