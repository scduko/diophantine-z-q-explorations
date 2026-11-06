"""Independent target-two delta on the pinned independent root-four audit.

The caller supplies and pins that audit module; no producer is imported.
Whole-source binding, unchanged modules and flattening remain outer duties.
"""
from copy import deepcopy

BASE_AUDIT_SHA='05fa04d6016212cdfde1613ce3c265f984cfa6f4adcc48737e714269dbbb01b2'
PROOF='cfc62097ffdbf072fe77524f7e0448356812712689394ca22dfc4a0fd64b7feb'
REVIEW='d5048cc8ac8944d26c8af6d9b8cfcdd672ddee1beed73efaf3d634a53b012155'
SECOND_VARIABLES={i for first in (122,142,162,182) for i in range(first,first+10)}
SECOND_ROWS={i for first in (110,130,150,170) for i in range(first,first+10)}
CONSTANT_ROWS=[196,197,269,270,271,272,291,292,293,294]
CONSTANT_VARIABLES=[210,211,287,288,285,286,307,308,309,310]
LINEAR_ROWS=[289,290,295,296]
LINEAR_VARIABLES=[305,306,311,312]


def replacements(base):
    """Literal scalar equations with original normalized-source IDs."""
    r=base.r
    rows={
        196:r((8,[210]),(-57,[])),197:r((2,[211]),(7,[])),
        269:r((1681,[287]),(-456,[])),270:r((1681,[288]),(-224,[])),
        271:r((41,[285]),(87,[])),272:r((164,[286]),(-129,[])),
        291:r((14637,[307]),(55123,[])),292:r((58548,[308]),(19301,[])),
        293:r((14161,[309]),(-7624,[])),294:r((127449,[310]),(39904,[])),
        289:r((357,[305]),(232,[208]),(-172,[209])),
        290:r((357,[306]),(-86,[208]),(232,[209])),
        295:r((127449,[311]),(-291673,[208]),(176640,[209])),
        296:r((127449,[312]),(88320,[208]),(-291673,[209])),
    }
    labels={index:'fixed Pstar '+name+'.'+str(component)
        for index,name,component in ((196,'x',0),(197,'x',1),(269,'f',0),(270,'f',1),
          (271,'q',0),(272,'q',1),(291,'conjugate s',0),(292,'conjugate s',1),
          (293,'conjugate t',0),(294,'conjugate t',1),(289,'r',0),(290,'r',1),
          (295,'u',0),(296,'u',1))}
    for j,(role,x,y) in enumerate((('A',14,16),('S',30,32),('T',46,48),('Z',62,64))):
        target=214+4*j;first=200+4*j
        for k in range(2):
            rows[first+k]=r((1,[target+k]),(2,[x+k]),(-1,[118+20*j+k]))
            rows[first+2+k]=r((1,[target+2+k]),(1,[y+k]),(-1,[120+20*j+k]))
            labels[first+k]='double target '+role+'.x.'+str(k)
            labels[first+2+k]='double target '+role+'.y.'+str(k)
    assert len(rows)==30
    return rows,labels


