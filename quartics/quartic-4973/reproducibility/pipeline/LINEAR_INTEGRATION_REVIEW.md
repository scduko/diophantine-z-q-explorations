# Independent linear-pole integration review

Static review and the bounded three-batch test pass. This approves the local
wrapper design and tested delta, not a complete generated source or artifact.

Exact files in source-pipeline/sub5000/normalized-linear-pole:

| File | SHA-256 |
| --- | --- |
| linear_pole_kernel.py | 01622f4c3f126d2c6bb190c0a4f87e7a22d45546baee99a33837c6ba60e96f1d |
| audit_linear_pole.py | 956d1f3f5d6e38248fde0edbedbf3c2ef5a175f89ac8770bb711a1490742ff9a |
| test_linear_integration.py | c7ddc64dc2678ef19d807693c693ff81cb148338ff2f171d0142328ec097e689 |

The kernel changes the exact two-row conic tail into a call to the separately
reviewed normalized10 literal. The wrapper verifies all three new call inputs
and corresponding metadata. It restores the old pole only as a specification
view, then invokes the pinned inherited whole-source checker on every retained
module and conic/field/tree equation. It enforces the new literal, exact module
set, ordinary-batch caller set and absence of old-pole calls. Extra metadata
passes through to the inherited strict checker rather than being discarded.
Boolean and floating inputs are distinguished through canonical JSON equality.

The arithmetic statement changes to the reviewed linear-unit negative-odd
exclusion. No unchanged Cayley witness or local projection equivalence is
claimed. The full source still needs its external arithmetic binding, source
reconstruction, module pins, flattening audit and final certificate replay.

I ran test_linear_integration.py with Python -E -B. All three isolated batches
passed the inherited conic checker, and all 75 semantic negatives were rejected.
The test changes retained equations, field/norm bindings, each call slot,
private-theta capture, old metadata, integer types, literal rows and signatures.
Resource failures from the inherited core are not caught as semantic rejection.
The run emitted no complete source and performed no artifact expansion.
