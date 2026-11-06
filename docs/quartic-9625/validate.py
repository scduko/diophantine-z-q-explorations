"""Fail-closed Version3 inventory, text-bridge and artifact binding validator.

This checks finite bindings and dependency closure, not mathematical truth
or a fresh replay of the arithmetic source/certificate. Run those separately.
"""
import argparse,gzip,hashlib,json,re
from pathlib import Path
from release_contract import *

def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(b):return hashlib.sha256(b).hexdigest()
def path(root,rel):
    require(isinstance(rel,str) and not Path(rel).is_absolute(),'Absolute/nonstring path')
    result=(root/rel).resolve();require(result.is_relative_to(root.resolve()),'Path escapes root: '+rel);return result
def checked_span(lines,anchor):
    value=anchor['lines']
    require(isinstance(value,list) and len(value)==2 and all(type(x)is int for x in value),'Malformed span')
    lo,hi=value;require(1<=lo<=hi<=len(lines),'Span outside manuscript')
    text='\n'.join(lines[lo-1:hi]);require(digest(text.encode())==anchor['excerpt_sha256'],'Excerpt changed')
    return text
def unique(items):
    result={x['id']:x for x in items};require(len(result)==len(items),'Duplicate node ID');return result
def all_ids(obj):
    if isinstance(obj,dict):return ({obj['id']} if isinstance(obj.get('id'),str) else set())|set().union(*(all_ids(v) for v in obj.values()),set())
    if isinstance(obj,list):return set().union(*(all_ids(x) for x in obj),set())
    return set()

