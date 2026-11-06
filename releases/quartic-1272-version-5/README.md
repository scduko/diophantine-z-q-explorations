# Version 5 release verification

The [Version 5 release](https://github.com/elliotglazer/diophantine-z-q/releases/tag/quartic-1272-version-5) is pinned to public snapshot `2aba1a2c458812d24d671307ed23dbde39523c07`. The archives, manuscript and polynomial package were built from that snapshot. This directory records subsequent publication and extraction checks; it is not part of those already-frozen archives.

The current archive passed authenticated extraction, all 14 polynomial reconstruction checks, inventory validation and all eight adversarial inventory tests. The full archive passed whole-file authentication and member verification. `PUBLICATION.json` lists the asset hashes verified against GitHub's server digests. `CI.json` records the successful Linux research checks on the frozen source commit.

These are finite reproducibility and source-accounting checks, not a formal verification of the arithmetic argument. The manuscript and theorem inventory retain the qualifications on external inputs, including the accepted-preprint version of Frei–Tinková and the explicit correction to its local norm estimate.
