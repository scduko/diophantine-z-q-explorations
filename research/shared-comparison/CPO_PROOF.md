<!-- Provenance: produced by an external AI reasoning model from a problem statement prepared in this branch, supplied by the repository owner on 2026-11-06. The supplied file has SHA-256 1235cd98a7791e4ba23aa079d0504a3b36687d4f4c0e4f599fa51418fb408d91. The only change is that the math delimiters \( \) and \[ \] were replaced by $ and $$ for GitHub rendering. Review: REVIEW_CPO_PROOF.md. -->

# One multiplier for simultaneous Gaussian Frobenius conditions

**A proof of Lemma CPO using Chebotarev prime patterns and Gaussian lattice sieves**  
**Version 1 — 6 November 2026**

## Purpose and scope

This note gives a proof of Lemma CPO under the affine-pattern hypotheses in the supplied problem statement. The principal external input is the unconditional theorem of Frei–Tinková on linear constellations of primes with prescribed Frobenius classes. The remaining argument establishes a quantitative lower bound for patterns satisfying all small-prime restrictions and uniform upper bounds for the excluded patterns.

The conclusion concerns CPO and its Chinese-remainder consequence. It does not independently verify the surrounding Diophantine-definition manuscript or the claimed variable count.

Two points are essential:

1. The Frobenius restrictions must be counted with their **conditional local densities**, accounting for the maximal abelian subextension. An unconditional product of class densities is generally incorrect.
2. In the upper-bound sieve, the constants must be independent of the small-prime cutoff. Gaussian ideal lattices make this uniformity explicit and also give a direct estimate for the large-prime tail.

## 1. Statement and assumptions

Let

$$
\Psi=(\Psi_1,\ldots,\Psi_m):\mathbb Z^2\longrightarrow\mathbb Z^m
$$

be the system of distinct affine-linear forms in the problem statement, with any repeated forms removed. We use the following established properties of that system:

- its linear parts are pairwise linearly independent over $\mathbb Q$;
- the system is admissible for simultaneous prime values;
- there is an open cone on which all its linear parts are positive;
- every prime value belongs to the prescribed progression $p\equiv c\pmod W$, and hence satisfies
  $$
  p\equiv1\pmod8,\qquad p\equiv1\pmod3,\qquad p\equiv1\pmod5;
  $$
- any additional fixed successor-roughness restrictions that are retained have a positive ordinary prime-pattern singular series.

Here the progression and forms are those specified by

$$
W=25878772920,\qquad c=18484837801,\qquad V_0=32W,
$$

$$
u=c+Wx,\qquad v=V_0(c+Wy),\qquad
\mathcal D=\{0,1,2401,-343/32\},
$$

with forms $v/V_0$, $u-\delta v$, and $u-(A_i-\delta)v$. The denominator in $-343/32$ is absorbed by $V_0$. The target-dependent admissibility assertions are inputs from the problem statement.

For a selected prime $p$, write

$$
p=a^2+b^2,\qquad a\text{ odd},\qquad
 d_p^-=(a-1)^2+b^2=p+1-2a,\qquad
 d_p^+=(a+1)^2+b^2=p+1+2a.
$$

The unordered pair of orders does not depend on the sign chosen for $a$.

**Theorem (CPO).** For every lower bound, there is a prime pattern above that bound such that its orders can be oriented as $d_{p,1},d_{p,2}$ with

$$
\gcd(d_{p,1},d_{p,2})=4,
$$

$$
\gcd(d_{p,1},d_{p',2})=4\quad(p\ne p'),
\qquad
p'\nmid d_{p,1}\quad(p\ne p').
$$

Moreover, $p\nmid d_{p,1}d_{p,2}$. Consequently, for every fixed positive integer $N$, one integer $h$ simultaneously satisfies

$$
h\equiv0\pmod{d_{p,1}},\qquad
h\equiv4\pmod{d_{p,2}},\qquad
h\equiv4\pmod{p^N}
$$