def validate(repo,docs=None):
    repo=repo.resolve();docs=(docs or repo/DOCS).resolve();pkg=repo/PACKAGE
    registry_file=docs/'publication-additions.json';require(sha(registry_file)==REGISTRY_SHA,'Unreviewed registry')
    registry=load(registry_file);inv=load(docs/'theorem-applications.json');closure=load(docs/'dependency-closure.json')
    spec=load(docs/'inventory-spec.json')
    require(spec==dict(format='quartic-9625-inventory-spec/v1',source_id=SOURCE_ID,expected_final=EXPECTED,
      arithmetic_registry_sha256=REGISTRY_SHA,required_arithmetic_lemmas=NEW,retained_algebraic_lemmas=RETAINED),'Inventory specification changed')
    require(inv['source_id']==SOURCE_ID and inv['certificate_binding']==EXPECTED,'Wrong finite target')
    require(inv['arithmetic_registry_sha256']==REGISTRY_SHA and inv['reviewed_patch_sha256']==PATCH_SHA,'Inventory proof pins')
    require(inv['manuscript']==MANUSCRIPT,'Wrong current manuscript')
    current=repo/MANUSCRIPT;lines=current.read_text(encoding='utf-8-sig').splitlines()
    require(sha(current)==inv['manuscript_sha256'],'Current manuscript changed; refresh required')
    labels={}
    for n,line in enumerate(lines,1):
        for label in re.findall(r'\\label\{([^}]+)\}',line):labels.setdefault(label,[]).append(n)
    for label in ['thm:quartic','subsec:quartic-source','subsec:quartic-reductions']+[x['label'] for x in registry['lemmas']]:
        require(len(labels.get(label,[]))==1,'Missing/duplicate current label '+label)
    main_start=labels['thm:quartic'][0]-1;main_end=next(i for i in range(main_start,len(lines)) if '\\end{theorem}' in lines[i])
    main='\n'.join(lines[main_start:main_end+1]).replace('\\,','')
    for value in (9625,9624,82476,EXPECTED['max_abs_coefficient']):require(str(value) in main,'Wrong main theorem count/bound')
    require('degree $4$' in main,'Wrong main theorem degree')
    patch=docs/'reviewed-arithmetic-patch.tex';require(sha(patch)==PATCH_SHA,'Changed reviewed patch')
    original_body=patch.read_text(encoding='utf-8-sig').split('% END BODY.',1)[0].rstrip('\n')
    require(original_body.count(LAYOUT_TRANSFORM['old'])==1,'Unexpected reviewed layout target')
    body=original_body.replace(LAYOUT_TRANSFORM['old'],LAYOUT_TRANSFORM['new'])
    layout=load(docs/'layout-transform.json')
    require(layout==dict(original_patch_sha256=PATCH_SHA,original_body_sha256=digest(original_body.encode()),
      current_body_sha256=digest(body.encode()),transformations=[LAYOUT_TRANSFORM],
      scope='Explicit reviewed layout edit only; original proof/review hashes are preserved.'),'Unapproved proof layout transformation')
    require(checked_span(lines,inv['reviewed_body'])==body,'Reviewed arithmetic body changed')
    require(inv['source_version_requirements']==registry['source_version_requirements'],'Lost source-version qualification')
    selected=registry['selected_source']
    require(selected['source_id']==SOURCE_ID and selected['residuals_sha256']==SOURCE_RAW_SHA,'Registry source target')
    require(selected['full_positions']==list(range(5))+list(range(13,37)) and selected['beta_only_positions']==list(range(5,13)),'Wrong selected positions')
    require((selected['height_exponent'],selected['high'],selected['beta'],selected['anchor_squarings'])==(19,40,12,25),'Wrong arithmetic parameters')
    require(selected['scalar_orders']==[1,1,1,1,32,32],'Wrong scalar orders')
    artifacts=unique(registry['artifacts'])
    for item in artifacts.values():
        relative=Path(item['publication_path']).relative_to(DOCS).as_posix();file=path(docs,relative)
        require(file.stat().st_size==item['bytes'] and sha(file)==item['sha256'],'Changed proof/evidence '+item['id'])
    arithmetic=unique(inv['arithmetic_lemmas']);expected_arithmetic=unique(registry['lemmas'])
    require(set(arithmetic)==set(NEW)==set(expected_arithmetic),'Dropped/added arithmetic lemma')
    for key,item in arithmetic.items():
        data=dict(item);anchor=data.pop('current_source')
        require(data==expected_arithmetic[key],'Changed arithmetic statement/dependencies '+key)
        text=checked_span(lines,anchor)
        require(anchor['label']==item['label'] and '\\label{'+item['label']+'}' in text,'Wrong lemma text binding')
        for proof in item['proofs']:require(proof['artifact'] in artifacts,'Dangling proof artifact')
    inherited=unique(inv['inherited_applications']);require(inherited==unique(registry['inherited_applications']),'Changed inherited applications')
    for item in inherited.values():
        require(item['inventory'] in artifacts,'Missing inherited inventory')
        for other in item.get('also',[]):require(other in artifacts,'Missing companion inventory')
        artifact=artifacts[item['inventory']]
        if item.get('application_ids'):
            doc=load(path(docs,Path(artifact['publication_path']).relative_to(DOCS).as_posix()))
            require(set(item['application_ids'])<=all_ids(doc),'Unknown inherited application ID')
    publications=unique(inv['additional_published_applications']);expected_pubs=unique(registry['additional_explicit_published_applications'])
    require(set(publications)==set(PUBLICATION_KEYS)==set(expected_pubs),'Dropped published application')
    for key,item in publications.items():
        data=dict(item);sites=data.pop('current_sites');keys=data.pop('citation_keys')
        require(data==expected_pubs[key] and keys==PUBLICATION_KEYS[key] and sites,'Changed published application')
        texts=[checked_span(lines,site) for site in sites]
        require(any(any(k in text for k in keys) for text in texts),'No supporting current citation')
        for k in keys:require(sum('\\bibitem{'+k+'}' in line for line in lines)==1,'Missing/duplicate bibliography '+k)
    base=repo/'docs/quartic-12504/theorem-applications.json';require(sha(base)==BASE_INVENTORY_SHA,'Changed historical inventory')
    base_items=unique(load(base)['elementary_lemmas']);retained=unique(inv['retained_algebraic_lemmas'])
    require(set(retained)==set(RETAINED),'Dropped retained algebraic rule')
    for key,item in retained.items():
        expected=dict(base_items[key]);expected.pop('source',None)
        if key=='normalization_and_sum_of_squares':expected['statement']='Input-fixing relabeling and nonzero rational row scaling preserve solvability; the sum of the 9161 unit-weight rational squares vanishes exactly when all residuals vanish.'
        actual=dict(item);provenance=actual.pop('historical_provenance');label=actual.pop('current_source_label')
        require(actual==expected,'Changed inherited algebraic lemma '+key)
        require(provenance==dict(path='docs/quartic-12504/theorem-applications.json',id=key,sha256=BASE_INVENTORY_SHA),'Retargeted historical review')
        require(label==('subsec:quartic-source' if key=='quadratic_field_and_rational_inverse' else 'subsec:quartic-reductions'),'Wrong algebraic anchor')
    expected_edges={('thm:quartic','V3_SOURCE','arithmetic'),('thm:quartic','certificate_binding','finite')}
    expected_edges|={('thm:quartic',k,'local') for k in RETAINED+['V3_CIRCUIT']}
    expected_edges|={(x['id'],d,'dependency') for x in arithmetic.values() for d in x['depends_on']}
    expected_edges|={(x['id'],d,'local') for x in retained.values() for d in x.get('elementary_dependencies',[])}
    edges={(x['source'],x['target'],x['kind']) for x in closure['edges']}
    require(edges==expected_edges and len(edges)==len(closure['edges']),'Dependency edge set changed')
    known=set(arithmetic)|set(inherited)|set(publications)|set(retained)|{'thm:quartic','certificate_binding'}
    require(all(a in known and b in known for a,b,_ in edges),'Dangling dependency')
    reached={'thm:quartic'}
    while True:
        new=reached|{b for a,b,_ in edges if a in reached}
        if new==reached:break
        reached=new
    require(reached==known,'Unreachable proof/application nodes')
    old_closure=load(repo/'docs/quartic-12504/dependency-closure.json')
    require(closure['evidence']==old_closure['source_application_documents'],'Inherited ledger closure dropped')
    for item in closure['evidence']:require(sha(path(repo,item['path']))==item['sha256'],'Inherited source ledger changed')
    validate_bridge(repo,docs,lines,sha(current))
    validate_finite(pkg)
    return dict(status='PASS',scope=__doc__.strip(),manuscript_sha256=sha(current),source_id=SOURCE_ID,
      arithmetic_lemmas=len(arithmetic),inherited_applications=len(inherited),published_applications=len(publications),
      retained_rules=len(retained),proof_artifacts=len(artifacts),dependency_edges=len(edges))

