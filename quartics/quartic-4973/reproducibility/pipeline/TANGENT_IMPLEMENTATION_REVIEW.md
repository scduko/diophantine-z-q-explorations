# Four first-tangent fragment review

Verdict: PASS for the exact target-two root transition, its inverse maps,
and the fixed-target row aggregation at the hashes below. Full source and
quartic acceptance remain with the independent composed-source audit.

| File | SHA-256 |
| --- | --- |
| elimination/sub5000/doubling-target-two/compress_doublings.py | a136e6cce43277ed63351fd1989c428c48b811b9a8682d213f6609d6a95f5cb2 |
| elimination/sub5000/doubling-target-two/PROOF.md | 3591709058c666a1dd2786d46039b408a04f1908b644c16c6f722a72788a50c8 |
| elimination/sub5000/doubling-target-two/test_doublings.py | d5f6c7e8a5c05e8503182446d89b22bf4d41ff0924ac49c2653ed5429994bee6 |
| elimination/sub5000/doubling-target-two/CONTRACT.json | d9ef1fedd0703377747353f44619d73eca47c160634757de7c477fc02c887e70 |
| probe_tangents.py | 75299d5a1118dd7d75892786079003cd8588dc0b814017ae33c82672d00b80b0 |
| PROBE.json | 91738ec7a50b766c06d8ccf1d66e65b73f7c82f5096f096fe853ede58620cae8 |

The input is the exact canonical target-two root
`1cf2a225d6aeff52adfd5f6e87ca5e4cdadcec0bd3f43d68d7ec972ce40b49b2`.
The output is
`e8b115ac5150212db52dc0a013db4a7d4c36c647c4b07f8654b9e9712239fe95`.
Canonical encoding means sorted-key compact ASCII JSON plus a newline.
These are module pins, not whole-source acceptance.

The algebra is exact over K. The retained equations give q=x^2 and
y^2=x^3-Dx, with D=11-6sqrt(2) nonzero. The new tangent equation is
2y*lambda=3q-D. Expanding

    (3q-D)(3q-2D)-9x(x^3-Dx)=2D^2

gives y[2lambda(3q-2D)-9xy]=2D^2. Therefore y is nonzero and

    h=[2lambda(3q-2D)-9xy]/(4D^2)

satisfies (2y)h=1 and lambda=(3q-D)h. The forward map forgets h;
this reverse map is polynomial in retained rational coordinates with
fixed rational coefficients. No square root, extra variable, or new
arithmetic hypothesis is needed. All other doubling equations are
unchanged, so the target point remains exactly 2Q.

I checked the full inverse incidence directly. The four removed pairs
38/39, 48/49, 58/59 and 68/69 occur only in their four corresponding
inverse/slope rows, respectively 16..19, 26..29, 36..39 and 46..49.
They occur in no call. PROBE.json records those complete row/call lists.
The independent literal transition preserves every remaining row, call,
construction event, live coordinate record and historical receipt under
one coordinate and row map. It matches all eight new tangent components
without using the producer's polynomial functions. There are 187 untouched
rows, eight replacement rows and eight deleted rows.

The fourteen fixed-target equations are unchanged under this map. I
recomputed their complete sum of squares before and after, translated
both into the same named variables and compared every coefficient with
the separately pinned FIXED_TARGET2.json. The aggregate constant remains
5,061,813,942 and the maximum absolute coefficient remains 154,563,475,872,
requiring 38 bits. This includes the overlapping shared-J terms.

The full root's sum-of-squares constant changes from 5,061,814,037 to
5,061,814,661, exactly +624. Each removed real inverse row contributed
one; each new tangent pair contributes 11^2+(-6)^2=157. Thus the increase
is four times 156. This is a root-row calculation, not certification of
the final expanded quartic's largest coefficient.

The independent probe passed complete-output comparison, 31 semantic
mutations and one resource-abort test. It bounds JSON input before copying
or serialization. After UnitScale's review, I added an import-time guard
against disabled assertions and checked that Python -O rejects the module.
The separate author suite also passed on rerun: forty
old and thirty-two new component equations, four inverse reconstructions,
the symbolic identities, all three affine two-torsion exclusions and
nine strict input-pin rejections. Only small root dictionaries were used.

The module has 210 local coordinates and 195 residual rows. These are
source counts. No final eight-variable saving is claimed. The transition
must be applied after target2_rewrite and before shared_square. The
composed source, source map, named-source binding, reduction replay and
final degree/coefficient check remain separate acceptance obligations.
