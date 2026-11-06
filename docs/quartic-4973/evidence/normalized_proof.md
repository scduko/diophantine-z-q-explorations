# Normalized local Lucas ratios

Status: separate arithmetic source proposal for independent review. The frozen joint-chart, conic and local-Lucas sources are unchanged. This construction preserves the local-Lucas root and the 13/6/10 field lists, but replaces its three Lucas quotient blocks and the evaluation of their residual. No new source or final variable count is accepted by this note.

## Exact local equations

Use K=Q(sqrt(2)), d=3-sqrt(2), D=d^2 and the same joint primary/difference chart. The common primary point is H, with retained f_H,p_H and

    Lambda p_H=G_H.

At a Lucas-bearing occurrence, let f_i,p_i,G_i denote the three numerator quantities for i=s,t,z. The G polynomials, their precisions and the field f_i tests are unchanged. Replace the old pairs C_i,B_i and equations B_i=C_i p_i, B_i Lambda=G_i by just three field pairs B_s,B_t,B_z and

    B_i Lambda=G_i,             i=s,t,z.                (1)

Introduce five field pairs P,U,V,Kc,E and impose

    P B_s=p_s,
    (U+V)p_t=P B_t,
    Kc p_t=(1-2P)B_t,
    V p_z=(1-2P)B_z,
    E=U^2-Kc V-P^2.                                    (2)

Every rational component of (1),(2) is quadratic because each G is the same unbound quadratic output expression as before. The symbol Kc is a private field coordinate, not the number field K or the precision.

The beta quotient, when present, retains both of its old pairs and both equations. The common Lambda equation is unchanged. The single Lucas field test is now E of order40. All formal and alternate tests, root points, raw contacts, the scalar batch, anchor and the beta test are unchanged.

## Nonzero facts and where division is permitted

The existing dyadic nonvanishing proof gives G_H,G_s,G_t,G_z nonzero for every value of their f coordinates. Explicitly, their constant coefficient is1 and every other coefficient has dyadic valuation1. If v_2(f)>=0 the constant term has uniquely least valuation; if v_2(f)<0 the highest term has uniquely least valuation because the truncation degree is at least2. This is the reciprocal-G nonvanishing argument, not an assertion of real positivity. Thus Lambda and p_H are nonzero, and (1) makes each B_i nonzero. These are unconditional rational-field facts for every source solution.

One also has p_t nonzero globally. If p_t=0, the second equation of (2) gives P=0 because B_t is nonzero. The third equation would then give 0=B_t, a contradiction.

Neither p_s nor p_z is asserted nonzero globally. The first equation gives P=0 if p_s=0. The fourth equation permits p_z=0 when P=1/2. These possibilities must not be hidden by invoking the old quotient blocks, since those blocks have been removed. No source equation takes an inverse of P,p_s,p_z,1-2P or U+V.

Now fix a prime p>76176 at which the current raw contact has odd valuation. The unchanged norm/pole argument makes that valuation positive and supplies all retained field orders at the selected split place. In particular v_p(f_i)>0 for every primary point. The joint-chart equations imply

    f_i p_i^2+D f_i^2=1.                               (3)

Since D is a unit at this prime, (3) gives v_p(f_i)+2v_p(p_i)=0. Consequently every p_i is nonzero, v_p(f_i) is positive even, and each primary point lies in the formal group. At this place P is also nonzero, by P B_s=p_s.

Only now define, for the local argument,

    C_i=B_i/p_i.

They are exactly the same finite-logarithm quotients G_i/(p_i Lambda) used in the reviewed local-Lucas proof. The unchanged alternate tests, doubled-point identities and reciprocal approximation imply

    C_s,C_t,C_z are p-integral,
    C_s=s, C_t=t, C_z=z modulo p^40.                   (4)

Here s,t,z are the fixed integer indices of the retained root points, not new source coordinates. In particular C_s need not be a p-adic unit in soundness. It is nonzero as a rational field element because B_s and p_s are nonzero at this occurrence.

## Exact normalized identity

At a place where the preceding divisions are legitimate, (2) gives

    P=1/C_s,
    V=(1-2P)C_z,
    U=P C_t-V,
    Kc=(1-2P)C_t.

Put X=P C_t. Then 2X+Kc=C_t and

    E=(X-V)^2-Kc V-P^2
     =X^2-C_t V+V^2-P^2
     =P^2 F(C_s,C_t,C_z),                             (5)

where

    F(S,T,Z)=T^2-S(S-2)TZ+(S-2)^2Z^2-1.

Thus F(C_s,C_t,C_z)=C_s^2 E. Since C_s is p-integral by (4), the new order40 test on E gives

    v_p(F(C_s,C_t,C_z))>=40.

Using (4) and the integer coefficients of F gives p^40 dividing the fixed integer Delta=F(s,t,z). This is exactly the conclusion required by the first height contradiction. No division by a p-adic nonunit has been discarded. The normalization strengthens the required local valuation when C_s has positive valuation; it never weakens the conclusion for Delta.

The unchanged coverage and H19/high40/anchor25 bounds force Delta=0, and the same Lucas lemma gives |t|>exp(|s|-3). The beta tests at the shared, A and T positions are unchanged, so the second height contradiction again proves beta=n and then integrality of the original input.

