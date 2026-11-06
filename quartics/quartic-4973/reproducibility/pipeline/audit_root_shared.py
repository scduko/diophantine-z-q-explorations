"""Full composed module audit against the exact measured normalized10 parent."""
if not __debug__:raise RuntimeError('Assertions required')
import json
from pathlib import Path
import audit_linear_pole
import audit_root_rewrite
import audit_target2
import probe_tangents
import audit_shared_square
import audit_first_norm

HERE=Path(__file__).resolve().parent
PARENT_PIN='248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0'

def same(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)

def parent_modules(c):
    c.tick();assert c.file_sha256(HERE/'SELECTED_PARENT.json')==PARENT_PIN
    pins=c.load(HERE/'SELECTED_PARENT.json');path=HERE/'parent'
    assert c.file_sha256(path/'source-entry.json')==pins['parent_source_entry_sha256']
    assert c.file_sha256(path/'source-audit.json')==pins['parent_source_audit_sha256']
    assert c.file_sha256(path/'construction-map.json')==pins['parent_construction_map_sha256']
    entry=c.load(path/'source-entry.json');audit=c.load(path/'source-audit.json')
    assert entry['source_id']==pins['parent_source_id']
    assert entry['source_sha256']==pins['parent_source_sha256']
    assert entry['uncompressed_sha256']==pins['parent_uncompressed_sha256']
    assert entry['source_audit_sha256']==pins['parent_source_audit_sha256']
    assert entry['construction_map_sha256']==pins['parent_construction_map_sha256']
    assert audit['status']=='PASS: SOURCE CONSTRUCTION ONLY'
    assert same(audit['counts'],entry['source_header'])
    result={}
    for name,pin in pins['files'].items():
        assert name.startswith('modules/') and name.endswith('.json')
        assert c.file_sha256(path/name)==pin==entry['inspected_files_sha256'][name]
        result[Path(name).stem]=c.load(path/name)
    assert set(result)=={'Z_definition','q_anchor','q_height_batch','q_primeparity',
        'q_compare4','q_compare_beta','q_compare_lucas','q_conic13','q_conic6','q_conic10','q_linearnormalpole'}
    c.tick();return result

def check_parent_modules(c,modules,old,joint,conic,anchor):
    parents=parent_modules(c)
    # The archived receipt is provenance. Recheck every parent module's
    # semantics through the original independent module specification.
    parent_report=audit_linear_pole.check_modules(c,parents,old,joint,conic,anchor)
    def root_parent_check(restored):
        c.tick();assert set(restored)==set(parents),'Root/shared module set'
        names=set(audit_root_rewrite.PINS)
        expected=audit_target2.expected_root(audit_root_rewrite,parents['Z_definition'])
        root_report=probe_tangents.audit_root_transition(expected,restored['Z_definition'])
        for name in names-{'Z_definition'}:
            audit_target2.check_comparison(audit_root_rewrite,parents[name],restored[name])
        for name in set(parents)-names:
            assert same(restored[name],parents[name]),('Unexpected change outside root rewrite',name)
        c.tick();return root_report
    result=audit_shared_square.check_modules(modules,root_parent_check)
    c.tick();return dict(parent=parent_report,root_shared=result,source_pin_authorized=False)


def check_modules(c,modules,old,joint,conic,anchor):
    def parent_check(restored):
        return check_parent_modules(c,restored,old,joint,conic,anchor)
    c.tick();result=audit_first_norm.check_modules(modules,parent_check);c.tick()
    return result