def validate_bridge(repo,docs,lines,current_sha):
    b=load(docs/'baseline-bridge.json');directory=repo/'docs/theorem-application-audit';coverage=load(directory/'coverage.json')
    require(b['status']=='PASS' and not b['unresolved'] and b['current_sha256']==current_sha,'Invalid bridge status/current source')
    require(b['historical_manuscript']==coverage['manuscript_path'],'Retargeted historical manuscript')
    oldfile=path(repo,b['historical_manuscript']);require(sha(oldfile)==b['historical_sha256']==coverage['manuscript_sha256'],'Historical source changed')
    old=oldfile.read_text(encoding='utf-8-sig').splitlines()
    anchors={f"{a['id']}-S{j:02}":x for a in load(directory/'applications.json') for j,x in enumerate(a['manuscript_anchors'],1)}
    actual=unique(b['anchors']);require(set(actual)==set(anchors),'Historical anchor coverage')
    for key,item in actual.items():
        anchor=anchors[key];lo,hi=anchor['line_start'],anchor['line_end'];nlo,nhi=item['current_lines']
        require(item['old_lines']==[lo,hi] and item['earlier_review_scope_preserved'] is True,'Historical anchor retargeted')
        require(lines[nlo-1:nhi]==old[lo-1:hi],'Historical application text changed')
        require(digest('\n'.join(old[lo-1:hi]).encode())==item['excerpt_sha256']==anchor['excerpt_sha256'],'Historical excerpt hash')
    cites=unique(load(directory/'citations.json'));actual=unique(b['citation_paragraphs'])
    require(set(actual)==set(cites),'Historical citation coverage')
    for key,item in actual.items():
        c=cites[key];lo,hi=item['current_paragraph_lines'];text=old[c['paragraph_start']-1:c['paragraph_end']]
        require(item['keys']==c['keys'] and item['role']==c['role'] and item['old_line']==c['line'],'Historical citation provenance')
        require(lines[lo-1:hi]==text and digest('\n'.join(text).encode())==item['paragraph_sha256']==c['paragraph_sha256'],'Historical citation changed')

def validate_finite(pkg):
    require(sha(pkg/'source-entry.json')==ENTRY_SHA,'Changed source entry')
    entry=load(pkg/'source-entry.json');require(entry['source_id']==SOURCE_ID and entry['source_variables']==9318 and entry['source_rows']==8854,'Wrong source')
    require(entry['high']==40 and entry['label']==12 and entry['compressed'] is True,'Wrong source precision')
    for name,pin in [('source-audit.json',AUDIT_SHA),('construction-map.json',MAP_SHA),('reproducibility/pipeline/check_source.py',AUDITOR_SHA),('source-residuals.jsonl.gz',SOURCE_SHA),
                     ('certificate.jsonl.gz',EXPECTED['certificate_sha256']),('verify_certificate.py',EXPECTED['checker_sha256']),('polynomial.expanded.txt',EXPECTED['expanded_sha256'])]:
        require(sha(pkg/name)==pin,'Changed finite input '+name)
    require(sha(pkg/'source-layout.json')==entry['source_layout_sha256'],'Changed source layout')
    audit=load(pkg/'source-audit.json')
    for name,pin in audit['checker_dependencies_sha256'].items():
        require(sha(path(pkg/'reproducibility/pipeline',name))==pin,'Changed source auditor dependency '+name)
    require(digest(gzip.decompress((pkg/'source-residuals.jsonl.gz').read_bytes()))==SOURCE_RAW_SHA,'Raw source differs')
    require(digest(gzip.decompress((pkg/'polynomial.expanded.txt.gz').read_bytes()))==EXPECTED['expanded_sha256'],'Expanded gzip differs')
    for rel,pin in entry['inspected_files_sha256'].items():
        file=path(pkg/'source',rel)
        if file.is_file():actual=sha(file)
        elif rel=='residuals.jsonl' and Path(str(file)+'.gz').is_file():actual=digest(gzip.decompress(Path(str(file)+'.gz').read_bytes()))
        else:raise ValueError('Missing inspected source '+rel)
        require(actual==pin,'Changed inspected source '+rel)
    receipt=load(pkg/'evidence/stages/coordinates.json')
    require(receipt['status']=='PASS' and receipt['source_id']==SOURCE_ID,'Invalid original replay receipt')
    for key,value in EXPECTED.items():require(receipt[key]==value,'Finite receipt mismatch '+key)
    require(load(pkg/'weights.json')==[1]*9161,'Changed square weights')
    vm=load(pkg/'variable-map.json');require(len(vm)==len(set(vm))==9625 and vm[0]==0,'Invalid input/variable map')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--docs',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args();result=validate(a.repo,a.docs)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
if __name__=='__main__':main()
