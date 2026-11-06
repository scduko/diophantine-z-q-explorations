"""Independent exact checker for a quartic projection-preserving certificate.

Only the Python standard library is required. No search/producer code is imported.
This checks algebraic equivalence to the pinned source residual system, not the
arithmetic theorem asserting that the source system defines the integers.
"""
import argparse,gzip,hashlib,itertools,json,math,time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

if not __debug__:raise RuntimeError('Do not disable the checks with python -O.')
SOURCE_SHA='6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2'

def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode('ascii')
def decode(terms):
    result={}
    for coefficient,variables in terms:
        assert type(coefficient) is int and coefficient!=0
        assert all(type(v) is int and v>=0 for v in variables)
        m=tuple(variables);assert m==tuple(sorted(m)) and m not in result
        result[m]=coefficient
    return result
def encode(row):return [[c,list(m)] for m,c in row.items()]
def add(*summands):
    result=defaultdict(Fraction)
    for scalar,poly in summands:
        for m,c in poly.items():result[m]+=scalar*c
    return {m:c for m,c in result.items() if c}
def mul(f,g):
    result=defaultdict(Fraction)
    for m,c in f.items():
        for n,d in g.items():result[tuple(sorted(m+n))]+=c*d
    return {m:c for m,c in result.items() if c}
