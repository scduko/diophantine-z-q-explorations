"""Private-conic batches after joint-chart and local-Lucas source hooks.

This is a new arithmetic source, not an old-source equivalence rule. The
caller must pin the builder and preceding hooks and independently audit the
entire generated source. This module does not authorize a source pin.
"""
from copy import deepcopy


MODEL = 'private conic field norm v1'
PROOF_SHA256 = 'ef4de3f02fa3d17c18dc7c2af490960a62f35cc541eac8e4b80958d320fa8ab9'
MODES = {
    'q_compare4': {
        'old_batch': 'q_batch31', 'batch': 'q_conic13', 'free': 58,
        'legacy_free': 28, 'theta_slot': 25, 'error_slot': 26, 'raw_slot': 27,
        'orders': [1]*6 + [12, 40] + [40, 12, 40, 40, 40],
    },
    'q_compare_beta': {
        'old_batch': 'q_batch13', 'batch': 'q_conic6', 'free': 28,
        'legacy_free': 16, 'theta_slot': 13, 'error_slot': 14, 'raw_slot': 15,
        'orders': [1]*3 + [12]*3,
    },
    'q_compare_lucas': {
        'old_batch': 'q_batch25', 'batch': 'q_conic10', 'free': 47,
        'legacy_free': 23, 'theta_slot': 20, 'error_slot': 21, 'raw_slot': 22,
        'orders': [1]*5 + [40]*5,
    },
}


