"""Use sparse common Hessian-kernel directions to remove more coordinates.

Only existing shear and rational-elimination certificate rules are emitted.
The search itself is untrusted; every accepted result needs the separate checker.
"""
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
import argparse,gzip,json,math,time
import polynomial_ops as p
from merge_coordinates import columns
from optimize import substitute_rational
from export_artifact import enc,export


def kernel_relations(rows,reverse=False):
    cols=columns(rows)
    variables=sorted(set().union(*(p.vars_in(row) for row in rows))-{0})
    frequency=Counter(k for col in cols.values() for k in col)
    order=sorted(variables,key=lambda v:(len(cols.get(v,{})), -v if reverse else v))
    pivots={};independent=set();relations=[];skips=Counter()
    for v in order:
        work=dict(cols.get(v,{}));relation={v:1}
        while work:
            key=min(work,key=lambda k:(frequency[k],k))
            if key not in pivots:
                pivots[key]=(work,relation);independent.add(v)
                break
            other,combination=pivots[key]
            a,b=other[key],-work[key];g=math.gcd(a,b);a//=g;b//=g
            new={k:c*a for k,c in work.items()}
            for k,c in other.items():
                value=new.get(k,0)+b*c
                if value:new[k]=value
                else:new.pop(k,None)
            new_relation={k:c*a for k,c in relation.items()}
            for k,c in combination.items():
                value=new_relation.get(k,0)+b*c
                if value:new_relation[k]=value
                else:new_relation.pop(k,None)
            g=math.gcd(*new.values(),*new_relation.values())
            work={k:c//g for k,c in new.items()}
            relation={k:c//g for k,c in new_relation.items()}
            if len(work)>384 or len(relation)>48 or any(abs(c).bit_length()>1024 for c in (*work.values(),*relation.values())):
                skips['sparse_elimination_cap']+=1
                break
        else:
            assert v in relation and set(relation)-{v}<=independent
            exact={}
            for variable,scalar in relation.items():
                for key,c in cols.get(variable,{}).items():exact[key]=exact.get(key,0)+scalar*c
            assert all(c==0 for c in exact.values())
            relations.append((v,relation))
    return relations,{'columns':len(variables),'independent_columns_found':len(independent),
                      'kernel_directions_found':len(relations),'skipped':dict(skips),
                      'support_sizes':dict(Counter(len(r) for _,r in relations))}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--parent',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--reverse',action='store_true')
    parser.add_argument('--max-terms',type=int,default=96)
    a=parser.parse_args();start=time.monotonic()
    rows=[{tuple(m):c for c,m in row} for row in json.loads(gzip.decompress((a.parent/'candidate-rows.json.gz').read_bytes()))]
    records=[json.loads(line) for line in gzip.decompress((a.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    allocated=records[-1]['allocated_variables'];records=[r for r in records if r['kind'] not in ('weights','final')]
    relations,diagnostic=kernel_relations(rows,a.reverse)
    print(json.dumps(diagnostic),flush=True)
    incidence=defaultdict(set);poly={}
    for i,row in enumerate(rows):
        for v in p.vars_in(row):incidence[v].add(i)
        p.poly_add(poly,p.square(row))
    initial=sum(bool(ids) for ids in incidence.values());accepted=0;reasons=Counter()
    for v,relation in relations:
        if not incidence[v]:reasons['already_absent']+=1;continue
        overlay={};shears=[];bad=False
        for w,c in sorted(relation.items()):
            if w==v:continue
            scalar=Fraction(c,relation[v]);num,den=scalar.numerator,scalar.denominator
            affected=sorted(i for i in incidence[w] if w in p.vars_in(overlay.get(i,rows[i])))
            changed={i:substitute_rational(overlay.get(i,rows[i]),w,{(w,):den,(v,):num},den) for i in affected}
            if any(len(row)>384 or any(abs(c).bit_length()>2048 for c in row.values()) for row in changed.values()):
                bad=True;break
            shears.append({'kind':'shear','data':{'variable':w,'other':v,'scalar':[num,den],'affected':affected},
                           'patches':[[i,enc(row)] for i,row in changed.items()]})
            overlay.update(changed)
        if bad:reasons['intermediate_cap']+=1;continue
        def after(i):return overlay.get(i,rows[i])
        affected=sorted(i for i in incidence[v]|overlay.keys() if v in p.vars_in(after(i)))
        if any(v in mon and len(mon)==2 for i in affected for mon in after(i)):
            reasons['direction_no_longer_null']+=1;continue
        best=None
        for definition in affected if affected else [None]:
            changed=dict(overlay);event=None
            if definition is not None:
                row=after(definition);c=row.get((v,),0)
                if not c:continue
                numerator={m:-d*(1 if c>0 else -1) for m,d in row.items() if m!=(v,)}
                denominator=abs(c);g=math.gcd(denominator,*numerator.values())
                numerator={m:d//g for m,d in numerator.items()};denominator//=g
                others=[i for i in affected if i!=definition]
                for i in others:changed[i]=substitute_rational(after(i),v,numerator,denominator)
                changed[definition]={}
                event={'kind':'eliminate','data':{'row':definition,'variable':v,'replacement':enc(numerator),
                       'denominator':denominator,'affected':others},
                       'patches':[[i,enc(changed[i])] for i in others]+[[definition,[]]]}
            if any(len(row)>a.max_terms or any(len(mon)>2 for mon in row) for row in changed.values()):continue
            delta={}
            for i,row in changed.items():
                p.poly_add(delta,p.square(rows[i]),-1);p.poly_add(delta,p.square(row))
            if any(abs(poly.get(m,0)+c)>=2**80 for m,c in delta.items()):continue
            score=(sum(bool(poly.get(m,0)+c)-(m in poly) for m,c in delta.items()),len(changed))
            if best is None or score<best[0]:best=(score,changed,delta,event)
        if best is None:reasons['final_bound_or_terms']+=1;continue
        _,changed,delta,event=best
        records.extend(shears)
        if event:records.append(event)
        p.poly_add(poly,delta)
        for i,row in changed.items():
            for w in p.vars_in(rows[i]):incidence[w].remove(i)
            rows[i]=row
            for w in p.vars_in(row):incidence[w].add(i)
        assert not incidence[v];accepted+=1
    report=export(a.output,a.parent/'source-residuals.jsonl.gz',rows,records,allocated,
                  {'initial_variables':initial,'kernel_coordinates_removed':accepted,
                   'kernel_diagnostic':diagnostic,'rejections':dict(reasons),'seconds':round(time.monotonic()-start,3)})
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
