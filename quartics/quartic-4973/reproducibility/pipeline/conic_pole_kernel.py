"""Candidate source hook, installed after the private-conic emitter.

This is an arithmetic-source restriction, not an algebraic certificate rule.
The caller must independently audit conic premises and field independence.
"""
NAMES={'q_conic13','q_conic6','q_conic10'}
MODEL='private conic Cayley parameter 2*s_c'


def make_pole(b):
    m=b.M('q_conicpole',3);P=b.P
    r,theta,W=map(P.v,range(3))
    D,U,L,z,e,p,c,w,s,q,j,k=[P.v(m.var('conic pole '+name)) for name in
                            ('D','U','L','z','e','p','c','w','s_p','q','j','k')]
    m.force(D-4*theta*theta+7,'conic pole denominator')
    m.force(D*(U+r)-2*r,'conic pole Cayley value')
    m.force(L-W*U,'conic pole scaled U')
    m.force(z-L*L,'conic pole scaled square')
    m.force(c-r*e,'conic pole scaled e')
    m.force(p*p-17*r-34*c+51*e*c,'conic pole first conic')
    m.force(w-17*r*c+c*z,'conic pole shared expression')
    m.force(j-s*s,'conic pole square')
    m.force(k-r*q,'conic pole scaled q')
    m.force(j*j+34*j*w-867*w*w-17*q*k,'conic pole second conic')
    m.save(input_layout='r;private theta;upper norm root',pole_model=MODEL,
           required_caller_premise='same theta^2-r*s_c^2=2',
           arithmetic_source_restriction=True)


def install(b):
    if not getattr(b,'_private_conic_installed',False) or b.MODULES:
        raise ValueError('Install after the private-conic hook on a fresh builder')
    if getattr(b,'_conic_pole_installed',False):raise ValueError('Already installed')
    b._conic_pole_installed=True
    old_save=b.M.save
    def save(m,**metadata):
        if m.name in NAMES:
            W=metadata['norm_root'];W2=metadata['norm_root_square'];arg=metadata['parity_argument']
            theta=metadata['conic_private']['theta']
            if [W2,arg]!=[m.count-2,m.count-1] or m.calls!=[{'module':'q_primeparity','args':[arg]}]:
                raise ValueError('Changed private conic pole boundary')
            expected=[(b.P.v(W2)-b.P.v(W)*b.P.v(W)).row(),
                      (b.P.v(arg)-b.P.v(0)*b.P.v(W2)).row()]
            if m.rows[-2:]!=expected:raise ValueError('Changed conic argument rows')
            tail=[['variable',W2,'batched square'],['equation',len(m.rows)-2,'batched square'],
                  ['variable',arg,'parity argument'],['equation',len(m.rows)-1,'parity argument']]
            if m.operations[-4:]!=tail:raise ValueError('Changed conic tail log')
            if metadata['parity_module']!='q_primeparity':raise ValueError('Wrong original parity module')
            m.rows=m.rows[:-2];m.operations=m.operations[:-4];m.count-=2
            m.calls=[{'module':'q_conicpole','args':[0,theta,W]}]
            metadata.pop('norm_root_square');metadata.pop('parity_argument')
            metadata.update(parity_module='q_conicpole',pole_model=MODEL,pole_inputs=[0,theta,W],
                semantics='Private theta^2-r*s_c^2=2; original packed fields and upper tree; conic-conditioned pole at (r,theta,root)')
            if 'q_conicpole' not in b.MODULES:make_pole(b)
        return old_save(m,**metadata)
    b.M.save=save
