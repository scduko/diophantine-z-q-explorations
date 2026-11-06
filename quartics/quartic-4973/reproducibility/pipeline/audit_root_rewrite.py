"""Independent literal specification of the doubled-index root source delta.

No producer is imported. The four baseline modules are pinned. The caller must
separately bind the complete parent source, check unchanged modules and perform
full source flattening. This is an arithmetic-source change, not an assertion
that the old 2E root predicate and the new E root predicate are equivalent.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

PINS = {
    'Z_definition': '5e96bf1b0de4e1694dcc7ff21a9a7b69b5e2cc61295c2fc2816696092c5dacde',
    'q_compare4': '924daadfdb5fb9f13b9e06fc7e457f224115d2e34801c070810d3ab5eef310c4',
    'q_compare_beta': '75189120b018c23bbf1573de56687103160872aca41d3d1d35138abb7b05203e',
    'q_compare_lucas': 'a9157980855175cc0072f63c193c43f31c1350d850fdaeb3569d75e738229feb',
}
PROOF = 'ecdbfc9acd575a8ab194f8e76c356e7898544a506c705a40f169c6686c70a80e'
CONTRACT = '4e41f830938c3bdf8b5361b410a2fb639bd74299f0461fb356afe2efb012f2b7'
SEMANTICS = '2Q=n_Q Pstar, n_Q integer'
MAX_NODES = 100000


class AuditResourceError(RuntimeError):
    pass


def bounded(obj):
    """Keep public helper entry points bounded and reject non-JSON scalar types."""
    todo = [(obj, 0)]; count = 0
    while todo:
        value, depth = todo.pop(); count += 1
        if count > MAX_NODES or depth > 30:
            raise AuditResourceError('Root delta object limit')
        if type(value) is dict:
            if len(value) > 1000 or any(type(k) is not str for k in value):
                raise AuditResourceError('Root delta dictionary limit')
            todo.extend((v, depth + 1) for v in value.values())
        elif type(value) is list:
            if len(value) > 10000:
                raise AuditResourceError('Root delta list limit')
            todo.extend((v, depth + 1) for v in value)
        elif type(value) is str:
            if len(value) > 10000:
                raise AuditResourceError('Root delta string limit')
        elif type(value) is int:
            if value.bit_length() > 1024:
                raise AuditResourceError('Root delta integer limit')
        elif value is None or type(value) is bool:
            pass
        else:
            raise AssertionError('Non-JSON root delta scalar')


def wire(obj):
    bounded(obj)
    return (json.dumps(obj, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def exact(actual, expected, message):
    bounded(actual); bounded(expected)
    # JSON text distinguishes bool from int, unlike Python container equality.
    assert json.dumps(actual, sort_keys=True, separators=(',', ':')) == json.dumps(
        expected, sort_keys=True, separators=(',', ':')), message


def pin(obj, name):
    assert sha256(wire(obj)).hexdigest() == PINS[name], 'Pinned parent ' + name


def load_parent(directory):
    result = {}
    for name, digest in PINS.items():
        path = Path(directory) / (name + '.json')
        if path.stat().st_size > 2000000:
            raise AuditResourceError('Root parent file limit')
        data = path.read_bytes()
        assert sha256(data).hexdigest() == digest, 'Pinned parent file ' + name
        result[name] = json.loads(data)
        pin(result[name], name)
    return result


def r(*terms):
    """Literal integral quadratic row, without general field arithmetic."""
    out = {}
    for coefficient, variables in terms:
        monomial = tuple(sorted(variables))
        assert len(monomial) <= 2
        out[monomial] = out.get(monomial, 0) + coefficient
    return [[c, list(m)] for m, c in sorted(out.items()) if c]


def intervals(*pairs):
    return {i for lo, hi in pairs for i in range(lo, hi + 1)}


REMOVED_VARIABLES = intervals((2,13), (18,23), (28,29), (34,45), (50,61),
    (68,73), (78,83), (92,111), (192,197), (202,207), (212,213))
REMOVED_ROWS = intervals((1,24), (29,56), (58,71), (80,99), (180,193), (198,199))
LIVE_IDS = [i for i in range(349) if i not in REMOVED_VARIABLES]
VARIABLE_MAP = {old: new for new, old in enumerate(LIVE_IDS)}
ROW_MAP = {old: new for new, old in enumerate(i for i in range(345) if i not in REMOVED_ROWS)}


def ids(old):
    return [VARIABLE_MAP[i] for i in old]


def row_ids(old):
    return [ROW_MAP[i] for i in old]


def literal_appendix():
    rows = []; log = []; charts = {}
    for role, x, y, square, square_row in (
        ('A',14,16,112,100), ('S',30,32,132,120),
        ('T',46,48,152,140), ('Z',62,64,172,160)):
        start = 329 + len(rows)
        rows += [
            r((1,[y,y]), (2,[y+1,y+1]), (-1,[x,square]),
              (-2,[x+1,square+1]), (11,[x]), (-12,[x+1])),
            r((2,[y,y+1]), (-1,[x,square+1]), (-1,[x+1,square]),
              (-6,[x]), (11,[x+1])),
        ]
        log += [['equation',start+j,'general root '+role+' curve.'+str(j)] for j in range(2)]
        charts[role] = dict(kind='first_double_curve', x=ids([x,x+1]), y=ids([y,y+1]),
            square=ids([square,square+1]), square_rows=row_ids([square_row,square_row+1]),
            curve_rows=row_ids([start,start+1]))
        if role == 'S':
            charts[role].update(f=ids([26,27]), z=ids([24,25]))
    for role, f, z, k in (('height J',76,74,345), ('common comparison J',200,198,347)):
        start = 329 + len(rows)
        log += [['variable',k+j,'general root '+role+'.k.'+str(j)] for j in range(2)]
        rows += [
            r((1,[k]), (-1,[f,z]), (-2,[f+1,z+1])),
            r((1,[k+1]), (-1,[f,z+1]), (-1,[f+1,z])),
            r((1,[f]), (-1,[z,z]), (-2,[z+1,z+1]), (11,[k,k]),
              (22,[k+1,k+1]), (-24,[k,k+1])),
            r((1,[f+1]), (-2,[z,z+1]), (-6,[k,k]),
              (-12,[k+1,k+1]), (22,[k,k+1])),
        ]
        log += [['equation',start+j,'general root '+role+' '+
                 ('k=fz.'+str(j) if j < 2 else 'reciprocal curve.'+str(j-2))] for j in range(4)]
        charts[role] = dict(kind='reciprocal_f_z', f=ids([f,f+1]), z=ids([z,z+1]),
                           k=ids([k,k+1]), curve_rows=row_ids(list(range(start,start+4))))
    assert len(rows) == 16
    return rows, log, charts


def expected_root(parent):
    pin(parent, 'Z_definition')
    result = deepcopy(parent)
    added, added_log, charts = literal_appendix()
    old_rows = deepcopy(parent['residuals']) + added
    for i, terms in {
        196: ((2285245536,[210]), (-8226963211,[])),
        197: ((1713934152,[211]), (1063929023,[])),
        271: ((143614994586,[285]), (-70757419981,[])),
        272: ((574459978344,[286]), (-344600359813,[])),
    }.items():
        old_rows[i] = r(*terms)
    result['locals'] = 258
    result['residuals'] = [[[coefficient, ids(monomial)] for coefficient, monomial in old_rows[i]]
                           for i in range(345) if i not in REMOVED_ROWS]
    result['calls'] = [dict(call, args=ids(call['args'])) for call in parent['calls']]
    replacement_labels = {196:'fixed 4R x.0',197:'fixed 4R x.1',271:'fixed 4R q.0',272:'fixed 4R q.1'}
    result['construction_log'] = []
    for kind, index, label in parent['construction_log'] + added_log:
        assert kind in ('variable','equation')
        index_map = VARIABLE_MAP if kind == 'variable' else ROW_MAP
        if index in index_map:
            result['construction_log'].append([kind,index_map[index],
                replacement_labels.get(index,label) if kind == 'equation' else label])
    result['proxy_indices'] = ids([1])
    result['point_coordinates'] = {role:ids(list(range(x,x+4))) for role,x in [('A',14),('S',30),('T',46),('Z',62)]}
    result['joint_chart_targets'] = [{
        'q':ids([285+4*j,286+4*j]), 'r':ids([305+8*j,306+8*j]),
        's':ids([307+8*j,308+8*j]), 't':ids([309+8*j,310+8*j]),
        'u':ids([311+8*j,312+8*j])} for j in range(5)]
    del result['jacobi_targets']
    result['root_targets'] = []
    for j in range(5):
        target = dict(kind='fixed_4R' if j==0 else 'quadruple',
                      p=ids([285+4*j,286+4*j]), f=ids([287+4*j,288+4*j]))
        target['x' if j==0 else 'original'] = ids(list(range(210+4*j,212+4*j if j==0 else 214+4*j)))
        result['root_targets'].append(target)
    result.update(chart='general_E_mixed', baseline_chart=10, general_root_charts=charts,
        root_carrier='nontorsion E(K)', root_index_semantics=SEMANTICS,
        comparison_base=dict(x=['1','1'],y=['0','2'],identity='2R=Pstar',fixed_target='4R=2Pstar'),
        beta_comparison_scale=2,height_effective_multiplier=5,
        fixed_target_bindings=dict(coordinates=ids([210,211,285,286]),rows=row_ids([196,197,271,272])))
    result['general_root_rewrite'] = dict(parent_root_sha256=PINS['Z_definition'], proof_sha256=PROOF,
        composition_contract_sha256=CONTRACT, original_removed_variables=sorted(REMOVED_VARIABLES),
        original_removed_rows=sorted(REMOVED_ROWS),original_added_k_variables=[345,346,347,348],
        original_replaced_rows=[196,197,271,272],
        original_index_scope='all original_* fields are historical pre-rewrite IDs',
        raw_variable_delta=-86,raw_row_delta=-86)
    return result


def expected_comparison(parent):
    name = parent['name']; assert name in PINS and name != 'Z_definition'
    pin(parent, name); result = deepcopy(parent)
    if name != 'q_compare_lucas':
        # Literal rows and coordinates from the pinned independent comparator.
        rid, target, ratio = {'q_compare4':(86,154,108),'q_compare_beta':(22,54,48)}[name]
        exact(parent['residuals'][rid],r((1,[0]),(1,[target]),(-1,[ratio])), 'Old beta row')
        result['residuals'][rid] = r((2,[0]),(1,[target]),(-1,[ratio]))
        result.update(beta_comparison_scale=2,root_index_semantics=SEMANTICS,
                      beta_field_row=rid,beta_rewrite_parent_sha256=PINS[name])
    result.update(comparison_fixed_target='4R=2Pstar', root_index_semantics=SEMANTICS)
    assert parent['input_layout'].count('Fq(P4)') == 1
    result['input_layout'] = parent['input_layout'].replace('Fq(P4)','Fq(R4)')
    return result


def check_root(parent, candidate):
    exact(candidate, expected_root(parent), 'Complete doubled-index root mismatch')
    # Independently check that the specified log declares every coordinate and
    # row exactly once, and never uses a coordinate before its declaration.
    available = {0}; seen_rows = set()
    for kind, index, label in candidate['construction_log']:
        if kind == 'variable':
            assert index == len(available), 'Root declaration sequence'
            available.add(index)
        else:
            assert index not in seen_rows, 'Root duplicate row declaration'
            seen_rows.add(index)
            assert all(i in available for _, mon in candidate['residuals'][index] for i in mon), 'Root forward row reference'
    assert available == set(range(259)) and seen_rows == set(range(243)), 'Root declaration coverage'
    assert all(i in available for call in candidate['calls'] for i in call['args']), 'Root call coordinate coverage'
    return dict(locals=258,rows=243,calls=39,raw_variable_delta=-86,raw_row_delta=-86)


def check_comparison(parent, candidate):
    exact(candidate, expected_comparison(parent), 'Complete doubled-index comparator mismatch')
    return dict(name=parent['name'],rows=len(parent['residuals']),beta_scale=2 if parent['name']!='q_compare_lucas' else None)


def check_modules(parents, candidates):
    """Check the four changed modules. Outer checker owns the full module set."""
    assert set(parents) == set(PINS) and set(candidates) == set(PINS), 'Four-module delta scope'
    root = check_root(parents['Z_definition'],candidates['Z_definition'])
    comparisons = [check_comparison(parents[n],candidates[n]) for n in PINS if n!='Z_definition']
    return dict(status='PASS: LITERAL ROOT AND BETA DELTA',root=root,comparisons=comparisons,
                arithmetic_acceptance='requires pinned doubled-index arithmetic proof',
                complete_source_acceptance=False)
