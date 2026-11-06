# Independent review of three comparator modes

PASS for the arithmetic proposal in `precision/THREE_MODE_CONTACTS.md`, SHA-256 `66311fffec418e9a6aa44f7f7503057133f92e21c4f70c3468971dd04ac55659`, with `precision/THREE-MODE-CONTRACT.json`, SHA-256 `d557c0533abdf0b750dc7c5316d5bee149c4e1e4dfdbd22da252773cb9691267`. This strengthens the separately reviewed 29-full/8-beta-only proposal. It remains a distinct source candidate and requires independent finite source validation.

## Exact coverage

The partition is correct for the frozen root37 target order A.x0,A.x1,S.x0,S.x1,T.x0,T.x1,Z.x0,Z.x1:

| Positions | Mode | Information retained |
| --- | --- | --- |
| 0 through 4 | Full | beta and all three Lucas proxies |
| 5 through 12 | Beta-only | beta |
| 13 through 20 | Lucas-only | all three Lucas proxies |
| 21 through 28 | Full | beta and all three Lucas proxies |
| 29 through 36 | Lucas-only | all three Lucas proxies |

Thus all 29 contacts covering the six S,T,Z coefficients have the three Lucas congruences. All 21 contacts covering the four A,T coefficients have the beta congruence. Each of these sets includes the common slope and infinity positions. Every raw position remains; identical values or primes do not merge positions or change their obligations.

The first contradiction is exactly the independently reviewed B_L argument. With `B_L=max(|s|,|t|,|z|)`, the high congruences give the Kth-power radical divisibilities for whichever S,T,Z point attains B_L. The bound `|Delta|<5B_L^4` then contradicts the anchor unless Delta=0. None of these uses needs the beta congruence at an S or Z position.

The key second-stage premise is stronger than a bound on B_L. The actual released `lem:o8-lucas` states `|t|>exp(|s|-3)`. Its hypotheses are unchanged: s,t,z are the integer point indices, z is nonzero, a=|s| exceeds 40, and Delta=0. Consequently `B_AT=max(|n|,|t|)` satisfies `log B_AT>a-3` without comparing t to z or n to t.

If beta differs from n, all A,T coefficient radicals have their qth powers dividing the nonzero reduced numerator N of beta-n. The 21 positions specified above are sufficient. Both points therefore satisfy the needed height estimate, and whichever realizes B_AT gives

```
B_AT^2<7H N^(h/q)+6,
N<=2 exp(h(beta)) B_AT.
```

The second inequality uses only |n|<=B_AT and the height of beta. It does not use |s| or |z|. Also B_AT>=|t|>1, so every division and bound in the existing second contradiction remains valid. The unchanged scalar batch and anchor yield `h(beta)<a/40` and `log(40H)<a/40`. Thus

```
log B_AT < (q+h)/(40(2q-h))*a < a-3,
```

contrary to the Lucas bound. At q=12, the coefficient is exactly 31/200 for H19 and 1/8 for H18. This proves beta=n and then X integral. S is still used in the scalar height estimate and anchor; its beta-specific contact tests are not needed in that estimate. No hidden inequality |z|<|t| is assumed.

## Lucas-only local module

The 26-input selection from the full boundary is correct: three proxies xi,tau,zeta; the four targets 4P_*,4S,4T,4Z; the four already-conjugated common-J coefficients; theta, epsilon, r. The index list is `[1,2,3,4,5,6,7,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]`. It excludes beta and 4A only.

Four primary points and four differences give nine formal field tests. Three primary ratios and four alternate ratios give seven order-K tests. Including the first root error gives exactly 33 rational tests, ordered `[1]*19+[K]*14`. The q_batch33 norm/pole proof is the same arbitrary finite-tree proof with the constant leaf on the left; it does not assume the original test count.

At an arbitrary odd raw-contact prime, the norm/pole argument excludes a negative odd valuation and supplies each assigned order. The root error selects the split place. Formal tests put the four primary points at that place and J and four differences at the conjugate place. The alternate tests give h0=4 modulo p^K and m_i=4n_i modulo p^K for n_i=s,t,z. Since h0 is a unit, all four finite logarithms at precision K give precisely the required integral proxy congruences. No beta statement is used or implied there.

G nonvanishing and the compressed inverse conditions remain valid for all four primary points. The beta-only module remains the separately reviewed two-point G12/G12 module. The full module is unchanged. All three modules use the same root error, raw-contact interpretation and common-J data.

## Completeness and composition limits

The target points and the 37-position rational prime-pattern construction are unchanged. Choose the common J using all selected primes. At each occurrence choose only the numerator points that its mode retains, using the same h_p CRT conditions and the same exclusions. The stronger K conditions suffice for beta-only positions since q<=K. There is no need to share private points across different occurrences. Choose theta last for the full finite collection of field-test coefficients across all three modes. Each norm tree then has the same unit-root, positivity and local-square completeness proof, including the root37 square factor at infinity. Repeated slopes and primes impose no new cross-prime compatibility condition.

The frozen contract uses the affine difference model and retains its guards. Composition with Jacobi requires the separate, explicit model change described in `jacobi/REVIEW.md`. Its local proof applies to four differences in a Lucas-only module and two in a beta-only module as well as five in a full module. The identity case gives infinite alternate valuation and causes no arithmetic obstruction. Shared target slots must be retyped explicitly; the original height coefficients remain unchanged. Any later elimination of square-root coordinates needs its own source equivalence and incidence check.

The source checker must bind every position to the exact mode and validate all three input maps, G profiles, ordered tests and norm trees. Verifying only counts 13/8/16 is insufficient because switching an A and S occurrence can lose a required congruence while preserving those counts. The independent diagnostic `verify_three_mode_contract.py` checks the positional coverage and proposed JSON contract, but does not validate any generated source or prove the universal arithmetic arguments above.

## Explicit Jacobi composition

I also reviewed `precision/THREE_MODE_JACOBI.md`, SHA-256 `9c12ff4ae8750e158a18c48b00cd5df397ee8c7697ec769f5b17d70983e181d8`. PASS for this explicit composition. It correctly retypes each four-slot target as U,q, retains the original affine height targets, uses conjugate(w) only for difference formal tests, keeps the alternate Z ratios, permits identity differences without introducing inverses, and chooses theta after all new coefficients. Its exact test lists agree with all three modes. The previously noted joint-contract distinction is therefore resolved for the source it describes. Later removal of U or primary u is not covered by that frozen note.

The finite diagnostic can be run remotely as follows; it has not been executed locally:

```sh
python3 -E -B work/quartic-sub10000-20261106/arithmetic-audit/verify_three_mode_contract.py --contract work/quartic-sub10000-20261106/precision/THREE-MODE-CONTRACT.json
```

Its SHA-256 at this checkpoint is `5b8f67b3bed7322580c2e6fdd1079d1ce458189533518eb26685520976204c41`. It checks 37 deletion mutations and seven wrong-mode mutations, in addition to the exact contract fields. It asserts no final variable count or arithmetic theorem from that finite result.
