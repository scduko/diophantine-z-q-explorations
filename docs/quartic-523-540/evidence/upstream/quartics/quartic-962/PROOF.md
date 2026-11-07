# A 962-variable quartic with the same rational projection

Let P1272 be the frozen baseline polynomial with SHA256 `02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586`. Let P962 be `frozen/polynomial.json`, with SHA256 `6b798de7d00ac3c7d725ca0a69d39f1eac1ddb02fee2756cb6323770b952af32`. The JSON table encodes an integer polynomial by keeping S=3^(2^27) as an exact fixed coefficient expression. S is not a coordinate.

For every rational x, P1272(x,-) has a rational zero if and only if P962(x,-) has a rational zero. P962 has exactly 962 active coordinates, including x, degree four, 55,409 monomials, primitive coefficient content one, and maximum coefficient magnitude 64*S². The original input coordinate is preserved pointwise.

This is a rational-projection equivalence claim. Any claim that the projection is the integers retains the baseline's arithmetic qualifications, including its current Frei–Tinková input. None of the changes below resolves that separate arithmetic issue.

## Systems and the general extension principle

The baseline builder introduces 90 base coordinates and 47 structural equations, then polynomial assignment gates and rational quotient gates. A polynomial assignment uniquely determines its output. A quotient equation b*z=a uniquely determines its output when b is nonzero. Over K=Q(sqrt(2)), each equation means its two rational component equations, and a nonzero denominator has nonzero field norm. Every change below either proves a polynomial identity or explicitly preserves and proves a quotient's nonzero denominator.

The new raw system has 994 coordinates, consisting of the same number of base coordinates and 904 arithmetic coordinates, and 951 quadratic residuals. The base-coordinate meanings change in the point, correction and pole blocks as specified below. The unchanged compiler performs 32 certified eliminations, leaving 962 coordinates and 919 residuals. Each elimination solves a constant-linear equation and substitutes its unique solution without increasing the residual degree. Its reverse formula appears in `reduction-certificate.json`. Nonzero rational row normalizations preserve the zero set. The coordinate map fixes coordinate zero. No free or unused coordinates are omitted.

Finally, P962 is the exact sum of squares of the normalized integer residuals. A sum of rational squares is zero exactly when all its summands are zero. The full table, gate identities, elimination certificate, input map, support, coefficient integrality, content and maximum coefficient are independently checked by the bundled checker.

Both builders apply the same invertible affine change to the three anchor witnesses: old_u=S+(U-3V+3W)/4, old_v=S/2+V/4, old_w=3S/2+W/4. Its linear determinant is 1/64. The translated anchor residual is sixteen times the old residual after this substitution. Thus the unchanged anchor and its size condition have the same rational solutions in both systems; no anchor witness or condition is removed.

## The point chart

Put D=11-6*sqrt(2). For each of the nine original halfpoints (a,b), replace the four rational components of a,b by the components of t,h. Define

    u=t², X=h², Y=h*(u/2-X),
    u*(X-u/4)=D.

There are three field assignments and one field structural equation. Their components are quadratic. These replace the four field assignments and one field structural equation used to double an affine halfpoint, saving two rational coordinates per point.

For a baseline halfpoint define t=b/a and h=(a²+D)/(2b). Both denominators are nonzero. The baseline tangent equation forces b nonzero: if b=0 then a=0 or a²=D, but 3a²-D is respectively -D or 2D. The curve equation then forces a nonzero. Using b²=a³-Da gives t²=a-D/a and h=a/t-t/2. Substitution proves u*(h²-u/4)=D, and the ordinary doubling formulas give X=h² and Y=h*(u/2-h²).

Conversely define

    a=t*h+t²/2, b=a*t, m=h+t.

The chart equation forces t nonzero because D is nonzero. If a=0, then h=-t/2 and the chart equation would give D=0. Thus a,b are nonzero. Direct expansion gives a²-t²*a=D, b²=a³-Da and 2*b*m=3*a²-D. The doubling equations yield m²-2*a=h² and m*(a-h²)-b=Y. Thus every new point is precisely a finite double of a valid old halfpoint. The two substitutions recover t,h and a,b in both directions. All downstream point values remain identical.

D is positive under both real embeddings of K. The chart equation and u=t² therefore imply h nonzero and X=h² strictly positive under both embeddings. In particular the rational component X0 is positive. This proves the scale nonvanishing needed below directly in the new coordinates.

## Exact polynomial circuits

All the following changes preserve their named polynomial outputs by identities, so their forward and reverse maps simply evaluate the corresponding assignment gates.

