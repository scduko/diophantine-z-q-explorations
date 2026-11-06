"""Refresh Version3 inventory without changing any historical review or source.

Only --out is written. Run on the metadata preparation worker; no polynomial
expansion is performed. Exact reviewed body and arithmetic registry are fixed.
"""
import argparse,copy,difflib,hashlib,json,re,shutil
from pathlib import Path
from release_contract import *

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def save(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def copy_file(src,dest):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if src.resolve()!=dest.resolve():shutil.copyfile(src,dest)
def labels(lines):
    out={}
    for n,line in enumerate(lines,1):
        for label in re.findall(r'\\label\{([^}]+)\}',line):out.setdefault(label,[]).append(n)
    return out
def excerpt(lines,lo,hi):return digest('\n'.join(lines[lo-1:hi]))
def theorem_span(lines,label,index):
    require(len(index.get(label,[]))==1,'Missing/duplicate label '+label)
    at=index[label][0]-1;lo=at
    while lo>=0 and not re.search(r'\\begin\{(?:lemma|theorem|proposition|corollary)\}',lines[lo]):lo-=1
    require(lo>=0,'No theorem start for '+label)
    hi=at
    while hi<len(lines) and '\\end{proof}' not in lines[hi]:hi+=1
    require(hi<len(lines),'No proof end for '+label)
    return dict(label=label,lines=[lo+1,hi+1],excerpt_sha256=excerpt(lines,lo+1,hi+1))
def bridge(repo,current):
    directory=repo/'docs/theorem-application-audit'
    coverage=load(directory/'coverage.json');historical=repo/coverage['manuscript_path']
    require(sha(historical)==coverage['manuscript_sha256'],'Historical manuscript changed')
    old=historical.read_text(encoding='utf-8-sig').splitlines();new=current.read_text(encoding='utf-8-sig').splitlines()
    mapping={}
    for block in difflib.SequenceMatcher(None,old,new,autojunk=False).get_matching_blocks():
        for k in range(block.size):mapping[block.a+k+1]=block.b+k+1
    def locate(lo,hi):
        mapped=[mapping.get(i) for i in range(lo,hi+1)]
        if all(x is not None for x in mapped) and mapped==list(range(mapped[0],mapped[0]+len(mapped))):return [mapped[0],mapped[-1]]
        found=[i+1 for i in range(len(new)-hi+lo) if new[i:i+hi-lo+1]==old[lo-1:hi]]
        require(len(found)==1,'Historical excerpt changed or ambiguous: '+str([lo,hi]))
        return [found[0],found[0]+hi-lo]
    anchors=[]
    for app in load(directory/'applications.json'):
        for j,a in enumerate(app['manuscript_anchors'],1):
            lo,hi=a['line_start'],a['line_end'];require(excerpt(old,lo,hi)==a['excerpt_sha256'],'Historical anchor hash')
            anchors.append(dict(id=f"{app['id']}-S{j:02}",application_id=app['id'],old_lines=[lo,hi],
              current_lines=locate(lo,hi),excerpt_sha256=a['excerpt_sha256'],earlier_review_scope_preserved=True))
    citations=[]
    for c in load(directory/'citations.json'):
        lo,hi=c['paragraph_start'],c['paragraph_end']
        require(excerpt(old,lo,hi)==c['paragraph_sha256'],'Historical citation hash')
        citations.append(dict(id=c['id'],keys=c['keys'],role=c['role'],old_line=c['line'],
          current_paragraph_lines=locate(lo,hi),paragraph_sha256=c['paragraph_sha256']))
    return dict(format='historical-review-current-text-bridge/v2',status='PASS',unresolved=[],
      historical_manuscript=coverage['manuscript_path'],historical_sha256=sha(historical),
      current_manuscript=MANUSCRIPT,current_sha256=sha(current),anchors=anchors,citation_paragraphs=citations,
      scope='Exact unchanged excerpts only. New H19 and selective-source applications have separate current bindings.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('repo','registry','out'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--workspace',type=Path,help='Optional original evidence root; omitted for a public refresh')
    a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve()
    require(sha(a.registry)==REGISTRY_SHA,'Unreviewed arithmetic registry')
    registry=load(a.registry);current=a.repo/MANUSCRIPT;lines=current.read_text(encoding='utf-8-sig').splitlines();index=labels(lines)
    require({x['id'] for x in registry['lemmas']}==set(NEW),'Arithmetic lemma set changed')
    patch=(a.workspace/registry['manuscript_patch']['path']) if a.workspace else a.out/'reviewed-arithmetic-patch.tex'
    require(sha(patch)==PATCH_SHA,'Arithmetic patch changed')
    original_body=patch.read_text(encoding='utf-8-sig').split('% END BODY.',1)[0].rstrip('\n')
    require(original_body.count(LAYOUT_TRANSFORM['old'])==1,'Unexpected reviewed layout target')
    transformed_body=original_body.replace(LAYOUT_TRANSFORM['old'],LAYOUT_TRANSFORM['new'])
    body=transformed_body.splitlines()
    found=[i for i in range(len(lines)-len(body)+1) if lines[i:i+len(body)]==body]
    require(len(found)==1,'Exact reviewed arithmetic body missing/duplicated')
    patch_span=[found[0]+1,found[0]+len(body)]
    basepath=a.repo/'docs/quartic-12504/theorem-applications.json'
    require(sha(basepath)==BASE_INVENTORY_SHA,'Historical Version2 inventory changed')
    base=load(basepath);byid={x['id']:x for x in base['elementary_lemmas']}
    retained=[copy.deepcopy(byid[k]) for k in RETAINED]
    for x in retained:
        x['historical_provenance']=dict(path='docs/quartic-12504/theorem-applications.json',id=x['id'],sha256=BASE_INVENTORY_SHA)
        x.pop('source',None)
        x['current_source_label']='subsec:quartic-source' if x['id']=='quadratic_field_and_rational_inverse' else 'subsec:quartic-reductions'
        require(len(index.get(x['current_source_label'],[]))==1,'Missing reductions label')
        if x['id']=='normalization_and_sum_of_squares':x['statement']='Input-fixing relabeling and nonzero rational row scaling preserve solvability; the sum of the 9161 unit-weight rational squares vanishes exactly when all residuals vanish.'
    nodes=[]
    for lemma in registry['lemmas']:
        item=copy.deepcopy(lemma);item['current_source']=theorem_span(lines,item['label'],index)
        if item['id']=='V3_CIRCUIT':
            item['current_source']['lines'][1]=patch_span[1]
            item['current_source']['excerpt_sha256']=excerpt(lines,*item['current_source']['lines'])
        nodes.append(item)
    public=[]
    height=theorem_span(lines,'thm:quartic-height19',index)['lines']
    for app in registry['additional_explicit_published_applications']:
        item=copy.deepcopy(app);keys=PUBLICATION_KEYS[item['id']];sites=[]
        for n in range(height[0],height[1]+1):
            if any(key in lines[n-1] for key in keys):
                lo=hi=n
                while lo>height[0] and lines[lo-2].strip():lo-=1
                while hi<height[1] and lines[hi].strip():hi+=1
                site=dict(lines=[lo,hi],excerpt_sha256=excerpt(lines,lo,hi))
                if site not in sites:sites.append(site)
        require(sites,'No current published application site: '+item['id'])
        item['current_sites']=sites;item['citation_keys']=keys;public.append(item)
    edges=[dict(source='thm:quartic',target='V3_SOURCE',kind='arithmetic'),dict(source='thm:quartic',target='certificate_binding',kind='finite')]
    edges += [dict(source='thm:quartic',target=k,kind='local') for k in RETAINED+['V3_CIRCUIT']]
    edges += [dict(source=x['id'],target=d,kind='dependency') for x in nodes for d in x['depends_on']]
    edges += [dict(source=x['id'],target=d,kind='local') for x in retained for d in x.get('elementary_dependencies',[])]
    inventory=dict(format='quartic-9625-theorem-inventory/v1',manuscript=MANUSCRIPT,manuscript_sha256=sha(current),
      arithmetic_registry_sha256=REGISTRY_SHA,reviewed_patch_sha256=PATCH_SHA,reviewed_body=dict(lines=patch_span,excerpt_sha256=excerpt(lines,*patch_span)),
      source_id=SOURCE_ID,certificate_binding=EXPECTED,retained_algebraic_lemmas=retained,
      arithmetic_lemmas=nodes,inherited_applications=registry['inherited_applications'],
      additional_published_applications=public,source_version_requirements=registry['source_version_requirements'],
      scope='Current Version3 source and finite artifact. Historical reviews retain original objects, versions and qualifications.')
    closure=dict(format='quartic-9625-dependency-closure/v1',root='thm:quartic',edges=edges,
      evidence=load(a.repo/'docs/quartic-12504/dependency-closure.json')['source_application_documents'])
    a.out.mkdir(parents=True,exist_ok=True)
    for artifact in registry['artifacts']:
        src=(a.workspace/artifact['path']) if a.workspace else a.repo/artifact['publication_path']
        require(sha(src)==artifact['sha256'],'Changed proof artifact '+artifact['id'])
        relative=Path(artifact['publication_path']).relative_to(DOCS);dest=a.out/relative
        copy_file(src,dest)
    copy_file(a.registry,a.out/'publication-additions.json');copy_file(patch,a.out/'reviewed-arithmetic-patch.tex')
    for name in ('validate.py','release_contract.py','build_inventory.py','test_inventory.py'):copy_file(Path(__file__).with_name(name),a.out/name)
    save(a.out/'theorem-applications.json',inventory);save(a.out/'dependency-closure.json',closure)
    save(a.out/'layout-transform.json',dict(original_patch_sha256=PATCH_SHA,
      original_body_sha256=digest(original_body),current_body_sha256=digest(transformed_body),
      transformations=[LAYOUT_TRANSFORM],scope='Explicit reviewed layout edit only; original proof/review hashes are preserved.'))
    save(a.out/'baseline-bridge.json',bridge(a.repo,current))
    save(a.out/'inventory-spec.json',dict(format='quartic-9625-inventory-spec/v1',source_id=SOURCE_ID,expected_final=EXPECTED,
      arithmetic_registry_sha256=REGISTRY_SHA,required_arithmetic_lemmas=NEW,retained_algebraic_lemmas=RETAINED))
    print(json.dumps(dict(status='BUILT; independent validation required',manuscript_sha256=sha(current),out=str(a.out))))
if __name__=='__main__':main()
