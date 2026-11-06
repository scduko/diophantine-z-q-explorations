"""Exact reciprocal-G circuit producer. No arithmetic source acceptance here."""
from fractions import Fraction as F


def coefficients(count):
    result = [F(1)]
    if count > 1:
        result.append(F(-2, 5))
    for j in range(2, count):
        result.append(result[-1]*F(4*j-5, 4*j+1))
    return result


def emit_g(b, field, fcoords, precision, *, bind_output=True, hscale=1,
           scheme='auto', normalization='auto'):
    """Return the exact G pair, using quadratic rows and a quadratic output.

    Same positional interface as precision-next/reciprocal_kernel.emit_g.
    `hscale` changes a private intermediate, never the returned G value.
    """
    if type(precision) is not int or precision not in (12, 40, 44, 48):
        raise ValueError('Supported precisions: 12, 40, 44, 48')
    if type(hscale) is not int or hscale not in (1, 2, 3, 4):
        raise ValueError('hscale must be 1, 2, 3, or 4')
    if scheme == 'auto':
        scheme = 'direct' if precision == 12 else 'powers45' if precision == 44 else 'block3'
    if normalization == 'auto':
        normalization = 'a6' if scheme == 'block3' else 'unit'
    count = precision//4
    a = coefficients(count)
    one, zero = (b.P(1), b.P()), (b.P(), b.P())

    def bind(pair):
        return tuple(field.m.value(x) for x in pair)

    def linear(values):
        out = zero
        for scalar, pair in values:
            out = b.fa(out, b.scale(pair, scalar))
        return out

    if scheme == 'direct':
        if precision != 12 or normalization != 'unit' or hscale != 1:
            raise ValueError('The direct three-term circuit has one fixed profile')
        w = bind(b.raw_fmul(field.D, b.raw_fmul(fcoords, fcoords)))
        out = linear([(1, one), (a[1], w), (a[2], b.raw_fmul(w, w))])
    elif scheme == 'block3':
        if count not in (10, 11, 12) or normalization not in ('unit', 'a3', 'a6', 'a9'):
            raise ValueError('Unsupported block-three profile')
        pivot = F(1) if normalization == 'unit' else a[int(normalization[1:])]
        w = bind(b.raw_fmul(field.D, b.raw_fmul(fcoords, fcoords)))
        w2 = field.mul(w, w)
        w3 = field.mul(w2, w)
        low = linear([(a[3], one), (a[4], w), (a[5], w2)])
        mid = linear([(a[6], one), (a[7], w), (a[8], w2)])
        if count == 10:
            # A single quadratic definition includes the degree-six term.
            middle = b.fa(mid, b.scale(w3, a[9]))
            unscaled = b.fa(low, b.raw_fmul(w3, middle))
        else:
            w6 = field.mul(w3, w3)
            upper = linear([(a[9], one), (a[10], w)] +
                           ([(a[11], w2)] if count == 12 else []))
            unscaled = b.fa(b.fa(low, b.raw_fmul(w3, mid)), b.raw_fmul(w6, upper))
        u = bind(b.scale(unscaled, F(hscale)/pivot))
        out = b.fa(linear([(a[0], one), (a[1], w), (a[2], w2)]),
                   b.scale(b.raw_fmul(w3, u), pivot/F(hscale)))
    elif scheme in ('powers45', 'powers56'):
        if scheme == 'powers45' and count not in (10, 11):
            raise ValueError('powers45 covers ten or eleven coefficients')
        if scheme == 'powers56' and count != 12:
            raise ValueError('powers56 covers twelve coefficients')
        if normalization not in ('unit', 'coefficient', 'reciprocal_denominator'):
            raise ValueError('Unsupported power-coordinate normalization')
        exponents = [1, 2, 4, 5] if scheme == 'powers45' else [1, 2, 3, 5, 6]
        parents = {1: None, 2: (1, 1), 3: (1, 2), 4: (2, 2), 5: (1, 4) if scheme == 'powers45' else (2, 3), 6: (3, 3)}
        values = {0: one}
        for exponent in exponents:
            factor = F(1) if normalization == 'unit' else a[exponent] if normalization == 'coefficient' else F(1, a[exponent].denominator)
            if exponent == exponents[-1]:
                factor *= hscale
            product = b.raw_fmul(field.D, b.raw_fmul(fcoords, fcoords)) if exponent == 1 else b.raw_fmul(*(values[x] for x in parents[exponent]))
            allocated = bind(b.scale(product, factor))
            # Store an expression for the unscaled power, not another target.
            values[exponent] = b.scale(allocated, 1/factor)
        out = zero
        for exponent, coefficient in enumerate(a):
            if exponent in values:
                term = values[exponent]
            else:
                pairs = [(j, k) for j in values for k in values if j <= k and j+k == exponent]
                if not pairs:
                    raise AssertionError(('Power basis has a gap', exponent))
                left, right = min(pairs, key=lambda jk: (jk[1]-jk[0], jk))
                term = b.raw_fmul(values[left], values[right])
            out = b.fa(out, b.scale(term, coefficient))
    else:
        raise ValueError('Unknown circuit scheme')
    return bind(out) if bind_output else out


def profiles():
    """The fixed 44-case search contract, including bound and direct outputs."""
    result = []
    for bound in (False, True):
        result.append((12, 'direct', 'unit', 1, bound))
    for precision in (40, 44, 48):
        for normalization in ('a3', 'a6'):
            for scale in (1, 2):
                for bound in (False, True):
                    result.append((precision, 'block3', normalization, scale, bound))
        scheme = 'powers45' if precision in (40, 44) else 'powers56'
        for normalization in ('unit', 'coefficient', 'reciprocal_denominator'):
            for bound in (False, True):
                result.append((precision, scheme, normalization, 1, bound))
    assert len(result) == 44
    return result


def profile_name(profile):
    precision, scheme, normalization, scale, bound = profile
    return f'g{precision}-{scheme}-{normalization}-s{scale}-'+('bound' if bound else 'direct')+'.json'
