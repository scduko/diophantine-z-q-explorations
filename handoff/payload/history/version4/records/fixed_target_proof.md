# Direct bindings for the new fixed target

This optional compiler part belongs to the doubled-index root source, not to the current source. Its fixed target is 4R=2P*, whose abscissa a and ordinate ratio q=y/a are

    a0= 8226963211/2285245536,
    a1=-1063929023/1713934152,
    q0= 70757419981/143614994586,
    q1=344600359813/574459978344.

The exact calculation and all component values are frozen in `charts/sub5000/half-generator-review/FIXED_TARGET.json`, SHA256 `03d5ffae826a5183d1c1470594c113bc62c285ca12a09702c26f1fb0e69c1409`. Its exact producer is `fixed_target.py`, SHA256 `74ae8b6cd995ab1e3927ee570594100af2927ea789e4a5893f6167c6bf953346`.

Bind four rational variables by the four primitive integer linear rows

    2285245536*a0 - 8226963211 = 0,
    1713934152*a1 + 1063929023 = 0,
    143614994586*q0 - 70757419981 = 0,
    574459978344*q1 - 344600359813 = 0.

Keep these as separate rows. Do not substitute their fractions into later rows during source construction. In particular the high-denominator s and t values are not emitted as direct rational constants.

For the fixed target use the same field coordinates F,r,s,t,u and equations as its current joint interface, apart from omitting the obsolete construction of q from a separately stored ordinate:

    a F=1,
    r conjugate(q)=jz,
    s conjugate(q)=conjugate(a+D F),
    t conjugate(a-D F)=1,
    u=r s,

where jz=1/conjugate(z(J)). The exact fixed values satisfy q^2=a-D F and describe the nontorsion point 4R, so their nonzero denominators and the joint identities have the same justification as in the main proof. There is no need to allocate its ordinate y=a q, which has no mathematical consumer after q is supplied directly. Any old metadata claiming a live ordinate coordinate must be replaced by truthful typed fixed-target metadata; it cannot be left pointing to a deleted coordinate.

The comparison input layouts stay unchanged: the fixed target contributes its r,q pair and its s,t,u triples in the same first-target slots. The other four targets remain actual quadruples of A,S,T,Z with their unchanged joint-coefficient equations. All base-doubling allocations and rows must be identified by a fresh exact incidence audit before omission. Do not delete a shared value merely because an old construction label called it a constant.

## Whole-polynomial coefficient accounting

The four binding-row squares, after full collection, have maximum absolute coefficient

    395918230471021175779344 < 2^80

and total constant coefficient

    C_bind=123824835334257812600380.

These are isolated-row facts only. They do not prove the new complete polynomial's bound.

For an actual all-weights-one SOS row replacement, let C_old be the old complete constant coefficient and let C_removed be the sum of the squares of the constant coefficients of the removed rows. If every other retained row has its old constant and the four binding rows are the only extra nonzero constants, then the exact identity is

    C_new=C_old-C_removed+C_bind.

All terms in C_removed are nonnegative. Using the normalized5512 complete maximum as an upper bound on C_old already gives the conservative numerical bound

    C_new <= 685783949153203534233600 + C_bind
           = 809608784487461346833980
           < 1208925819614629174706176 = 2^80.

The headroom in this bound is 399317035127167827872196. The exact new row list must still establish the stated correspondence and include any additional changed constant rows. A later elimination or rescaling changes the row constants and requires recomputation; the inequality cannot simply be copied to that later system.

UnitScale subsequently checked the actual normalized5512 constant-base rows. Its receipt `elimination/sub5000/normalized5512-constant-base.json`, SHA256 `f3a98b7a021c689fc3e953ca819412b7c53b0c8b22470a36963d24c16c63c1d2`, matches the 20 fixed-doubling definitions to the source and initial lift, then checks the selected 26 current rows and all source/current consumers of the proposed removed coordinates. For this selected-row change alone it reports

    C_old=1834570187176371839071,
    C_removed=1834568286842801281051,
    C_new=123824837234591383158400 < 2^80.

The earlier value 685783949153203534233600 was the full maximum coefficient, not the actual constant; it was used only as a safe upper bound. The exact receipt does not yet include the other root-chart changes or the later normalized10 parent. Repeat the accounting against the actual parent and final row list. Eight of the 20 original fixed-doubling coordinates survive in normalized5512; the receipt also distinguishes output-binding and initial-lift allocations, so these numbers must not be added to a claimed source saving without its mapping.

Nonconstant coefficients need separate full collection. Removing rows can remove cancellations, and the new binding rows can overlap existing monomials. Thus an old maximum plus the isolated block's maximum is not a complete certificate. The pinned constant-base census is an intermediate check; the final acceptance gate remains the independent exact expansion of the new SOS.
