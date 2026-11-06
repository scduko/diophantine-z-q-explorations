# Share the square of the common conjugate f(J) field

This is an exact rational projection-preserving source rewrite. It keeps
every original field order and every normalized norm value W. It introduces
no division, nonzero premise, prime restriction or arithmetic specialization.
It composes with the separately approved ordinary pole by leaving that pole
and all of its inputs unchanged.

## Exact identity and maps

Let F=A+B*sqrt(2) be the one shared field conj(f(J)). Retain A and B in the
root. Introduce two root coordinates C,D and quadratic equations

    C-A^2-2*B^2=0,
    D-2*A*B=0.

Thus (C,D) are the coefficients of F^2. If the original f(J) coefficients
are (a,b), then A=a, B=-b, C=a^2+2b^2 and D=-2ab. Conjugation of the second
component must not be lost.

At each ordinary contact, the old designated field contributes

    R_y = Y-A-theta*B=0,
    R_w = P*W-2*A*Y+A^2-2*B^2=0,

where P=r^2 is the existing contact-power coordinate for original order one.
Replace these by the single quadratic row

    R_new = P*W-C-theta*D=0.

No test of F^2 with order one is being substituted for the old test. The new
row computes exactly the old packed numerator for the original field F and
its original order. Its input channel is explicitly typed as pre-squared
coefficients so a generic batch constructor cannot square it again.

Write R_C=C-A^2-2B^2 and R_D=D-2AB. The polynomial identity is

    R_new = R_w+2*A*R_y-R_C-theta*R_D.

Forward, assign C=A^2+2B^2 and D=2AB, drop every designated Y, and keep all
other coordinates. Reverse, set Y=A+theta*B separately at every contact,
drop C,D, and keep all other coordinates. The identity proves all old and
new equations in both directions. The input variable is fixed. These maps
remain valid at A=0, B=0, F=0, P=0, r=0, W=0 and arbitrary theta. The actual
conic source still has its existing r-nonzero proof, but this rewrite does
not need it.

Every new row already has degree at most two. C=A^2+2B^2 needs no square
witnesses: squares are legal monomials of a quadratic residual. D=2AB and
P*W-C-theta*D likewise require no new product witnesses. Their maximum
absolute coefficient is two. A later final polynomial expansion must still
be checked against the global coefficient bound.

## Actual source allocation

The read-only census binds the measured normalized source and its 5310-variable
post-power endpoint in CENSUS.json. All three modes pass the same root pair
(200,230), where root coordinate 200 is f(J)_0 and coordinate 230 is the
retained arithmetic alias -f(J)_1=-coordinate201.

| Comparator | Calls | Existing free slots | Designated field index | Batch slots |
| --- | ---: | --- | ---: | --- |
| q_compare4 | 13 | 21,22 | 5 | 11,12 |
| q_compare_beta | 8 | 9,10 | 2 | 5,6 |
| q_compare_lucas | 16 | 16,17 | 4 | 9,10 |

Those comparator slots have no residual use. Each is passed exactly once to
its designated batch coefficient channel. Retyping these slots changes no
comparator equation or arity. All designated fields have original order one,
all use the existing r^2 coordinate, and each Y has precisely its defining
row and packed-norm row as residual consumers. The original W is retained
in the same upper-tree position.

The census found only one directly shared field coefficient pair in the
entire tested field list: this conj(f(J)) pair, occurring 37 times. Shared
target ratios and inverse-z(J) coefficients are comparator inputs but do not
themselves occur as another globally shared tested field. A direct source-row
scan found no pre-existing common-pair quadratic products that already define
C or D. This is a finite direct-allocation finding, not an exhaustive ideal
membership claim.

All 37 designated Y coordinates and all 37 corresponding W coordinates
survive in the measured normalized-power endpoint. Therefore deleting the Y
coordinates is not merely removing dead raw-source output. The forecast is
37 removed coordinates minus two added root coordinates, or 35 fewer total
coordinates. This is an estimate; only a new full pipeline run can determine
the actual endpoint change after cleanup. No measured 5275-variable artifact
is claimed.

## Source binding and composition

SOURCE_CONTRACT.json specifies the delta. A complete new source must have a
fresh identity and must be accepted by independent reconstruction, not by
substituting a new source hash into an old entry.

The root retains its original f(J), all point equations and all other uses
of A,B. It appends exactly C,D and the two defining rows. Only the designated
two argument slots of each of the 37 comparator calls change to C,D. Every
comparison retains all residuals and all other inputs, with an explicit
pre-squared-channel metadata record. In each batch, remove just Y and its
defining row, replace just its packed-norm row, and remap later local variable
and row indices consistently. All other field rows, sorted order, contact
powers, private conic, literal-one tree and pole remain the original objects
under that renumbering.

The independent source checker must validate the root square identities
before restoring an old comparison/batch view. After reversal of the exact
declared delta, the complete old source must pass the pinned parent checker.
The restored view is justified by the displayed maps, not merely a convenient
shape comparison. Unchanged modules and all compiler inputs remain bound to
the selected parent. The new flattening map and every source residual still
need independent verification.

The normalized-Lucas and conic-pole arithmetic compositions are unchanged.
The original fields are fixed before choosing each private conic. Their
shared square C,D is fixed at that same stage. Each reconstructed old W is
identical, so all old valuation inequalities, real nonnegativity arguments,
weak-approximation choices and zero branches are inherited literally.

## Other inspected channels

No tested field pair has a syntactically zero coefficient in the actual
three-mode allocation. The beta residual is a field ratio minus a rational
proxy, which does not force its imaginary coefficient to vanish. The
normalized-Lucas block also does not force a rational residual on its own:
with Lambda=p_s=p_t=p_z=B_s=B_z=1 and B_t=sqrt(2), its equations admit
P=1,U=1+sqrt(2),V=-1,K=-sqrt(2),E=2+sqrt(2). This is a block-level
counterexample to a rational-output inference, not a claimed full-source
elliptic solution. Discarding the imaginary E channel would require a new
global theorem absent from the current source.

No conjugate identification is asserted between independent private points
or between a primary point and its target difference. The common-field square
rewrite above is the only saving claimed by this packet.

## Bounded verification

test_shared_square.py proves the displayed polynomial identity by exact
dictionary polynomial arithmetic, checks 625 rational assignments including
zero coefficients, exercises two zero-power cases and checks the conjugation
sign. census_shared_field.py performs read-only source/metadata checks and
records exact input hashes. Neither script generates a full source, expands
the final quartic or certifies the estimated endpoint reduction.