def normal(row):
    if not row:return ()
    common=math.lcm(*(Fraction(c).denominator for c in row.values()))
    terms={m:int(c*common) for m,c in row.items() if c}
    divisor=math.gcd(*terms.values())
    if terms[min(terms)]<0:divisor=-divisor
    return tuple(sorted((m,c//divisor) for m,c in terms.items()))
def substitute(row,v,replacement):
    result={}
    for m,c in row.items():
        value={():Fraction(c)}
        for variable in m:value=mul(value,replacement if variable==v else {(variable,):1})
        result=add((1,result),(1,value))
    return result
def variables(row):return {v for m in row for v in m}

def expand_definitions(row,definitions):
    result={}
    for monomial,coefficient in row.items():
        term={():Fraction(coefficient)}
        for v in monomial:term=mul(term,definitions.get(v,{(v,):1}))
        result=add((1,result),(1,term))
    return result

def decode_affine(obj):
    denominator=obj['denominator']
    assert type(denominator) is int and denominator>0
    row=decode(obj['terms'])
    assert all(len(mon)<=1 for mon in row)
    return {m:Fraction(c,denominator) for m,c in row.items()}

def unit_scale_expected(rows,d,nextvar):
    """Use the rational nonsquareness proof in UNIT_SCALING.md, not a field axiom."""
    E,theta,proof=d['unit'],d['root'],d['root_row']
    assert all(type(v) is int and 0<v<nextvar for v in (E,theta)) and E!=theta
    assert type(proof) is int and 0<=proof<len(rows)
    assert normal(rows[proof])==normal({(E,):1,(theta,theta):-1,():2})
    pairs=d['weights'];weights={v:k for v,k in pairs}
    assert len(weights)==len(pairs) and weights
    assert all(type(v) is int and 0<v<nextvar and v not in (E,theta)
               and type(k) is int and 1<=k<=8 for v,k in pairs)
    replacements=defaultdict(dict);bridges=[];aliased=set()
    for v,a,consumers in d['aliases']:
        assert type(v) is int and weights.get(v)==1 and v not in aliased
        aliased.add(v)
        assert type(a) is int and a==nextvar;nextvar+=1
        assert consumers and len(consumers)==len(set(consumers))
        for j in consumers:
            assert type(j) is int and 0<=j<len(rows) and j!=proof
            assert v in variables(rows[j])
            replacements[j][v]=a
        bridges.append({(v,):1,tuple(sorted((E,a))):-1})
    expected={}
    for j,row in enumerate(rows):
        if not variables(row)&weights.keys():continue
        laurent=defaultdict(Fraction);aliases=replacements[j]
        for mon,c in row.items():
            exponent=0;other=[]
            for v in mon:
                if v==E:exponent+=1
                elif v in aliases:other.append(aliases[v])
                else:other.append(v);exponent-=weights.get(v,0)
            laurent[(tuple(sorted(other)),exponent)]+=c
        laurent={m:c for m,c in laurent.items() if c}
        least=min((power for (_,power) in laurent),default=0)
        transformed={tuple(sorted(mon+(E,)*(power-least))):c
                     for (mon,power),c in laurent.items()}
        assert all(len(mon)<=2 for mon in transformed),'Unit scaling exceeds quadratic degree'
        expected[j]=transformed
    assert proof not in expected
    for k,row in enumerate(bridges):expected[len(rows)+k]=row
    return expected,nextvar

def redundant_inverse_expected(rows,d,nextvar,incidence):
    """Discard a private inverse using R*H=E^2 and E=theta^2-2 != 0."""
    i,u=d['row'],d['inverse'];nz=d['nonzero']
    assert type(i) is int and 0<=i<len(rows)
    assert type(u) is int and 0<u<nextvar and incidence[u]=={i}
    assert nz['kind']=='root_error'
    j,k=nz['root_row'],nz['relation_row']
    assert all(type(n) is int and 0<=n<len(rows) for n in (j,k))
    assert len({i,j,k})==3
    R,theta,E,H=[decode_affine(obj) for obj in
                 (d['factor'],nz['root'],nz['error'],nz['cofactor'])]
    for form in (R,theta,E,H):
        assert all(v<nextvar and v!=u for v in variables(form))
    assert normal(rows[i])==normal(add((1,mul({(u,):1},R)),(-1,{():1})))
    assert normal(rows[j])==normal(add((1,E),(-1,mul(theta,theta)),(2,{():1})))
    assert normal(rows[k])==normal(add((1,mul(R,H)),(-1,mul(E,E))))
    return {i:{}}

def verify(root,write_report=True):
    start=time.monotonic();source_bytes=(root/'source-residuals.jsonl.gz').read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest()==SOURCE_SHA
    source=[decode(json.loads(line)) for line in gzip.decompress(source_bytes).splitlines()[1:]]
    assert len(source)==15107 and set.union(*(variables(r) for r in source))==set(range(15672))
    counts=defaultdict(int)
    with gzip.open(root/'certificate.jsonl.gz','rt',encoding='ascii') as stream:
        initial=json.loads(next(stream));assert initial['kind']=='initial'
        assert initial['source_sha256']==SOURCE_SHA and initial['source_variables']==15672 and initial['source_rows']==15107
        rows=[decode(r) for r in initial['rows']]
        rules={};anchors=set()
        for rule in initial['reuse']:
            pair=tuple(rule['product']);v=rule['variable'];scale=Fraction(*rule['scale']);index=rule['anchor']
            assert len(pair)==2 and pair==tuple(sorted(pair)) and pair not in rules and v not in pair and scale
            assert 0<=index<len(source) and 0<=v<15672
            assert normal(source[index])==normal({pair:1,(v,):-scale})
            rules[pair]=(v,scale);anchors.add(index)
        def reduce_anchor_terms(row):
            result={}
            for monomial,coefficient in row.items():
                current=list(monomial);coefficient=Fraction(coefficient)
                while True:
                    choices=sorted(set(itertools.combinations(current,2))&rules.keys())
                    if not choices:break
                    pair=choices[0];v,scale=rules[pair]
                    for w in pair:current.remove(w)
                    current.append(v);current.sort();coefficient*=scale
                key=tuple(current);result[key]=result.get(key,0)+coefficient
            return {m:c for m,c in result.items() if c}
        expanded_vars={v:(v,) for v in range(15672)};nextvar=15672
        gates=initial['gates'];assert len(rows)==15107+len(gates)
        for position,gate in enumerate(gates):
            v=gate['variable'];pair=tuple(gate['product'])
            assert v==nextvar and len(pair)==2 and all(w in expanded_vars for w in pair)
            expanded_vars[v]=tuple(sorted(expanded_vars[pair[0]]+expanded_vars[pair[1]]));nextvar+=1
            assert rows[15107+position]=={pair:-1,(v,):1}
        for i,original in enumerate(source):
            expanded=defaultdict(int)
            for monomial,coefficient in rows[i].items():
                assert all(v in expanded_vars for v in monomial)
                key=tuple(sorted(v for w in monomial for v in expanded_vars[w]));expanded[key]+=coefficient
            expanded={m:c for m,c in expanded.items() if c}
            if i in anchors:assert normal(expanded)==normal(original),('anchor',i)
            else:assert normal(reduce_anchor_terms(expanded))==normal(reduce_anchor_terms(original)),('source',i)
        assert all(len(m)<=2 for r in rows for m in r)
        incidence=defaultdict(set)
        for i,r in enumerate(rows):
            for v in variables(r):incidence[v].add(i)
        def fresh(v):
            nonlocal nextvar
            assert type(v) is int and v==nextvar;nextvar+=1
        def patch(data,expected):
            supplied={i:decode(r) for i,r in data}
            assert len(supplied)==len(data) and supplied.keys()==expected.keys()
            for i,r in supplied.items():
                assert normal(r)==normal(expected[i]),('incorrect row',i)
                assert all(len(m)<=2 for m in r) and all(v<nextvar for v in variables(r))
                assert 0<=i<=len(rows)
                if i==len(rows):rows.append({})
                for v in variables(rows[i]):incidence[v].remove(i)
                rows[i]=r
                for v in variables(r):incidence[v].add(i)
        final=None;weights=None;circuit_cache=set()
        for line in stream:
            event=json.loads(line);kind=event['kind']
            if kind=='final':
                assert final is None;final=event
                assert not stream.read().strip(),'Data after final record'
                break
            if kind=='weights':
                assert weights is None
                weights=event['values'];assert len(weights)==len(rows) and all(type(w) is int and w>0 for w in weights)
                continue
            assert weights is None,'Transformations after final weights are not supported'
            assert final is None
            d=event['data'];expected={};counts[kind]+=1
            if kind=='cse':
                v=d['variable'];fresh(v);definition=decode(d['definition']);assert v not in variables(definition)
                for i,factor in d['rows']:
                    assert 0<=i<len(rows) and i not in expected and type(factor) is int
                    expected[i]=add((1,rows[i]),(-factor,definition),(factor,{(v,):1}))
                expected[len(rows)]=add((1,definition),(-1,{(v,):1}))
            elif kind=='split':
                v=d['variable'];fresh(v);i=d['row'];assert 0<=i<len(rows)
                left=decode(d['left']);assert v not in variables(left)
                right=add((1,rows[i]),(-1,left))
                expected={i:add((1,left),(-1,{(v,):1})),len(rows):add((1,right),(1,{(v,):1}))}
            elif kind=='eliminate':
                i=d['row'];v=d['variable'];assert v!=0 and 0<=i<len(rows)
                replacement=decode(d['replacement']);assert v not in variables(replacement)
                denominator=d.get('denominator',1)
                assert type(denominator) is int and denominator>0
                replacement={m:Fraction(c,denominator) for m,c in replacement.items()}
                assert normal(rows[i])==normal(add((1,{(v,):1}),(-1,replacement)))
                affected=d['affected'];assert len(set(affected))==len(affected) and set(affected)==incidence[v]-{i}
                expected={j:substitute(rows[j],v,replacement) for j in affected};expected[i]={}
            elif kind=='linear':
                i,j=d['target'],d['other'];a,b=d['a'],d['b']
                assert 0<=i<len(rows) and 0<=j<len(rows) and i!=j and type(a) is int and a!=0 and type(b) is int
                expected={i:add((a,rows[i]),(b,rows[j]))}
            elif kind=='unit_scale':
                expected,nextvar=unit_scale_expected(rows,d,nextvar)
            elif kind=='redundant_inverse':
                expected=redundant_inverse_expected(rows,d,nextvar,incidence)
            elif kind=='norm_inverse':
                i=d['row'];u=d['inverse'];definitions=d['definitions']
                assert type(i) is int and 0<=i<len(rows)
                assert type(u) is int and 0<u<nextvar
                indices=[pair[0] for pair in definitions];targets=[pair[1] for pair in definitions]
                assert definitions and len(indices)==len(set(indices)) and len(targets)==len(set(targets))
                assert i not in indices and u not in targets
                assert all(type(j) is int and 0<=j<len(rows) for j in indices)
                assert all(type(v) is int and 0<v<nextvar for v in targets)
                target_set=set(targets);expanded={}
                for j,v in definitions:
                    coefficient=rows[j].get((v,),0);assert coefficient
                    rhs=add((Fraction(-1,coefficient),rows[j]),(1,{(v,):1}))
                    assert v not in variables(rhs)
                    assert variables(rhs)&target_set<=expanded.keys(),'Non-acyclic norm-guard definitions'
                    expanded[v]=expand_definitions(rhs,expanded)
                removed={u}|{v for v in targets if u in variables(expanded[v])}
                assert len(d['removed'])==len(set(d['removed'])) and set(d['removed'])==removed
                changed={i}|{j for j,v in definitions if v in removed}
                assert len(changed)>=2
                for v in removed:assert incidence[v]<=changed,'Removed norm coordinate has outside uses'
                for j,v in definitions:
                    if v not in removed:assert not variables(rows[j])&removed
                components=d['components'];assert len(components)==2
                A,B=map(decode,components)
                for component in (A,B):
                    assert all(len(m)<=1 for m in component)
                    assert all(v<nextvar for v in variables(component))
                    assert not variables(component)&(target_set|{u})
                N=add((1,mul(A,A)),(-2,mul(B,B)))
                assert normal(expand_definitions(rows[i],expanded))==normal(add((1,mul({(u,):1},N)),(-1,{():1})))
                new=d['new_variables'];assert len(new)==2
                s,t=new;fresh(s);fresh(t)
                S,T={(s,):1},{(t,):1}
                real=add((1,mul(A,S)),(2,mul(B,T)))
                imag=add((1,mul(A,T)),(1,mul(B,S)))
                # Exact norm multiplicativity supplies the reverse solution map.
                assert mul(N,add((1,mul(S,S)),(-2,mul(T,T))))==add((1,mul(real,real)),(-2,mul(imag,imag)))
                second=min(changed-{i})
                expected={j:{} for j in changed}
                expected[i]=add((1,real),(-1,{():1}));expected[second]=imag
            elif kind=='circuit':
                old_ids=d['old_rows'];old_targets=d['old_targets'];outputs=d['outputs'];new_targets=d['new_targets']
                assert len(old_ids)==len(set(old_ids))==len(old_targets)==len(set(old_targets))
                assert all(type(i) is int and 0<=i<len(rows) for i in old_ids)
                assert all(type(v) is int and 0<v<nextvar for v in old_targets)
                assert outputs and len(outputs)==len(set(outputs)) and set(outputs)<=set(old_targets)
                assert all(type(v) is int for v in outputs+new_targets)
                assert 0<len(new_targets)<=len(old_ids) and len(new_targets)==len(set(new_targets))
                assert set(outputs)<=set(new_targets) and set(new_targets)&set(old_targets)==set(outputs)
                for v in set(old_targets)-set(outputs):
                    assert incidence[v]<=set(old_ids),'Removed circuit variable used outside selected rows'
                for v in new_targets:
                    if v not in outputs:fresh(v)
                supplied={i:decode(r) for i,r in event['patches']}
                assert len(supplied)==len(event['patches']) and set(supplied)==set(old_ids)
                assert all(not supplied[i] for i in old_ids[len(new_targets):])
                old_defs=[rows[i] for i in old_ids]
                new_defs=[supplied[i] for i in old_ids[:len(new_targets)]]
                external=set().union(*(variables(r) for r in old_defs))-set(old_targets)
                assert (set().union(*(variables(r) for r in new_defs))-set(new_targets))<=external
                ext=sorted(external)
                def normalized_circuit(defs,targets):
                    mapping={v:i for i,v in enumerate(ext+targets)}
                    assert len(mapping)==len(ext)+len(targets)
                    seen=set(ext);normalized=[]
                    for target,row in zip(targets,defs):
                        assert row.get((target,),0)!=0
                        assert all(target not in mon for mon in row if mon!=(target,))
                        assert variables(row)-{target}<=seen,'Circuit is cyclic or has a forward reference'
                        assert all(len(mon)<=2 for mon in row)
                        renamed={tuple(sorted(mapping[v] for v in mon)):c for mon,c in row.items()}
                        normalized.append((mapping[target],normal(renamed)))
                        seen.add(target)
                    return normalized,[mapping[v] for v in outputs]
                old_norm,old_outputs=normalized_circuit(old_defs,old_targets)
                new_norm,new_outputs=normalized_circuit(new_defs,new_targets)
                # The cache key is the complete normalized data, not a digest.
                cache_key=canonical([len(ext),old_norm,old_outputs,new_norm,new_outputs])
                if cache_key not in circuit_cache:
                    def evaluate(defs):
                        env={i:{(i,):Fraction(1)} for i in range(len(ext))}
                        for target,terms in defs:
                            row=dict(terms);leading=row[(target,)];value={}
                            for mon,c in terms:
                                if mon==(target,):continue
                                term={():Fraction(-c,leading)}
                                for v in mon:term=mul(term,env[v])
                                value=add((1,value),(1,term))
                            env[target]=value
                        return env
                    old_values=evaluate(old_norm);new_values=evaluate(new_norm)
                    assert all(old_values[a]==new_values[b] for a,b in zip(old_outputs,new_outputs)),'Circuit outputs differ'
                    circuit_cache.add(cache_key)
                expected=supplied
            elif kind in ('translate','shear'):
                v=d['variable'];assert 0<v<nextvar
                affected=d['affected'];assert len(set(affected))==len(affected) and set(affected)==incidence[v]
                if kind=='translate':replacement={(v,):1,():Fraction(*d['shift'])}
                else:
                    w=d['other'];assert 0<=w<nextvar and w!=v
                    replacement={(v,):1,(w,):Fraction(*d['scalar'])}
                expected={i:substitute(rows[i],v,replacement) for i in affected}
            else:raise AssertionError(('unknown operation',kind))
            patch(event['patches'],expected)
        assert final is not None and final['allocated_variables']==nextvar
        if weights is None:weights=[1]*len(rows)
        assert hashlib.sha256(canonical([encode(r) for r in rows])).hexdigest()==final['rows_sha256']
    saved=[decode(r) for r in json.loads(gzip.decompress((root/'candidate-rows.json.gz').read_bytes()))];assert saved==rows
    active=json.loads((root/'variable-map.json').read_bytes())
    assert active[0]==0 and len(active)==len(set(active))
    assert set(active)=={v for v,indices in incidence.items() if indices}
    mapping={v:i for i,v in enumerate(active)}
    compact=[{tuple(sorted(mapping[v] for v in m)):coefficient for m,coefficient in r.items()} for r in rows if r]
    assert compact==[decode(r) for r in json.loads(gzip.decompress((root/'residuals.json.gz').read_bytes()))]
    compact_weights=[w for r,w in zip(rows,weights) if r]
    if (root/'weights.json').exists():assert json.loads((root/'weights.json').read_bytes())==compact_weights
    else:assert all(w==1 for w in compact_weights)
    # All ordered products, independent of the producer's triangular expansion.
    polynomial=defaultdict(int)
    for row,weight in zip(compact,compact_weights):
        for m,coefficient in row.items():
            for n,other in row.items():polynomial[tuple(sorted(m+n))]+=weight*coefficient*other
    polynomial={m:c for m,c in polynomial.items() if c}
    expanded_bytes=(root/'polynomial.expanded.txt').read_bytes()
    assert gzip.decompress((root/'polynomial.expanded.txt.gz').read_bytes())==expanded_bytes
    supplied={}
    for line in expanded_bytes.decode('ascii').splitlines():
        if line.startswith('#'):continue
        coefficient,*m=map(int,line.split());m=tuple(m)
        assert coefficient and m not in supplied and m==tuple(sorted(m));supplied[m]=coefficient
    assert polynomial==supplied
    degree=max(map(len,polynomial));maximum=max(map(abs,polynomial.values()))
    assert degree==4 and set.union(*(set(m) for m in polynomial))==set(range(len(active)))
    assert maximum<2**80,'Expanded coefficient reaches the strict 2^80 bound'
    stats={'witnesses':len(active)-1,'variables':len(active),'rows':len(compact),'monomials':len(polynomial),'degree':degree,'max_abs_coefficient':maximum}
    for key in ('variables','witnesses','rows','monomials','degree','max_abs_coefficient'):assert stats[key]==final['report'][key],key
    report={'status':'PASS','scope':'Exact projection-preserving algebraic equivalence to the pinned source system; exact full integer expansion. The source arithmetic theorem is not checked here.',
            **stats,'source_sha256':SOURCE_SHA,'operations':dict(counts),'total_operations':sum(counts.values()),'weights_greater_than_one':sum(w>1 for w in compact_weights),
            'expanded_bytes':len(expanded_bytes),'compressed_bytes':(root/'polynomial.expanded.txt.gz').stat().st_size,
            'expanded_sha256':hashlib.sha256(expanded_bytes).hexdigest(),
            'certificate_sha256':hashlib.sha256((root/'certificate.jsonl.gz').read_bytes()).hexdigest(),
            'distinct_circuit_identities_checked':len(circuit_cache),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':round(time.monotonic()-start,3)}
    if write_report:(root/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);arguments=parser.parse_args()
    print(json.dumps(verify(arguments.directory),indent=2))
