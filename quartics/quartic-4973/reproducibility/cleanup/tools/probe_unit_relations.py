"""Search certified affine-unit pivots modulo retained quadratic equations.

Expands the current SOS once for exact coefficient control: remote execution
only. Every accepted event is also checked by independent check_localized.py.
The complete named-source replay remains mandatory after export.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

import check_localized as independent
import probe_localized as loc
import probe_relation_eliminate as rel


class UnitSearch(rel.Search):
    def candidates(self):
        self.units = loc.discover_units(self.rows)
        self.rowvars = [loc.variables(r) for r in self.rows]
        self.proof_cache = {}
        candidates = []
        for i, row in enumerate(self.rows):
            for v in sorted(self.rowvars[i]-{0}):
                split = loc.split(row, v)
                if split is None: continue
                a, n = split
                if not a or max(map(len, a)) != 1: continue
                choices = self.units.get(loc.signature(a), [])
                proof = next((p for _,p in choices if v not in loc.proof_variables(p, self.rowvars, self.proof_cache)), None)
                if proof is None: continue
                affected = self.incidence[v]-{i}
                if not affected or len(affected) > self.args.max_consumers: continue
                difficulty = (sum(len(self.rows[j]) for j in affected),len(affected),len(n),i,v)
                candidates.append((difficulty,i,v,proof))
        candidates.sort(key=lambda x:x[0])
        return [(i,v,proof) for _,i,v,proof in candidates]

    def attempt(self, i, v, proof, deadline):
        split = loc.split(self.rows[i], v)
        if split is None: return None
        a,n = split
        if not a or max(map(len,a)) != 1: return None
        # Earlier accepted events can alter a proof row. Independent checking
        # is repeated on the current state, never the cached initial state.
        try: independent.prove_unit(self.rows,a,proof,v,self.args.allocated)
        except AssertionError:
            self.reasons['unit_proof_changed'] += 1; return None
        affected = self.incidence[v]-{i}
        if not affected or len(affected)>self.args.max_consumers: return None
        valid_units = []
        for choices in self.units.values():
            if time.monotonic()>=deadline: raise rel.BoundExceeded('time_limit')
            for factor,p in choices:
                if v in loc.proof_variables(p,self.rowvars,self.proof_cache): continue
                try: independent.prove_unit(self.rows,factor,p,v,self.args.allocated)
                except AssertionError: continue
                valid_units.append((factor,p)); break
        # Try the denominator first, then all other independently certified
        # affine factors. Each exact quotient lowers polynomial degree.
        valid_units.sort(key=lambda item:(loc.signature(item[0]) != loc.signature(a),len(item[0]),loc.signature(item[0])))
        images={}; factors={}; products={}
        for j in sorted(affected):
            image=loc.cleared_substitute(self.rows[j],v,a,n)
            if len(image)>self.args.max_linear_terms:
                self.reasons['cleared_size_limit']+=1; return None
            factors[j]=[]; products[j]={():1}
            for factor,p in valid_units:
                if time.monotonic()>=deadline: raise rel.BoundExceeded('time_limit')
                while image and len(factors[j])<8:
                    quotient=loc.divide_exact(image,factor)
                    if quotient is None: break
                    image=quotient; products[j]=loc.mul(products[j],factor)
                    factors[j].append({'factor':loc.enc(factor),'proof':p})
            images[j]=image
        seed=set().union(*(set(rel.high(image)) for image in images.values())) if images else set()
        if len(seed)>self.args.max_high_terms:
            self.reasons['seed_limit']+=1; return None
        generators=self.generators(seed,self.incidence[v],v,deadline)
        basis=self.build_basis(generators,deadline)
        patches={i:{}}; reductions=[]
        for j,image in images.items():
            solution=self.solve(image,basis,deadline)
            if solution is None:
                self.reasons['high_part_not_spanned']+=1; return None
            multipliers=defaultdict(dict)
            for number,coefficient in solution.items():
                support,multiplier=generators[number][0]
                multipliers[support]=rel.plus(multipliers[support],{multiplier:coefficient})
            new=image; terms=[]
            for support,multiplier in sorted(multipliers.items()):
                if not multiplier: continue
                new=rel.plus(new,rel.times(multiplier,self.rows[support]),-1)
                full=rel.times(products[j],multiplier)
                if max(map(len,full),default=0)>2:
                    self.reasons['multiplier_degree_limit']+=1; return None
                terms.append({'support':support,'multiplier':rel.rational(full)})
            assert not rel.high(new) and v not in rel.vars_in(new)
            new=rel.primitive(new)
            if len(new)>self.args.max_row_terms:
                self.reasons['row_size_limit']+=1; return None
            patches[j]=new; reductions.append({'row':j,'terms':terms})
        data={'row':i,'variable':v,'denominator':loc.enc(a),'numerator':loc.enc(n),
              'nonzero':proof,'affected':sorted(affected),'reductions':reductions,
              'cancellations':[{'row':j,'factors':factors[j]} for j in sorted(affected)]}
        event={'kind':'localized_relation','data':data,'patches':[[j,loc.enc(p)] for j,p in sorted(patches.items())]}
        independent.relation_expected(self.rows,data,self.args.allocated,self.incidence,event['patches'])
        stats=dict(variable=v,definition=i,consumers=len(affected),high_terms=len(seed),
                   generated=len(generators),rank=len(basis),unit_proof=proof['kind'],
                   canceled_factors=sum(map(len,factors.values())),support_rows=sum(len(x['terms']) for x in reductions))
        return event,patches,stats


def main():
    assert __debug__, 'Assertions must remain enabled.'
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--events',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--research-dir',type=Path)
    parser.add_argument('--source-entry',type=Path)
    parser.add_argument('--seconds',type=float,default=120)
    parser.add_argument('--candidate-seconds',type=float,default=1)
    for name,default in [('candidates',20000),('operations',500),('consumers',8),('support-terms',12),
                         ('row-terms',96),('rows-per-term',16),('generators',240),('high-terms',240),
                         ('linear-terms',1200),('bits',512)]:
        parser.add_argument('--max-'+name,type=int,default=default)
    args=parser.parse_args()
    assert args.seconds>0 and args.candidate_seconds>0
    rows=[loc.dec(r) for r in json.loads(gzip.decompress((args.parent/'candidate-rows.json.gz').read_bytes()))]
    records=[json.loads(line) for line in gzip.decompress((args.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    source_entry = args.source_entry or args.parent/'source-entry.json'
    entry_bytes = source_entry.read_bytes()
    entry = json.loads(entry_bytes)
    assert entry['source_id'] == records[0]['source_id']
    assert entry['source_sha256'] == records[0]['source_sha256']
    assert hashlib.sha256(entry_bytes).hexdigest() == records[0]['source_entry_sha256']
    # This producer's unweighted coefficient accounting is exact only for
    # all-one inputs. Refuse a weighted parent rather than silently dropping it.
    weights=json.loads((args.parent/'weights.json').read_text()) if (args.parent/'weights.json').exists() else [1]
    assert all(type(w) is int and w==1 for w in weights)
    args.allocated=records[-1]['allocated_variables']
    records=[r for r in records if r['kind'] not in ('weights','final')]
    search=UnitSearch(rows,args)
    candidates=search.candidates()
    initial_active=sum(bool(ids) for ids in search.incidence.values())
    polynomial={}
    for row in rows: rel.add_to(polynomial,rel.times(row,row))
    assert max(map(abs,polynomial.values()))<2**80
    start=time.monotonic(); deadline=start+args.seconds
    stats=[]; events=[]; attempted=0
    for i,v,proof in candidates[:args.max_candidates]:
        if time.monotonic()>=deadline or len(events)>=args.max_operations: break
        attempted+=1
        try: found=search.attempt(i,v,proof,min(deadline,time.monotonic()+args.candidate_seconds))
        except rel.BoundExceeded as exc:
            search.reasons[str(exc)]+=1; continue
        if found is None: continue
        event,patches,measured=found
        delta={}
        for j,row in patches.items():
            delta=rel.plus(delta,rel.times(rows[j],rows[j]),-1)
            delta=rel.plus(delta,rel.times(row,row))
        if any(abs(polynomial.get(mon,0)+c)>=2**80 for mon,c in delta.items()):
            search.reasons['global_coefficient_limit']+=1; continue
        rel.add_to(polynomial,delta); search.apply(patches)
        events.append(event); stats.append(measured)
        print(json.dumps({'accepted':len(events),**measured}),flush=True)
    args.events.parent.mkdir(parents=True,exist_ok=True)
    args.events.write_text(''.join(json.dumps(e,separators=(',',':'))+'\n' for e in events))
    active=sum(bool(ids) for ids in search.incidence.values())
    report=dict(status='UNTRUSTED SEARCH RESULT; full independent replay required',parent=str(args.parent),
        total_candidates=len(candidates),attempted=attempted,operations=len(events),initial_variables=initial_active,
        final_variables=active,variables_removed=initial_active-active,monomials=len(polynomial),
        max_abs_coefficient=str(max(map(abs,polynomial.values()))),seconds=time.monotonic()-start,
        reasons=dict(search.reasons),accepted=stats)
    if args.output:
        assert args.research_dir
        sys.path.insert(0,str(args.research_dir))
        from export_artifact import export
        report['export']=export(args.output,args.parent/'source-residuals.jsonl.gz',rows,records+events,args.allocated,
                                {'localized_relations':len(events)})
        # The named entry remains byte-identical to the parent's frozen entry.
        import shutil
        shutil.copy2(source_entry,args.output/'source-entry.json')
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__': main()
