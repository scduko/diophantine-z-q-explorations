"""Extend the frozen unit search with both affine factors of a product proof.

No new certificate rule: B*C=c*M proves either B or C nonzero. Every
elimination still requires its nonzero proof rows to exclude the removed
variable. In particular the defining row cannot prove its own pivot unit.
"""
from copy import deepcopy

import probe_localized as loc
import probe_unit_relations as search

base_discover_units = loc.discover_units


def discover_units(rows):
    units = base_discover_units(rows)
    extra = []
    for choices in list(units.values()):
        for _, proof in choices:
            if proof['kind'] != 'product_unit': continue
            factor = loc.primitive(loc.dec(proof['cofactor']))
            if not factor or max(map(len, factor)) != 1: continue
            reverse = deepcopy(proof)
            reverse['factor'], reverse['cofactor'] = proof['cofactor'], proof['factor']
            extra.append((factor, reverse))
    for factor, proof in extra:
        key = loc.signature(factor)
        if not any(p == proof for _, p in units[key]): units[key].append((factor, proof))
    return units


if __name__ == '__main__':
    loc.discover_units = discover_units
    search.main()