The case C_s=2 is included. It has P=1/2, V=Kc=0 and U=C_t/2, with E=(C_t^2-1)/4. No division by 1-2P occurs. The prime-avoidance condition below excludes primes dividing s, not primes dividing s-2.

## Joint-chart scope when a primary p_i vanishes

The joint-chart recovery of (3) does not use p_i nonzero. Its eliminant is

    -4D q^2 (f_i p_i^2+D f_i^2-1),

where q is the nonzero ordinate ratio of the unchanged shared target. Hence it still proves (3), f_i nonzero, x_i=p_i^2+D f_i=1/f_i, and that (x_i,x_i p_i) is a point on y^2=x^3-Dx.

If p_i=0, then x_i is d or -d, and the primary is a nonzero two-torsion point. This is a new permitted global branch. It cannot occur at a consumed odd-contact prime because its f_i has valuation zero there, contrary to the retained formal f_i test.

The difference graph also extends to that branch. In the notation of the joint-chart proof, let Q=(a,aq), c=a+D/a and

    U_graph=q(x_i+D f_i)+c p_i.

At p_i=0 this equals 2q x_i, which is nonzero. The graph therefore determines the finite value

    z(P_i-Q)=-q/(2x_i).

The target Q is a nonzero point in the torsion-free root group, so P_i-Q cannot be a two-torsion pole. Substituting this value in the joint identities, or using their regular extension, gives the same difference parameter and alternate field A. No new component or inverse is introduced. At consumed primes the old non-torsion formal-point argument applies verbatim; at other occurrences this larger domain imposes no arithmetic conclusion.

The source and its auditor must therefore replace the old blanket statement that every numerator p_i is globally nonzero. The correct claims are the unconditional nonzero facts for Lambda,B_i,p_H,p_t, and the local nonzero facts for all p_i at each consumed prime.

## Completeness and quantifier order

For an integral input first choose the scalar-height data and the root point S=sP_* satisfying the anchor. This fixes a nonzero integer s. Next choose the integer Lucas solution t,z and the corresponding root points T,Z, as in the existing proof. The input point A and all height targets and denominator-clearing data are now fixed. None of these choices depends on the later contact primes.

Apply the same positive linear-prime pattern construction in its prescribed open cone, with the additional finite avoidance condition that every selected prime is larger than |s|. Include the previous finite exclusions and denominator divisors in this lower bound. The inherited theorem produces arbitrarily large patterns in this cone, so removing these finitely many primes adds no analytic input. In particular no selected prime divides s. This condition may be imposed on all37 positions, although only the29 Lucas-bearing positions need it. Repeated primes between occurrences remain allowed.

Only after the contact primes are chosen, choose the common comparison J and the private primary points by the existing CRT construction. Then choose the private conic parameters last, after all new field expressions have been evaluated. This is the order

    input -> scalar/anchor S -> integer Pell T,Z and root data
          -> contact prime pattern avoiding s
          -> common J and private points -> new ratio coordinates
          -> private conics and norm/pole witnesses.

For these complete witnesses the old nonzero quotient values C_i exist. Set

    B_i=C_i p_i, P=1/C_s,
    V=(1-2P)C_z, U=P C_t-V, Kc=(1-2P)C_t,
    E=P^2 F(C_s,C_t,C_z).

These are rational field elements and satisfy (1),(2) exactly. At every assigned prime, (4) and p not dividing s make C_s a unit. The existing complete witness has v_p(F(C_s,C_t,C_z))>=40, so (5) gives v_p(E)>=40. The remaining field tests already meet their old orders. The private-conic approximation and positive norm/pole construction therefore supply all remaining witnesses, exactly as for the unnormalized local-Lucas source.

This proves equality of the final input projections. It does not assert an algebraic transformation of every old private witness: when an old C_s has positive valuation, dividing its residual by C_s^2 can fail the new order40 test. The complete witness construction avoids that situation by the explicit finite prime exclusion above.

## Source interface and cost

The root module remains byte-for-byte the root of the frozen local-Lucas source, including its removal of the three unused global proxies. All comparison free-input layouts remain58/28/47, their legacy prefixes remain28/16/23, and the theta/error/raw slots remain25/26/27,13/14/15,20/21/22. The same conic13/6/10 modules and field orders are reused without modification. The only changed field value is E at the existing Lucas position.

At each full or Lucas-only occurrence, the old three pairs C_i plus three pairs B_i plus V,D,E, nine field pairs, are replaced by B_s,B_t,B_z,P,U,V,Kc,E, eight field pairs. One field pair and one field equation disappear at each of29 occurrences, giving58 fewer raw rational coordinates and58 fewer rational residuals in this isolated block. The equations remain quadratic, and the G, norm and power circuits are unchanged. This is exact block accounting, not a measured final polynomial count; downstream sharing and elimination must still be replayed.

The named new source must bind the existing root and batches, these exact normalized equations, the unchanged beta quotient, all formal/alternate tests, and the new global/local nonzero scope. The independent checker must reject a removed formal test, a changed normalization sign or factor2, a changed numerator role, an omitted B_i equation, or an accidental claim that the tested E is the unnormalized F. Fresh source auditing, flattening, lifting, replay and coefficient expansion remain necessary.
