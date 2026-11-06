"""Independent arithmetic checks for the reconstructed Brox program.

No producer/compiler imports. The source-review AST is interpreted directly,
including direct products rather than the IR's symmetric coefficient scheme.
Full evaluations use exact finite-field arithmetic. Selected small dependency
closures use Fraction. Neither kind of sampling proves a rational identity.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import reduce
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path
import random
import time


class Mod:
    p = 1000003

    def __init__(self, x=0):
        if isinstance(x, Mod): self.n = x.n
        elif isinstance(x, Fraction): self.n = x.numerator * pow(x.denominator, -1, self.p) % self.p
        else: self.n = int(x) % self.p

    def __add__(self, other): return Mod(self.n + Mod(other).n)
    __radd__ = __add__
    def __neg__(self): return Mod(-self.n)
    def __sub__(self, other): return self + -Mod(other)
    def __rsub__(self, other): return Mod(other) - self
    def __mul__(self, other): return Mod(self.n * Mod(other).n)
    __rmul__ = __mul__
    def __truediv__(self, other):
        n = Mod(other).n
        if not n: raise ZeroDivisionError('zero modular denominator')
        return Mod(self.n * pow(n, -1, self.p))
    def __rtruediv__(self, other): return Mod(other) / self
    def __pow__(self, exponent):
        if exponent < 0 and not self.n: raise ZeroDivisionError('zero modular power denominator')
        return Mod(pow(self.n, exponent, self.p))
    def __eq__(self, other): return self.n == Mod(other).n
    def __repr__(self): return str(self.n)


def kadd(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def kneg(x): return (-x[0], -x[1])
def ksub(x, y): return kadd(x, kneg(y))
def kscale(c, x): return (c*x[0], c*x[1])
def kmul(*xs):
    def mul(x, y): return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
    return reduce(mul, xs)
def kinv(x):
    n = x[0]**2-2*x[1]**2
    return (x[0]/n, -x[1]/n)
def kdiv(x, y): return kmul(x, kinv(y))
def kpow(x, n):
    r = (x[0]*0+1, x[1]*0)
    while n:
        if n & 1: r = kmul(r, x)
        x, n = kmul(x, x), n//2
    return r


class Source:
    def __init__(self, inventory, bases, number):
        self.number = number
        self.values = dict(bases)
        self.defs = {x['name']: x['expression'] for x in inventory['definitions']}

    def get(self, name):
        if name not in self.values:
            self.values[name] = self.expr(self.defs[name])
        return self.values[name]

    def expr(self, e, local=None):
        if isinstance(e, int): return self.number(e)
        if isinstance(e, str): return local[e] if local and e in local else self.get(e)
        op, *args = e
        if op == 'rat': return self.number(Fraction(*args))
        if op == 'formal_product': return ('formal_product', args)
        if op == 'point_component': return self.expr(args[0], local)[args[1]]
        if op == 'component': return self.expr(args[0], local)[args[1]]
        if op in ('pow', 'kpow'):
            value = self.expr(args[0], local)
            return value**args[1] if op == 'pow' else kpow(value, args[1])
        vals = [self.expr(x, local) for x in args]
        if op == 'field': return tuple(vals)
        if op == 'point': return dict(zip(('x', 'y'), vals))
        if op == 'add': return sum(vals)
        if op == 'sub': return vals[0]-vals[1]
        if op == 'mul': return reduce(lambda x, y: x*y, vals)
        if op == 'div': return vals[0]/vals[1]
        if op == 'kadd': return kadd(*vals)
        if op == 'ksub': return ksub(*vals)
        if op == 'kneg': return kneg(*vals)
        if op == 'kmul': return kmul(*vals)
        if op == 'kscale': return kscale(*vals)
        if op == 'kinv': return kinv(*vals)
        if op == 'kdiv': return kdiv(*vals)
        if op == 'conjugate': return (vals[0][0], -vals[0][1])
        if op == 'point_double':
            x, y = vals[0]['x'], vals[0]['y']
            m = kdiv(ksub(kscale(3, kpow(x, 2)), self.get('D')), kscale(2, y))
            nx = ksub(kpow(m, 2), kscale(2, x))
            return {'x': nx, 'y': ksub(kmul(m, ksub(x, nx)), y)}
        if op == 'point_subtract':
            x, y = vals[0]['x'], vals[0]['y']
            a, b = vals[1]['x'], vals[1]['y']
            m = kdiv(kadd(y, b), ksub(x, a))
            nx = ksub(ksub(kpow(m, 2), x), a)
            return {'x': nx, 'y': ksub(kmul(m, ksub(x, nx)), y)}
        if op == 'evaluate_field_polynomial':
            variable, *factors = vals[0][1]
            # The source product is evaluated as factors. No coefficient
            # recursion or Horner routine from the producer is used here.
            return kmul(*(self.expr(f, {variable: vals[1]}) for f in factors))
        raise ValueError(op)


def base_mapping(name):
    if name == 'X': return 'input'
    if name == 'scalar.t': return 'scalar.preparation'
    if name == 'epsilon.minus': return 'correction.sign'
    if name.startswith('epsilon.'): return name.replace('epsilon.', 'correction.')
    if name.startswith('pole.'):
        _, i, comp = name.split('.')
        return f'detector{i}.{comp}'
    if name.startswith('half.'):
        _, q, comp = name.split('.')
        return q.replace('_', '')+'.half.'+comp.replace('a', 'x').replace('b', 'y')
    return name


def terms_value(terms, coordinates, parameter, number):
    return sum(number(Fraction(t['coefficient'])) * parameter**t.get('sPower', 0)
               * reduce(lambda a, i: a*coordinates[i], t['monomial'], number(1))
               for t in terms)


def evaluate_ir(ir, bases, parameter, number, targets=None):
    coordinates = dict(bases)
    gates = {g['coordinateId']: g for g in ir['gates']}
    def evaluate(i):
        if i in coordinates: return coordinates[i]
        g = gates[i]
        for d in g['dependencies']: evaluate(d)
        ev = lambda t: terms_value(t, coordinates, parameter, number)
        if g['operation'] == 'quadratic_assignment': answer = ev(g['expression'])
        elif g['operation'] == 'rational_quotient': answer = ev(g['numerator'])/ev(g['denominator'])
        elif g['operation'] == 'field_quotient_component':
            # Solve the displayed 2x2 linear system by its determinant.
            # Kept separate from the source Q(sqrt(2)) division helper.
            a, b = map(ev, g['numerator'])
            c, d = map(ev, g['denominator'])
            determinant = c*c-2*d*d
            answer = (a*c-2*b*d)/determinant if g['component'] == 0 else (b*c-a*d)/determinant
        else: raise ValueError(g['operation'])
        coordinates[i] = answer
        return answer
    for i in (targets if targets is not None else gates): evaluate(i)
    return coordinates


def comparisons(inventory):
    """Explicit semantic correspondences, independent of gate allocation."""
    result = []
    def scalar(alias, expression): result.append((alias, expression))
    def field(alias, expression):
        for c in range(2): scalar(f'{alias}.{c}', ['component', expression, c])
    def point(alias, name):
        for comp in ('x', 'y'): field(alias+'.'+comp, ['point_component', name, comp])
    for q in ['A', 'S', 'T', 'Z', 'H', 'U_A', 'U_S', 'U_T', 'U_Z']:
        point(q.replace('_', ''), q)
    for q in ['P', 'A', 'S', 'T', 'Z']:
        point(q+'2', 'twice.'+q); point(q+'4', 'four.'+q)
    for i, q in enumerate(['H', 'U_A', 'U_S', 'U_T', 'U_Z']):
        point(f'V{i}', f'V{i}')
        for prefix, source in [(f'U{i}', q), (f'V{i}', f'V{i}')]:
            field(prefix+'.f', 'f.'+source); field(prefix+'.z', 'z.'+source)
            field('log'+prefix, 'ell.'+source)
    for i in range(1, 5):
        # LP is the raw quotient; the IR applies conjugation in test10..13.
        field(f'L{i}', f'L{i}'); field(f'LP{i}', ['conjugate', f'Lprime{i}'])
    for i, test in enumerate(inventory['field_tests']): field(f'test{i}', test['name'])
    scalar('beta', 'beta')
    for i in range(9):
        for key in ['t', 'R', 'q1', 'q16', 'q52']:
            scalar(f'detector{i}.{key}', f'detector.{i}.{key}')
        field(f'detector{i}.W', f'detector.{i}.W')
        scalar(f'detector{i}.Bsemantic', f'pole.{i}.b')
        scalar(f'detector{i}.h', f'pole.{i}.h')
    for i in range(6): scalar(f'scalar.leaf{i}', f'scalar.leaf{i+1}')
    for key in ['r', 'n0', 'n1', 'n3', 'W', 'b', 'U', 'h']:
        scalar('scalar.'+key, 'scalar.'+key)
    scalar('scalar.nLeft', 'scalar.m0'); scalar('scalar.nRight', 'scalar.m1')
    field('scalar.zRatio', 'scalar.ratio')
    field('Sscalar.f', 'f.S'); field('Sscalar.z', 'z.S')
    scalar('anchor.physicalA', 'anchor.A')
    return result


def structural_mapping(name):
    if name.startswith('curve.'):
        _, q, c = name.split('.')
        return q.replace('_', '')+f'.curve.{c}'
    if name.startswith('pole.'):
        _, i, which = name.split('.')
        return f'detector{i}.{which}Conic'
    if name.startswith('boolean.'):
        component = name.split('.')[1]
        return 'correction.boolean'+str(['2', '3', '5', '7', '11', '13', '17', 'minus'].index(component))
    if name.startswith('scalar.pole.'): return 'scalar.'+name.split('.')[-1]+'Conic'
    if name == 'anchor': return 'anchor.equation'
    raise ValueError(name)


def check_equal(name, actual, expected):
    if actual != expected:
        raise AssertionError(f'{name}: IR={actual!r}; source={expected!r}')


def finite_sample(ir, inventory, prime, seed):
    Mod.p = prime
    rng = random.Random(seed)
    bases = {c['id']: Mod(rng.randrange(1, prime)) for c in ir['coordinates'] if c['kind'] in ('base', 'input')}
    name_ids = {c['name']: c['id'] for c in ir['coordinates']}
    # All Boolean choices are explicitly sampled as Boolean. Other base
    # variables are generic and need not satisfy structural equations.
    for name, i in name_ids.items():
        if name.startswith('correction.') and i in bases: bases[i] = Mod(rng.randrange(2))
    parameter = Mod(rng.randrange(1, prime))
    source_bases = {b['name']: bases[name_ids[base_mapping(b['name'])]] for b in inventory['base_variables']}
    source_bases['kappa'] = parameter**2
    source = Source(inventory, source_bases, Mod)
    coordinates = evaluate_ir(ir, bases, parameter, Mod)
    for d in inventory['definitions']: source.get(d['name'])
    pairs = comparisons(inventory)
    for alias, expr in pairs:
        check_equal(alias, terms_value(ir['values'][alias]['terms'], coordinates, parameter, Mod), source.expr(expr))
    # Every gate's actual residual, not just its evaluator metadata, is checked.
    for row in ir['residuals']:
        if row['kind'] == 'gate': check_equal(row['name'], terms_value(row['terms'], coordinates, parameter, Mod), Mod(0))
    residuals = {r['name']: r for r in ir['residuals']}
    for row in inventory['structural_constraints']:
        other = residuals[structural_mapping(row['name'])]
        check_equal(row['name'], terms_value(other['terms'], coordinates, parameter, Mod), source.expr(row['residual']))
    # Explicitly compare the displayed local-parameter product at each detector,
    # independently of both the symmetric product and q exponent simplification.
    for i in range(9):
        R, delta = source.get(f'detector.{i}.R'), source.get(f'detector.{i}.delta')
        factors = []
        for test in inventory['field_tests']:
            m = test['order']; D = source.get(test['name'])
            normalized = kscale(1/(delta**(m+1)*R**m), D)
            factors.append(kadd((Mod(1), Mod(0)), kscale(R, kpow(normalized, 2))))
        check_equal(f'direct detector {i}', kmul(*factors), source.get(f'detector.{i}.W'))
    return {'prime': prime, 'seed': seed, 'parameterSpecialization': parameter.n,
            'baseValues': [bases[i].n for i in sorted(bases)],
            'arithmeticGates': len(ir['gates']), 'gateResiduals': sum(r['kind']=='gate' for r in ir['residuals']),
            'semanticAliases': len(pairs), 'structuralResiduals': len(inventory['structural_constraints']),
            'directDetectorProducts': 9, 'status': 'pass'}


def fraction_samples(ir, inventory):
    wanted = [(alias, expr) for alias, expr in comparisons(inventory)
              if alias.startswith(('A.x.', 'A.y.', 'V1.x.', 'V1.y.', 'logU0.', 'logU1.'))]
    ids = {c['name']: c['id'] for c in ir['coordinates']}
    rng = random.Random(1315)
    bases = {c['id']: Fraction(rng.randrange(1, 6), rng.randrange(1, 4))
             for c in ir['coordinates'] if c['kind'] in ('base', 'input')}
    source_bases = {b['name']: bases[ids[base_mapping(b['name'])]] for b in inventory['base_variables']}
    source_bases['kappa'] = Fraction(9)
    source = Source(inventory, source_bases, Fraction)
    targets = {i for name, _ in wanted for t in ir['values'][name]['terms'] for i in t['monomial']}
    coordinates = evaluate_ir(ir, bases, Fraction(3), Fraction, targets)
    maxbits = 0
    for name, expr in wanted:
        actual = terms_value(ir['values'][name]['terms'], coordinates, Fraction(3), Fraction)
        expected = source.expr(expr)
        check_equal(name, actual, expected)
        maxbits = max(maxbits, actual.numerator.bit_length(), actual.denominator.bit_length())
    return {'status': 'pass', 'seed': 1315, 'parameterSpecialization': 3,
            'semanticAliases': [name for name, _ in wanted],
            'evaluatedCoordinates': len(coordinates), 'maximumResultBits': maxbits,
            'meaning': 'Exact rational samples, not universal identities.'}


class Poly:
    """Tiny independent Q-polynomial ring for the anchor identity."""
    def __init__(self, value=0):
        self.terms = dict(value.terms) if isinstance(value, Poly) else ({(): Fraction(value)} if value else {})
    @classmethod
    def var(cls, name):
        x = cls(); x.terms = {(name,): Fraction(1)}; return x
    def __add__(self, other):
        out = Poly(self)
        for k, v in Poly(other).terms.items():
            out.terms[k] = out.terms.get(k, 0)+v
            if not out.terms[k]: del out.terms[k]
        return out
    __radd__ = __add__
    def __neg__(self): return self * -1
    def __sub__(self, other): return self + -Poly(other)
    def __rsub__(self, other): return Poly(other)-self
    def __mul__(self, other):
        out = Poly()
        for a, x in self.terms.items():
            for b, y in Poly(other).terms.items():
                k = tuple(sorted(a+b)); out.terms[k] = out.terms.get(k, 0)+x*y
        out.terms = {k:v for k,v in out.terms.items() if v}
        return out
    __rmul__ = __mul__
    def __truediv__(self, other): return self * (1/Fraction(other))
    def __pow__(self, n): return reduce(lambda a, _: a*self, range(n), Poly(1))
    def __eq__(self, other): return self.terms == Poly(other).terms
    def __repr__(self): return repr(self.terms)


def anchor_identity(ir, translated):
    U, V, W, S = [Poly.var(x) for x in ('U', 'V', 'W', 'S')]
    original = {c['id']: Poly.var('x'+str(c['id'])) for c in ir['coordinates']}
    changed = dict(original)
    u, v, w = ir['anchor']['privateCoordinateIds']
    original.update({u: S+(U-3*V+3*W)/4, v: S/2+V/4, w: 3*S/2+W/4})
    changed.update({u: U, v: V, w: W})
    oldrow = ir['residuals'][ir['anchor']['rowId']]
    newrow = translated['residuals'][translated['anchor']['rowId']]
    oldvalue = terms_value(oldrow['terms'], original, S, Poly)
    newvalue = terms_value(newrow['terms'], changed, S, Poly)
    check_equal('symbolic anchor affine identity', newvalue, 16*oldvalue)
    check_equal('anchor inverse U', 4*original[u]+12*original[v]-12*original[w]+8*S, U)
    check_equal('anchor inverse V', 4*original[v]-2*S, V)
    check_equal('anchor inverse W', 4*original[w]-6*S, W)
    other_differences = [i for i, (a,b) in enumerate(zip(ir['residuals'], translated['residuals']))
                         if i != ir['anchor']['rowId'] and a['terms'] != b['terms']]
    check_equal('unchanged nonanchor rows', other_differences, [])
    return {'status': 'pass', 'identity': 'translated actual IR anchor = 16 * original actual IR anchor after affine substitution',
            'ring': 'Q[S,U,V,W,all original nonprivate coordinates]',
            'inverseIdentities': 3, 'otherChangedResiduals': other_differences,
            'meaning': 'Universal polynomial identity over Q, with S unexpanded.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    paths = {key: args.root / rel for key, rel in {
        'sourceInventory': 'source-review/source_inventory.json',
        'rawIR': 'builder/raw-ir.json', 'translatedIR': 'builder/raw-translated-ir.json'}.items()}
    data = {key: json.loads(path.read_text()) for key, path in paths.items()}
    started = time.monotonic()
    report = {'status': 'running', 'importsProducerOrCompiler': False,
              'inputs': {key: {'path': path.relative_to(args.root).as_posix(), 'sha256': sha256(path.read_bytes()).hexdigest()} for key,path in paths.items()},
              'scope': ['Source AST arithmetic versus generated raw IR.',
                        'All actual arithmetic gate residuals and 47 source structural residual functions.',
                        'Exact finite-field samples with all encountered denominators nonzero.',
                        'Selected exact rational samples and universal symbolic anchor identity.'],
              'limitations': ['Sample agreement does not prove rational identities or structural solution existence.',
                              'Generic halfpoints need not lie on the elliptic curve.',
                              'S is specialized to small residues only for tests. No coefficient-height claim follows.',
                              'No external arithmetic theorem, domain theorem, elimination, or final coefficient table is certified here.']}
    try:
        samples = []
        rejected = []
        for prime in [1000003, 1000037, 1000099]:
            assert all(prime % d for d in range(2, isqrt(prime)+1))
            assert pow(2, (prime-1)//2, prime) == prime-1
            for j in range(2):
                seed = 2026110600+j+prime
                for attempt in range(20):
                    try:
                        samples.append(finite_sample(data['rawIR'], data['sourceInventory'], prime, seed+attempt))
                        break
                    except ZeroDivisionError as error:
                        rejected.append({'prime': prime, 'seed': seed+attempt, 'reason': str(error)})
                else: raise AssertionError('Unable to find valid generic point in 20 attempts')
        report['finiteFieldSamples'] = samples
        report['rejectedZeroDenominatorSamples'] = rejected
        report['rationalSamples'] = fraction_samples(data['rawIR'], data['sourceInventory'])
        report['symbolicAnchor'] = anchor_identity(data['rawIR'], data['translatedIR'])
        report['status'] = 'pass'
    except Exception as error:
        report['status'] = 'fail'; report['error'] = repr(error)
        raise
    finally:
        report['wallSeconds'] = round(time.monotonic()-started, 3)
        target = args.output or args.root/'oracle/results.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps({k:v for k,v in report.items() if k in ['status', 'error', 'wallSeconds']}))


if __name__ == '__main__': main()
