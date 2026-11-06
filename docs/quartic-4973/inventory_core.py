"""Bounded metadata and text binding for one reviewed V4 source family.

This does not establish arithmetic truth, run the source auditor, or replay a
certificate.  Those are separate acceptance inputs and mandatory release gates.
"""
import copy
import gzip
import hashlib
import json
import re
import time
from pathlib import Path, PurePosixPath

import tex_subset as tex

HERE = Path(__file__).resolve().parent
INPUTS_SHA = 'ae388dfb7f577f3240bbbb96cfae38711c9d460c866eb8701fdc2279c850d523'
FAMILY = 'H19-root37-target2-tangent-first-norm-normalized-linear-pole-v1'
PREFIX = 'target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-'
SELECTED = ['N1','N2','N3','N4a','N4b','N4c','N5','N6','N7','N8','C1','N9','N10','N12','N13','N14','N15']
REQUIRED_ROLES = {'manuscript','integrated_manuscript_review','source_arithmetic_review',
    'verification','reproduction','source_entry','source_audit','source_auditor',
    'construction_map','source_layout','source_residuals','certificate',
    'certificate_checker','expanded','compiled_rows','residuals','weights','variable_map'}
EXPECTED_KEYS = {'source_id','source_sha256','source_raw_sha256','variables','witnesses',
    'rows','monomials','degree','max_abs_coefficient','source_variables','source_rows'}
SCOPES = {
    'integrated_manuscript_review':'exact integrated manuscript and selected arithmetic exposition',
    'source_arithmetic_review':'exact emitted source and its integer rational-projection theorem',
    'verification':'exact certificate replay, full quartic expansion and coefficient bound',
    'reproduction':'clean source regeneration, fresh base pipeline and exact selected certificate replay',
}


class InvalidInventory(ValueError):
    pass


class ResourceLimit(RuntimeError):
    pass


def require(ok, message):
    if not ok:
        raise InvalidInventory(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True)+'\n').encode()


class Budget:
    def __init__(self, seconds=45, max_bytes=600_000_000):
        require(type(seconds) in (int,float) and 0 < seconds <= 120, 'Invalid time budget')
        self.until = time.monotonic()+seconds
        self.left = max_bytes

    def tick(self, amount=0):
        self.left -= amount
        if self.left < 0 or time.monotonic() > self.until:
            raise ResourceLimit('Inventory byte or time budget exceeded')


def relative(value):
    require(type(value) is str and 0 < len(value) < 500, 'Relative path required')
    require('\\' not in value and ':' not in value and '\x00' not in value, 'Unsafe path')
    p = PurePosixPath(value)
    require(not p.is_absolute() and all(x not in ('','.','..') for x in value.split('/')), 'Unsafe path components')
    return value


def inside(root, name):
    name = relative(name)
    root = Path(root).resolve()
    path = (root/name).resolve()
    require(path.is_relative_to(root), 'Path escapes root')
    return path


def tree_limit(value):
    stack = [(value,0)]
    nodes = 0
    while stack:
        x, depth = stack.pop(); nodes += 1
        if depth > 40 or nodes > 250_000:
            raise ResourceLimit('JSON nesting/node limit')
        if type(x) is dict:
            stack.extend((k,depth+1) for k in x)
            stack.extend((v,depth+1) for v in x.values())
        elif type(x) is list:
            stack.extend((v,depth+1) for v in x)
        elif type(x) is str:
            if len(x) > 2_000_000: raise ResourceLimit('JSON string limit')
        elif type(x) is int:
            if x.bit_length() > 1024: raise ResourceLimit('JSON integer limit')
        elif x is not None and type(x) not in (bool,float):
            raise InvalidInventory('Unsupported JSON value')


