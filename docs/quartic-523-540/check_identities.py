"""Small exact algebra checks supporting the arithmetic review."""
from fractions import Fraction as Q
import json
from pathlib import Path
from independent_finite import add, mul, OUT

ROOT = Path(__file__).resolve().parent


def c(value):
    return {} if not value else {(0, ()): Q(value)}


def scale(p, value):
    return {key: coefficient*value for key, coefficient in p.items() if coefficient*value}


def power(p, exponent):
    result = c(1)
    for _ in range(exponent):
        result = mul(result, p)
    return result


h, j, t = [{(0, (i,)): Q(1)} for i in range(3)]
x = power(h, 2)
d = add(power(h, 4), scale(power(j, 2), -1))
a = add(mul(t, h), x, j)
b = mul(a, t)
tangent = add(h, t)
t2 = scale(add(x, j), 2)


def reduce_t(p):
    result = {}
    for (s, monomial), coefficient in p.items():
        count = monomial.count(2)
        tail = tuple(v for v in monomial if v != 2) + (2,)*(count % 2)
        term = mul({(s, tail): coefficient}, power(t2, count//2))
        result = add(result, term)
    return result


checks = {
    'halfpoint_abscissa_identity': add(power(a, 2), scale(mul(a, power(t, 2)), -1), scale(d, -1)),
    'halfpoint_curve_equation': add(power(b, 2), scale(power(a, 3), -1), mul(d, a)),
    'tangent_slope_identity': add(scale(mul(tangent, b), 2), scale(power(a, 2), -3), d),
    'double_abscissa': add(power(tangent, 2), scale(a, -2), scale(x, -1)),
    'double_ordinate': add(mul(tangent, add(a, scale(x, -1))), scale(b, -1), scale(mul(h, j), -1)),
}
assert all(not reduce_t(p) for p in checks.values())

# Exact arithmetic in Q(sqrt(2)) for the displayed fixed point.
def ka(u, v): return (u[0]+v[0], u[1]+v[1])
def ks(u, v): return (u[0]-v[0], u[1]-v[1])
def km(u, v): return (u[0]*v[0]+2*u[1]*v[1], u[0]*v[1]+u[1]*v[0])
def kd(u, v):
    norm = v[0]*v[0]-2*v[1]*v[1]
    return km(u, (v[0]/norm, -v[1]/norm))
def scalar(value): return (Q(value), Q(0))

rx, ry, D = (Q(1), Q(1)), (Q(0), Q(2)), (Q(11), Q(-6))
assert km(ry, ry) == ks(km(km(rx, rx), rx), km(D, rx))
slope = kd(ks(km(scalar(3), km(rx, rx)), D), km(scalar(2), ry))
px = ks(km(slope, slope), km(scalar(2), rx))
py = ks(km(slope, ks(rx, px)), ry)
assert px == (Q(57, 8), Q(-7, 2)) and py == (Q(-165, 8), Q(417, 32))
ph, pj = (Q(-1), Q(7, 4)), (Q(39, 8), Q(-9, 2))
assert km(ph, ph) == px and km(ph, pj) == py
def mod7(v):
    value = v[0]+3*v[1]
    return value.numerator*pow(value.denominator, -1, 7) % 7
assert (mod7(px), mod7(py)) == (1, 6)

for alpha in range(7, 62, 6):
    k = 2*(alpha-2)
    u, v = 0, 1
    for _ in range(k):
        u, v = v, alpha*v-u
    assert u % (alpha-2) == 0
    beta, tau = u//(alpha-2), v
    assert beta % 2 == tau % 2 == 1
    assert tau*tau-alpha*(alpha-2)*tau*beta+(alpha-2)**2*beta*beta == 1

assert 10*(7+2093966) < Q(50331647, 2)
assert Q(50331647, 2)*Q(13, 32) > 7+2093966
assert 7*Q(5, 2)+6 < 24
assert 7*4+6 < 40
result = {'odd_chart_identities': list(checks), 'fixed_point_doubling_and_chart': 'PASS',
          'bad_prime_7_reduction': [1, 6], 'lucas_finite_examples': 10,
          'anchor_integer_exponent_comparisons': 'PASS',
          'scope': 'Exact algebra and finite sanity checks; general valuation and completeness arguments reviewed separately.'}
(OUT / 'IDENTITIES.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
