# Combining shared comparisons with the exponent-19 height bound

**Proposal, 6 November 2026.** This is an additive refinement of Version 5 at
`bf2fe53459c0cceff74566ea9b966eca54d11ca5`, using the exponent-19 theorem in
the preserved Version 4 manuscript. It retains the original arithmetic inputs
and the Version 5 simultaneous-prime theorem. The argument below is an AI
author derivation and self-review, not independent mathematical refereeing.
Finite certificates check the compiled equations, not those arithmetic inputs.

## 1. Two scalar norm identities

In the scalar block, $r\ne0$ is explicitly guarded and the first four leaves
are $l_i=Y_i/r$. Thus
$$
N_r(1,l_1)=1+Y_1l_1,\qquad
N_r(l_2,l_3)=l_2^2+Y_3l_3.
$$
Indeed $rl_i^2-Y_il_i=l_i(rl_i-Y_i)=0$. These substitutions retain the
leaf-defining equations, all nonzero guards, and the exact values of the norm
nodes. They therefore preserve the entire source projection in both directions.
Each new right-hand side is quadratic in existing affine values and needs one
assignment instead of two. This implements the two optional savings described
in upstream `quartics/quartic-1272/optimization/REPORT.md`.

## 2. Lower comparison precisions

Use Version 4, `thm:quartic-height19`, with
$$
H=2(2^{109}210^{1800})B_*^{19}+128,
\qquad 1\le H<2^{2093966}.
$$
Keep the Version 5 nine positive-square scales and its sixteen field tests.
Change the beta order from 16 to 12, and each high comparison order from 52
to 40. Consequently the logarithms use $G_2$ and $G_9$, respectively, and
the denominator logarithms have order 40.

These polynomials are nonzero by `lem:quartic-reciprocal-nonzero`, whose
dyadic argument covers all truncation degrees. Version 4 explicitly consumes
these same two truncations. To cover inert primes as well as split primes,
apply the proof of Version 5 `lem:v5-unramified-log` with $m=e/4=3,10$.
Its argument only requires $1\le m\le16$. For a formal point with
$r=v(z)\ge1$, $v(Df^2)=4r$; the omitted terms have valuation at least
$er$, and hence the logarithm error has valuation at least $(e+1)r$.
The factorial denominator bound and the large-index estimate are unchanged.
Thus relative errors have orders 12 and 40 at every unramified place.

The proof of `lem:v5-two-anchors` uses the assigned orders only through
these errors and the corresponding cross tests. At least one of $h,h-4$
is a $p$-unit; both ratios become integral and subtracting their two
congruences gives $4L_i\equiv4n_i$. Thus the new source yields
$L_i\equiv n_i\pmod{p^{12}}$ for beta and modulo $p^{40}$ for the
three other labels. The sixteen tests have order multiplicities ten, two,
and four for orders 1, 12, and 40.

The one-place detector lemma is stated for arbitrary positive integer
orders. All nonzero guards on $F_5(t)$, $\delta$, $e$, $W$, and its trace
remain in place. With $e=(A\delta)^5/F_5(A\lambda)$, its weights are
$$
q_1=e/\delta^3,\qquad q_{12}=q_1e^{22},\qquad q_{40}=q_1e^{78}.
$$
These are exactly $\delta^{-2m-2}R^{1-2m}$ for $m=1,12,40$,
since $R=1/(e\delta)$. Shared elementary symmetric coefficients still
evaluate the original detector product, now grouped by these three orders.
The simultaneous addition chain
$$
1,2,3,6,9,11,22,33,39,78
$$
computes both required powers in nine multiplications. Every entry after one
is the sum of two earlier entries. Separate binary chains cost more gates;
their use initially hid the saving from the shorter logarithms.

The proof of `lem:v5-height-transfer` now uses the exponent-19 theorem on
$\phi(t)=2+1/t$. The contact radicals and exceptional primes are unchanged.
It gives $h(t_r)\le(H+\log3)M_r^{19}$; the same square-scale inequalities
therefore give
$$
h(x(Q_i))<7H|N|^{19/k}
$$
when every relevant radical to the $k$th power divides $N\ne0$.

## 3. Scalar order and the anchor

The selected variant retains scalar order 32. An exploratory order-24
variant is also generated, but has the same variable and monomial counts;
there is consequently no size reason to prefer it.

For either $s=32$ or $s=24$, the proof of `v5:scalar32-bridge` works with
leaf orders $(1,1,1,1,s,s)$. At an odd contact, descending the norm tree
gives $v_p(Y_i)>(m_i-1)v_p(r)\ge m_i-1$. Hence the formal ratio has
valuation at least $s$, and $M_5(\beta)^s\mid a$, where $a$ is the
nonzero integer label of the scalar point. The new height bound gives
$$
h(\beta)\le H|a|^{19/s}.
$$
The same completeness construction makes these finitely many valuation
bounds hold, and continuity preserves them on the progression of the
eventual shared point.