def parse(data):
    if len(data) > 8_000_000: raise ResourceLimit('JSON byte limit')
    def pairs(items):
        result = {}
        for k,v in items:
            require(k not in result, 'Duplicate JSON key '+k)
            result[k] = v
        return result
    try:
        value = json.loads(data, object_pairs_hook=pairs,
                           parse_constant=lambda s: (_ for _ in ()).throw(InvalidInventory('Nonfinite JSON')))
    except RecursionError as e:
        raise ResourceLimit('JSON parser nesting limit') from e
    tree_limit(value)
    return value


def small(path, budget, maximum=8_000_000):
    require(path.is_file(), 'Missing file '+str(path))
    size = path.stat().st_size
    if size > maximum: raise ResourceLimit('File size limit '+str(path))
    budget.tick(size)
    data = path.read_bytes()
    require(len(data) == size, 'File changed while reading')
    return data


def file_digest(path, budget, unpack=False):
    require(path.is_file(), 'Missing file '+str(path))
    h = hashlib.sha256(); length = 0
    opener = gzip.open if unpack else open
    with opener(path,'rb') as f:
        while True:
            data = f.read(262144)
            if not data: break
            length += len(data); budget.tick(len(data)); h.update(data)
    return h.hexdigest(),length


def record(value):
    require(type(value) is dict and set(value)=={'path','sha256','bytes'}, 'File record keys')
    relative(value['path'])
    require(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}',value['sha256']), 'Bad SHA256')
    require(type(value['bytes']) is int and 0 <= value['bytes'] <= 100_000_000, 'Bad file length')


def check_record(root, value, budget):
    record(value)
    got = file_digest(inside(root,value['path']),budget)
    require(got == (value['sha256'],value['bytes']), 'Changed file '+value['path'])


def load_inputs():
    data = (HERE/'inputs.json').read_bytes()
    require(digest(data)==INPUTS_SHA, 'Tool input registry changed')
    return parse(data)


def context_name(role, rec):
    return 'context/'+role+Path(rec['path']).suffix


def load_context(root, budget, packaged=False):
    records = load_inputs(); content = {}
    for role,rec in records.items():
        name = context_name(role,rec) if packaged else rec['path']
        data = small(inside(root,name),budget)
        require((digest(data),len(data))==(rec['sha256'],rec['bytes']), 'Changed context '+role)
        content[role] = data
    return content


def graph_context(content):
    graph = parse(content['graph']); consumption = parse(content['consumption'])
    old = parse(content['v3_inventory']); publications = parse(content['publications'])
    require(graph['selected_line']==SELECTED,'Wrong selected proof line')
    require(consumption['source_version_requirements']==old['source_version_requirements'], 'Source qualifications changed')
    require(len(consumption['source_version_requirements'])==5, 'Five qualifications required')
    byid = {x['id']:x for x in graph['nodes']}
    require(len(byid)==len(graph['nodes']), 'Duplicate graph node')
    nodes = [copy.deepcopy(byid[x]) for x in SELECTED]
    external = {x['id'] for x in consumption['groups']} | {x['id'] for x in publications['additional_applications']}
    require(len(external)==11,'External group count')
    edges = []
    for node in nodes:
        for key in ('depends_on','source_composition_after'):
            for target in node.get(key,[]):
                require(target in SELECTED,'Unselected dependency')
                edges.append({'source':node['id'],'target':target,'kind':key})
        for target in node['external']:
            require(target in external,'Unknown external dependency')
            edges.append({'source':node['id'],'target':target,'kind':'external_application'})
    active = set(); done = set()
    def visit(name):
        require(name not in active,'Dependency cycle')
        if name in done:return
        active.add(name)
        for e in edges:
            if e['source']==name:visit(e['target'])
        active.remove(name);done.add(name)
    for name in SELECTED:visit(name)
    pins = {x['id']:x for x in parse(content['proof_pins'])['artifacts']}
    wanted = sorted({p for x in nodes for p in x['proofs']+x['reviews']})
    require(all(p in pins for p in wanted),'Unbound proof artifact')
    return nodes,edges,consumption,publications,[pins[p] for p in wanted]


