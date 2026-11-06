"""Independent audit of the three-mode rational-difference source."""
import argparse,ast,copy,hashlib,importlib.util,json,time
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
CORE_SHA='0da0dfef661211fd4ada262050895ef24ca54dfdc1aca4aa4bec4e69c1dcbce8'
JACOBI_AUDIT_SHA='105f4cc79a85649041e95be4a9059ed93e1d296fb77e0937e612f54aa801bb33'
CONIC_AUDIT_SHA='446ff0fb520d3922d1a3c96455dd4fade07206dbed5357dcc38700ce6eb2e0ce'
ANCHOR_AUDIT_SHA='0e5f93f61114f9bd6589dc950271938b5d630820a920565043f63ab749081e30'
POLE_HELPERS={'audit_conic_pole.py': '35b774437705759c2309aa905cf8f2d1fd91c19669dc35b1489b8a466db36bff', 'check_conic_pole.py': 'd0e11d3fa4405eff7012bee7e112f74a6eda528382ebb14ca5433982fa4e4933', 'audit_linear_pole.py': '956d1f3f5d6e38248fde0edbedbf3c2ef5a175f89ac8770bb711a1490742ff9a', 'spec_linear.py': '86789c5fd288d2c739659b1f15779d9c81599f84d54c14d7d26f17efe083603b', 'audit_root_shared.py': '50add2b9cd294e86f91c45cc373b4433807a464a4a4cb7c8934688d0a623c281', 'audit_root_rewrite.py': '05fa04d6016212cdfde1613ce3c265f984cfa6f4adcc48737e714269dbbb01b2', 'audit_shared_square.py': '2e7498a05baad8996341ce7c87c839683a6f196a2682167a731fd329f9101fba', 'SELECTED_PARENT.json': '248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0', 'audit_target2.py': 'b2737e3575ad8512dcc33c6c1d84f38178172e53b5d786193d8eed5c1df886c3', 'probe_tangents.py': '75299d5a1118dd7d75892786079003cd8588dc0b814017ae33c82672d00b80b0', 'audit_first_norm.py': '5e13e16621f5de043a5bb63d069f91fbab7b6284e19c4f077b093746efa2a2a5'}
POSITIONS=list(range(5,13));SELECTION=[0,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30]
ORDERS=[1]*3+[12]*3
LUCAS_POSITIONS=list(range(13,21))+list(range(29,37))
LUCAS_SELECTION=[1,2,3,4,5,6,7]+list(range(12,31))
LUCAS_ORDERS=[1]*5+[40]*5
FULL_POSITIONS=list(range(5))+list(range(21,29))
MODULES=('Z_definition','q_anchor','q_height_batch','q_primeparity','q_compare4','q_conic13','q_compare_beta','q_conic6','q_compare_lucas','q_conic10','q_linearnormalpole')
def core():
    path=HERE/'core_audit.py';assert hashlib.sha256(path.read_bytes()).hexdigest()==CORE_SHA
    spec=importlib.util.spec_from_file_location('selective_core_auditor',path);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);return c
def baseline(c,path):
    pins=c.load(HERE/'BASELINE.json')
    for name,digest in pins['files'].items():assert c.file_sha256(path/name)==digest,('baseline pin',name)
    return pins,{name:c.load(path/'modules'/(name+'.json')) for name in pins['modules']}
def flatten(c,source,modules):
    # Reuse the exact hash-pinned independent generic flattening code. Only
    # its final expected module-instance counts change for this new source.
    code=(HERE/'core_audit.py').read_text(encoding='utf-8');tree=ast.parse(code)
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='flatten_and_check')
    body=ast.get_source_segment(code,node)
    old="assert visits_by_module == {'Z_definition':1, 'q_anchor':1, 'q_height_batch':1,\n                               'q_compare4':37, 'q_batch41':37, 'q_primeparity':38}"
    new="assert visits_by_module == {'Z_definition':1, 'q_anchor':1, 'q_height_batch':1, 'q_compare4':13, 'q_conic13':13, 'q_compare_beta':8, 'q_conic6':8, 'q_compare_lucas':16, 'q_conic10':16, 'q_primeparity':1, 'q_linearnormalpole':37}"
    assert body.count(old)==1
    ns=dict(c.__dict__);exec(compile(body.replace(old,new),'<selective-independent-flatten>','exec'),ns)
    body2=body.replace(old,new)
    marker='anchor_squarings=squarings, chart=10'
    assert body2.count(marker)==1
    exec(compile(body2.replace(marker,"anchor_squarings=squarings, chart='general_E_mixed'"),'<root-shared-independent-flatten>','exec'),ns)
    return ns['flatten_and_check'](source,modules,40)
