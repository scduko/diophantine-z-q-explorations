"""Emit one proposed pole module. Installation requires a new arithmetic source audit."""
def make(b,normalized=False):
    name='q_linearnormalpole' if normalized else 'q_linearconicpole'
    m=b.M(name,3);P=b.P;r,theta,W=map(P.v,range(3))
    labels=['l','z','e','p','c','w','s_p','q','j','k'] if normalized else ['U','L','z','e','p','c','w','s_p','q','j','k']
    values=[P.v(m.var('linear pole '+label)) for label in labels]
    if normalized:
        l,z,e,p,c,w,s,q,j,k=values
        m.force(l-(3-2*theta)*W,'linear pole linear product')
    else:
        U,l,z,e,p,c,w,s,q,j,k=values
        m.force(U-r*(3-2*theta),'linear pole linear unit')
        m.force(l-W*U,'linear pole scaled U')
    m.force(z-l*l,'linear pole scaled square')
    m.force(c-r*e,'linear pole scaled e')
    m.force(p*p-17*r-34*c+51*e*c,'linear pole first conic')
    m.force(w-17*e+c*z if normalized else w-c*(17*r-z),'linear pole shared expression')
    m.force(j-s*s,'linear pole square')
    m.force(k-r*q,'linear pole scaled q')
    m.force(j*j+34*j*w-867*w*w-17*q*k,'linear pole second conic')
    m.save(input_layout='r;private theta;upper norm root',pole_model='linear unit 3-2*theta',
        required_caller_premise='same theta^2-r*s_c^2=2',arithmetic_source_restriction=True,
        r_normalized=normalized)
    return b.MODULES[name]