def selected_text(content, edits=()):
    # The original independently reviewed appendix and the explicit splice diff
    # remain pinned context. Final integration changes are separately reviewed;
    # they are not treated as whitespace-only or retroactively covered by an old review.
    tex.select(content['draft'].decode('utf-8-sig'))
    text = content['integrated_appendix'].decode('utf-8-sig')
    text = tex.layout_edits(text,list(edits))
    nodes,*_ = graph_context(content)
    labels = sorted({x['label'] for x in nodes if x['label']} | {'thm:quartic-selective-arithmetic'})
    spans = {label:tex.theorem_span(text,label) for label in labels}
    require('lem:quartic-scalar-inverse-fusion' not in tex.structure(text)[1], 'Optional J0 was selected')
    return text,spans


def acceptance_schema(a):
    keys = {'schema','accepted','version','source_family','features','main_label','layout_edits',
            'package','files','expected','approval_scopes','finite_rules'}
    require(type(a) is dict and set(a)==keys,'Acceptance keys')
    require(a['schema']=='quartic-v4-final-inventory-acceptance-v1' and a['accepted'] is True, 'Final acceptance required')
    require(type(a['version']) is int and a['version']==4 and a['source_family']==FAMILY,'Wrong version/source family')
    require(a['features']==tex.FLAGS and all(type(x) is bool for x in a['features'].values()),'Wrong feature selection')
    require(a['main_label']=='thm:quartic','Unexpected main theorem')
    require(a['approval_scopes']==SCOPES,'Approval scopes must be explicit and separate')
    require(type(a['layout_edits']) is list,'Layout edits must be explicit')
    require(type(a['package']) is dict and set(a['package'])=={'root','source_root','auditor_root'},'Package paths')
    for name in a['package'].values():relative(name)
    files = a['files']; require(type(files) is dict and REQUIRED_ROLES <= set(files), 'Missing required acceptance file role')
    for role,rec in files.items():
        require(re.fullmatch('[a-z][a-z0-9_]{0,79}',role),'Unsafe file role');record(rec)
    require(len({x['path'] for x in files.values()})==len(files),'File roles must be distinct')
    e = a['expected'];require(type(e) is dict and set(e)==EXPECTED_KEYS,'Expected endpoint keys')
    require(type(e['source_id']) is str and re.fullmatch(re.escape(PREFIX)+'[0-9a-f]{12}',e['source_id']), 'Wrong source ID family')
    for key in ('source_sha256','source_raw_sha256'):
        require(type(e[key]) is str and re.fullmatch('[0-9a-f]{64}',e[key]),'Source digest')
    require(e['source_id']==PREFIX+e['source_raw_sha256'][:12],'Source ID/raw hash disagreement')
    for key in EXPECTED_KEYS-{'source_id','source_sha256','source_raw_sha256'}:
        require(type(e[key]) is int and e[key]>0, 'Positive integer endpoint field '+key)
    require(e['variables']<5000 and e['variables']==e['witnesses']+1,'Target counts must include the input')
    require(e['degree']==4 and e['max_abs_coefficient']<2**80,'Quartic/coefficient claim')
    require(type(a['finite_rules']) is dict and a['finite_rules'],'Finite rule evidence required')
    for kind,binding in a['finite_rules'].items():
        require(re.fullmatch('[a-z][a-z0-9_]{0,79}',kind),'Operation name')
        require(type(binding) is dict and set(binding)=={'proof_role','review_role'},'Rule binding')
        require(binding['proof_role'] in files and binding['review_role'] in files,'Unbound finite rule')
        require(binding['proof_role']!=binding['review_role'],'Proof and review must be distinct')


def compare_fields(actual, expected, prefix):
    for key,value in expected.items():
        require(key in actual and type(actual[key]) is type(value) and encoded(actual[key])==encoded(value),prefix+': '+key)