for every selected prime $p$.

In fact, the proof excludes every odd common divisor between any orders belonging to two different selected primes, a stronger conclusion than the displayed cross condition.

## 2. Counting region and order of choices

Choose a fixed rectangular box $B\subset\mathbb R^2$, with positive area, lying strictly inside the common positivity cone. For sufficiently large $X$, all points $\mathbf n\in XB$ satisfy

$$
c_\Psi X\leq \Psi_\nu(\mathbf n)\leq C_\Psi X
\qquad(1\leq\nu\leq m)
\tag{2.1}
$$

for positive constants depending only on the fixed system and the box.

We count the two active variables. The unused third coordinate in the original formulation simply multiplies all bounds by a factor of order $X$.

If successor-roughness restrictions are desired, fix their cutoff $L$ at this stage. Such restrictions mean exclusion of **odd** prime factors of $p+1$; exclusion of the prime $2$ would be impossible. They can be expressed as a finite union of congruence conditions on $\mathbf n$.

The subsequent order of choices is:

1. fix the targets, system, box, and optional cutoff $L$;
2. choose a sufficiently large fixed cutoff $L_0$;
3. let $X$ tend to infinity.

No theorem uniform in a ray modulus growing with $X$ is used.

## 3. The external prime-pattern theorem

Frei–Tinková, Theorem 1.4 of [FT], proves an unconditional Green–Tao–Ziegler asymptotic for a finite-complexity system of affine-linear forms whose prime values have prescribed Frobenius conjugacy classes in fixed finite Galois extensions of $\mathbb Q$. The theorem extends to finite unions of conjugacy classes by finite summation.

Its leading constant incorporates compatibility with the maximal abelian subextensions. Corollary 1.6 gives the corresponding existence criterion.

This supplies the appropriate version of Hypothesis H: a unit- and conjugation-stable set of Gaussian ray classes is a union of rational Frobenius conjugacy classes. The statement with an uncorrected product of unconditional class densities is not valid in general. Below we compute enough of the abelian compatibility and conditional densities to obtain the required uniform lower bound.

## 4. Gaussian ray classes and their abelian information

Set

$$
R=\prod_{\substack{\ell\leq L_0\\\ell\text{ odd prime}}}\ell,
\qquad F=\mathbb Q(i),
$$

and let $H_R/F$ be the ray class field of modulus $2R\mathbb Z[i]$. This modulus is sufficient: parity distinguishes the odd coordinate, and goodness only uses the square of that coordinate modulo odd primes.

Since $\mathbb Z[i]$ has class number one,

$$
A:=\operatorname{Gal}(H_R/F)
\simeq \frac{(\mathbb Z[i]/2R)^\times}{\{\pm1,\pm i\}}
\simeq \frac{(\mathbb Z[i]/R)^\times}{\{\pm1\}}.
\tag{4.1}
$$

For the second identification, multiply a representative by a unit to make it congruent to $1\pmod2$. Its real coordinate is then odd and its imaginary coordinate even. The remaining ambiguity is multiplication by $-1$.

Complex conjugation preserves the modulus, so $H_R/\mathbb Q$ is Galois and

$$
G:=\operatorname{Gal}(H_R/\mathbb Q)
\simeq A\rtimes\langle\sigma\rangle,
\qquad \sigma(u)=\bar u.
\tag{4.2}
$$

**Lemma 4.1.** The maximal abelian subfield of $H_R/\mathbb Q$ is

$$
H_R^{\mathrm{ab}}=\mathbb Q(i,\zeta_R).
\tag{4.3}
$$

**Proof.** For each odd $\ell$, the algebra $\mathbb Z[i]/\ell$ is either $\mathbb F_\ell\times\mathbb F_\ell$ or $\mathbb F_{\ell^2}$. In either case the norm map on units surjects onto $\mathbb F_\ell^\times$, and its kernel consists of the elements $u/\bar u$. Thus, by the Chinese remainder theorem, the same assertion holds modulo $R$.

