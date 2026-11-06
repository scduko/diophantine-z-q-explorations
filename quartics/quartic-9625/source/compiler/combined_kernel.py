"""Producer for the explicit H19/root37/reciprocal compressed source proposal.

This changes the arithmetic starting source. It is not an algebraic rewrite
of the original finite logarithm or a certificate of source acceptance.
"""
from copy import deepcopy


HEIGHT_EXPONENT = 19
HEIGHT_CONSTANT = {
    'symbol': 'H19',
    'formula': '2*A19*B_star^19+128',
    'A19': {'power_of_2': 109, 'power_of_210': 1800},
    'B_star': {'prime_bound_inclusive': 76176},
    'multiplier': 2,
    'prime_product_exponent': 19,
    'addend': 128,
    'log2_strict_upper_bound': 2093966,
}
SCALAR_ORDERS = [1, 1, 1, 1, 32, 32]
ANCHORS = {40: 25, 44: 24, 48: 23}
HIGH_PROFILES = {
    40: {'precision': 40, 'scheme': 'block3', 'normalization': 'a6', 'hscale': 1, 'bound_output': False},
    44: {'precision': 44, 'scheme': 'powers45', 'normalization': 'unit', 'hscale': 1, 'bound_output': False},
    48: {'precision': 48, 'scheme': 'block3', 'normalization': 'a6', 'hscale': 1, 'bound_output': False},
}
BETA_PROFILE = {'precision': 12, 'scheme': 'direct', 'normalization': 'unit', 'hscale': 1, 'bound_output': False}


def configuration(high, label):
    if type(high) is not int or high not in ANCHORS or type(label) is not int or label != 12:
        raise ValueError('Reviewed combined tuples have high 40/44/48 and beta 12')
    return {
        'high_precision': high,
        'label_precision': label,
        'anchor_squarings': ANCHORS[high],
        'root_comparison_calls': 37,
        'coordinate_scalar_count': 8,
        'rational_tests_per_comparison': 41,
        'scalar_orders': list(SCALAR_ORDERS),
        'field_inequality_orders': [1]*11+[label, high, high, high, high, label, high, high, high],
        'rational_inequality_orders': [1]*23+[label]*2+[high]*8+[label]*2+[high]*6,
        'height_exponent': HEIGHT_EXPONENT,
        'height_constant': deepcopy(HEIGHT_CONSTANT),
        'compressed_primary_charts': True,
        'high_log_profile': deepcopy(HIGH_PROFILES[high]),
        'beta_log_profile': deepcopy(BETA_PROFILE),
    }


def comparison_point(b, field, label):
    """The four-equation primary chart; surrounding G ratios force p != 0."""
    m = field.m
    u, v, f, x, p = [b.fvar(m, label+'.'+s) for s in ('u', 'v', 'f', 'x', 'p')]
    one = (b.P(1), b.P())
    d = tuple(b.P(q) for q in b.CURVE_DROOT)
    b.feq(m, b.fs(f, b.raw_fmul(u, u)), label+'.f=u2')
    b.feq(m, b.fs(b.fa(b.raw_fmul(v, v), b.raw_fmul(d, f)), one), label+'.v2+df=1')
    b.feq(m, b.fs(b.raw_fmul(p, p), b.fs(x, b.raw_fmul(field.D, f))), label+'.p2=x-Df')
    b.feq(m, b.fs(b.raw_fmul(x, f), one), label+'.xf=1')
    return {'x': x, 'y': b.raw_fmul(x, p), 'f': f, 'p': p}


