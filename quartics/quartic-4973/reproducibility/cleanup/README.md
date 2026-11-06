# Bounded conic power-chain branch

Run `python -E -B PACKET/run.py --output FRESH_OUTPUT` on Linux.
Allow 2,400 seconds as a conservative outer bound; every child retains the
2 GiB address-space limit and separate process group. All work is sequential.

BINDING.json records the exact stage/parity baseline count. The runner
replays it with the original named-source checker, rewrites the power
circuits using the existing circuit rule, and fully replays the result.
It then runs ordinary optimize/merge and replays both with that same
original checker. The already reviewed constant/affine cleanup sequence
follows, with the frozen extended checker regenerated before any search.
Every stage must pass before its output becomes another stage's input.

The new nonsquare_product proof branch is not installed. Both unit search
and localized checker are byte-identical to the old reusable kit. The
power producer imports only unchanged polynomial helpers from that kit.
The small power-chain test is run before the research stages.

MANIFEST.json pins all files. The caller authenticates that manifest.
The baseline arithmetic acceptance remains separate from finite replay.
No projected 52-coordinate saving is claimed as a measured endpoint.
SUMMARY.json keeps the raw circuit change, pre-cleanup and full cleanup
measurements separate, including which original or extended checker ran.

`support/MIXED_MODE_DENOMINATOR_CLARIFICATION.md` supplies the arithmetic
clarification for this source: denominator order is 12 in beta-only mode
and 40 in full/Lucas mode, with every numerator order at most its mode's
denominator order. It corrects the cited proof wording without changing
source or checker bytes. Finite algebraic replay remains separate from
acceptance of the arithmetic source theorem.
