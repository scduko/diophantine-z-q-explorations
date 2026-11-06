"""Build the version-bound theorem application audit without changing the paper."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, sys
from collections import Counter
from source_map import SOURCE_PATHS, NOTES, EVIDENCE
AUTHOR=Path(__file__).resolve().parent
APPS=json.loads((AUTHOR/'FROZEN_APPLICATIONS.json').read_text(encoding='utf-8'))
ROLES=json.loads((AUTHOR/'CITATION_ROLES.json').read_text(encoding='utf-8'))
ADDITIONS=json.loads((AUTHOR/'SOURCE_ADDITIONS.json').read_text(encoding='utf-8'))
FILE_METADATA={}
for row in ADDITIONS:
 key=row['id']
 old=[] if row.get('replace_files') else SOURCE_PATHS.get(key,[])
 SOURCE_PATHS[key]=list(dict.fromkeys(old+[f['workspace_relative_path'] for f in row['files']]))
 note=' '.join(row['version_notes'])
 NOTES[key]=note if row.get('replace_version_notes') else (NOTES.get(key,'')+' '+note).strip()
 for f in row['files']:FILE_METADATA[f['workspace_relative_path']]=f
for key,row in json.loads((AUTHOR/'EVIDENCE_ADDITIONS.json').read_text(encoding='utf-8')).items():
 EVIDENCE[key]=row['workspace_relative_path']

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workspace',type=Path,required=True)
parser.add_argument('--repo',type=Path,required=True)
args=parser.parse_args()
ROOT=args.workspace.resolve()
REPO=args.repo.resolve()
OUT=REPO/'docs/theorem-application-audit'
OUT.mkdir(parents=True,exist_ok=True)
TEX=OUT/'source/audited-baseline.tex'
raw=TEX.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
EXPECTED='cb1148cd6c7769d2af3f1636b60ff0ada4b40431978d1e98d0c339274b3d792b'
if sha!=EXPECTED:
 raise SystemExit('Manuscript changed: review the specifications and anchors before regenerating. Expected '+EXPECTED)
text=raw.decode('utf-8-sig'); lines=text.splitlines()
def digest(b): return hashlib.sha256(b).hexdigest()
def dump(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def uncomment(s): return re.sub(r'(?<!\\)%[^\n]*','',s)
clean=uncomment(text)
bib_start=next(i for i,l in enumerate(lines,1) if r'\begin{thebibliography}' in l)
pre='\n'.join(lines[:bib_start-1])
clean_pre=uncomment(pre)
cite_re=re.compile(r'\\cite(?:[a-zA-Z*]*)\s*(?:\[([^]]*)\])?\s*\{([^}]+)\}')
citations=[]
for n,m in enumerate(cite_re.finditer(clean_pre),1):
 line=clean_pre.count('\n',0,m.start())+1
 start=line
 while start>1 and lines[start-2].strip(): start-=1
 end=line
 while end<len(lines) and lines[end].strip(): end+=1
 excerpt='\n'.join(lines[start-1:end])
 citations.append(dict(id=f'C{n:03}',line=line,locator=m[1],keys=[k.strip() for k in m[2].split(',')],
  paragraph_start=start,paragraph_end=end,paragraph=excerpt,paragraph_sha256=digest(excerpt.encode())))
by_cite={c['id']:c for c in citations}
bibs=[]
for m in re.finditer(r'\\bibitem\{([^}]+)\}([\s\S]*?)(?=\\bibitem|\\end\{thebibliography\})',text):
 bibs.append(dict(id=m[1],citation=m[2].strip(),urls=re.findall(r'\\url\{([^}]+)\}',m[2])))
downloads=json.loads((Path(__file__).parent/'DOWNLOADS.json').read_text())
for row in downloads:
 if row['status']=='downloaded':
  key='berger2002' if row['id']=='berger-arxiv-v3' else row['id']
  SOURCE_PATHS.setdefault(key,[]).append('work/theorem-application-audit-20261105/primary/'+Path(row['path']).name)

# Additional publisher downloads have paths registered explicitly in source_map.
downloads += json.loads((Path(__file__).parent/'CLOSURE_DOWNLOADS.json').read_text(encoding='utf-8'))

evidence=[]
(OUT/'evidence').mkdir(exist_ok=True)
for id,path in EVIDENCE.items():
 p=ROOT/path
 if not p.exists(): raise ValueError('missing review '+path)
 name=id+p.suffix
 shutil.copyfile(p,OUT/'evidence'/name)
 evidence.append(dict(id=id,path='evidence/'+name,sha256=digest(p.read_bytes()),
   historical_workspace_path=path,
   scope=('Current bounded root review; listed premises remain dependencies; not an independent second review.' if id.startswith('closure-') else 'Current bounded independent agent review; listed dependencies and exclusions remain; not acceptance of the whole manuscript.' if id.startswith('parallel-') else 'Historical limited review; its own source versions and exclusions govern. Not an independent check of the current whole manuscript.')))

sources=[]
for id in sorted(set(SOURCE_PATHS)|{b['id'] for b in bibs}):
 bib=next((b for b in bibs if b['id']==id),{})
 files=[]
 for path in SOURCE_PATHS.get(id,[]):
  p=ROOT/path
  if p.exists():
   f=dict(workspace_relative_path=path,sha256=digest(p.read_bytes()),bytes=p.stat().st_size)
   dl=next((x for x in downloads if x.get('sha256')==f['sha256']),None)
   if dl: f['retrieval_url']=dl['url'];f['retrieved_date']='2026-11-05'
   meta=FILE_METADATA.get(path,{})
   if meta:
    if meta['sha256']!=f['sha256']:raise ValueError('Reviewed source changed: '+path)
    for field in ('retrieval_url','retrieved_date','url'):
     if field in meta:f['retrieval_url' if field=='url' else field]=meta[field]
   files.append(f)
  else: files.append(dict(workspace_relative_path=path,status='MISSING'))
 sources.append(dict(id=id,bibliography=bib.get('citation'),urls=bib.get('urls',[]),files=files,
  version_notes=NOTES.get(id,'Exact bytes pinned below; publication/version equivalence is not inferred from the filename.'),
  source_status='bytes_pinned' if files and all('sha256' in f for f in files) else 'source_pin_missing'))

if set(ROLES)!=set(by_cite):raise ValueError('Frozen citation roles do not cover this manuscript')
for c in citations:
 row=ROLES[c['id']]
 ids=[a['id'] for a in APPS if c['id'] in a['citations']]
 if ids!=row['application_ids']:raise ValueError('Frozen citation membership differs: '+c['id'])
 c.update(row)

applications=[]
for a in APPS:
 a=dict(a)
 anchors=[]
 for cid in a['citations']:
  c=by_cite[cid]
  anchors.append(dict(kind='citation',citation_id=cid,line_start=c['paragraph_start'],line_end=c['paragraph_end'],excerpt_sha256=c['paragraph_sha256']))
 # Additional line arrays describe multiple manuscript anchors. Each individual
 # point has exact nearby text; the array does not assert that every consecutive
 # pair is a contiguous range.
 for line in a.pop('additional_lines'):
  if not 1<=line<=len(lines): raise ValueError((a['id'],line))
  lo=max(1,line-2);hi=min(len(lines),line+2)
  excerpt='\n'.join(lines[lo-1:hi])
  anchors.append(dict(kind='context',line_start=lo,line_end=hi,excerpt=excerpt,excerpt_sha256=digest(excerpt.encode())))
 a['manuscript_anchors']=anchors
 a['manuscript_sha256']=sha
 a['hypothesis_status']='Source interface and registered translations reviewed with stated internal premises; no whole-proof certificate.'
 a['source_pin_complete']=bool(a['sources']) and all(next(s for s in sources if s['id']==id)['source_status']=='bytes_pinned' for id in a['sources'])
 applications.append(a)

# Each occurrence remains inspectable even where the mathematical interface is
# shared by an application family. This is not a claim that nearby anchors are
# distinct theorem invocations, nor that implicit invocations are exhaustive.
sites=[]
for a in applications:
 for j,anchor in enumerate(a['manuscript_anchors'],1):
  sites.append(dict(id=f"{a['id']}-S{j:02}",application_id=a['id'],
   anchor=anchor,source_ids=a['sources'],
   interface_inheritance='objects_and_maps, hypotheses_and_discharge, conventions and translation_justification in parent application record',
   status='anchored occurrence/context; individual hypothesis discharge not certified'))

# Every explicit internal reference has a target in the frozen manuscript.
labels={}
for i,l in enumerate(lines,1):
 for m in re.finditer(r'\\label\{([^}]+)\}',uncomment(l)):
  labels.setdefault(m[1],[]).append(i)
internal=[]
for m in re.finditer(r'\\(?:eqref|ref|autoref|cref|Cref)\{([^}]+)\}',clean_pre):
 line=clean_pre.count('\n',0,m.start())+1
 for name in m[1].split(','):
  internal.append(dict(line=line,label=name,target_lines=labels.get(name,[])))

# Index named input signals separately; a lexical hit is NOT automatically an
# application. This makes the boundary and remaining manual coverage visible.
patterns={
 'Dirichlet':('Dirichlet', ['A057','A011']),
 'Chebotarev':('Chebotarev',['A064','A067']),
 'Faltings':('Faltings',['A004','A006','A008','A009','A014','A018','A063']),
 'Skolem-Noether':('Skolem',['A062']),
 'Mordell-Weil':('Mordell',['A059']),
 'Poincare':('Poincar',['A063']),
 'Minkowski':('Minkowski',['A058']),
 'Lagrange':('Lagrange',['A055']),
 'Hasse':('Hasse',['A072']),
 'Hilbert90':('Hilbert',['A073']),
 'Poitou-Tate':('Poitou',['A045']),
 'Nakayama':('Nakayama',['A075']),
 'Weil':('Weil',['A053','A054','A037','A059']),
 'Artin':('Artin',['A068','A012','A075']),
 'CRT':('Chinese|CRT',['A057']),
 'ultrafilter':('ultrafilter',['A076']),
 'formal group':('formal (?:group|log)|local logarithm',['A071']),
}
named=[]
for id,(pattern,apps) in patterns.items():
 for i,l in enumerate(lines[:bib_start-1],1):
  if re.search(pattern,uncomment(l),re.I):
   named.append(dict(signal=id,line=i,text=l,related_application_ids=apps,classification='lexical index; inspect context, may be definition/provenance rather than application'))

coverage=dict(manuscript_path='docs/theorem-application-audit/source/audited-baseline.tex',manuscript_sha256=sha,manuscript_lines=len(lines),
 citation_occurrences=len(citations),citation_key_occurrences=sum(len(c['keys']) for c in citations),
 cited_works=len({k for c in citations for k in c['keys']}),bibliography_works=len(bibs),
 citation_roles=dict(Counter(c['role'] for c in citations)),applications=len(applications),
 uncited_application_records=sum(not a['citations'] for a in applications),
 applications_with_open_items=sum(bool(a['open_items']) for a in applications),
 source_records=len(sources),sources_byte_pinned=sum(s['source_status']=='bytes_pinned' for s in sources),
 anchored_application_contexts=len(sites),
 fresh_source_interface_checks=sum('fresh_source_check' in a for a in applications),
 citation_strength_findings=[a['id'] for a in applications if a['status'] in {'citation_strength_mismatch_repair_proposed','citation_repair_applied_separate_acceptance_pending'}],
 internal_reference_occurrences=len(internal),unresolved_internal_references=[r for r in internal if not r['target_lines']],
 duplicate_labels={k:v for k,v in labels.items() if len(v)>1},named_input_signals=len(named),
 mechanically_complete_citation_classification=all(c['role']!='UNCLASSIFIED' for c in citations),
 semantic_exhaustiveness='NOT CERTIFIED: this is a manuscript-wide inventory of explicit citations and identified uncited substantive inputs; a lexical search cannot prove absence of further implicit uses.',
 application_correctness='NOT CERTIFIED: source pinning, inventory coverage and inherited reviews do not prove the applications.',
 frozen_date='2026-11-05')

dump('sources.json',sources);dump('applications.json',applications);dump('citations.json',citations)
dump('internal-references.json',internal);dump('named-input-index.json',named);dump('evidence.json',evidence);dump('coverage.json',coverage)
dump('application-sites.json',sites)

def paper_link(n):return 'source/audited-baseline.tex#L'+str(n)
md=['# Theorem application inventory','',f'Manuscript SHA256: `{sha}`. Line numbers refer only to this frozen source.','',
 'This document records the checked source applications, their exact consumers, and the hypotheses, translations and dependencies retained by each decision. Linked evidence includes historical reports and current bounded reviews; their stated scope and source version govern. An accepted application is not a certificate of every internal premise or the main theorem.','',
 'The JSON files preserve every citation occurrence and excerpt hash, source byte hashes, internal references, and a separate named-input search index. See [coverage](coverage.json) and [source versions](SOURCES.md).','',
 '| ID | Application | Citation occurrences | Open item |','|---|---|---|---|']
for a in applications:md.append(f"| [{a['id']}](#{a['id'].lower()}) | {a['title']} | {', '.join(a['citations']) or 'uncited'} | {'yes' if a['open_items'] else 'none within reviewed scope'} |")
for a in applications:
 md += ['',f"<a id=\"{a['id'].lower()}\"></a>",f"## {a['id']}: {a['title']}",'',
   'Manuscript: '+', '.join(f"[L{x['line_start']}]({paper_link(x['line_start'])})" for x in a['manuscript_anchors'])+'.',
   '', '**Source:** '+(', '.join(f'[{s}](SOURCES.md#{s})' for s in a['sources']) or '**Not yet identified.**')+'. '+a['source_locator']+'.',
   '', '**Objects and maps.** '+a['objects_and_maps'],
   '', '**Hypotheses and claimed discharge.** '+a['hypotheses_and_discharge'],
   '', '**Conventions.** '+a['conventions'],
   '', '**Translation.** '+a['translation_justification'],
   '', '**Review evidence:** '+(', '.join(f'[{e}]({next(x["path"] for x in evidence if x["id"]==e)})' for e in a['prior_evidence']) or 'No bounded source/application review attached.')+'.',
   '', '**Status:** '+a['status']+'.',
   '', '**Open item:** '+(a['open_items'] or 'No unresolved item within the recorded source-application scope. Named internal premises remain dependencies; this is not a whole-proof certificate.')]
 if a.get('independent_acceptance_reviews'):
  for item in a['independent_acceptance_reviews']:
   md += ['', '**Independent acceptance:** '+item['reviewer']+'. The complete decision, retained premises and baseline binding are in applications.json and the linked acceptance report.']
 if a.get('retained_internal_premises'):
  md += ['', '**Retained internal premises.** '+str(a['retained_internal_premises'])]
 if a.get('dependency_phases') or a.get('dependency_clarifications'):
  md += ['', 'See [dependency phases](DEPENDENCIES.md) and [the machine-readable distinctions](DEPENDENCY_PHASES.json); a source check does not discharge its own prerequisites.']
 if 'fresh_source_check' in a:
  md += ['', '**Source inspection on 2026-11-05:** '+a['fresh_source_check']['result'], '', a['fresh_source_check']['scope']]
(OUT/'INVENTORY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
def markdown_bibliography(text):
 # GitHub otherwise autolinks the closing TeX brace as part of the URL.
 return re.sub(r'\\url\{(https?://[^{}\s]+)\}', lambda m: '<'+m[1]+'>', text)

sm=['# Source versions','', 'Hashes identify the files actually available for review. A hash does not identify a journal version unless that equivalence has been checked. Primary files are not duplicated here; workspace-relative paths locate them in the research corpus, and retrieval URLs are supplied where recorded.','']
for s in sources:
 sm += [f'<a id="{s["id"]}"></a>',f'## {s["id"]}','',markdown_bibliography(s['bibliography']) or 'Supplementary source, not a distinct current bibliography entry.','',s['version_notes'],'',f'Pin status: **{s["source_status"]}**.','']
 for f in s['files']:
  sm += ['- `'+f['workspace_relative_path']+'`', '  - SHA256: `'+f.get('sha256','MISSING')+'`']
  if 'retrieval_url' in f:sm+=['  - [Retrieved source]('+f['retrieval_url']+') on '+f.get('retrieved_date','date not recorded')+'.']
(OUT/'SOURCES.md').write_text('\n'.join(sm)+'\n',encoding='utf-8')
om=['# Open review obligations','',
 'These are unresolved obligations, not automatically mathematical gaps. A closed documentation item does not certify the entire application. Each link gives the maps, hypotheses, conventions, translations, and evidence already recorded.','',
 'The concrete source-strength mismatch is recorded separately in [FINDINGS.md](FINDINGS.md).','']
if not any(a['open_items'] for a in applications):om += ['No unresolved source-application review items remain within the 82 recorded families. Retained internal premises are documented in the inventory and dependency phases; this statement does not certify the entire proof.','']
for a in applications:
 if a['open_items']:
  om += [f"- [ ] [{a['id']}: {a['title']}](INVENTORY.md#{a['id'].lower()}): {a['open_items']}"]
(OUT/'OPEN_ITEMS.md').write_text('\n'.join(om).rstrip()+'\n',encoding='utf-8')
print(json.dumps(coverage,indent=2))
