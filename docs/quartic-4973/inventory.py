"""Prepare reviewed text, build a final inventory, or validate that inventory.

An externally supplied --acceptance-sha256 is mandatory for final operations.
No final endpoint, manuscript digest, or approval is inferred from a draft.
"""
import argparse
import json
import sys
from pathlib import Path

import inventory_core as c

TOOL_FILES = ('inventory.py','inventory_core.py','tex_subset.py','inputs.json')


def fresh(path):
    path=path.resolve()
    c.require(not path.exists() or (path.is_dir() and not any(path.iterdir())),
              'Output must be a new or empty directory')
    return path


def write_files(out, files):
    out.mkdir(parents=True,exist_ok=True)
    for name,data in sorted(files.items()):
        path=c.inside(out,name);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)


def acceptance(path,wanted,budget):
    c.require(type(wanted) is str and len(wanted)==64,'External acceptance SHA256 is required')
    raw=c.small(path,budget)
    c.require(c.digest(raw)==wanted,'Acceptance is not the externally selected object')
    value=c.parse(raw);c.acceptance_schema(value)
    return value,raw


def template():
    return dict(schema='quartic-v4-final-inventory-acceptance-v1',accepted=False,version=4,
        source_family=c.FAMILY,features=c.tex.FLAGS,main_label='thm:quartic',layout_edits=[],
        package=dict(root=None,source_root=None,auditor_root=None),
        files={k:dict(path=None,sha256=None,bytes=None) for k in sorted(c.REQUIRED_ROLES)},
        expected={k:None for k in sorted(c.EXPECTED_KEYS)},approval_scopes=c.SCOPES,
        finite_rules={})


def prepare(args,budget):
    out=fresh(args.out);content=c.load_context(args.workspace,budget)
    body,spans=c.selected_text(content)
    _,_,_,_,pins=c.graph_context(content)
    for rec in pins:c.check_record(args.workspace,{k:rec[k] for k in ('path','sha256','bytes')},budget)
    result=dict(status='PREPARED REVIEWED TEXT ONLY; NO ENDPOINT ACCEPTANCE',features=c.tex.FLAGS,
        original_draft=c.load_inputs()['draft'],selected_body_sha256=c.digest(body.encode()),
        theorem_proof_spans=spans,selected_proof_artifacts=len(pins),final_acceptance_required=True)
    write_files(out,{'SELECTED_APPENDIX.tex':body.encode(),'PREPARATION.json':c.encoded(result),
        'acceptance.template.json':c.encoded(template())})
    print(json.dumps(result,sort_keys=True))


def readme(a):
    e=a['expected'];name=Path(a['files']['manuscript']['path']).name
    return f'''# Version 4 theorem inventory

This inventory binds the accepted `{name}` to `{e['source_id']}` and the finite
certificate with {e['variables']} total variables, including the input, and
{e['witnesses']} rational witnesses. The reported polynomial has {e['monomials']}
monomials and degree {e['degree']}; its maximum absolute coefficient is
{e['max_abs_coefficient']}.

`theorem-applications.json` records each selected lemma and exact statement/proof
span. `dependency-closure.json` separates arithmetic dependencies, published
applications, and active finite certificate rules. `baseline-bridge.json` keeps
the historical reviewed objects and maps only their unchanged text to the
current manuscript. Historical source conventions are qualified by the explicit
current-consumption records; they are not silently carried forward.

The selected line includes target two, tangent fusion, shared square, first-norm
fusion, and the mixed-mode denominator correction. Optional scalar/J0 fusion is
excluded. Frozen context files may mention other branches as historical records;
their unselected proof artifacts are not copied here.

The new external application is Koenigsmann's quaternion trace criterion in
Definition 4, Observation 5 and the proof of Proposition 6, Facts (a),(b),(c),(e).
The other new steps are author-proved elementary/arithmetic construction lemmas.
All five inherited source-version and proof-status qualifications remain explicit.

Validate from a trusted checkout with the independently recorded acceptance hash:

```
python -E -B inventory.py validate --repo REPOSITORY --docs THIS_DIRECTORY --acceptance-sha256 TRUSTED_HASH
```

This command checks text spans, graph closure, source metadata, all inspected
source/auditor file pins, the compiled payload pins, and receipt correspondence.
It does not rerun the mathematical source audit, certificate replay, or clean
reproduction. Their separate accepted review/receipt objects are mandatory in
`acceptance.json`; the release must also run those checks. An internal hash list
alone is not an external trust anchor. Changes to the selected mathematics,
source family, final counts, or acceptance object require renewed review.
'''.encode()


