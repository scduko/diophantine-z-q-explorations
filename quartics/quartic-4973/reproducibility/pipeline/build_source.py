"""Build the three-mode proposal from the exact measured high40 source."""
import argparse,hashlib,importlib.util,json,shutil,sys
from pathlib import Path
import beta_kernel
import rational_difference
import joint_chart
import local_lucas
import normalized_lucas
import conic_lucas
from copy import deepcopy
import anchor_four_kernel
import linear_pole_kernel
import target2_rewrite as root_rewrite
import shared_square
import compress_doublings
import first_norm
HERE=Path(__file__).resolve().parent
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def configure(b):
    b.CURVE_DROOT=(3,-1);b.CURVE_D2=(11,-6)
    b.BASE_POINT=((b.F(57,8),b.F(-7,2)),(b.F(-165,8),b.F(417,32)))
    b.CHART=10;b.PARITY=7;b.LOG_BLOCK=2;b.BASE_GATES=True;b.UNIT_SCALE=True
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--proxy-fixture',type=Path);a=p.parse_args()
    pins=json.loads((HERE/'BASELINE.json').read_bytes())
    for relative,pin in pins['files'].items():assert digest(a.baseline/relative)==pin,relative
    compiler=a.baseline/'compiler'
    def fresh(tag):
        b=load(compiler/'archive_build.py',tag+'_builder');configure(b)
        c=load(compiler/'combined_kernel.py',tag+'_combined');low=load(compiler/'lowprecision_kernel.py',tag+'_low')
        return b,c,low
    b,c,low=fresh('baseline');c.install(b,low.emit_g,high=40,label=12)
    b.write=lambda name,data:None
    b.make_parity();b.make_anchor();b.make_batch('q_batch41',[1]*23+[40]*18,'q_primeparity')
    b.make_batch('q_height_batch',[1]*4+[48]*2,'q_primeparity');b.make_multi_comparison();b.make_root()
    originals={name:json.loads((a.baseline/'modules'/(name+'.json')).read_bytes()) for name in pins['modules']}
    assert b.MODULES==originals,'Measured baseline modules did not regenerate exactly'
    b,c,low=fresh('selective');base_make_batch=b.make_batch;beta_kernel.install(b,c,low);rational_difference.install(b,c,low,base_make_batch);joint_chart.install(b,rational_difference,low,base_make_batch);local_lucas.install(b,rational_difference,low,base_make_batch);normalized_lucas.install(b,rational_difference,low,base_make_batch);conic_lucas.install(b);anchor_four_kernel.install(b);linear_pole_kernel.install(b)
    captured=[];old_removal=local_lucas.remove_root_proxies
    def removal(builder,obj):
        captured.append(deepcopy(obj));return old_removal(builder,obj)
    local_lucas.remove_root_proxies=removal
    if a.proxy_fixture:
        assert not a.proxy_fixture.resolve().is_relative_to(a.out.resolve())
        assert not a.proxy_fixture.exists()
    a.out.mkdir(parents=True,exist_ok=False)
    sys.argv=[str(compiler/'archive_build.py'),'--out',str(a.out.resolve()),'--chart','10','--parity','7','--base-gates','--unit-scale','--log-block','2']
    parent=json.loads((HERE/'SELECTED_PARENT.json').read_bytes())
    assert digest(HERE/'SELECTED_PARENT.json')=='248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0'
    flatten_parent=b.flatten
    def finalize_modules():
        assert set(b.MODULES)=={Path(name).stem for name in parent['files']}
        for name,pin in parent['files'].items():
            raw=(json.dumps(b.MODULES[Path(name).stem],separators=(',',':'))+'\n').encode('utf-8')
            assert hashlib.sha256(raw).hexdigest()==pin,('Regenerated parent module changed',name)
        updated,root_receipt=root_rewrite.postprocess_modules(b.MODULES)
        updated['Z_definition'],tangent_receipt=compress_doublings.rewrite_root(updated['Z_definition'])
        updated,square_receipt=shared_square.postprocess_modules(updated)
        updated,first_norm_receipt=first_norm.postprocess_modules(updated)
        b.MODULES=updated;b.CHART='general_E_mixed'
        for name,module in updated.items():b.write('modules/'+name+'.json',module)
        return flatten_parent()
    b.flatten=finalize_modules
    b.main()
    assert digest(HERE/'PARENT_SOURCE_PINS.json')=='003211cbd8995b9b251596d56411a2c51ca7121176ada686c22591f333f56bac'
    parent_pins=json.loads((HERE/'PARENT_SOURCE_PINS.json').read_bytes())
    for name,pin in parent_pins['files'].items():
        if name in {'shared.json','modules/q_anchor.json','modules/q_height_batch.json','modules/q_primeparity.json'}:assert digest(a.out/name)==pin,('Changed inherited file',name)
    assert digest(HERE/'NORMALIZED_PARENT_PINS.json')=='d94bf88c98b5c3e5110ed9ab58c587ba83a7cda17b736f1a0d9d226e0b415e59'
    normalized_pins=json.loads((HERE/'NORMALIZED_PARENT_PINS.json').read_bytes())
    for name,pin in normalized_pins['files'].items():assert parent['files'][name]==pin,('Historical comparator pin mismatch',name)
    assert len(captured)==1
    if a.proxy_fixture:a.proxy_fixture.write_text(json.dumps(captured[0],sort_keys=True,indent=2)+"\n",encoding="utf-8")
    for name in pins['modules']:
        if name not in ('Z_definition','q_compare4','q_batch41','q_anchor'):assert b.MODULES[name]==originals[name],name
    destination=a.out/'compiler';destination.mkdir();hashes={}
    for path in [compiler/'archive_build.py',compiler/'combined_kernel.py',compiler/'lowprecision_kernel.py',HERE/'beta_kernel.py',HERE/'rational_difference.py',HERE/'joint_chart.py',HERE/'local_lucas.py',HERE/'normalized_lucas.py',HERE/'conic_lucas.py',HERE/'anchor_four_kernel.py',HERE/'linear_pole_kernel.py',HERE/'emit_linear.py',HERE/'target2_rewrite.py',HERE/'compress_doublings.py',HERE/'shared_square.py',HERE/'first_norm.py',Path(__file__)]:
        shutil.copyfile(path,destination/path.name);hashes[path.name]=digest(path)
    contract=dict(source_family='H19-root37-target2-tangent-first-norm-normalized-linear-pole-v1',arithmetic_acceptance=False,source_pin_authorized=False,
      comparison_target_multiplier=2,final_root_chart='general_E_mixed',root_index_semantics='2Q=n_Q Pstar, n_Q integer',
      root_doubling_model='direct tangent with retained square coordinates',direct_tangent_doublings=4,
      first_norm_field_role='H.f',first_norm_field_order=1,first_norm_instances=37,
      first_norm_virtual_denominator_exponent=1,first_norm_arithmetic_change=True,conic_norm_fields=340,
      root_beta_comparison_scale=2,shared_square_fields=37,conic_evaluations=340,old_gpoint_rewrite_instances=0,
      selected_parent_pins_sha256='248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0',
      root_shared_contract_sha256='73e17ecc19a797ce442412549931ff11e43f42ebff9c48e1b2c636ff2d839a8c',
      high=40,label=12,anchor_squarings=25,scalar_orders=[1,1,1,1,32,32],height_exponent=19,
      beta_only_positions=beta_kernel.POSITIONS,lucas_only_positions=beta_kernel.LUCAS_POSITIONS,full_positions=beta_kernel.FULL_POSITIONS,
      beta_input_selection=beta_kernel.SELECTION,beta_field_orders=local_lucas.MODES['q_compare_beta']['orders'],
      lucas_input_selection=beta_kernel.LUCAS_SELECTION,lucas_field_orders=local_lucas.MODES['q_compare_lucas']['orders'],
      full_field_orders=local_lucas.MODES['q_compare4']['orders'],
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
      baseline_source_id=pins['source_id'],baseline_source_sha256=pins['source_sha256'],
      baseline_module_sha256=pins['modules'],compiler_sha256=hashes,
      scope='New arithmetic source requiring the general-root, direct-tangent, shared-square, first-norm arithmetic, normalized-Lucas, private-conic, linear-unit pole and anchor4 proofs; no old-source projection equivalence asserted')
    shutil.copyfile(HERE/'JOINT_SOURCE_CONTRACT.json',a.out/'JOINT_SOURCE_CONTRACT.json')
    shutil.copyfile(HERE/'JOINT_CHART_CONTRACT_ADDON.json',a.out/'JOINT_CHART_CONTRACT_ADDON.json')
    for name in ('SELECTED_PARENT.json','ROOT_SHARED_CONTRACT.json','FIRST_NORM_CONTRACT.json','FIRST_NORM_PROOF.md','MIXED_MODE_DENOMINATOR_CLARIFICATION.md','TANGENT_SOURCE_CONTRACT.json','TANGENT_PROOF.md','TARGET_TWO_PROOF.md','TARGET_TWO_CONTRACT.md','TARGET_TWO_SOURCE_CONTRACT.json','TARGET2_COMPOSITION_CONTRACT.json','ROOT_SOURCE_CONTRACT.json','ROOT_COMPOSITION_CONTRACT.json','SHARED_SQUARE_CONTRACT.json','LOCAL_LUCAS_SOURCE_CONTRACT.json','LOCAL_LUCAS_CONTRACT_ADDON.json','NORMALIZED_SOURCE_CONTRACT.json','NORMALIZED_LUCAS_CONTRACT_ADDON.json','PARENT_SOURCE_PINS.json','NORMALIZED10_CONTRACT.json','NORMALIZED_POLE_CONTRACT.json','NORMALIZED_PARENT_PINS.json','CONIC_POLE_CONTRACT_ADDON.json','LOCAL_LUCAS_POLE_CONTRACT.json'):
        shutil.copyfile(HERE/name,a.out/name)
    (a.out/'CONIC_SOURCE.json').write_text(json.dumps(contract,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(contract,indent=2))
if __name__=='__main__':main()
