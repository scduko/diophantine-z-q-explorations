# Reuse the private conic parameter in the pole predicate

This is a proposed new arithmetic source. It is not a generic algebraic rewrite of the current batch with its conic coordinates fixed. It preserves the integer-defining rational-input theorem by the soundness and completeness arguments below, under the same inherited arithmetic inputs. The existing parity-square fusion packets remain unchanged.

## Exact input contract

At one ordinary comparison occurrence retain its raw contact r, private rational conic coordinates theta,s_c,S_c, and equations

```text
S_c=s_c^2,       theta^2-r*S_c=2.
```

Retain the current fixed ordered field coefficients A_i,B_i and positive orders e_i. They are independent of theta,s_c,S_c. The packed nodes and upper norm tree are exactly the current ones:

```text
W_i(theta)=(A_i^2+2*A_i*B_i*theta+2*B_i^2)/r^(2e_i),
N_r(a,b)=a^2+r*b^2,
W(theta)=the upper tree on literal 1 and the W_i(theta).
```

The source writes these without division, as in the accepted conic source. The conic implies r!=0 and s_c!=0 over Q, since otherwise theta^2=2. Thus for fixed r and field coefficients, every W_i and W is a polynomial in theta with rational coefficients. No new dependence of any field coefficient on theta is allowed.

The old pole argument is b=r*W^2. The proposed replacement deletes its two argument gates and old pole module, and uses the twelve private variables D,U,L,z,e,p,c,w,s_p,q,j,k with ten quadratic equations:

```text
D=4*theta^2-7,
D*(U+r)=2*r,
L=W*U,
z=L^2,
c=r*e,
p^2-17*r-34*c+51*e*c=0,
w=c*(17*r-z),
j=s_p^2,
k=r*q,
j^2+34*j*w-867*w^2-17*q*k=0.
```

Here s_p is a new parity witness, distinct from the retained conic coordinate s_c. The maximum absolute residual coefficient is 867; all residuals have integral coefficients and total degree at most two. Do not use this pole module on the unchanged scalar-height batch, which lacks the required paired private conic.

## Every new solution extends to the old source

For rational theta, D is nonzero: D=0 would imply (2theta)^2=7. Define

```text
t=2*s_c,
U=r*(9-4*theta^2)/(4*theta^2-7).
```

The conic gives `1+r*t^2=1+4r*s_c^2=4theta^2-7=D`, so the first two new equations force exactly the old Cayley expression

```text
U=r*(1-r*t^2)/(1+r*t^2).
```

Set `v=4*r*s_c/D` and `a=r*v`. Directly, D=1+4r*s_c^2 and

```text
U^2+r*v^2
 = r^2*((D-2)^2+4*(D-1))/D^2
 = r^2.
```

The remaining equations therefore extend to the thirteen-variable scaled parity template of `PARITY_SCALE_PROOF.md` by adding v,a and keeping U,L,z,e,p,c,w,s_p,q,j,k. Its already proved rational maps extend to the original pole predicate at b=rW^2, including W=0, while preserving every outside coordinate. Thus all original pole, norm and height soundness conclusions remain valid.

For clarity, W=0 is not excluded by the new equations. For any rational conic point, keep its D and forced U and take

```text
L=z=p=q=k=0, e=1, c=r, w=17r^2,
s_p=17r, j=289r^2.
```

All ten equations hold, and the old pole predicate at b=0 has its usual zero tuple. No division by W is needed for this branch. All other divisions in the soundness map are by D, which was proved nonzero.

## The exact fixed-U completion lemma used

The proof of the inherited seven-witness pole completeness lemma proves the following strengthened formulation, with its existing restricted converse, descent and forward-rank inputs unchanged.

Let b>0 be rational, have square reduced denominator, and be a square in Q_2,Q_3,Q_17. Put B=17b. Fix rational t_o,U_o satisfying the Cayley equation, rather than choosing them anew. If

```text
U_o^2/B < 1 at the real place,
v_2(U_o^2/B)>=3,
v_3(U_o^2/B)>=1,
v_17(U_o^2/B)>=1,
```

then the remaining old parity witnesses e_o,p_o,q_o,s_o,h_o exist for these fixed b,t_o,U_o. Use valuation infinity when U_o=0.

Here is why the existing proof applies to the fixed choices. The displayed conditions make `V=B*(B-U_o^2)=B^2*(1-U_o^2/B)` positive and square at 2,3,17. The positive squarefree representatives beta,eta of B,V have beta=17 mod24, eta=1 mod24, and 17 does not divide eta. At any odd-support prime of beta outside the exceptional set, the square denominator condition makes v(b) positive odd. The fixed Cayley equation gives v(U_o)=v(b), independently of how t_o was chosen, so `1-U_o^2/B` is a square unit. This gives disjoint supports and squareness of eta at all beta-support primes, including 17 from the explicit local condition. Conversely, odd valuation of V at an eta-support prime forces strict cancellation in B-U_o^2 with v(B)=2v(U_o); hence B/U_o^2 is a square unit there. If U_o=0, V=B^2 and eta=1, so that converse assertion is unnecessary. The inherited simultaneous-realization lemma therefore applies to beta,eta and supplies the same two points and witness rescalings as before. No later step of that proof requires additional freedom in t_o or U_o.