The commutator subgroup of (4.2) is the image of these norm-one elements in $A$. Quotienting by it gives

$$
G^{\mathrm{ab}}\simeq (\mathbb Z/R)^\times\times C_2.
$$

The cyclotomic extension $\mathbb Q(i,\zeta_R)/F$ is contained in the ray class field: its Artin map on an ideal is given by the ideal norm modulo $R$, and it is trivial on the principal ray subgroup. Its degree over $\mathbb Q$ is $2\varphi(R)$, equal to the order of the abelianization just computed. This proves (4.3). ∎

In particular, above a rational prime that splits in $F$, the abelian information is exactly its norm residue modulo $R$. There are no additional abelian conditions on the odd coordinate.

## 5. A lower bound for small-prime goodness

Call $p=a^2+b^2$, with $a$ odd, **$L_0$-good** if

$$
\ell\nmid (p+1)^2-4a^2=d_p^-d_p^+
$$

for every odd prime $\ell\leq L_0$.

For a nonzero residue $t\in\mathbb F_\ell^\times$, define

$$
g_\ell(t)=
\frac{\#\{(a,b)\in\mathbb F_\ell^2:
 a^2+b^2=t,\ (t+1)^2\ne4a^2\}}
 {\#\{(a,b)\in\mathbb F_\ell^2:a^2+b^2=t\}}.
$$

The denominator is $\ell-\chi_{-4}(\ell)$. The excluded equation gives at most two values of $a$, each with at most two values of $b$. Consequently,

$$
g_\ell(t)\geq1-\frac4{\ell-\chi_{-4}(\ell)}
\geq1-\frac4{\ell-1}>0
\qquad(\ell\geq7).
\tag{5.1}
$$

At $\ell=3,5$, the prescribed progression gives $t=1$, and direct enumeration gives

$$
g_3(1)=g_5(1)=\frac12.
\tag{5.2}
$$

The goodness condition is well defined on (4.1), invariant under conjugation, and therefore defines a union of conjugacy classes in $G$. Conditional on a fixed allowed norm residue, the good proportion is

$$
\prod_{\ell\mid R}g_\ell(t\bmod\ell).
\tag{5.3}
$$

The quotient by the global sign does not change this proportion, since goodness is sign invariant. Passing from ray classes to rational conjugacy classes likewise leaves the proportion unchanged when classes are weighted by their sizes.

By (5.1), (5.2), and Mertens' theorem,

$$
\prod_{\ell\mid R}g_\ell(t\bmod\ell)
\geq \frac14\prod_{7\leq\ell\leq L_0}
 \left(1-\frac4{\ell-1}\right)
\gg (\log L_0)^{-4},
\tag{5.4}
$$

uniformly over allowed norm residues.

Apply [FT, Theorem 1.4], summing over all good conjugacy classes rather than choosing just one class. Lemma 4.1 identifies the necessary abelian compatibility, and (5.4) bounds the loss in every admissible residue fiber. Refining the fixed ordinary congruence restrictions to a modulus containing $4R$ does not change their ordinary singular series. The modified singular series is at least a constant times $(\log L_0)^{-4m}$ times that ordinary series.

It follows that, for each fixed sufficiently large $L_0$,

$$
\#\{\mathbf n\in XB\cap\mathbb Z^2:
\text{all }\Psi_\nu(\mathbf n)\text{ are }L_0\text{-good primes}\}
\geq
\frac{c_{\Psi,L}}{(\log L_0)^{4m}}
\frac{X^2}{(\log X)^m}
\tag{5.5}
$$

for all sufficiently large $X$. The positive constant $c_{\Psi,L}$ is independent of $L_0$; the threshold for $X$ may depend on $L_0$.