def build(args,budget):
    out=fresh(args.out);a,raw=acceptance(args.acceptance,args.acceptance_sha256,budget)
    content=c.load_context(args.workspace,budget)
    c.validate_finite(args.repo,a,budget,content)
    manuscript=c.small(c.inside(args.repo,a['files']['manuscript']['path']),budget,2_000_000).decode('utf-8-sig').replace('\r\n','\n')
    documents,body,pins=c.make_documents(content,a,manuscript)
    files={'acceptance.json':raw,'SELECTED_APPENDIX.tex':body.encode(),'README.md':readme(a)}
    files.update({name:c.encoded(value) for name,value in documents.items()})
    for role,data in content.items():files[c.context_name(role,c.load_inputs()[role])]=data
    for rec in pins:
        data=c.small(c.inside(args.workspace,rec['path']),budget)
        c.require((c.digest(data),len(data))==(rec['sha256'],rec['bytes']),'Changed proof '+rec['id'])
        files['evidence/'+rec['id']+Path(rec['path']).suffix]=data
    # The public baseline dependency files remain at their existing repository
    # paths. Their frozen hashes are rechecked instead of duplicating them.
    for rec in c.parse(content['v3_closure'])['evidence']:c.check_record(args.repo,rec,budget)
    for name in TOOL_FILES:files[name]=(c.HERE/name).read_bytes()
    files['DOCUMENTS.json']=c.encoded(dict(schema='quartic-v4-document-file-list-v1',
        acceptance_sha256=args.acceptance_sha256,
        files=[dict(path=name,sha256=c.digest(data),bytes=len(data)) for name,data in sorted(files.items())]))
    write_files(out,files)
    print(json.dumps(dict(status='BUILT: FINAL ACCEPTANCE BOUND',files=len(files),
        acceptance_sha256=args.acceptance_sha256,output=str(out)),sort_keys=True))


def validate(args,budget):
    docs=args.docs.resolve();a,_=acceptance(docs/'acceptance.json',args.acceptance_sha256,budget)
    manifest=c.parse(c.small(docs/'DOCUMENTS.json',budget))
    c.require(manifest['schema']=='quartic-v4-document-file-list-v1' and
              manifest['acceptance_sha256']==args.acceptance_sha256,'Document manifest acceptance')
    names=[r['path'] for r in manifest['files']]
    c.require(len(names)==len(set(names)),'Duplicate document path')
    present={p.relative_to(docs).as_posix() for p in docs.rglob('*') if p.is_file()}
    c.require(present==set(names)|{'DOCUMENTS.json'},'Missing or extra inventory file')
    for rec in manifest['files']:c.check_record(docs,rec,budget)
    content=c.load_context(docs,budget,packaged=True)
    c.validate_finite(args.repo,a,budget,content)
    manuscript=c.small(c.inside(args.repo,a['files']['manuscript']['path']),budget,2_000_000).decode('utf-8-sig').replace('\r\n','\n')
    documents,body,pins=c.make_documents(content,a,manuscript)
    for name,expected in documents.items():
        c.require(c.parse(c.small(docs/name,budget))==expected,'Derived inventory changed '+name)
    c.require(c.small(docs/'SELECTED_APPENDIX.tex',budget)==body.encode(),'Selected appendix changed')
    c.require(c.small(docs/'README.md',budget)==readme(a),'Inventory README changed')
    required=set(TOOL_FILES)|set(documents)|{'acceptance.json','SELECTED_APPENDIX.tex','README.md'}
    required|={c.context_name(role,rec) for role,rec in c.load_inputs().items()}
    for rec in pins:
        name='evidence/'+rec['id']+Path(rec['path']).suffix;required.add(name)
        c.check_record(docs,dict(path=name,sha256=rec['sha256'],bytes=rec['bytes']),budget)
    c.require(set(names)==required,'Document set differs from selected proof closure')
    for rec in c.parse(content['v3_closure'])['evidence']:c.check_record(args.repo,rec,budget)
    print(json.dumps(dict(status='PASS: METADATA, TEXT AND DEPENDENCY BINDING',
        arithmetic_proof_executed=False,certificate_replayed=False,
        source_id=a['expected']['source_id'],acceptance_sha256=args.acceptance_sha256,
        selected_nodes=len(c.SELECTED)),sort_keys=True))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds',type=float,default=45)
    s=p.add_subparsers(dest='command',required=True)
    prep=s.add_parser('prepare');prep.add_argument('--workspace',type=Path,required=True);prep.add_argument('--out',type=Path,required=True)
    b=s.add_parser('build');b.add_argument('--workspace',type=Path,required=True);b.add_argument('--repo',type=Path,required=True)
    b.add_argument('--acceptance',type=Path,required=True);b.add_argument('--acceptance-sha256',required=True);b.add_argument('--out',type=Path,required=True)
    v=s.add_parser('validate');v.add_argument('--repo',type=Path,required=True);v.add_argument('--docs',type=Path,required=True);v.add_argument('--acceptance-sha256',required=True)
    args=p.parse_args();c.require(sys.flags.optimize==0,'Do not run with Python optimization')
    budget=c.Budget(args.seconds)
    {'prepare':prepare,'build':build,'validate':validate}[args.command](args,budget)


if __name__=='__main__':main()
