"""Bind the Version 9 derivations to exact source, convention and dependency records.

This is a document-integrity checker, not a decision procedure for proof validity.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('v7_inventory',ROOT/'docs/quartic-962/inventory.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def fail(ok, message):
    if not ok: raise ValueError(message)

def read(path): return json.loads((ROOT/path).read_bytes())
def digest(raw): return hashlib.sha256(raw).hexdigest()
def pin(path):
    p=ROOT/path
    return {'path':path,'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size}
def encoded(obj): return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()

def build():
    rev=read('docs/quartic-523-540/revision.json')
    texts=[]
    for name in ['baseline','candidate']:
        item=rev[name]; raw=(ROOT/item['path']).read_bytes()
        fail(digest(raw)==item['sha256'],'Changed revision '+name)
        texts.append(raw.decode().replace('\r\n','\n'))
    baseline,current=texts
    expected=baseline
    prior=len(baseline)+1
    for edit in reversed(rev['edits']):
        a,b=edit['start'],edit['end']
        fail(0<=a<=b<prior,'Overlapping revision edits');prior=a
        fail(baseline[a:b]==edit['old'],'Revision old text differs')
        expected=expected[:a]+edit['new']+expected[b:]
    fail(expected==current,'Unrecorded manuscript edit')
    addition=(HERE/'addition.tex').read_text()
    fail(current.count(addition)==1,'Changed or duplicated Version 9 addition')
    tex=old.Tex(current.encode(),rev['candidate']['path'])
    registers=read('docs/quartic-523-540/new-applications.json')
    declared={x['label']:x for x in registers['new_derivations']}
    fail(len(declared)==len(registers['new_derivations']),'Duplicate new derivation')
    missing=[]
    refs=list(old.REF_RE.finditer(tex.code))
    for match in refs:
        for label in match.group(1).split(','):
            if label.strip() not in tex.labels: missing.append(label.strip())
    fail(not missing,'Unresolved references: '+str(missing))
    start=current.index(addition);end=start+len(addition)
    new_results=[r for r in tex.results if start<=r['start']<end]
    for r in new_results:
        fail(any(label in declared for label in r['labels']),'New result omitted from authored register: '+str(r['labels']))
    # Rebind every previously reviewed external application site to unchanged text.
    previous=old.Tex((ROOT/'manuscripts/archive/quartic_v7.tex').read_bytes(),'manuscripts/quartic_v7.tex')
    graph=read('docs/quartic-962/dependency-graph.json')
    inherited=[]
    for item in graph['application_nodes']:
        sites=[]
        for site in item['current_sites']:
            fragment=previous.text[site['start_character']:site['end_character']]
            fail(digest(fragment.encode())==site['text_sha256'],'Old site hash mismatch')
            positions=[m.start() for m in re.finditer(re.escape(fragment),current)]
            fail(len(positions)==1,'Inherited application not uniquely unchanged: '+item['id'])
            sites.append(tex.span(positions[0],positions[0]+len(fragment)))
        inherited.append({'id':item['id'],'sites':sites,'status':'inherited reviewed text unchanged'})
    def span_for(label):
        fail(label in tex.labels,'Dependency label absent: '+label)
        enclosing=tex.enclosing(tex.labels[label])
        if enclosing: return tex.span(enclosing['start'],enclosing['end'])
        if label.startswith(('sec:','subsec:','app:','v9:sec:')):
            return tex.span(*tex.section_span(label))
        return tex.span(*tex.label_span(label))
    # Traverse the authored new dependencies and explicit source references.
    # Citations terminate at recorded literature applications, not at claims of truth.
    todo=list(declared);nodes={}
    while todo:
        label=todo.pop()
        if label in nodes:continue
        span=span_for(label);fragment=tex.code[span['start_character']:span['end_character']]
        deps={x.strip() for m in old.REF_RE.finditer(fragment) for x in m.group(1).split(',')}
        deps.update(declared.get(label,{}).get('dependencies',[]));deps.discard(label)
        cited=sorted({x.strip() for m in old.CITE_RE.finditer(fragment) for x in m.group(3).split(',')})
        nodes[label]={'id':label,'span':span,'dependencies':sorted(deps),'citation_keys':cited,
                      'kind':'new reviewed derivation' if label in declared else 'inherited source site',
                      'check':declared.get(label,{}).get('check')}
        todo.extend(deps-nodes.keys())
    new_apps=[]
    for item in registers['applications']:
        fail(all(item.get(k) for k in ['id','label','source_location','hypotheses','conventions','translation']),'Incomplete new application')
        new_apps.append(dict(item,span=span_for(item['label']),source=registers['source']))
    new_cites=[{'keys':m.group(3),'span':tex.span(m.start(),m.end())} for m in old.CITE_RE.finditer(tex.code,start,end)]
    fail(all(c['keys']=='silverman' for c in new_cites),'Unregistered new literature citation')
    sources=read('docs/theorem-application-audit/sources.json')
    silverman=next(s for s in sources if s['id']=='silverman')
    fail(any(f['sha256']==registers['source']['sha256'] for f in silverman['files']),'Source edition mismatch')
    fail(registers['assumed_new_unpublished_results']==[],'Unexpected new assumed result')
    pins=[pin(x) for x in ['manuscripts/archive/quartic_v7.tex',rev['baseline']['path'],rev['candidate']['path'],
          'docs/quartic-523-540/new-applications.json','docs/quartic-523-540/revision.json','docs/quartic-523-540/addition.tex',
          'docs/quartic-523-540/evidence/AUDIT.md','docs/quartic-523-540/evidence/SOURCE_LINEAGE.json',
          'docs/quartic-523-540/evidence/source-convention-review.json','docs/quartic-523-540/evidence/integrated-CHECKS.json',
          'docs/quartic-962/new-applications.json','docs/quartic-962/dependency-graph.json',
          'docs/quartic-962/coverage.json','docs/theorem-application-audit/sources.json',
          'quartics/quartic-523-540/SHA256SUMS.json']]
    coverage={'status':'PASS_DOCUMENT_AND_DEPENDENCY_BINDING','new_application_families':len(new_apps),
       'inherited_application_and_ledger_nodes':len(inherited),'new_declared_derivations':len(declared),
       'new_result_environments':len(new_results),'reachable_source_nodes':len(nodes),
       'unresolved_references':missing,'new_citations':new_cites,'new_unpublished_theorems_assumed':[],
       'inherited_scope':registers['inherited_scope'],
       'all_final_published_versions_checked':False,'formal_proof':False,
       'claim':'New dependencies resolve to explicit manuscript arguments and unchanged reviewed input sites. This check verifies bindings and coverage, not mathematical truth.'}
    return {'schema':'version9-inventory-1','input_pins':pins,'coverage':coverage,
            'inherited_applications':inherited,'new_applications':new_apps,
            'dependency_nodes':sorted(nodes.values(),key=lambda n:n['id'])}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['build','validate']);args=parser.parse_args()
    result=build();path=HERE/'inventory.json';raw=encoded(result)
    if args.command=='build':path.write_bytes(raw)
    else:fail(path.read_bytes()==raw,'Stale inventory; inspect changes before rebuilding')
    print(json.dumps(result['coverage'],indent=2))

if __name__=='__main__':main()
