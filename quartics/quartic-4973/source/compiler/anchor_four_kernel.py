"""Install the four-witness homogeneous anchor in an isolated source builder.

The source pipeline must pin the builder and retain its shared C chain.
Arithmetic justification is ANCHOR_FOUR_PROOF.md; this is not an algebraic rule.
"""

def install(builder):
    if builder.ANCHOR_SQUARINGS != 25:
        raise ValueError('This packet is fixed to the current anchor25 source')
    def make_anchor():
        b=builder;m=b.M('q_anchor',2)
        C=b.P.v(-26);f0=b.P.v(0);f1=b.P.v(1)
        H,U,V,W=[b.P.v(m.var('anchor homogeneous trace '+name)) for name in ('H','U','V','W')]
        m.force(C*H-9*C*C-3*f0*f0-3*f1*f1,'anchor trace of coefficient squares')
        m.force(H*H-8*U*U-12*V*V+24*W*W-4*C*C,'anchor homogeneous single trace')
        m.save(anchor_squarings=25,anchor_constant_global_index=-26,
               inputs='two coordinates of f(S)=1/x(S)',
               encoding='homogeneous trace 9+3(a^2+b^2) in S_2_3',
               arithmetic_dependency='Koenigsmann Proposition 6 proof Facts (b),(e); explicit trace inclusion 4Z_2')
    builder.make_anchor=make_anchor
