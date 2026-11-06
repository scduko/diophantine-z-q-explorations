"""Independent exact audit of selective beta-only source; no arithmetic approval."""
import argparse,ast,copy,hashlib,importlib.util,json,time
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
CORE_SHA='0da0dfef661211fd4ada262050895ef24ca54dfdc1aca4aa4bec4e69c1dcbce8'
POSITIONS=list(range(5,13));SELECTION=[0,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30]
ORDERS=[1]*11+[12]*6
MODULES=('Z_definition','q_anchor','q_height_batch','q_primeparity','q_compare4','q_batch41','q_compare_beta','q_batch17')
def core():
    path=HERE/'core_audit.py';assert hashlib.sha256(path.read_bytes()).hexdigest()==CORE_SHA
    spec=importlib.util.spec_from_file_location('selective_core_auditor',path);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);return c
def baseline(c,path):
    pins=c.load(HERE/'BASELINE.json')
    for name,digest in pins['files'].items():assert c.file_sha256(path/name)==digest,('baseline pin',name)
    return pins,{name:c.load(path/'modules'/(name+'.json')) for name in pins['modules']}
def check_beta(c,obj):
    m=c.Module(obj);expected=defaultdict(list)
    assert obj['name']=='q_compare_beta' and m.free==16
    assert obj['precision']==obj['label_precision']==12 and obj['modeled_points']==1
    assert obj['compressed_primary_charts'] is True and obj['logarithm_coordinate']=='reciprocal f=1/x'
    assert obj['high_log_profile']==obj['beta_log_profile']==c.BETA_PROFILE
    assert obj['input_layout']=='beta;4P;4A;conj_fJ;inv_conj_zJ;root;root_error;r'
    assert obj['field_inequality_orders']==[1]*5+[12]*3
    def feq(tag,pair):
        for j,p in enumerate(pair):assert p;expected[tag+'.'+str(j)].append(p)
    points=[]
    for name in ('H','X0'):
        u,v,f,x,p=[m.pair(name+'.'+s) for s in ('u','v','f','x','p')]
        feq(name+'.f=u2',c.fs(f,c.fm(u,u)))
        feq(name+'.v2+df=1',c.fs(c.fa(c.fm(v,v),c.fm(c.SMALL_D,f)),c.ONE))
        feq(name+'.p2=x-Df',c.fs(c.fm(p,p),c.fs(x,c.fm(c.D,f))))
        feq(name+'.xf=1',c.fs(c.fm(x,f),c.ONE))
        points.append(dict(x=x,y=c.fm(x,p),f=f,p=p))
    differences=[]
    for j,point in enumerate(points):
        at=1+4*j;tx=(c.v(at),c.v(at+1));ty=(c.v(at+2),c.v(at+3))
        lam,nu,x,y,f,z=[m.pair('difference.'+s,j,2) for s in ('lambda','nu','x','y','f','z')]
        feq('difference line at first point',c.fs(c.fs(c.fm(lam,point['x']),point['y']),nu))
        feq('difference line at negated second point',c.fs(c.fa(c.fm(lam,tx),ty),nu))
        feq('difference abscissa',c.fa(c.fs(x,c.fm(lam,lam)),c.fa(point['x'],tx)))
        feq('difference line at output',c.fs(c.fa(c.fm(lam,x),y),nu))
        feq('difference reciprocal abscissa',c.fs(c.fm(f,x),c.ONE))
        feq('difference formal parameter',c.fa(c.fm(z,y),x))
        guard=m.scalar('distinct abscissae guard',j,2);delta=c.fs(point['x'],tx)
        norm=c.add((1,c.mul(delta[0],delta[0])),(-2,c.mul(delta[1],delta[1])))
        expected['distinct abscissae guard'].append(c.add((1,c.mul(guard,norm)),(-1,c.const(1))))
        differences.append(dict(f=f,z=z))
    lam=m.pair('common negative logarithm');gs=[c.expected_g(p['f'],12) for p in points]
    feq('H pH=GH',c.fs(c.fm(lam,points[0]['p']),gs[0]))
    ratio=m.pair('retained logarithm ratio');aux=m.pair('ratio times p')
    feq('A=C p',c.fs(aux,c.fm(ratio,points[1]['p'])))
    feq('A H=G',c.fs(c.fm(aux,lam),gs[1]))
    formal=[p['f'] for p in points]+[(c.v(9),c.v(10))]+[c.conj(p['f']) for p in differences]
    primary=[c.fs(ratio,(c.v(0),{}))]
    alternate=[c.fm(c.conj(p['z']),(c.v(11),c.v(12))) for p in differences]
    tests=[c.v(14)]
    for real,imag in formal+primary+alternate:
        tests.extend([c.mul(c.v(14),imag),c.add((1,real),(1,c.mul(c.v(13),imag)))])
    assert len(tests)==17 and set(m.equations)-{'arithmetic'}==set(expected)
    for tag,ps in expected.items():
        ids=m.equations[tag];assert len(ids)==len(ps)
        for i,p in zip(ids,ps):assert c.normal(c.subst(m.rows[i],m.env))==c.normal(p),('beta equation',tag,i)
    assert len(obj['calls'])==1
    call=obj['calls'][0];assert call['module']=='q_batch17' and len(call['args'])==18
    for i,(v,p) in enumerate(zip(call['args'],[c.v(15)]+tests)):assert m.env[v]==p,('beta ordered argument',i)
    assert m.core|set(m.definitions)==set(range(m.free,m.total)) and not m.core&set(m.definitions)
    used=set().union(*(c.variables(r) for r in m.rows));assert set(range(m.free,m.total))<=used
    return dict(free=16,locals=obj['locals'],primary_points=2,differences=2,ordered_tests=17)