def check(c,source,base):
    pins,old=baseline(c,base);contract=c.load(source/'CONIC_SOURCE.json')
    expected=dict(source_family='H19-root37-target2-tangent-first-norm-normalized-linear-pole-v1',arithmetic_acceptance=False,source_pin_authorized=False,
      comparison_target_multiplier=2,final_root_chart='general_E_mixed',root_index_semantics='2Q=n_Q Pstar, n_Q integer',
      root_doubling_model='direct tangent with retained square coordinates',direct_tangent_doublings=4,
      first_norm_field_role='H.f',first_norm_field_order=1,first_norm_instances=37,
      first_norm_virtual_denominator_exponent=1,first_norm_arithmetic_change=True,conic_norm_fields=340,
      root_beta_comparison_scale=2,shared_square_fields=37,conic_evaluations=340,old_gpoint_rewrite_instances=0,
      selected_parent_pins_sha256='248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0',
      root_shared_contract_sha256='73e17ecc19a797ce442412549931ff11e43f42ebff9c48e1b2c636ff2d839a8c',
      high=40,label=12,anchor_squarings=25,scalar_orders=[1,1,1,1,32,32],height_exponent=19,
      beta_only_positions=POSITIONS,lucas_only_positions=LUCAS_POSITIONS,full_positions=FULL_POSITIONS,
      beta_input_selection=SELECTION,beta_field_orders=ORDERS,
      lucas_input_selection=LUCAS_SELECTION,lucas_field_orders=LUCAS_ORDERS,
      full_field_orders=[1]*6+[12,40]+[40,12,40,40,40],
      difference_model='joint f,p,A,K curve and complete z graph; no difference formal tests',
      primary_square_transfer=False,x_squareclass_membership=False,jacobi_primary_pair_count=145,
      private_index_group='(1/2)Z via doubling',difference_formal_tests=False,rational_difference_four_fields=False,joint_primary_difference_chart=True,
      comparison_norm='private conic field norm v1',private_conics=37,conic_field_nodes=377,
      conic_batch_modules={'q_compare4':'q_conic13','q_compare_beta':'q_conic6','q_compare_lucas':'q_conic10'},
      global_root_error_retained_but_unused=True,comparison_contact_inverse_emitted=False,
      anchor_private_coordinates=4,anchor_residuals=2,
      ordinary_pole_module='q_linearnormalpole',ordinary_pole_instances=37,height_parity_instances=1,
      ordinary_pole_input_layout=['r','theta','W'],ordinary_pole_private_coordinates=10,ordinary_pole_residuals=8,
      linear_pole_contract_sha256='19c3f7d65aae9f38aeaea9cc9c079d0ec7ca9918123d96d1744813ae81e61869',
      ordinary_pole_soundness='negative odd exclusion; no full Psi projection',
      ordinary_pole_full_Psi_projection=False,
      ordinary_pole_parent_manifest='07ded5a9a1fb0dcdd2e0f1e0930268841fcdc79bf4b1335189a952fef024963b',
      inherited_pole_contract_scope='preservation pins and reference audit only; pole arithmetic superseded',
      normalized_pole_contract_sha256='0ad8288dd3a44daa524e753dfba04b0b788de46d84bfa63d3f34a71d3272dd10',
      anchor_encoding='homogeneous trace 9+3(a^2+b^2) in S_2_3',
      joint_contract_sha256='e658843c6ba95dc797f10e7c25c086189f9694a0689a88c203979c38f05ed79e',
      joint_chart_contract_sha256='1793c7bdf798365247f04100d22c30490fa8e7e0df4f80534aaec8e2e775ffb3',
      comparison_free_counts={'q_compare4':58,'q_compare_beta':28,'q_compare_lucas':47},
      comparison_legacy_counts={'q_compare4':28,'q_compare_beta':16,'q_compare_lucas':23},
      joint_chart_extra_target_coordinates=40,
      local_lucas_residual=True,global_lucas_proxies_removed=True,
      parent_unchanged_pins_sha256='003211cbd8995b9b251596d56411a2c51ca7121176ada686c22591f333f56bac',
      normalized_parent_pins_sha256='d94bf88c98b5c3e5110ed9ab58c587ba83a7cda17b736f1a0d9d226e0b415e59',
      normalized_lucas_residual=True,normalized_lucas_contract_sha256='b038a32f4b22de7a43680857dc693d5614d25c6d0f432841bbafd2a8577898d6',
      normalized_lucas_addon_sha256='af365079cce1bd502dc2d683fc1f76fa2a2ca85c396c22be888dbd9fb3237cb0',
      normalized_lucas_formula='F(C_s,C_t,C_z)/C_s^2',normalized_lucas_occurrences=29,
      normalized_global_nonzero_scope='Lambda,B_s,B_t,B_z,p_H,p_t; all numerator p_i locally at consumed primes',
      normalized_lucas_proof_sha256='e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811',
      removed_comparison_proxy_slots={'q_compare4':[1,2,3],'q_compare_beta':[],'q_compare_lucas':[0,1,2]},
      local_lucas_source_contract_sha256='233ea7424864fb0d828346cfbfe29459cbc09e801d3d5cd327675b5ea3d95ad8',
      local_lucas_typed_addon_sha256='13ebcdd31363e8d482a8daac988da75ac314d66a1d989926e39bdf01d4418048',
      baseline_source_id=pins['source_id'],baseline_source_sha256=pins['source_sha256'],baseline_module_sha256=pins['modules'],
      scope='New arithmetic source requiring the general-root, direct-tangent, shared-square, first-norm arithmetic, normalized-Lucas, private-conic, linear-unit pole and anchor4 proofs; no old-source projection equivalence asserted')
    assert set(contract)==set(expected)|{'compiler_sha256'}
    for k,v in expected.items():assert type(contract[k]) is type(v) and contract[k]==v,('contract',k)
    compilers=contract['compiler_sha256'];assert set(compilers)=={'archive_build.py','combined_kernel.py','lowprecision_kernel.py','build_source.py','beta_kernel.py','rational_difference.py','joint_chart.py','local_lucas.py','normalized_lucas.py','conic_lucas.py','anchor_four_kernel.py','linear_pole_kernel.py','emit_linear.py','target2_rewrite.py','compress_doublings.py','shared_square.py','first_norm.py'}
    for name,digest in compilers.items():
        assert c.file_sha256(source/'compiler'/name)==digest
        if 'compiler/'+name in pins['files']:assert digest==pins['files']['compiler/'+name]
    assert {p.stem for p in (source/'modules').glob('*.json')}==set(MODULES)
    modules={name:c.load(source/'modules'/(name+'.json')) for name in MODULES}
    helper=HERE/'audit_normalized_lucas.py';assert c.file_sha256(helper)==JACOBI_AUDIT_SHA
    spec=importlib.util.spec_from_file_location('independent_minimal_jacobi_audit',helper)
    jacobi=importlib.util.module_from_spec(spec);spec.loader.exec_module(jacobi)
    anchor_path=HERE/'check_anchor_four.py';assert c.file_sha256(anchor_path)==ANCHOR_AUDIT_SHA
    anchor_spec=importlib.util.spec_from_file_location('independent_anchor_audit',anchor_path)
    anchor=importlib.util.module_from_spec(anchor_spec);anchor_spec.loader.exec_module(anchor)
    conic_path=HERE/'check_lucas_batch.py';assert c.file_sha256(conic_path)==CONIC_AUDIT_SHA
    conic_spec=importlib.util.spec_from_file_location('independent_conic_batch_audit',conic_path)
    conic=importlib.util.module_from_spec(conic_spec);conic_spec.loader.exec_module(conic)
    for name,pin in POLE_HELPERS.items():assert c.file_sha256(HERE/name)==pin,('Pole helper pin',name)
    from audit_root_shared import check_modules
    module_report=check_modules(c,modules,old,jacobi,conic,anchor)
    counts,visits=flatten(c,source,modules)
    residual='residuals.jsonl' if (source/'residuals.jsonl').exists() else 'residuals.jsonl.gz'
    assert c.file_sha256(source/'JOINT_SOURCE_CONTRACT.json')==expected['joint_contract_sha256']
    assert c.file_sha256(source/'JOINT_CHART_CONTRACT_ADDON.json')==expected['joint_chart_contract_sha256']
    assert c.file_sha256(source/'LOCAL_LUCAS_SOURCE_CONTRACT.json')==expected['local_lucas_source_contract_sha256']
    assert c.file_sha256(source/'LOCAL_LUCAS_CONTRACT_ADDON.json')==expected['local_lucas_typed_addon_sha256']
    assert c.file_sha256(source/'NORMALIZED_SOURCE_CONTRACT.json')==expected['normalized_lucas_contract_sha256']
    assert c.file_sha256(source/'NORMALIZED_LUCAS_CONTRACT_ADDON.json')==expected['normalized_lucas_addon_sha256']
    assert c.file_sha256(source/'PARENT_SOURCE_PINS.json')==expected['parent_unchanged_pins_sha256']
    parent_pins=c.load(source/'PARENT_SOURCE_PINS.json')
    addon=c.load(source/'NORMALIZED_LUCAS_CONTRACT_ADDON.json')
    assert parent_pins['parent_source_id']==addon['parent_source_id']
    assert parent_pins['parent_source_sha256']==addon['parent_source_sha256']
    unchanged={'shared.json'}|{'modules/'+n+'.json' for n in ('Z_definition','q_compare_beta','q_height_batch','q_primeparity','q_anchor')}
    assert set(parent_pins['files'])==unchanged
    for name,pin in parent_pins['files'].items():
        if name in {'shared.json','modules/q_anchor.json','modules/q_height_batch.json','modules/q_primeparity.json'}:assert c.file_sha256(source/name)==pin,('Changed inherited file',name)
    assert c.file_sha256(source/'NORMALIZED_POLE_CONTRACT.json')==expected['normalized_pole_contract_sha256']
    assert c.file_sha256(source/'NORMALIZED_PARENT_PINS.json')==expected['normalized_parent_pins_sha256']
    normalized_pins=c.load(source/'NORMALIZED_PARENT_PINS.json')
    assert set(normalized_pins['files'])=={'modules/q_compare4.json','modules/q_compare_lucas.json'}
    selected=c.load(source/'SELECTED_PARENT.json')
    for name,pin in normalized_pins['files'].items():assert selected['files'][name]==pin,('Historical comparator pin mismatch',name)
    composition=c.load(source/'NORMALIZED_POLE_CONTRACT.json')
    assert normalized_pins['packet_manifest_sha256']==composition['parent_normalized_packet_manifest_sha256']
    assert parent_pins['files']==composition['preserved_file_pins']
    assert parent_pins['superseded_files_sha256']==composition['reference_old_batch_pins']
    assert parent_pins['inherited_pins_sha256']==composition['parent_pin_record_sha256']
    assert set(composition['provenance_pole_contracts'])=={'CONIC_POLE_CONTRACT_ADDON.json','LOCAL_LUCAS_POLE_CONTRACT.json'}
    for name,pin in composition['provenance_pole_contracts'].items():assert c.file_sha256(source/name)==pin
    assert c.file_sha256(source/'NORMALIZED10_CONTRACT.json')==expected['linear_pole_contract_sha256']
    assert c.file_sha256(source/'SELECTED_PARENT.json')==expected['selected_parent_pins_sha256']
    assert c.file_sha256(source/'ROOT_SHARED_CONTRACT.json')==expected['root_shared_contract_sha256']
    revised=c.load(source/'ROOT_SHARED_CONTRACT.json')
    assert c.file_sha256(source/'FIRST_NORM_CONTRACT.json')==revised['first_norm_contract_sha256']
    assert c.file_sha256(source/'FIRST_NORM_PROOF.md')==revised['first_norm_proof_sha256']
    assert c.file_sha256(source/'MIXED_MODE_DENOMINATOR_CLARIFICATION.md')==revised['mixed_mode_clarification_sha256']
    assert c.file_sha256(source/'TANGENT_SOURCE_CONTRACT.json')==revised['tangent_contract_sha256']
    assert c.file_sha256(source/'TANGENT_PROOF.md')==revised['tangent_proof_sha256']
    assert c.file_sha256(HERE/'probe_tangents.py')==revised['tangent_transition_checker_sha256']
    assert c.file_sha256(source/'TARGET_TWO_PROOF.md')==revised['target_two_proof_sha256']
    assert c.file_sha256(source/'TARGET_TWO_CONTRACT.md')==revised['target_two_source_contract_sha256']
    assert c.file_sha256(source/'TARGET_TWO_SOURCE_CONTRACT.json')==revised['target_two_machine_contract_sha256']
    assert c.file_sha256(source/'TARGET2_COMPOSITION_CONTRACT.json')==revised['target_two_typed_contract_sha256']
    for filename,key in [('ROOT_SOURCE_CONTRACT.json','root_contract_sha256'),('ROOT_COMPOSITION_CONTRACT.json','root_composition_contract_sha256'),('SHARED_SQUARE_CONTRACT.json','shared_square_contract_sha256')]:
        assert c.file_sha256(source/filename)==revised[key]
    assert c.file_sha256(source/'modules/q_linearnormalpole.json')==selected['files']['modules/q_linearnormalpole.json']
    names=['SELECTED_PARENT.json','ROOT_SHARED_CONTRACT.json','FIRST_NORM_CONTRACT.json','FIRST_NORM_PROOF.md','MIXED_MODE_DENOMINATOR_CLARIFICATION.md','TANGENT_SOURCE_CONTRACT.json','TANGENT_PROOF.md','TARGET_TWO_PROOF.md','TARGET_TWO_CONTRACT.md','TARGET_TWO_SOURCE_CONTRACT.json','TARGET2_COMPOSITION_CONTRACT.json','ROOT_SOURCE_CONTRACT.json','ROOT_COMPOSITION_CONTRACT.json','SHARED_SQUARE_CONTRACT.json','NORMALIZED10_CONTRACT.json','NORMALIZED_PARENT_PINS.json','CONIC_POLE_CONTRACT_ADDON.json','LOCAL_LUCAS_POLE_CONTRACT.json','NORMALIZED_POLE_CONTRACT.json','PARENT_SOURCE_PINS.json','NORMALIZED_SOURCE_CONTRACT.json','NORMALIZED_LUCAS_CONTRACT_ADDON.json','LOCAL_LUCAS_SOURCE_CONTRACT.json','LOCAL_LUCAS_CONTRACT_ADDON.json','JOINT_CHART_CONTRACT_ADDON.json','JOINT_SOURCE_CONTRACT.json','CONIC_SOURCE.json','counts.json','polynomial.json','shared.json',residual]
    if residual=='residuals.jsonl' and (source/'residuals.jsonl.gz').exists():names.append('residuals.jsonl.gz')
    names+=['modules/'+n+'.json' for n in MODULES]+['compiler/'+n for n in compilers]
    hashes={n:c.file_sha256(source/n) for n in sorted(names)}
    return dict(status='PASS: SOURCE CONSTRUCTION ONLY',source_pin_authorized=False,arithmetic_acceptance=False,
      high=40,label=12,compressed=True,counts=counts,jacobi_modules=module_report,inspected_files_sha256=hashes,source_residual_file=residual,
      construction_map_sha256=hashlib.sha256(c.construction_map_bytes(visits)).hexdigest(),
      checker_dependencies_sha256={'core_audit.py':CORE_SHA,'BASELINE.json':c.file_sha256(HERE/'BASELINE.json'),'audit_normalized_lucas.py':JACOBI_AUDIT_SHA,'check_lucas_batch.py':CONIC_AUDIT_SHA,'check_anchor_four.py':ANCHOR_AUDIT_SHA,**POLE_HELPERS},
      not_established=['general-root, shared-square, normalized-Lucas, private-conic, linear-unit pole and anchor4 arithmetic theorem','source defines the integers','final quartic bound']),visits
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','baseline','report','map'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=int,default=180);a=p.parse_args();assert 1<=a.seconds<=600
    c=core();c.DEADLINE=time.monotonic()+a.seconds;report,visits=check(c,a.source,a.baseline)
    report['checker_sha256']=c.file_sha256(Path(__file__));a.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8');a.map.write_bytes(c.construction_map_bytes(visits));print(json.dumps(report))
if __name__=='__main__':main()