def install(b, emit_g, *, high=40, label=12):
    """Install only the changes listed in the combined source ledger."""
    config = configuration(high, label)
    b.PELL_PRECISION = high
    b.ANCHOR_SQUARINGS = config['anchor_squarings']
    old_batch = b.make_batch

    def new_batch(name, source_orders, parity):
        if name == 'q_batch41':
            orders = list(config['rational_inequality_orders'])
        elif name == 'q_height_batch':
            orders = list(SCALAR_ORDERS)
        else:
            raise ValueError('Unexpected batch module in combined compiler')
        old_batch(name, orders, parity)
        if name == 'q_height_batch':
            module = b.MODULES[name]
            module['height_exponent'] = HEIGHT_EXPONENT
            module['height_constant'] = deepcopy(HEIGHT_CONSTANT)
            b.write('modules/'+name+'.json', module)
    b.make_batch = new_batch

    def forbidden_old_logarithm(*args, **kwargs):
        raise RuntimeError('Combined source must use the explicitly profiled reciprocal G circuit')
    b.Field.logarithm = forbidden_old_logarithm

    def g(field, point, profile):
        assert profile['bound_output'] is False
        return emit_g(b, field, point['f'], profile['precision'], bind_output=False,
                      hscale=profile['hscale'], scheme=profile['scheme'], normalization=profile['normalization'])

    def new_comparison():
        n = 4
        free = n+4+4*n+4+3
        m = b.M('q_compare4', free); field = b.Field(m); at = n
        proxies = tuple(b.P.v(i) for i in range(n))
        def read_point():
            nonlocal at
            result = {'x': (b.P.v(at), b.P.v(at+1)), 'y': (b.P.v(at+2), b.P.v(at+3))}
            at += 4
            return result
        p4 = read_point(); q4 = [read_point() for _ in range(n)]
        fj = (b.P.v(at), b.P.v(at+1)); at += 2
        zji = (b.P.v(at), b.P.v(at+1)); at += 2
        root, error, r = b.P.v(at), b.P.v(at+1), at+2
        assert r == free-1
        points = [comparison_point(b, field, s) for s in ('H', 'X0', 'X1', 'X2', 'X3')]
        differences = [field.difference(point, target) for point, target in zip(points, [p4]+q4)]
        formal = [field.f(point) for point in points]+[fj]+[field.conj(field.f(point)) for point in differences]
        lam = b.fvar(m, 'common negative logarithm')
        gh = g(field, points[0], config['high_log_profile'])
        b.feq(m, b.fs(b.raw_fmul(lam, points[0]['p']), gh), 'H pH=GH')
        primary = []
        for i, (point, proxy) in enumerate(zip(points[1:], proxies)):
            ratio = b.fvar(m, 'retained logarithm ratio')
            aux = b.fvar(m, 'ratio times p')
            b.feq(m, b.fs(aux, b.raw_fmul(ratio, point['p'])), 'A=C p')
            gi = g(field, point, config['beta_log_profile'] if i == 0 else config['high_log_profile'])
            b.feq(m, b.fs(b.raw_fmul(aux, lam), gi), 'A H=G')
            primary.append(b.fs(ratio, (proxy, b.P())))
        alternate = [field.mul(field.conj(field.z(point)), zji) for point in differences]
        tests = b.field_tests(m, root, error, formal+primary+alternate)
        assert len(tests) == 41
        m.call('q_batch41', [r]+tests)
        m.save(precision=high, label_precision=label, modeled_points=4,
               field_inequality_orders=list(config['field_inequality_orders']),
               logarithm_coordinate='reciprocal f=1/x', compressed_primary_charts=True,
               high_log_profile=deepcopy(config['high_log_profile']),
               beta_log_profile=deepcopy(config['beta_log_profile']),
               input_layout='beta,s,t,z;4P;4A;4S;4T;4Z;conj_fJ;inv_conj_zJ;root;root_error;r')
    b.make_multi_comparison = new_comparison

    def new_root():
        # The prefix is the original root construction, including all six
        # full root charts, the two doublings, and the common J parameters.
        P = b.P
        m = b.M('Z_definition', 1); field = b.Field(m)
        beta = P.v(m.bind(P.v(0)*P.v(0)+2, 'beta=X^2+2'))
        points = [field.gpoint(k) for k in ('A', 'S', 'T', 'Z')]
        A, S, T, Z = points
        m.call('q_anchor', [m.bind(t) for t in S['f']])
        s, t, z = [P.v(m.var('index proxy '+k)) for k in ('s', 't', 'z')]
        m.force(t*t-s*(s-2)*t*z+(s-2)**2*z*z-1, 'Lucas norm proxy certificate')
        root = P.v(m.var('common sqrt2 approximation')); error = m.value(root*root-2, 'root error')
        j0 = field.gpoint('height J')
        first = field.f(j0)+field.f(S)+field.div(field.z(S), field.z(j0))
        r = P(1)
        for c in (beta, beta-1, beta-2401, 32*beta+343, 2*beta-1):
            r = m.value(r*c, 'scalar height contact product')
        m.call('q_height_batch', [m.bind(r)]+[m.bind(a) for a in first])
        if b.BASE_GATES:
            base = {'x': tuple(P(a) for a in b.BASE_POINT[0]), 'y': tuple(P(a) for a in b.BASE_POINT[1])}
            p4 = field.double(field.double(base))
        else:
            p4 = b.base4()
        q4 = [field.double(field.double(point)) for point in points]
        j = field.gpoint('common comparison J')
        fj = field.conj(field.f(j)); zji = field.inv(field.conj(field.z(j)))
        prefix = [m.bind(a) for a in (beta,s,t,z)+b.flat_point(p4)+sum((b.flat_point(q) for q in q4),())+fj+zji+(root,error)]
        assert len(prefix) == 30
        # The eight rational abscissa coefficients are the height targets.
        # The denominator D in the prime-pattern proof is not a source input.
        scalars = [x for point in points for x in point['x']]
        contacts = b.contacts(m, scalars)
        assert len(scalars) == 8 and len(contacts) == 37
        for contact in contacts:
            m.call('q_compare4', prefix+[contact], 'simultaneous four-index comparison')
        m.save(precision=high, anchor_squarings=b.ANCHOR_SQUARINGS, chart=b.CHART,
               prime_parity_witnesses=b.PARITY,
               proxy_indices=[m.bind(a) for a in (beta,s,t,z)],
               point_coordinates={k:[m.bind(x) for x in b.flat_point(q)] for k,q in zip(('A','S','T','Z'),points)},
               coordinate_scalar_count=8, ordinary_contact_count=37,
               contact_scale=b.CONTACT_SCALE, contact_shift=b.CONTACT_SHIFT, contact_W=b.CONTACT_W,
               scalar_height_orders=list(SCALAR_ORDERS),
               height_exponent=HEIGHT_EXPONENT, height_constant=deepcopy(HEIGHT_CONSTANT),
               scalar_rule='beta=X^2+2', pell_equation='t^2-s*(s-2)*t*z+(s-2)^2*z^2-1=0')
    b.make_root = new_root
    return config