def check_root(obj,old):
    expected=copy.deepcopy(old);position=0
    for call in expected['calls']:
        if call['module']!='q_compare4':continue
        if position in POSITIONS:
            call['module']='q_compare_beta';call['args']=[call['args'][i] for i in SELECTION]
        position+=1
    assert position==37
    expected['beta_only_positions']=POSITIONS
    expected['full_comparison_positions']=[i for i in range(37) if i not in POSITIONS]
    assert obj==expected,'Root changed outside exact selected calls/metadata'
def flatten(c,source,modules):
    # Reuse the exact hash-pinned independent generic flattening code. Only
    # its final expected module-instance counts change for this new source.
    code=(HERE/'core_audit.py').read_text(encoding='utf-8');tree=ast.parse(code)
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='flatten_and_check')
    body=ast.get_source_segment(code,node)
    old="assert visits_by_module == {'Z_definition':1, 'q_anchor':1, 'q_height_batch':1,\n                               'q_compare4':37, 'q_batch41':37, 'q_primeparity':38}"
    new="assert visits_by_module == {'Z_definition':1, 'q_anchor':1, 'q_height_batch':1, 'q_compare4':29, 'q_batch41':29, 'q_compare_beta':8, 'q_batch17':8, 'q_primeparity':38}"
    assert body.count(old)==1
    ns=dict(c.__dict__);exec(compile(body.replace(old,new),'<selective-independent-flatten>','exec'),ns)
    return ns['flatten_and_check'](source,modules,40)
def check(c,source,base):
    pins,old=baseline(c,base);contract=c.load(source/'BETA_SOURCE.json')
    expected=dict(source_family='H19-root37-selective-beta12-high40-v1',arithmetic_acceptance=False,source_pin_authorized=False,
      high=40,label=12,anchor_squarings=25,scalar_orders=[1,1,1,1,32,32],height_exponent=19,
      beta_only_positions=POSITIONS,full_positions=[i for i in range(37) if i not in POSITIONS],
      beta_input_selection=SELECTION,beta_rational_orders=ORDERS,
      baseline_source_id=pins['source_id'],baseline_source_sha256=pins['source_sha256'],baseline_module_sha256=pins['modules'],
      scope='New arithmetic source requiring selective-contact proof; no old-source projection equivalence asserted')
    assert set(contract)==set(expected)|{'compiler_sha256'}
    for k,v in expected.items():assert type(contract[k]) is type(v) and contract[k]==v,('contract',k)
    compilers=contract['compiler_sha256'];assert set(compilers)=={'archive_build.py','combined_kernel.py','lowprecision_kernel.py','build_source.py','beta_kernel.py'}
    for name,digest in compilers.items():
        assert c.file_sha256(source/'compiler'/name)==digest
        if 'compiler/'+name in pins['files']:assert digest==pins['files']['compiler/'+name]
    assert {p.stem for p in (source/'modules').glob('*.json')}==set(MODULES)
    modules={name:c.load(source/'modules'/(name+'.json')) for name in MODULES}
    for name in old:
        if name!='Z_definition':assert modules[name]==old[name],('unchanged module',name)
    check_root(modules['Z_definition'],old['Z_definition']);beta=check_beta(c,modules['q_compare_beta'])
    batch=copy.deepcopy(modules['q_batch17']);assert batch['name']=='q_batch17';batch['name']='q_batch41';c.check_batch(batch,ORDERS)
    counts,visits=flatten(c,source,modules)
    residual='residuals.jsonl' if (source/'residuals.jsonl').exists() else 'residuals.jsonl.gz'
    names=['BETA_SOURCE.json','counts.json','polynomial.json','shared.json',residual]
    if residual=='residuals.jsonl' and (source/'residuals.jsonl.gz').exists():names.append('residuals.jsonl.gz')
    names+=['modules/'+n+'.json' for n in MODULES]+['compiler/'+n for n in compilers]
    hashes={n:c.file_sha256(source/n) for n in sorted(names)}
    return dict(status='PASS: SOURCE CONSTRUCTION ONLY',source_pin_authorized=False,arithmetic_acceptance=False,
      high=40,label=12,compressed=True,counts=counts,beta=beta,inspected_files_sha256=hashes,source_residual_file=residual,
      construction_map_sha256=hashlib.sha256(c.construction_map_bytes(visits)).hexdigest(),
      checker_dependencies_sha256={'core_audit.py':CORE_SHA,'BASELINE.json':c.file_sha256(HERE/'BASELINE.json')},
      not_established=['selective-contact arithmetic theorem','source defines the integers','final quartic bound']),visits
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','baseline','report','map'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=int,default=180);a=p.parse_args();assert 1<=a.seconds<=600
    c=core();c.DEADLINE=time.monotonic()+a.seconds;report,visits=check(c,a.source,a.baseline)
    report['checker_sha256']=c.file_sha256(Path(__file__));a.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8');a.map.write_bytes(c.construction_map_bytes(visits));print(json.dumps(report))
if __name__=='__main__':main()
