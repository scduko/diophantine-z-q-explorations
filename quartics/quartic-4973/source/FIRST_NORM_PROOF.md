# Fuse the first packed numerator with the constant norm node

This proposal changes the arithmetic source's first packed denominator and
then applies an exact rational coordinate change. It is not a fixed-witness
equivalence to the old denominator-r-squared source. No emitted source or
endpoint saving is claimed here.

## The unchanged conic and valuation lemma

Each batch retains rational theta, s, S with

    S=s^2, theta^2-r*S=2.

Consequently r and s are nonzero: either zero would give a rational square
root of 2. This is a global rational fact, independent of which primes are
consumed by soundness. At r=0 the isolated new equation below would indeed
admit extraneous solutions; the retained conic excludes that branch.

Let p>76176 have odd valuation R=v_p(r). The unchanged conic argument gives
delta=v_p(theta^2-2)>0 odd, theta a unit, and a unique p-adic root rho of 2
close to theta, with v_p(theta-rho)=delta. The unchanged upper binary norm
argument and one-sided pole exclude R<0. They give R>0 and, for every
virtual leaf W, v_p(W)>-R. These are precisely the old tree conclusions;
no integrality of field coefficients or bound on R is added.

For F=A+B*sqrt(2), put

    Y=A+theta*B,
    T=2*A*Y-A^2+2*B^2=Y^2-(theta^2-2)*B^2.

For any integer e>=1 the weaker bound v_p(T)>=2e-1 already gives
v_p(A+rho*B)>=e. Indeed the two summands of T have distinct valuation
parities, so neither cancels the other. Both 2*v_p(Y) and delta+2*v_p(B)
are at least 2e-1. Hence v_p(Y)>=e and

    delta+v_p(B) >= e+(delta-1)/2 >= e.

Apply the ultrametric inequality to
A+rho*B=Y+(rho-theta)*B. The same argument covers Y=0 or B=0 by valuation
infinity. If T=0, distinct parities force Y=B=0 at this place, so F=0.
Negative valuations of A and B were never excluded.

More generally a virtual denominator r^(2e-1) would suffice: from
v_p(W)>-R we obtain v_p(T)>(2e-2)R>=2e-2, then the preceding integer bound.
This proposal uses only e=1. It does not change any high-order power.

## Only the first field changes its denominator

The designated field is original field index 0, H.f, of order 1, in each
of q_conic13, q_conic6 and q_conic10. It is the first sorted field, directly
after the literal 1 leaf. All other fields retain their old denominator,
including the independently typed shared-square field at indices 5,2,4.

The old first leaf was W_old=T/r^2. Instead define the virtual first leaf

    W=T/r.

Then v_p(W)>-R gives v_p(T)>0, enough for the original order-one test by
the lemma above, for every positive odd R. All remaining field deductions
are exactly the old ones. No field order, contact, prime or orientation
condition changes.

For integer completeness retain the existing choice of raw contacts,
points and field coefficients before theta. At an ordinary selected prime
with R=1, the old depth-two approximation gives v_p(T)>=2. Thus W=T/r is
integral, as all other virtual leaves are. The constant-first tree root
remains a unit there. More generally multiplying the old first virtual
leaf by r preserves its required integrality whenever R>0. At the real
place r>0 makes every binary norm nonnegative and the constant path
strictly positive. For fixed nonzero r, the new leaf is a polynomial in
theta with rational coefficients. The old simultaneous approximation near
the selected root and near 3/2 at the exceptional places therefore still
applies to the same one-sided linear pole proof. No new division by a
field value or by a norm node is introduced.

These facts give the same global input projection through the existing
integer completeness and soundness theorem. They do not preserve an
arbitrary old private tuple or its old norm-root value.

## Exact fusion after that arithmetic change

The first binary node of the virtual tree is N=1+r*W^2. Replace the virtual
W coordinate by T and compile the two rows as

    T-2*A*Y+A^2-2*B^2=0,
    r*N-r-T^2=0.

Retain Y-A-theta*B=0 and every other row. Both displayed rows have degree
at most two and integer coefficients of magnitude at most 2.

Forward from the virtual mixed-denominator source, set T=r*W. Reverse,
set W=T/r, using the conic-proved r!=0. The second displayed equation is
exactly r times N-1-r*W^2. Preserve N and every later norm node and pole
witness. These maps cover T=0, W=0, N=0, negative r, and all rational
coefficient values. In particular N=0 is permitted when r<0; no division
by N or T is used. If the conic is omitted, r=0,T=0 allows arbitrary N
and the equivalence fails. The checker must retain the conic unchanged.

The original coordinate ID for W can be reused for T, but its type must
change explicitly. It must occur only in its numerator equation and the
first norm-node equation. Every later tree consumer continues to use N.
Calls, higher node rows, conic rows, power definitions, and all other field
bindings are frozen. The original power r^2 is retained for other leaves
and is not counted as a deletion.

The current G-square relation can eliminate the same Y as before: the
numerator T remains eval_theta(F^2), so the existing retained-row identity
still applies. The separately shared conjugate-f(J) square is untouched.

## Cost and remaining checks

The source has the same coordinate and row counts. Its first cubic node
becomes quadratic, so its straightforward quadratic lift needs one fewer
auxiliary product coordinate per batch. There are 37 designated batch
occurrences. This is a structural estimate of 37, not a measured endpoint
delta. A current incidence/survival census and a fresh emitted source,
quadratic lift, cleanup, replay and complete coefficient check are required.

The isolated new coefficients are small. That fact does not certify the
coefficient bound of the full sum of squares.