def make_conic_batch(b, name, orders, parity='q_primeparity'):
    """Emit a batch with free inputs r,A0,B0,A1,B1,... in field-list order."""
    orders = list(orders)
    if not orders or any(type(e) is not int or e <= 0 for e in orders):
        raise ValueError('Positive integer field orders required')
    if parity != 'q_primeparity' or name not in {v['batch'] for v in MODES.values()}:
        raise ValueError('Unexpected conic batch or pole module')
    expected_orders = next(spec['orders'] for spec in MODES.values() if spec['batch'] == name)
    if orders != expected_orders:
        raise ValueError('Unexpected field order list for named conic batch')
    if name in b.MODULES:
        raise ValueError('Conic batch was already emitted')
    m = b.M(name, 1+2*len(orders)); P = b.P; r = P.v(0)
    theta_id = m.var('private conic theta')
    s_id = m.var('private conic s')
    square_id = m.var('private conic S')
    theta, s, square = map(P.v, (theta_id, s_id, square_id))
    m.force(square-s*s, 'private conic square')
    m.force(theta*theta-r*square-2, 'private conic discriminant')

    powers = {0: P(1), 1: r}
    def rp(exponent):
        if exponent not in powers:
            half = rp(exponent//2)
            powers[exponent] = m.value(half*half, 'shared conic contact power')
            if exponent % 2:
                powers[exponent] = m.value(powers[exponent]*r, 'shared conic contact power')
        return powers[exponent]

    nodes = [P(1)]
    plan = [{'type': 'literal', 'value': 1}]
    bindings = []
    for index in sorted(range(len(orders)), key=lambda i: (orders[i], i)):
        order = orders[index]
        a_id, b_id = 1+2*index, 2+2*index
        A, B = P.v(a_id), P.v(b_id)
        y_id = m.var('conic evaluation'); Y = P.v(y_id)
        m.force(Y-A-theta*B, 'conic evaluation')
        w_id = m.var('conic packed field norm'); W = P.v(w_id)
        power = rp(2*order)
        m.force(power*W-2*A*Y+A*A-2*B*B, 'conic packed field norm')
        record = dict(type='conic_field', field=index, order=order,
                      inputs=[a_id, b_id], evaluation=y_id, norm=w_id,
                      power=m.bind(power))
        plan.append(record)
        bindings.append(dict(record))
        nodes.append(W)

    levels = []
    while len(nodes) > 1:
        levels.append(len(nodes))
        nodes = [m.value(nodes[i]*nodes[i]+r*nodes[i+1]*nodes[i+1], 'cubic norm node')
                 if i+1 < len(nodes) else nodes[i] for i in range(0, len(nodes), 2)]
    root = nodes[0]
    root_square = m.value(root*root, 'batched square')
    argument = m.bind(r*root_square, 'parity argument')
    m.call(parity, [argument])
    m.save(
        orders=orders, field_inequality_orders=orders, norm_tree=plan,
        norm_level_sizes=levels, parity_module=parity, squareclass_correction=False,
        input_layout='r;A0;B0;A1;B1;...', comparison_norm=MODEL,
        conic_private=dict(theta=theta_id, s=s_id, square=square_id),
        conic_equations=[0, 1],
        field_input_order=[[1+2*i, 2+2*i] for i in range(len(orders))],
        sorted_field_indices=sorted(range(len(orders)), key=lambda i: (orders[i], i)),
        field_bindings=sorted(bindings, key=lambda item: item['field']),
        contact_powers=[dict(exponent=e, variable=m.bind(v))
                        for e, v in sorted(powers.items()) if e],
        norm_root=m.bind(root), norm_root_square=m.bind(root_square),
        parity_argument=argument,
        semantics='Private theta^2-r*s^2=2; packed eval_theta(F_i^2)/r^(2e_i); '
                  'upper N_r tree on literal1 and packed nodes; Psi(r*root^2)',
    )


def install(b):
    """Install after beta_kernel, rational_difference, joint_chart and local_lucas.

    The old root and its free comparison interfaces are retained exactly.
    Their common theta/error slots are ignored by the new comparators.
    No contact inverse is introduced in a new conic batch.
    """
    if not getattr(b, '_rational_difference_installed', False):
        raise ValueError('Install the pinned rational-difference hook first')
    if not getattr(b, '_joint_chart_installed', False):
        raise ValueError('Install the pinned joint-chart hook first')
    if not getattr(b, '_local_lucas_installed', False):
        raise ValueError('Install the pinned local-Lucas hook first')
    if getattr(b, '_private_conic_installed', False) or getattr(b, '_private_conic_joint_installed', False):
        raise ValueError('Private conic hook already installed')
    if (b.PELL_PRECISION, b.ANCHOR_SQUARINGS, b.CURVE_DROOT, b.CURVE_D2) != \
            (40, 25, (3, -1), (11, -6)):
        raise ValueError('Expected H19/root37/high40/beta12/anchor25 source')
    if b.MODULES:
        raise ValueError('Install on a fresh builder before emitting modules')
    b._private_conic_installed = True
    b._private_conic_joint_installed = True
    old_batch = b.make_batch
    old_tests = b.field_tests
    old_call = b.M.call
    old_save = b.M.save
    old_comparison = b.make_multi_comparison

    def batch(name, orders, parity):
        if name == 'q_batch41':
            spec = MODES['q_compare4']
            make_conic_batch(b, spec['batch'], spec['orders'], parity)
        elif name == 'q_height_batch':
            old_batch(name, orders, parity)
        else:
            raise ValueError('Unexpected top-level batch in conic source')
    b.make_batch = batch

    def field_tests(m, root, error, expressions):
        if m.name not in MODES:
            return old_tests(m, root, error, expressions)
        spec = MODES[m.name]
        expressions = list(expressions)
        if m.free != spec['free'] or len(expressions) != len(spec['orders']):
            raise ValueError('Unexpected comparison field interface')
        if hasattr(m, '_conic_field_inputs'):
            raise ValueError('A comparison emitted its field list twice')
        if root.key() != b.P.v(spec['theta_slot']).key() or error.key() != b.P.v(spec['error_slot']).key():
            raise ValueError('Unexpected old shared-root interface')
        inputs = []
        for pair in expressions:
            if len(pair) != 2 or any(any(len(mon) > 1 for mon in value.d) for value in pair):
                raise ValueError('Conic field coefficients must be affine')
            inputs.append([m.bind(value, 'conic field coefficient') for value in pair])
        m._conic_field_inputs = inputs
        # The pinned preceding hook expects the old list length 1+2m.
        # This slot is immediately checked and removed by call() below.
        # It is never an input to a conic batch or an emitted field test.
        return [spec['error_slot']]+[v for pair in inputs for v in pair]
    b.field_tests = field_tests

    old_names = {spec['old_batch'] for spec in MODES.values()}
    def call(m, name, args, label=None):
        if name in old_names:
            if m.name not in MODES:
                raise ValueError('An old comparison batch has an outside caller')
            spec = MODES[m.name]
            if name != spec['old_batch'] or getattr(m, '_conic_called', False):
                raise ValueError('Wrong or repeated comparison batch call')
            expected = [spec['raw_slot'], spec['error_slot']]+[v for pair in m._conic_field_inputs for v in pair]
            if list(args) != expected:
                raise ValueError('Raw contact or field input mapping changed')
            m._conic_called = True
            return old_call(m, spec['batch'], [args[0]]+list(args[2:]), label)
        return old_call(m, name, args, label)
    b.M.call = call

    def save(m, **metadata):
        if m.name in MODES:
            spec = MODES[m.name]
            if not getattr(m, '_conic_called', False):
                raise ValueError('Comparison has no conic batch call')
            if metadata.get('field_inequality_orders') != spec['orders']:
                raise ValueError('Preceding hook field orders changed')
            metadata.update(
                comparison_norm=MODEL, conic_batch=spec['batch'],
                conic_field_inputs=deepcopy(m._conic_field_inputs),
                ignored_shared_root_inputs=[spec['theta_slot'], spec['error_slot']],
                conic_legacy_input_count=spec['legacy_free'],
            )
        return old_save(m, **metadata)
    b.M.save = save

    def comparison():
        # The preceding hook closes over the archive constructor for its
        # two small old batches. Suppress their files, then remove exactly
        # those unreachable temporary modules. Its comparison bodies and
        # metadata still regenerate through that pinned hook.
        temporary = {'q_batch13', 'q_batch25'}
        if any(name in b.MODULES for name in old_names):
            raise ValueError('Unexpected pre-existing old comparison batch')
        original_write = b.write
        def write(path, data):
            if path in {'modules/'+name+'.json' for name in temporary}:
                return
            return original_write(path, data)
        b.write = write
        try:
            old_comparison()
        finally:
            b.write = original_write
        if not temporary.issubset(b.MODULES):
            raise ValueError('Pinned hook did not emit its expected temporary batches')
        if any(call['module'] in old_names for module in b.MODULES.values() for call in module['calls']):
            raise ValueError('An old comparison batch remains reachable')
        for name in temporary:
            del b.MODULES[name]
        if any(name in b.MODULES for name in old_names):
            raise ValueError('Unexpected leftover old comparison batch')
        for name in ('q_compare_beta', 'q_compare_lucas'):
            spec = MODES[name]
            make_conic_batch(b, spec['batch'], spec['orders'])
    b.make_multi_comparison = comparison
    return dict(comparison_norm=MODEL, proof_sha256=PROOF_SHA256,
                source_pin_authorized=False, arithmetic_acceptance=False,
                modes=deepcopy(MODES), global_root_error_retained_but_unused=True,
                contact_inverse_emitted=False, joint_chart_interface=True,
                local_lucas_field_lists=True)
