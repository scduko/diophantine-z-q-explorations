"""Small exact examples, malformed events, and bounded producer smoke tests."""
from copy import deepcopy
from fractions import Fraction
import time
from types import SimpleNamespace
from check_relation_eliminate import verify_event, normalize


def poly(terms, denominator=1):
    return {'terms': terms, 'denominator': denominator}


def fixture(square=False, rational=False):
    if square:
        rows = [{(3,): 1, (1, 2): -1}, {(4,): 1, (3, 3): -1},
                {(5,): 1, (1, 1): -1}, {(6,): 1, (2, 2): -1}]
        data = {'row': 0, 'variable': 3, 'replacement': poly([[1, [1, 2]]]),
                'reductions': [{'row': 1, 'terms': [
                    {'support': 2, 'multiplier': poly([[1, [2, 2]]])},
                    {'support': 3, 'multiplier': poly([[1, [5]]])}]}]}
        patches = [[0, []], [1, [[1, [4]], [-1, [5, 6]]]]]
    else:
        rows = [{(4,): 2 if rational else 1, (1, 2): -1},
                {(5,): 1, (3, 4): -2 if rational else -1},
                {(6,): 1, (2, 3): -1}]
        if rational:
            rows[0][()] = -1
        data = {'row': 0, 'variable': 4,
                'replacement': poly([[1, [1, 2]]]+([[1, []]] if rational else []), 2 if rational else 1),
                'reductions': [{'row': 1, 'terms': [
                    {'support': 2, 'multiplier': poly([[1, [1]]])}]}]}
        patches = [[0, []], [1, [[1, [5]], [-1, [1, 6]]]+([[-1, [3]]] if rational else [])]]
    return rows, {'kind': 'relation_eliminate', 'data': data, 'patches': patches}


def reject(name, mutate, square=False):
    rows, event = fixture(square=square)
    mutate(rows, event)
    try:
        verify_event(rows, event, 8)
    except (AssertionError, KeyError, ValueError, TypeError):
        return name
    raise AssertionError('Malformed event accepted: '+name)


def evaluate(row, values):
    total = Fraction(0)
    for mon, c in row.items():
        term = Fraction(c)
        for v in mon:
            term *= values[v]
        total += term
    return total


def main():
    for square, rational in [(False, False), (True, False), (False, True)]:
        rows, event = fixture(square, rational)
        patches = verify_event(rows, event, 8)
        assert patches[0] == {}
        if square:
            values = {1: 2, 2: 3, 3: 6, 4: 36, 5: 4, 6: 9}
        elif rational:
            values = {1: 2, 2: 3, 3: 5, 4: Fraction(7, 2), 5: 35, 6: 15}
        else:
            values = {1: 2, 2: 3, 3: 5, 4: 6, 5: 30, 6: 15}
        assert all(evaluate(row, values) == 0 for row in rows)
        assert all(evaluate(row, values) == 0 for row in patches.values())
    cases = [
        ('input removal', lambda r, e: e['data'].update(variable=0)),
        ('bad defining row', lambda r, e: r[0].update({(1, 2): -2})),
        ('bad replacement', lambda r, e: e['data']['replacement'].update(terms=[[2, [1, 2]]])),
        ('zero denominator', lambda r, e: e['data']['replacement'].update(denominator=0)),
        ('negative denominator', lambda r, e: e['data']['replacement'].update(denominator=-1)),
        ('noninteger denominator', lambda r, e: e['data']['replacement'].update(denominator=1.5)),
        ('replacement self-use', lambda r, e: e['data']['replacement'].update(terms=[[1, [4]]])),
        ('replacement cubic', lambda r, e: e['data']['replacement'].update(terms=[[1, [1, 2, 3]]])),
        ('replacement fresh variable', lambda r, e: e['data']['replacement'].update(terms=[[1, [9]]])),
        ('missing occurrence', lambda r, e: r.append({(4, 7): 1})),
        ('missing reduction', lambda r, e: e['data'].update(reductions=[])),
        ('duplicate reduction', lambda r, e: e['data']['reductions'].append(e['data']['reductions'][0])),
        ('support is affected', lambda r, e: e['data']['reductions'][0]['terms'][0].update(support=1)),
        ('support is defining row', lambda r, e: e['data']['reductions'][0]['terms'][0].update(support=0)),
        ('support contains eliminated variable', lambda r, e: r[2].update({(4,): 1})),
        ('duplicate support', lambda r, e: e['data']['reductions'][0]['terms'].append(e['data']['reductions'][0]['terms'][0])),
        ('wrong multiplier', lambda r, e: e['data']['reductions'][0]['terms'][0]['multiplier'].update(terms=[[2, [1]]])),
        ('multiplier self-use', lambda r, e: e['data']['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1, [4]]])),
        ('multiplier cubic', lambda r, e: e['data']['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1, [1, 2, 3]]])),
        ('multiplier fresh variable', lambda r, e: e['data']['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1, [9]]])),
        ('multiplier zero coefficient', lambda r, e: e['data']['reductions'][0]['terms'][0]['multiplier'].update(terms=[[0, [1]]])),
        ('multiplier duplicate monomial', lambda r, e: e['data']['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1, [1]], [1, [1]]])),
        ('wrong supplied row', lambda r, e: e['patches'][1][1].append([1, []])),
        ('missing supplied row', lambda r, e: e['patches'].pop()),
        ('duplicate supplied row', lambda r, e: e['patches'].append(e['patches'][0])),
    ]
    rejected = [reject(name, mutate) for name, mutate in cases]
    # These smoke tests exercise the producer independently, then submit its
    # exact output to the checker. Their systems contain only three/four rows.
    from probe_relation_eliminate import Search
    args = SimpleNamespace(max_support_terms=12, max_consumers=8, max_rows_per_term=16,
                           max_generators=240, max_high_terms=240, max_linear_terms=1200,
                           max_bits=512, max_row_terms=96)
    for square in (False, True):
        rows, want = fixture(square)
        search = Search(deepcopy(rows), args)
        result = search.attempt(0, 3 if square else 4, time.monotonic()+5)
        assert result is not None
        event, patches, stats = result
        checked = verify_event(rows, event, 8)
        assert checked.keys() == patches.keys()
        assert all(normalize(checked[i]) == normalize(row) for i, row in patches.items())
        if square:
            assert stats['quadratic_multiplier']
    print({'status': 'PASS', 'valid_cases': 3, 'malformed_cases_rejected': len(rejected),
           'producer_smoke_cases': 2, 'cases': rejected})


if __name__ == '__main__':
    main()