The parameter-encoded benchmark keeps Version 5's original fixed constant
$S=3^{2^{27}}$. For the ordinary-coefficient variant we can reduce it to
$$
S'=3^{2^{26}},\qquad C'=3^{2^{25}},\qquad S'=(C')^2.
$$
The three-witness anchor proof applies with this constant: its rational
quaternion criterion is valid for any positive scaling constant, and its
local calculation gives
$$
0\ne a\in 2\,3^{2^{24}-1}\mathbb Z.
$$
In particular
$$
\log_2|a|>1+\tfrac32(2^{24}-1)=25165823.5
>10(6+2093966)=20939720.
$$
Therefore $|a|>(40H)^{10}$, since $40<2^6$. This is sufficient for both
height contradictions below. It also implies, for $s=24$ or 32,
$$
h(\beta)<|a|/40,\qquad \log(40H)<|a|/40.
$$
For the first inequality, $|a|^{1-19/s}>40H$ follows from
$10(1-19/s)>1$. For the second, $x^{10}>40\log x$ for $x\ge40$.
This reduction in the anchor constant is an arithmetic refinement, not an
identity with the source specialized at the old fixed value of $S$.

## 4. Soundness

Let $B=\max(|n|,|a|,|t|,|b|)$ and $\Delta=F(a,t,b)\in\mathbb Z$.
If $\Delta\ne0$, the order-40 direct Lucas test and the height transfer give
$$
B^2-6<7H|\Delta|^{19/40},\qquad |\Delta|<5B^4.
$$
As $B\ge1$, division by $B^{19/10}$ shows
$$
B^{1/10}<(7\cdot5^{19/40}+6)H<24H.
$$
Here $5^{19/40}<\sqrt5<5/2$. This contradicts
$B\ge|a|>(40H)^{10}$. Thus $\Delta=0$. The nonzero point guards
retain $b\ne0$, so the original Lucas lemma gives
$\log B>|a|-3$.

If $\beta\ne n$, set $N=|\operatorname{num}(\beta-n)|$. The beta tests
give the corresponding twelfth-power radical divisibilities. Hence
$$
B^2<7HN^{19/12}+6,\qquad N\le2e^{h(\beta)}B.
$$
It follows that $B^{5/12}<40He^{19h(\beta)/12}$, using
$7\cdot2^{19/12}+6<40$, and therefore
$$
\log B<\frac{12}{5}\log(40H)+\frac{19}{5}h(\beta)
<\frac{31}{200}|a|<|a|-3.
$$
This is a contradiction. Thus $\beta=n\in\mathbb Z$, and
$X\in\mathbb Q$, $X^2=\beta-2\in\mathbb Z$ imply $X\in\mathbb Z$.

## 5. Completeness and dependencies

For integral $X$ use the Version 5 completeness proof with the new finite
orders and the chosen anchor constant. Its anchor subgroup still contains
arbitrarily divisible positive indices. The scalar continuity argument
and the real progression argument apply to the new rational functions;
the truncation nonvanishing just checked prevents new logarithm poles.
Choose the sixteen-test valuation and real bounds before the prime pattern.

Use the unchanged Version 5 simultaneous-prime theorem to choose primes of
the forms $u+c_jw^2$, with the prescribed Gaussian classes and avoidance
of the odd factors of the continuity modulus. Its CRT argument then gives
the same shared $h$. The exact ratios are the integer labels, so the new
logarithm estimates supply all assigned orders; the direct Lucas test
vanishes to order 40. The detector proof is uniform in the positive test
orders. Increasing the divisibility and real size prescribed for $w$ and
$u/w^2$ supplies its same local-square and preparation-zero bounds. The
scalar norm identities of section 1 leave its values unchanged. The
original pole-completeness inputs then furnish all witnesses.

Our earlier CPO lemma concerns affine prime patterns in two active variables.
It is not substituted for the stronger quadratic-pattern input here. In
particular this proposal retains the Version 5 Sun appendix and its source
qualifications, including the local correction to the Gowers-norm exponent
in the Frei–Tinková argument (`rem:v5-ft-norm-repair`). No new independent
verification of that full external proof is asserted.

## 6. Ordinary coefficients

Introduce a chain starting at the explicit integer $3^{1024}$:
$$
c_{10}=3^{1024},\qquad c_{j+1}=c_j^2\quad(10\le j<26).
$$
There are seventeen new coordinates, uniquely determined over $\mathbb Q$,
and $c_{26}=S'$. Replace the single linear occurrence of $S$ in the translated
anchor by $c_{26}$. It multiplies one anchor coordinate, so the new residual
is still quadratic. Adding the chain equations proves exact equivalence
with the refined source specialized at $S'$, preserving every original
coordinate. For the unchanged-height scalar-fused variant, extend the chain
one step further to recover the original $S$.

All resulting coefficients are ordinary integers after the compiler's
certified row normalizations. A sum of their residual squares vanishes over
$\mathbb Q$ exactly when every residual vanishes. The ordinary JSON export
contains every coefficient as an explicit integer string and has no symbolic
fixed parameter. The upstream checker's intermediate schema retains an
unused declaration of $S$ for compatibility; every coefficient has
`sPower = 0`, which is checked separately.