def validate_finite(repo,a,budget,content):
    acceptance_schema(a)
    for rec in a['files'].values():check_record(repo,rec,budget)
    def path(role):return inside(repo,a['files'][role]['path'])
    def load(role):return parse(small(path(role),budget))
    e=a['expected'];v=load('verification');entry=load('source_entry');audit=load('source_audit')
    compare_fields(v,{k:e[k] for k in ('source_id','source_sha256','variables','witnesses','rows','monomials','degree','max_abs_coefficient')},'Verification')
    require(v['status']=='PASS','Verification did not pass')
    for role,key in (('certificate','certificate_sha256'),('certificate_checker','checker_sha256')):
        require(v[key]==a['files'][role]['sha256'],'Verification file binding '+role)
    require(type(v['operations']) is dict and set(v['operations'])==set(a['finite_rules']),'Active rule coverage')
    require(all(type(n) is int and n>0 for n in v['operations'].values()),'Operation counts')
    require(sum(v['operations'].values())==v['total_operations'],'Total operation count')
    expanded=file_digest(path('expanded'),budget,unpack=path('expanded').suffix=='.gz')
    require(expanded==(v['expanded_sha256'],v['expanded_bytes']),'Exact expanded file binding')
    compare_fields(entry,{'source_id':e['source_id'],'source_sha256':e['source_sha256'],
        'uncompressed_sha256':e['source_raw_sha256'],'source_variables':e['source_variables'],
        'source_rows':e['source_rows'],'high':40,'label':12,'compressed':True},'Source entry')
    compare_fields(audit,{'status':'PASS: SOURCE CONSTRUCTION ONLY','source_pin_authorized':False,
        'arithmetic_acceptance':False,'high':40,'label':12,'compressed':True},'Source audit')
    require(a['files']['source_residuals']['sha256']==e['source_sha256'],'Compressed source binding')
    require(file_digest(path('source_residuals'),budget,True)[0]==e['source_raw_sha256'],'Raw source binding')
    for key,role in (('source_audit_sha256','source_audit'),('source_audit_checker_sha256','source_auditor'),
                     ('construction_map_sha256','construction_map'),('source_layout_sha256','source_layout')):
        require(entry[key]==a['files'][role]['sha256'],'Entry file binding '+role)
    require(audit['checker_sha256']==entry['source_audit_checker_sha256'],'Audit checker binding')
    policy=parse(content['source_auditor_policy'])
    require(audit['checker_sha256']==policy['checker_sha256'],'Source auditor is not the reviewed first-norm auditor')
    require(audit['checker_dependencies_sha256']==policy['helper_files'],'Complete source auditor dependency set')
    require(audit['construction_map_sha256']==entry['construction_map_sha256'],'Construction map binding')
    require(audit['counts']==entry['source_header'],'Source header agreement')
    require(entry['source_header']['witnesses']+1==e['source_variables'] and entry['source_header']['residuals']==e['source_rows'],'Source counts')
    require(audit['inspected_files_sha256']==entry['inspected_files_sha256'],'Complete inspected-source binding')
    residual=audit['source_residual_file']
    require(residual in ('residuals.jsonl','residuals.jsonl.gz'),'Unexpected source residual name')
    expected_source={'SELECTED_PARENT.json','ROOT_SHARED_CONTRACT.json','FIRST_NORM_CONTRACT.json',
        'FIRST_NORM_PROOF.md','MIXED_MODE_DENOMINATOR_CLARIFICATION.md','TANGENT_SOURCE_CONTRACT.json',
        'TANGENT_PROOF.md','TARGET_TWO_PROOF.md','TARGET_TWO_CONTRACT.md','TARGET_TWO_SOURCE_CONTRACT.json',
        'TARGET2_COMPOSITION_CONTRACT.json','ROOT_SOURCE_CONTRACT.json','ROOT_COMPOSITION_CONTRACT.json',
        'SHARED_SQUARE_CONTRACT.json','NORMALIZED10_CONTRACT.json','NORMALIZED_PARENT_PINS.json',
        'CONIC_POLE_CONTRACT_ADDON.json','LOCAL_LUCAS_POLE_CONTRACT.json','NORMALIZED_POLE_CONTRACT.json',
        'PARENT_SOURCE_PINS.json','NORMALIZED_SOURCE_CONTRACT.json','NORMALIZED_LUCAS_CONTRACT_ADDON.json',
        'LOCAL_LUCAS_SOURCE_CONTRACT.json','LOCAL_LUCAS_CONTRACT_ADDON.json','JOINT_CHART_CONTRACT_ADDON.json',
        'JOINT_SOURCE_CONTRACT.json','CONIC_SOURCE.json','counts.json','polynomial.json','shared.json',residual}
    if residual=='residuals.jsonl' and 'residuals.jsonl.gz' in audit['inspected_files_sha256']:
        expected_source.add('residuals.jsonl.gz')
    expected_source|={'compiler/'+n for n in policy['compiler_files']}
    expected_source|={'modules/'+n+'.json' for n in ('Z_definition','q_anchor','q_height_batch','q_primeparity',
        'q_compare4','q_conic13','q_compare_beta','q_conic6','q_compare_lucas','q_conic10','q_linearnormalpole')}
    require(set(audit['inspected_files_sha256'])==expected_source,'Complete inspected-source file set')
    require(audit['inspected_files_sha256']['ROOT_SHARED_CONTRACT.json']==digest(content['active_source_contract']),
            'Active combined source contract changed')
    source=inside(repo,a['package']['source_root']);auditor=inside(repo,a['package']['auditor_root'])
    for name,wanted in audit['inspected_files_sha256'].items():
        p=inside(source,name)
        if p.is_file():got=file_digest(p,budget)[0]
        elif name=='residuals.jsonl':got=file_digest(path('source_residuals'),budget,True)[0]
        else:raise InvalidInventory('Missing inspected source '+name)
        require(got==wanted,'Changed inspected source '+name)
    for name,wanted in audit['checker_dependencies_sha256'].items():
        require(file_digest(inside(auditor,name),budget)[0]==wanted,'Changed source auditor dependency '+name)
    proposal=parse(small(inside(source,'CONIC_SOURCE.json'),budget))
    require(proposal==entry['proposal'],'Proposal/entry agreement')
    compare_fields(proposal,dict(source_family=FAMILY,high=40,label=12,anchor_squarings=25,
        height_exponent=19,scalar_orders=[1,1,1,1,32,32],comparison_target_multiplier=2,
        root_index_semantics='2Q=n_Q Pstar, n_Q integer',root_beta_comparison_scale=2,
        root_doubling_model='direct tangent with retained square coordinates',direct_tangent_doublings=4,
        first_norm_field_role='H.f',first_norm_field_order=1,first_norm_instances=37,
        first_norm_virtual_denominator_exponent=1,first_norm_arithmetic_change=True,
        normalized_lucas_residual=True,normalized_lucas_occurrences=29,
        normalized_lucas_formula='F(C_s,C_t,C_z)/C_s^2',shared_square_fields=37,
        ordinary_pole_module='q_linearnormalpole',ordinary_pole_private_coordinates=10,
        ordinary_pole_full_Psi_projection=False,private_index_group='(1/2)Z via doubling',
        beta_only_positions=list(range(5,13)),lucas_only_positions=list(range(13,21))+list(range(29,37)),
        full_positions=list(range(5))+list(range(21,29)),
        full_field_orders=[1]*6+[12,40,40,12,40,40,40],beta_field_orders=[1]*3+[12]*3,
        lucas_field_orders=[1]*5+[40]*5), 'Selected arithmetic interface')
    layout=load('source_layout')
    require(layout['counts']==entry['layout_counts'],'Layout counts binding')
    compare_fields(layout['counts'],dict(comparisons=37,batches=37,conic_fields=377,
        conic_first_numerators=37,conic_norm_fields=340,conic_evaluations=340,
        private_conics=37,conic_poles=37,parity=1,norm_guards=0,batch_pairs=0),'Layout')
    compare_fields(layout['module_counts'],dict(q_compare4=13,q_compare_beta=8,q_compare_lucas=16),'Mode instance counts')
    reproduction=load('reproduction')
    require(reproduction.get('status')=='PASS' and
            reproduction.get('mandatory_status')=='PASS: FRESH SOURCE AND EXACT FROZEN CERTIFICATE REPLAY',
            'Fresh source and exact frozen replay did not pass')
    require(reproduction.get('source_id')==e['source_id'],'Reproduction source identity')
    compare_fields(reproduction['final_verification'],{k:value for k,value in v.items() if k!='seconds'},'Fresh final replay')
    package_manifest=inside(repo,a['package']['root']+'/reproducibility/manifest.json')
    require(reproduction.get('package_manifest_sha256')==file_digest(package_manifest,budget)[0],
            'Reproduction belongs to another package')
    steps=reproduction.get('steps',[])
    require(type(steps) is list and bool(steps),'Missing reproduction steps')
    require(all(type(s.get('exit_code')) is int and not s.get('timeout') and not s.get('memory_abort') and
                (s['exit_code']>0 if s.get('expected_rejection') else s['exit_code']==0) for s in steps),
            'Incomplete or failed reproduction steps')
    compare_fields(reproduction['expected'],{k:e[k] for k in ('source_id','source_sha256','variables',
        'witnesses','rows','monomials','degree','max_abs_coefficient')},'Reproduction endpoint')
    compare_fields(reproduction['expected'],dict(certificate_sha256=a['files']['certificate']['sha256'],
        expanded_sha256=v['expanded_sha256']),'Reproduction exact artifact')
    return dict(verification=v,entry=entry,audit=audit)