The weighted von Mangoldt asymptotic converts to (5.5) because of (2.1). Prime powers of exponent at least two contribute a lower-order term: for one form there are $O_\Psi(\sqrt X\log X)$ possible proper prime-power values and $O_\Psi(X)$ points on each corresponding affine line.

## 6. A uniform elementary sieve estimate

We record the sieve bookkeeping used below. All exceptional sieve primes belong to a fixed finite set $E_\Psi$, except for the collision prime $\ell$, which is also omitted. Enlarge $E_\Psi$ to contain small primes as necessary.

Suppose a product of integral polynomials in four variables has, modulo each remaining prime $q$, zero density

$$
g(q)=\frac{m+2\chi_{-4}(q)}q+O_\Psi(q^{-2}).
\tag{6.1}
$$

For a squarefree modulus $d$, the number of zero classes is at most $C_\Psi^{\omega(d)}d^3$. In a box of side $T$, elementary counting of residue classes gives a remainder

$$
O_\Psi(C_\Psi^{\omega(d)}T^3)
\qquad(d\leq T)
$$

after the volume term. The Selberg upper-bound sieve, with weights supported on $d\leq Z$, consequently gives

$$
\#\{\text{sifted points}\}
\ll_\Psi \frac{T^4}{(\log Z)^m}
             +T^3Z^{2+o(1)},
\qquad Z^2\leq T.
\tag{6.2}
$$

To see the dependence in the error, expand the square of the Selberg weight. The moduli are $[d,e]\leq Z^2$. The usual weights satisfy bounds of the form $Z^{o(1)}$, uniformly here, and the sum of the remainders over $d,e\leq Z$ is $T^3Z^{2+o(1)}$. These bounds depend on the fixed local-root bounds, not on the sizes of the polynomial coefficients.

The sieve dimension is $m$: the character term in (6.1) has bounded contribution to the logarithm of the sieve product, by the prime number theorem in the fixed progression modulo $4$. Omitting one additional prime $\ell\notin E_\Psi$ changes the sieve estimates by a bounded factor, uniformly in $\ell$.

Similarly, in a three-dimensional box of side lengths $T,T,X$, with $X\geq T$, zero density

$$
g(q)=\frac{m+\chi_{-4}(q)}q+O_\Psi(q^{-2})
\tag{6.3}
$$

gives

$$
\#\{\text{sifted points}\}
\ll_\Psi \frac{T^2X}{(\log Z)^m}
             +TXZ^{2+o(1)},
\qquad Z^2\leq T.
\tag{6.4}
$$

Indeed, there are $O_\Psi(C_\Psi^{\omega(d)}d^2)$ zero classes, and their total counting remainder is $O_\Psi(C_\Psi^{\omega(d)}TX)$.

These are standard Selberg-sieve estimates with explicit elementary distribution errors. No distribution theorem for prime values of quadratic forms is being assumed.

## 7. Cross-prime collisions for medium primes

Fix two distinct indices $r,s$. Put

$$
p=\Psi_r(\mathbf n)=N(z),\qquad
p'=\Psi_s(\mathbf n)=N(w).
$$

