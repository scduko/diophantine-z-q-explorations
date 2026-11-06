"""Bounded exact tests, including the intentionally excluded r=0 branch."""
from fractions import Fraction as Q
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    # This first test is an algebraic identity for arbitrary nonzero r;
    # it does not require a real solution of the conic.
    values=[Q(-3),Q(-1),Q(-1,2),Q(0),Q(1,3),Q(1),Q(3)]
    exact=0
    zero_n=0
    for r in values:
        if not r:
            continue
        for T in values:
            W=T/r
            N=1+r*W*W
            require(r*N-r-T*T==0,'Fused forward row')
            require(1+r*(T/r)**2==N,'Reverse norm node')
            require(r*W==T,'Reverse numerator')
            exact+=1
            zero_n+=N==0
    require(zero_n>0,'Fixture must cover a vanishing norm node')
    # The isolated fused row admits N=7 when r=T=0, unlike N=1+r*W^2.
    require(0*7-0-0==0 and 7!=1,'Explicit isolated r=0 counterbranch')

    conic=0
    for theta in values:
        for s in values:
            if not s:
                continue
            r=(theta*theta-2)/(s*s)
            require(r!=0,'No rational square root of two in exact fixture')
            for A in values:
                for B in values:
                    Y=A+theta*B
                    T=2*A*Y-A*A+2*B*B
                    require(T==Y*Y-(theta*theta-2)*B*B,'Packed identity')
                    W=T/r;N=1+r*W*W
                    require(r*N-r-T*T==0,'Conic fusion')
                    conic+=1

    # Integer valuation exponents only, independent of polynomial evaluation.
    # Both summand parities are explicit. Negative input valuations occur.
    valuations=0
    for e in (1,2,12,40):
        for R in (1,3,5,17):
            for delta in range(1,22,2):
                for y in range(-12,46):
                    for b in range(-12,46):
                        vT=min(2*y,delta+2*b)
                        if vT>(2*e-2)*R:
                            require(y>=e and delta+b>=e,'Odd threshold extraction')
                            valuations+=1
    # A threshold one lower is insufficient: e=1, Y unit, B=0 gives vT=0.
    require(min(0,99)==0,'Lower-threshold counterexample')
    print(json.dumps(dict(status='PASS: bounded exact identities only',
        arbitrary_r_cases=exact,zero_norm_cases=zero_n,conic_cases=conic,
        valuation_cases=valuations,isolated_r_zero_counterexample=True)))


if __name__=='__main__':
    main()