def bridge_item(old_text,new_text,item,line_key,hash_key):
    lo,hi=item[line_key]
    lines=old_text.splitlines()
    require(type(lo) is int and type(hi) is int and 1<=lo<=hi<=len(lines),'Historical line range')
    excerpt='\n'.join(lines[lo-1:hi])
    require(digest(excerpt.encode())==item[hash_key],'Historical excerpt pin changed')
    start=new_text.find(excerpt)
    require(start>=0,'Changed historical excerpt '+item['id'])
    if new_text.find(excerpt,start+1)>=0:
        # Context disambiguates occurrence identity, rather than taking the
        # first of several equal excerpts with possibly different roles.
        found=False
        for extra in (2,4,8,16,32):
            a=max(0,lo-1-extra);b=min(len(lines),hi+extra)
            context='\n'.join(lines[a:b]);at=new_text.find(context)
            if at>=0 and new_text.find(context,at+1)<0:
                start=at+len('\n'.join(lines[a:lo-1]))+(1 if lo-1>a else 0);found=True;break
        require(found,'Ambiguous historical excerpt '+item['id'])
    result=copy.deepcopy(item)
    result['version3_location']=result.pop(line_key)
    result['version4_location']=tex.span(new_text,start,start+len(excerpt))
    result['review_scope']='Original historical object and qualifications; exact text bridge only'
    return result


