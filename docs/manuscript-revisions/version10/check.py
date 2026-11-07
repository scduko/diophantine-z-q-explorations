"""Check the exact revision and inventory bindings; not mathematical proof validity."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def load(p):return json.loads((ROOT/p).read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def encode(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def pin(p):return {'path':p,'sha256':sha((ROOT/p).read_bytes())}
def module(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def build():
    rev=load('docs/manuscript-revisions/version10/revision.json')
    need(rev['version']==10 and rev['base_version']==9,'Wrong versions')
    raw=[]
    for key in ['baseline','candidate']:
        p=ROOT/rev[key]['path'];b=p.read_bytes();need(sha(b)==rev[key]['sha256'],'Changed '+key);raw.append(b)
    before,after=[r.decode().replace('\r\n','\n') for r in raw]
    current=before;edits=[]
    for index,e in enumerate(rev['sequential_edits']):
        need(current.count(e['old'])==1,'Ambiguous edit '+str(index))
        p=current.index(e['old']);edits.append((p,len(e['old']),len(e['new']),e['issue_item']))
        current=current.replace(e['old'],e['new'],1)
    need(current==after,'Unrecorded manuscript changes')
    def block(s,a,b):return s[s.index(a):s.index(b,s.index(a))+len(b)]
    need(block(before,r'\begin{abstract}',r'\end{abstract}')==block(after,r'\begin{abstract}',r'\end{abstract}'),'Abstract changed')
    for name in ['coordinate.tex','kato.tex','templates.tex']:
        need(after.count((HERE/name).read_text())==1,'Missing reviewed fragment '+name)
    v9=module('v9_inventory','docs/quartic-523-540/inventory.py')
    previous=v9.build();need((ROOT/'docs/quartic-523-540/inventory.json').read_bytes()==v9.encoded(previous),'Historical inventory stale')
    tex=v9.old.Tex(after.encode(),rev['candidate']['path'])
    refs=[]
    for m in v9.old.REF_RE.finditer(tex.code):
        keys=[s.strip() for s in m.group(1).split(',')]
        need(all(k in tex.labels for k in keys),'Unresolved labels: '+str(keys));refs.append({'labels':keys,'span':tex.span(m.start(),m.end())})
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',after))
    cites=[]
    for m in v9.old.CITE_RE.finditer(tex.code):
        keys=[s.strip() for s in m.group(3).split(',')]
        need(all(k in bib for k in keys),'Unresolved citations '+str(keys));cites.append({'keys':keys,'span':tex.span(m.start(),m.end())})
    def translated(site):
        a,b=site['start_character'],site['end_character'];need(sha(before[a:b].encode())==site['text_sha256'],'Old application span mismatch')
        touched=[]
        for p,old,new,item in edits:
            end=p+old;delta=new-old
            if b<=p:continue
            if a>=end:a+=delta;b+=delta;continue
            touched.append(item)
            if a>p:a=p
            b=b+delta if b>=end else p+new
        return {'previous_span':site,'current_span':tex.span(a,b),'issue_items':sorted(set(touched)),
                'status':'changed; see specified issue review' if touched else 'byte-identical application text'}
    inherited=[]
    for row in previous['inherited_applications']:
        inherited.append({'id':row['id'],'sites':[translated(s) for s in row['sites']]})
    for row in previous['new_applications']:
        inherited.append({'id':row['id'],'sites':[translated(row['span'])]})
    responses=load('docs/manuscript-revisions/version10/responses.json');need([i['number'] for i in responses['items']]==list(range(1,10)),'Nine issue dispositions required')
    applications=load('docs/manuscript-revisions/version10/new-applications.json')
    need(applications['assumed_new_unpublished_results']==[],'New assumed unpublished result')
    for row in responses['items']:
        need(all(x in tex.labels for x in row['labels']),'Missing response target')
    for row in applications['applications']:
        need(all(row.get(k) for k in ['id','source','locator','hypotheses','conventions','translation','labels']),'Incomplete new application')
        need(all(k in tex.labels for k in row['labels']),'Missing application label')
    saved=load('construction/ordinary-integer-definition.json')
    templates=[{'name':t['name'],'parameters':t['parameterCount'],'witnesses':t['witnessCount'],'root':t['root']} for t in saved['library']['templates']]
    need(len(templates)==23,'Template census changed')
    recipes=[{'name':name,'format':r['format'],'witnesses':r['witnessCount']} for name,r in saved['recipes'].items()]
    need(len(recipes)==7,'Recipe census changed')
    need(saved['rootRecipe']=='integers' and saved['parameterNames']==['t'],'External input changed')
    pins=[pin(p) for p in [rev['baseline']['path'],rev['candidate']['path'],'docs/quartic-523-540/inventory.json',
       'docs/manuscript-revisions/version10/revision.json','docs/manuscript-revisions/version10/responses.json',
       'docs/manuscript-revisions/version10/new-applications.json','docs/manuscript-revisions/version10/sources.json',
       'docs/manuscript-revisions/version10/issue2.json','construction/ordinary-integer-definition.json',
       'construction/variable-shift-polynomial-library.js','construction/multiplication-certificate.js',
       'construction/ordinary-integer-polynomial.js','construction/rational-elliptic-core.js',
       'construction/rational-polynomial-library.js','construction/integer-diophantine-compiler.js']]
    changed=[r['id'] for r in inherited if any(s['issue_items'] for s in r['sites'])]
    review=load('docs/manuscript-revisions/version10/site-review.json')
    need(sorted(review['application_reviews'])==sorted(changed),'Changed application review incomplete')
    need(review['revision_sha256']==sha((HERE/'revision.json').read_bytes()),'Stale changed application review')
    pins.append(pin('docs/manuscript-revisions/version10/site-review.json'))
    kato=(HERE/'kato.tex').read_text();kp=after.index(kato)
    new_sites=[{'id':'V10-KATO-1999','span':tex.span(kp,kp+len(kato))},
               {'id':'V10-MAZUR-CONJECTURE2','spans':next(x['sites'] for x in inherited if x['id']=='A047')}]
    return {'schema':'version10-issue2-inventory-1','pins':pins,'inherited_applications':inherited,
       'new_applications':applications,'new_application_sites':new_sites,
       'changed_application_review':review,'citations':cites,'references':refs,'templates':templates,'recipes':recipes,
       'coverage':{'status':'PASS_DOCUMENT_BINDINGS','issue_items':9,'exact_edits':len(edits),'inherited_application_nodes':len(inherited),
          'changed_application_nodes':changed,'new_application_families':len(applications['applications']),
          'citations':len(cites),'references':len(refs),'polynomial_data_changed':False,
          'entire_mathematical_proof_verified':False,'all_final_published_source_versions_compared':False}}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',action='store_true');args=parser.parse_args()
    result=build();raw=encode(result);path=HERE/'inventory.json'
    if args.build:path.write_bytes(raw)
    else:need(path.read_bytes()==raw,'Stale current inventory')
    print(json.dumps(result['coverage'],indent=2))
if __name__=='__main__':main()
