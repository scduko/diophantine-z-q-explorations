"""Tiny affine-cofactor discovery and circular-proof regression tests."""
from collections import defaultdict
from copy import deepcopy
from types import SimpleNamespace
import json
import time

import check_localized as check
import probe_localized as loc
from probe_unit_relations import UnitSearch
from probe_affine_unit_relations import discover_units
from test_unit_relations import fixture, verify


def main():
    assert __debug__
    rows, _, _ = fixture()
    units = discover_units(rows)
    factor = {(4,): 1, (): -1}
    proof = units[loc.signature(factor)][0][1]
    check.prove_unit(rows, factor, proof, 5, 12)
    try: check.prove_unit(rows, factor, proof, 3, 12)
    except AssertionError: pass
    else: raise AssertionError('Defining row incorrectly proved its own denominator')
    # An independent pivot can use this retained first-leaf proof.
    rows[2] = {(4,5):1,(5,):-1,(6,7):-1}
    args = SimpleNamespace(max_support_terms=12,max_consumers=8,max_high_terms=240,
        max_rows_per_term=16,max_generators=240,max_linear_terms=1200,max_bits=512,
        max_row_terms=96,allocated=12)
    original = loc.discover_units
    loc.discover_units = discover_units
    try:
        search = UnitSearch(deepcopy(rows),args)
        proof = next(p for i,v,p in search.candidates() if (i,v)==(2,5))
        event,_,stats = search.attempt(2,5,proof,time.monotonic()+5)
        verify(rows,event['data'],event['patches'])
        assert stats['support_rows'] > 0
    finally: loc.discover_units = original
    print(json.dumps({'status':'PASS','affine_unit_discovered':True,
                      'circular_pivot_proof_rejected':True,'producer_event_replayed':True}))


if __name__ == '__main__': main()