def make_documents(content,a,manuscript):
    acceptance_schema(a)
    nodes,edges,consumption,publications,pins=graph_context(content)
    body,_=selected_text(content,a['layout_edits']);location=tex.locate_exact(manuscript,body)
    main=tex.statement_span(manuscript,a['main_label'])
    maintext=tex.clean_comments(manuscript[main['start_character']:main['end_character']])
    numbers=set(int(s) for s in re.findall(r'(?<![A-Za-z0-9])\d+(?![A-Za-z0-9])',
        re.sub(r'\\[,;! ]','',maintext)))
    require({a['expected']['variables'],a['expected']['witnesses'],a['expected']['monomials'],
             a['expected']['max_abs_coefficient'],4}<=numbers,'Main theorem lacks exact endpoint claims')
    for node in nodes:
        node['current_source']=tex.theorem_span(manuscript,node['label']) if node['label'] else location
        node['proof_artifacts']=[{'id':key,'path':'evidence/'+key+Path(next(p['path'] for p in pins if p['id']==key)).suffix}
                                 for key in node['proofs']+node['reviews']]
    summary=tex.theorem_span(manuscript,'thm:quartic-selective-arithmetic')
    old=parse(content['v3_inventory']);oldtext=content['v3_manuscript'].decode('utf-8-sig').replace('\r\n','\n')
    inherited={x['id']:x for x in old['inherited_applications']}
    groups=[]
    for group in consumption['groups']:
        value=copy.deepcopy(group)
        value['historical_application_only']=inherited[group['id']]
        value['current_consumption_scope']='Only retained statement and replacement above; historical convention text is not a current premise'
        groups.append(value)
    historical=parse(content['v3_bridge'])
    bridge=dict(schema='quartic-v4-historical-bridge-v1',status='PASS',unresolved=[],
        historical_sha256=historical['historical_sha256'],version3_sha256=load_inputs()['v3_manuscript']['sha256'],
        current_sha256=a['files']['manuscript']['sha256'],
        anchors=[bridge_item(oldtext,manuscript,x,'current_lines','excerpt_sha256') for x in historical['anchors']],
        citation_paragraphs=[bridge_item(oldtext,manuscript,x,'current_paragraph_lines','paragraph_sha256') for x in historical['citation_paragraphs']])
    inherited_publications=copy.deepcopy(old['additional_published_applications'])
    for app in inherited_publications:
        for i,site in enumerate(app['current_sites']):
            site['id']=app['id']+'-'+str(i)
            mapped=bridge_item(oldtext,manuscript,site,'lines','excerpt_sha256')
            site.clear();site.update(mapped)
    for app in publications['additional_applications']:
        app['current_source']=tex.theorem_span(manuscript,'lem:quartic-anchor-four')
    edges += [{'source':'source_arithmetic','target':x,'kind':'arithmetic_lemma'} for x in SELECTED]
    edges += [{'source':a['main_label'],'target':'source_arithmetic','kind':'arithmetic'},
              {'source':a['main_label'],'target':'finite_certificate','kind':'finite'}]
    for kind,binding in a['finite_rules'].items():
        edges.append({'source':'finite_certificate','target':'rule:'+kind,'kind':'active_certificate_rule'})
    inventory=dict(schema='quartic-v4-theorem-inventory-v1',source_id=a['expected']['source_id'],
        source_family=FAMILY,manuscript=a['files']['manuscript'],main_theorem=main,selected_body=location,
        selected_features=tex.FLAGS,arithmetic_summary=summary,arithmetic_lemmas=nodes,
        inherited_applications=groups,additional_published_applications=publications['additional_applications'],
        inherited_additional_published_applications=inherited_publications,
        source_version_requirements=consumption['source_version_requirements'],
        endpoint=a['expected'],finite_rules=a['finite_rules'],approval_scopes=a['approval_scopes'],
        scope='Text, dependency and exact artifact binding; arithmetic truth, source audit and replay are separate reviewed gates')
    closure=dict(schema='quartic-v4-dependency-closure-v1',root=a['main_label'],edges=edges,
                 selected_nodes=SELECTED,optional_J0=False,external_groups=[x['id'] for x in groups]+['K_TRACE_23'])
    return {'theorem-applications.json':inventory,'dependency-closure.json':closure,'baseline-bridge.json':bridge},body,pins