The exact source is the proof of `lem:original-seven-parity-completeness` and its preceding simultaneous-realization lemma in the Version 3 manuscript. Its statement already lists these real and 2,3,17 smallness conditions before the squareclass construction. This reformulation does not upgrade the inherited arithmetic review or add a new simultaneous-realization assumption.

## Completeness with the reused conic coordinate

Follow the current conic-source construction through the choice of the root data, rational targets, ordinary primes, private elliptic points and their field coefficients. At the occurrence under consideration, the raw contact has the form `r=d0^2*p`, where p is its selected ordinary prime, p>76176, p=1 mod8, and r is positive and a local square at 2,3,17. The parameter d0 is the existing rational square factor, equal to 1 for finite contacts and the proof's common denominator for the infinity contact. All field coefficients are now fixed independently of the conic.

The retained proof gives a rational point on `theta^2-r*s_c^2=2`. This smooth rational conic has weak approximation: parametrize it by lines through that rational point and approximate the parameter at finitely many places. Therefore its rational points can simultaneously approach the following local points.

* At the selected prime p, approach `(rho,0)`, where rho is the already chosen root of 2. Require the same sufficiently high approximation depth as in the current proof. Then `v_p(theta^2-2)=1+2v_p(s_c)` is positive odd and arbitrarily large. The current packed-node proof makes all W_i p-integral and the constant-left norm root W a p-unit.
* At infinity and at each of 2,3,17, approach the local point
  `theta=3/2, s_c=1/(2*sqrt(r))`.
  These points exist because r is positive at infinity and a square at the three finite places. The sign of the square root is immaterial.

These are conditions at distinct places, not competing requirements at the same prime. Repeated contact primes still use separate conics. At a local target theta=3/2, D=2 and `g(theta)=(9-4theta^2)/(4theta^2-7)` is defined and zero. Since W(theta) is a polynomial, the rational function

```text
R(theta) = (r/17)*W(theta)^2*g(theta)^2
```

is continuous and zero there, including when W itself vanishes at that local target. Consequently we can require `R<1` at infinity and valuations at least 3,1,1 at 2,3,17 respectively. At 2 the value D=2 is nonzero, so there is no continuity exception; at 17 its fixed denominator in R only changes the required approximation depth.

For any resulting rational conic point, the real norm tree has positive root W>=1 because r>0 and its literal-left path starts at 1. Hence W is a nonzero rational number and `b=rW^2>0`. At the selected prime, v_p(b)=1 by the unit property. At every other prime v(r) is even, so v(b) is even; its reduced denominator is a square. It is a square at 2,3,17 because r is a local square there and W!=0.

Set `t_o=2*s_c/W` and `U_o=W^2*U`. The Cayley relation holds at b by the square-factor rescaling, and

```text
U_o^2/(17b) = (r/17)*W(theta)^2*g(theta)^2 = R(theta).
```

Thus the fixed-U completion lemma supplies all remaining old pole witnesses for these exact choices. Divide them by the same nonzero powers of W as in `PARITY_SCALE_PROOF.md` to obtain e,p,c,w,s_p,q,j,k. Add the forced D,U,L,z. This gives every new source equation without changing any previously chosen root, elliptic or contact data. The only additional conic choice was the finite list of weak-approximation neighborhoods just proved compatible.

The new source therefore has the same rational input set of integers claimed by the current conic source under its existing arithmetic dependencies. There is no generic converse for an arbitrary fixed old conic assignment; it is not claimed.

## Cost and source-audit requirements

The new quadratic pole block has twelve private variables and ten rows. Together, the old twelve-variable pole block and its two argument gates had fourteen variables and eleven rows. Thus the predicted local quadratic saving is two variables and one row per ordinary occurrence. Relative to the already proved thirteen-variable square-factor fusion, this is one additional variable with the same ten rows. There are 37 potential ordinary occurrences; final savings require source generation, independent audit and full measured replay.

The source audit must retain the paired conic with the exact same r and theta for every call, all original packed-field inputs and powers, the constant-left tree, and the independence of A_i,B_i from the conic. It must check the twelve-variable block literally and leave the height batch unchanged. No generic q_primeparity call may be retargeted without these premises. New private variables, dropped argument gates, complete call maps and the full coefficient bound must all be checked in the new source pipeline.