1. The logarithm polynomial P(w)=sum(a_j*w^j), of degree twelve, is written as a12*Q(w)²+R(w), where Q is monic of degree six and R has degree at most five. Matching coefficients from degree eleven down to degree six determines Q recursively, dividing only by the fixed nonzero rationals 2 and a12. Powers w²,w³ make Q and R quadratic in the available field coordinates. The emitted coefficient recurrence verifies the identity exactly. The degree-three logarithm keeps its exact original polynomial.
2. A balanced product tree computes the coefficients of product(1+y_i*T). Each coefficient convolution is assigned as one quadratic expression per field component. These are the same elementary symmetric coefficients as the baseline sequential recurrence.
3. For a degree-ten polynomial C(q), write C(q)=A(q)+q^5*B(q), with degrees at most four and five. Compute q² through q^5, assign B, and assign the raw quadratic expression A+q^5*B. This uses eight rational coordinates instead of the eleven used by the first direct-evaluation optimization. The degree-two and degree-four polynomials use their direct power sums. The output of every detector polynomial is unchanged.
4. The Lucas expression t²-a(a-2)tb+((a-2)b)²-1 is evaluated as t²-(at)*C+C²-1, where C=(a-2)b. This is a regrouping of multiplication, with no change to the tested expression.
5. The fixed quintic F is regrouped using its exact rational coefficients and t². Its value is still t(t+1/2)(t+1)(t-1/2399)(t+32/407).
6. The two weights q16=q1*e24*e6 and q52=q1*e96*e6 share c=q1*e6. The forward map assigns c. The reverse map restores the old e30=e24*e6 and e102=e96*e6. No division is used.

## Quotients and all new domain obligations

Write delta=A*lambda-1, di=1/delta, e for the detector weight, and n for Norm(W)/(2*w0). The original inverse equations for delta and w0 remain. The nine scales A are 1, four squares X0² and four values (1+X1²)². By the point-chart argument, every A is positive, hence nonzero.

The new weight equation is F*e=(A*delta)^5, with its numerator calculated as the fourth power times A*delta. Since A and delta are nonzero, this equation forces both F and e nonzero. The old F inverse and e inverse may therefore be reconstructed as 1/F and 1/e. Deleting their original inverse coordinates creates no zero-denominator branch.

The new equations include

    delta*q1=e*di²,
    w0*n=(w0²-2*w1²)/2,
    e*v=di*n, b=n*v.

The first restores q1=e/delta³. The second restores n=Norm(W)/(2*w0), because the w0 inverse remains. The last two give b=di*n²/e, exactly the original R*n² with R=di/e. For the forward map take v=R*n; for the reverse map restore R=di/e and the old n² assignment. W=w0+w1*sqrt(2) is nonzero because w0 is nonzero, and its norm is nonzero in K. Thus n and b are nonzero. This also supplies the pole domains below. No implication is inferred from an unguarded equation w0*n=Norm(W)/2 alone.

For U0 and V0 only, omit z=-x/y and define log by y*log=-x*P. The same finite-double or finite-difference ordinate lemma already used by the baseline guarantees y nonzero. Therefore this log equals z*P. The new point chart reconstructs an old halfpoint, so it preserves that lemma's hypotheses. All subtraction abscissa-inequality guards remain. The other eight logarithms retain their local-parameter quotients.

The scalar ratio replaces zH*ratio=zS by xH*ratio=-yH*zS. Both xH and yH are nonzero by the retained inverse and inherited point lemma; substituting zH=-xH/yH proves equivalence. The scalar tree retains r*i=1. Its two changed nodes are r*n0=r+f² and r*n1=u²*i+g², with the original leaf u*i retained. They equal 1+r*(f*i)² and (u*i)²+r*(g*i)² because r*i=1. Every deleted leaf or product is reconstructed uniquely. All other inverse equations and quotient domains are unchanged.

## Pole witnesses

At all ten poles put C=17b. The preceding argument proves C nonzero for the nine coordinate poles; the scalar pole retains its explicit inverse of b. The scalar preparation variable, expression for U and its original denominator domain are unchanged. The other poles use U=b.

Replace the base witness e_old by z=C*e_old. Define P=p², F=U², H=z*(C-F), V=s² and Q=q². Impose

    C*P=(C-z)(C+3z),
    C*Q=(V-H)(V+3H).

Each equation is quadratic in its available coordinates. The old first residual was p²-C*(1-e_old)*(1+3e_old). After z=C*e_old, the new first residual is C times the old one, and the new second residual equals the old second residual with H=C*e_old*(C-U²). The reverse map is e_old=z/C, which is defined by the established C nonzero. This removes one intermediate per pole and changes neither pole predicate.

## Finite scalar correction

Replace the eight Boolean choices and seven multiplication gates by eight signed partial products c0,...,c7. Require c0²=1 and, for p_i=2,3,5,7,11,13,17,

    (ci-c(i-1))*(ci-p_i*c(i-1))=0.

Induction gives nonzero ci and ci/c(i-1) in {1,p_i}, so c7 is exactly one of the original 256 signed squarefree corrections. Conversely every original choice defines the chain. Recover the old Booleans by epsilon_sign=(1-c0)/2 and epsilon_i=(ci/c(i-1)-1)/(p_i-1). All denominators are nonzero. The scalar pole input is consequently unchanged.

## Composition and validation boundary

Start with any baseline solution. Apply the point substitution, correction-chain substitution and pole rescaling, and evaluate every changed assignment or quotient in dependency order. The identities and nonzero facts above prove every new structural residual zero. The input remains x. Conversely reconstruct the old halfpoints, Booleans and pole e witnesses; recover all omitted quotient values using the proven domains; and evaluate every old assignment. The old named detector, logarithm, scalar and anchor values agree, so all old structural equations vanish. This proves both rational-projection implications before compilation. The certified compiler and sum-of-squares steps then prove the stated theorem for P962 and P1272.

The full table checker proves algebraic facts about the actual emitted files, not the separate baseline number-theoretic theorems. Independent source reviews are included with their exact hashes. Component certificates remain archived for the circuit transformations, and the frozen package reproduces its builder, raw system and table without reading the production repository.