def expected_root(base,parent):
    old=base.expected_root(parent)
    gone={base.VARIABLE_MAP[i] for i in SECOND_VARIABLES}
    deleted={base.ROW_MAP[i] for i in SECOND_ROWS}
    vm={old:new for new,old in enumerate(i for i in range(259) if i not in gone)}
    rm={old:new for new,old in enumerate(i for i in range(243) if i not in deleted)}
    vi=lambda values:[vm[i] for i in values]
    ri=lambda values:[rm[i] for i in values]
    original_vi=lambda values:vi(base.ids(values))
    original_ri=lambda values:ri(base.row_ids(values))
    replace,labels=replacements(base)
    rows=deepcopy(old['residuals'])
    for index,row in replace.items():
        rows[base.ROW_MAP[index]]=[[c,base.ids(mon)] for c,mon in row]
    result=deepcopy(old);result['locals']=218
    result['residuals']=[[[c,vi(mon)] for c,mon in rows[i]] for i in range(243) if i not in deleted]
    result['calls']=[dict(call,args=vi(call['args'])) for call in old['calls']]
    labels={base.ROW_MAP[i]:label for i,label in labels.items()}
    result['construction_log']=[]
    for kind,index,label in old['construction_log']:
        mapping=vm if kind=='variable' else rm
        if index in mapping:
            result['construction_log'].append([kind,mapping[index],labels.get(index,label) if kind=='equation' else label])
    result['proxy_indices']=vi(old['proxy_indices'])
    result['point_coordinates']={name:vi(values) for name,values in old['point_coordinates'].items()}
    result['joint_chart_targets']=[{key:vi(values) for key,values in target.items()} for target in old['joint_chart_targets']]
    result['general_root_charts']={name:{key:value if key=='kind' else ri(value) if key.endswith('_rows') else vi(value)
        for key,value in record.items()} for name,record in old['general_root_charts'].items()}
    result['root_targets']=[]
    for j,target in enumerate(old['root_targets']):
        item={key:vi(value) for key,value in target.items() if key!='kind'}
        item['kind']='fixed_Pstar' if j==0 else 'double';result['root_targets'].append(item)
    result['comparison_base']['fixed_target']='2R=Pstar'
    result['comparison_target_multiplier']=2
    result['target_two_bindings']=dict(rows=original_ri(list(range(200,216))),first_doubling_only=True)
    result['fixed_target_bindings']=dict(coordinates=original_vi(CONSTANT_VARIABLES),rows=original_ri(CONSTANT_ROWS),
        linear_coordinates=original_vi(LINEAR_VARIABLES),linear_rows=original_ri(LINEAR_ROWS))
    provenance=result['general_root_rewrite']
    provenance.update(target_two_proof_sha256=PROOF,target_two_review_sha256=REVIEW,
        original_removed_variables=sorted(base.REMOVED_VARIABLES|SECOND_VARIABLES),
        original_removed_rows=sorted(base.REMOVED_ROWS|SECOND_ROWS),
        original_replaced_rows=sorted(replace),raw_variable_delta=-126,raw_row_delta=-126)
    return result


def expected_comparison(base,parent):
    result=base.expected_comparison(parent)
    result['comparison_fixed_target']='2R=Pstar'
    result['comparison_target_multiplier']=2
    result['input_layout']=result['input_layout'].replace('Fq(R4)','Fq(Pstar)')
    return result


def check_root(base,parent,candidate):
    base.exact(candidate,expected_root(base,parent),'Complete target-two root mismatch')
    variables={0};rows=set()
    for kind,index,label in candidate['construction_log']:
        if kind=='variable':
            assert index==len(variables),'Target-two variable sequence';variables.add(index)
        else:
            assert index not in rows,'Target-two repeated row';rows.add(index)
            assert all(v in variables for _,mon in candidate['residuals'][index] for v in mon),'Target-two forward use'
    assert variables==set(range(219)) and rows==set(range(203)),'Target-two declaration coverage'
    assert all(v in variables for call in candidate['calls'] for v in call['args']),'Target-two call coverage'
    return dict(locals=218,rows=203,calls=39,raw_variable_delta=-126,raw_row_delta=-126)


def check_comparison(base,parent,candidate):
    base.exact(candidate,expected_comparison(base,parent),'Complete target-two comparison mismatch')
    return dict(name=parent['name'],target_multiplier=2)


def check_modules(base,parents,candidates):
    assert set(parents)==set(base.PINS) and set(candidates)==set(base.PINS),'Target-two four-module scope'
    root=check_root(base,parents['Z_definition'],candidates['Z_definition'])
    modes=[check_comparison(base,parents[n],candidates[n]) for n in base.PINS if n!='Z_definition']
    return dict(status='PASS: LITERAL TARGET-TWO SOURCE DELTA',root=root,comparisons=modes,complete_source_acceptance=False)
