"""Check identities, numerical budgets and pins, not the arithmetic theorems."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


class Polynomial(dict):
    """Tiny exact Z[s,b,u] arithmetic for the displayed identities."""
    def __add__(self, other):
        if isinstance(other, int):
            other = {(0, 0, 0): other}
        out = defaultdict(int, self)
        for key, value in other.items():
            out[key] += value
        return Polynomial({key: value for key, value in out.items() if value})

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({key: -value for key, value in self.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, int):
            other = {(0, 0, 0): other}
        out = defaultdict(int)
        for key, value in self.items():
            for key2, value2 in other.items():
                out[tuple(x+y for x, y in zip(key, key2))] += value*value2
        return Polynomial({key: value for key, value in out.items() if value})

    __rmul__ = __mul__

    def __pow__(self, exponent):
        result = Polynomial({(0, 0, 0): 1})
        for _ in range(exponent):
            result = result*self
        return result


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    supplied = json.loads((HERE/'SUPPLIED_SOURCES.json').read_bytes())
    dependencies = json.loads((HERE/'DEPENDENCIES.json').read_bytes())
    for item in supplied['files']:
        raw = (HERE/item['path']).read_bytes()
        assert len(raw) == item['bytes'] and sha256(raw).hexdigest() == item['sha256'], item['path']
    for item in dependencies['existing_files']:
        raw = (REPO/item['path']).read_bytes()
        assert sha256(raw).hexdigest() == item['sha256'], item['path']
    manuscript = (REPO/'quartic_4973.tex').read_text(encoding='utf-8')
    span = manuscript[manuscript.index(dependencies['span_start']):manuscript.index(dependencies['span_end'])]
    assert sha256(span.encode()).hexdigest() == dependencies['span_sha256']
    assert '\\label{hyp:o8-height}' in span
    assert 'Kret' not in span and 'vKK' not in span
    assert 'hyp:RC' not in span and 'hyp:PC' not in span
    assert (HERE/'existing-height-proof.tex').read_text(encoding='utf-8') == span

    forms = [(0, 1), (1, 0), (1, -1), (1, -2401), (32, 343)]
    assert all(gcd(a, b) == 1 for a, b in forms)
    determinants = []
    for i, (a, b) in enumerate(forms):
        for c, d in forms[i+1:]:
            determinant = a*d-b*c
            assert determinant != 0
            remainder = abs(determinant)
            for p in (2, 3, 5, 7):
                while remainder % p == 0:
                    remainder //= p
            assert remainder == 1
            determinants.append(determinant)
    assert [-Fraction(b, a) for a, b in forms[1:]] == [0, 1, 2401, Fraction(-343, 32)]

    sieve = bytearray(b'\x01')*76177
    sieve[0:2] = b'\x00\x00'
    for p in range(2, isqrt(76176)+1):
        if sieve[p]:
            sieve[p*p::p] = b'\x00'*len(sieve[p*p::p])
    primes = [p for p in range(2, 76177) if sieve[p]]
    assert len(primes) == 7499 and primes[-1] == 76163
    assert prod(primes).bit_length() == 109445
    assert 4608 < 2**13 and 210 < 2**8 and 4608 > 2**12
    assert 6**100 < 4608**100 and 128 < 4608
    assert 3+165888*13+24*109445 == 4783227
    assert 24+3600*8 == 28824 < 12*165888
    assert 854 < 6**4
    transfer_budget = Fraction(16, 24**4)+Fraction(25+3, 288)+Fraction(25, 16*288)
    assert transfer_budget < 1

    s, b, u = [Polynomial({tuple(int(i == j) for i in range(3)): 1}) for j in range(3)]
    denominator = s*s+3*b
    numerator = b*(s*s-b)
    assert not ((s*(numerator-b*denominator))**2-b*(b*denominator-numerator)*(b*denominator+3*numerator))
    h = b*(b-u*u)
    t_numerator, t_denominator = b*(s+u), u*s+b
    a = (b+3*u*u)*s*s+8*b*u*s+b*u*u+3*b*b
    assert not (t_numerator**2-b*t_denominator**2-h*(s*s-b))
    assert not (t_numerator**2+3*b*t_denominator**2-b*a)
    assert not ((8*b*u)**2-4*(b+3*u*u)*(b*u*u+3*b*b)+12*b*(b-u*u)**2)
    assert not (a-(b+3*u*u)*(s*s+3*b)-8*b*u*(s-u))
    print(json.dumps(dict(status='PASS', source_files=len(supplied['files']),
        existing_pins=len(dependencies['existing_files']), contact_determinants=determinants,
        prime_count=len(primes), primorial_bit_length=109445, height_log2_upper_bound=4783227,
        exponent=24, transfer_budget=str(transfer_budget), algebra='Exact cleared-denominator identities passed',
        scope='Pins, elementary identities and numerical bounds only; no modularity, height theorem or point-existence proof certified'), indent=2))


if __name__ == '__main__':
    main()