The map $\mathbf n\mapsto(p,p')$ is an invertible affine map over $\mathbb Q$. Every other form is therefore a fixed rational affine combination of $p,p'$. After multiplication by a fixed common denominator, the prime-testing polynomials are the two norm forms and mixed polynomials of the shape

$$
A_\nu N(z)+B_\nu N(w)+C_\nu,
\qquad A_\nu B_\nu\ne0.
\tag{7.1}
$$

The nonvanishing of both coefficients follows from pairwise independence of the original linear parts. All denominators, coefficient degeneracies, and pairwise determinants contribute only fixed exceptional primes to $E_\Psi$. Ignoring the congruences needed to recover integral $\mathbf n$ only enlarges the upper bound.

Fix signs $\varepsilon,\varepsilon'\in\{\pm1\}$. We count

$$
\ell\mid N(z-\varepsilon),\qquad
\ell\mid N(w-\varepsilon').
\tag{7.2}
$$

For split $\ell$, choose one of the two Gaussian prime factors $\alpha$ above $\ell$, and similarly $\beta$. Then (7.2) is covered by the four choices

$$
z=\varepsilon+\alpha u,\qquad
w=\varepsilon'+\beta v,
\qquad N(\alpha)=N(\beta)=\ell.
\tag{7.3}
$$

Since $|z|,|w|\ll_\Psi\sqrt X$, the four integer coordinates of $u,v$ lie in boxes of side

$$
T\asymp_\Psi\sqrt{X/\ell}.
$$

For $q\ne\ell$, multiplication by $\alpha$ and $\beta$ is invertible modulo $q$. Hence the local densities after (7.3) are those before substitution, independent of $\ell$ and of the chosen generators.

For the product of the prime-testing polynomials, that density is (6.1). Each norm form contributes

$$
\frac{1+\chi_{-4}(q)}q+O(q^{-2}),
$$

whereas each mixed quadratic (7.1), having nondegenerate rank four, contributes $1/q+O_\Psi(q^{-2})$. Any two distinct equations fix both norms modulo $q$, so their intersection has at most $O_\Psi(q^2)$ points in four variables. Inclusion–exclusion proves (6.1).

Take

$$
\eta=\frac1{10},\qquad Z=X^{1/100}.
\tag{7.4}
$$

For $\ell\leq X^\eta$, one has $T\gg_\Psi X^{9/20}$. Thus the error in (6.2) is uniformly negligible relative to $T^4/(\log X)^m$. The original prime values exceed every sieve prime by (2.1), so they are among the sifted points. We obtain

$$
\#\{\text{prime patterns satisfying (7.2)}\}
\ll_\Psi \frac{X^2}{\ell^2(\log X)^m}.
\tag{7.5}
$$

For inert $\ell$, divisibility in (7.2) forces

$$
z=\varepsilon+\ell u,\qquad
w=\varepsilon'+\ell v.
$$

Now $T\asymp_\Psi\sqrt X/\ell\gg_\Psi X^{2/5}$, and the same argument gives the stronger denominator $\ell^4$.

Choose $L_0$ larger than every prime in $E_\Psi$. Summing (7.5) over $L_0<\ell\leq X^\eta$, the signs, Gaussian prime factors, and pairs of indices yields

$$
\ll_\Psi \frac{X^2}{L_0(\log X)^m}.
\tag{7.6}
$$

Its implied constant is independent of $L_0$.

## 8. Cross-prime collisions for large primes

Write $B_1=C_\Psi\sqrt X$, increasing the fixed constant if necessary. A Gaussian prime ideal above a split prime $\ell$ is a rotated square lattice with spacing $\sqrt\ell$. Thus

$$
\#\{z\in\mathbb Z[i]:|z|\leq B_1,
 z\equiv\varepsilon\pmod\alpha\}
\ll_\Psi \left(\frac{\sqrt X}{\sqrt\ell}+1\right)^2.
$$

Only $\ell\ll_\Psi X$ can divide a nonzero order $N(z-\varepsilon)$. Throughout this range the last expression is $O_\Psi(X/\ell)$. The number of pairs satisfying (7.2), even without primality, is therefore

$$
O_\Psi(X^2/\ell^2).
$$

Summing over split primes $\ell>X^\eta$, or even over all integers in that range, gives

$$
O_\Psi(X^{2-\eta}).
\tag{8.1}
$$

For inert $\ell$, the lattice spacing is $\ell$. When $\ell\leq B_1+1$, the corresponding pair bound is $O_\Psi(X^2/\ell^4)$. When $\ell>B_1+1$, the only possible point is $z=\varepsilon$, whose norm is $1$, so it does not arise from a prime pattern. This contribution is also bounded by (8.1).

Since $m$ is fixed,

$$
X^{2-\eta}=o\left(X^2/(\log X)^m\right).
\tag{8.2}
$$

This proves the large-prime estimate without an appeal to a divisor heuristic or to a large-modulus distribution result.

## 9. Same-prime collisions

For odd $\ell$,

$$
\ell\mid d_p^-,\quad\ell\mid d_p^+
\quad\Longrightarrow\quad
\ell\mid a,\quad b^2\equiv-1\pmod\ell.
\tag{9.1}
$$

Thus $\ell$ must split in $\mathbb Z[i]$.

For $L_0<\ell\leq X^\eta$, choose a root $b_0$ of $-1$ and set

$$
a=\ell r,\qquad b=b_0+\ell s.
\tag{9.2}
$$

Choose a second independent affine coordinate $t$, for example another form in the system. After clearing a fixed denominator, the prime-testing polynomials consist of $N(a+bi)$ and expressions

$$
A_\nu N(a+bi)+B_\nu t+C_\nu,
\qquad B_\nu\ne0.
$$

The box dimensions are $T,T,X$, with $T\asymp_\Psi\sqrt X/\ell$. Away from the fixed exceptional set and $\ell$, (9.2) is invertible modulo the sieve prime. The norm equation contributes $(1+\chi_{-4}(q))/q+O(q^{-2})$, and the other equations, being linear in $t$, each contribute $1/q$. Intersections have density $O_\Psi(q^{-2})$. This gives (6.3).

Equations (6.4) and (7.4) therefore imply

$$
\#\{\text{same-prime failures at }\ell\}
\ll_\Psi\frac{X^2}{\ell^2(\log X)^m}.
\tag{9.3}
$$

For $\ell>X^\eta$, use $a\ne0$ and $|a|,|b|\leq B_1$. Since $\ell\mid a$, necessarily $\ell\leq B_1$. For each such prime, there are at most

$$
O\left(\frac{B_1}{\ell}
\left(\frac{B_1}{\ell}+1\right)\right)
$$

pairs $(a,b)$ satisfying (9.1). Summing and allowing $O_\Psi(X)$ values of the independent coordinate gives

$$
O_\Psi\left(X^{2-\eta}+X^{3/2}\log X\right)
=o\left(X^2/(\log X)^m\right).
\tag{9.4}
$$

Summation of (9.3) contributes $O_\Psi(X^2/(L_0(\log X)^m))$, with a constant independent of $L_0$.

This establishes the same-prime coprimality needed here directly; it does not require transferring an earlier same-prime estimate to a newly restricted family.

## 10. A selected prime dividing another order

Suppose $p'=\Psi_s(\mathbf n)$ divides one of the orders at $p=\Psi_r(\mathbf n)$, where $r\ne s$. Then

$$
N(z\pm1)=jp'
$$

for a positive integer $j=O_\Psi(1)$, by (2.1).

There are $O_\Psi(X)$ Gaussian integers $z$ with $N(z)\ll_\Psi X$. Each choice of $z$, sign, and $j$ determines both $p=N(z)$ and $p'=N(z\pm1)/j$. Independence of the two affine forms determines $\mathbf n$ uniquely over $\mathbb Q$, and hence gives at most one integral point. The total number of such patterns is therefore

$$
O_\Psi(X)=o\left(X^2/(\log X)^m\right).
\tag{10.1}
$$

The estimate excludes divisibility by a selected prime in either order, which is stronger than (X2).

If desired, discard coincidences $\Psi_r(\mathbf n)=\Psi_s(\mathbf n)$ as well. Each is a nontrivial affine-line condition and contributes only $O_\Psi(X)$ points.

## 11. Completion of the counting argument

Every $L_0$-good prime has both orders free of odd prime factors at most $L_0$. By Sections 7–10, the number of additional failures among all prime patterns is at most

$$
\frac{C_\Psi}{L_0}\frac{X^2}{(\log X)^m}
+o_{\Psi,L_0}\left(\frac{X^2}{(\log X)^m}\right),
\tag{11.1}
$$

where $C_\Psi$ is independent of $L_0$. These are upper bounds for unrestricted prime patterns, so they also bound failures among the patterns counted in (5.5).

Choose a fixed $L_0$, larger than the exceptional primes, such that

$$
\frac{C_\Psi}{L_0}
<\frac{c_{\Psi,L}}{2(\log L_0)^{4m}}.
\tag{11.2}
$$

Such a choice exists because $L_0/(\log L_0)^{4m}\to\infty$. Then choose $X$ sufficiently large. Equations (5.5), (11.1), and (11.2) show that surviving patterns exist, and indeed have order $X^2/(\log X)^m$ in this fixed family.

For a surviving pattern:

- the two orders at each prime have no common odd divisor;
- orders at different selected primes have no common odd divisor, for any choices of signs;
- no selected prime divides an order at a different selected prime.

All selected primes exceed any prescribed lower bound once $X$ is large enough.

## 12. Orientation and the common multiplier

Since $p\equiv1\pmod8$ and $a$ is odd, both orders are divisible by $4$, and

$$
d_p^-+d_p^+=2(p+1)\equiv4\pmod{16}.
$$

Exactly one order is congruent to $4\pmod8$. Define it to be $d_{p,2}$; define the other to be $d_{p,1}$. Thus

$$
v_2(d_{p,2})=2,\qquad v_2(d_{p,1})\geq3.
$$

The odd-divisor exclusions imply

$$
\gcd(d_{p,1},d_{p,2})=4,
\qquad
\gcd(d_{p,1},d_{p',2})=4\quad(p\ne p').
$$

For sufficiently large $p$, the inequality

$$
|1\pm2a|\leq1+2\sqrt p<p
$$

and the fact that $1\pm2a\ne0$ show that $p\nmid d_p^-d_p^+$.

Now consider all congruences

$$
h\equiv0\pmod{d_{p,1}},\qquad
h\equiv4\pmod{d_{p,2}},\qquad
h\equiv4\pmod{p^N}.
$$

Congruences with equal right-hand sides are automatically compatible. Between a zero congruence and an order congruence with right-hand side $4$, the gcd is exactly $4$. Between a zero congruence and a prime-power congruence, the moduli are coprime by the divisibility exclusions and the preceding same-prime observation. Thus every pair is compatible, and the generalized Chinese remainder theorem produces the desired integer $h$. This proves CPO. ∎

## 13. What the argument supplies

The proof supplies the particular quantitative form of Hypothesis H required for CPO, with the correct abelian local factors. It also verifies the uniformity of the medium-prime sieve and replaces the large-prime sketch with a direct lattice estimate.

The choices $\ell\leq X^{1/10}$ and sieve-weight support $d\leq X^{1/100}$ are deliberately conservative. No optimization is needed. Restoring the unused coordinate changes the lower bound and medium-prime upper bounds from $X^2$ to $X^3$, the cross large-prime bound to $O_\Psi(X^{3-1/10})$, and the selected-prime divisibility bound to $O_\Psi(X^2)$.

The only prime-pattern input beyond ordinary sieve theory is the fixed-field Chebotarev extension of Green–Tao–Ziegler. Gaussian-prime orthogonality against norm-composed nilsequences does not need to be proved separately.

## Reference

**[FT]** Christopher Frei and Magdaléna Tinková, *Linear constellations in primes with arithmetic restrictions*, with an appendix by Christopher Frei, Joachim König, and Magdaléna Tinková. arXiv:2408.17441v3, 5 November 2025. See Theorem 1.4, formula (1.15), and Corollary 1.6 for prescribed Artin symbols, the local-factor formula, and the existence criterion.

- Abstract and version information: <https://arxiv.org/abs/2408.17441v3>
- Full text: <https://arxiv.org/pdf/2408.17441v3>

The Artin-symbol theorem used here is unconditional. The separate primitive-root theorem in the same paper has a Riemann-hypothesis assumption and is not used.
