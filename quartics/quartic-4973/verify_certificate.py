"""Independent exact checker for a quartic projection-preserving certificate.

Only the Python standard library is required. No search/producer code is imported.
This checks algebraic equivalence to the pinned source residual system, not the
arithmetic theorem asserting that the source system defines the integers.
"""
import argparse,gzip,hashlib,itertools,json,math,time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

if not __debug__:raise RuntimeError('Do not disable the checks with python -O.')
SOURCE_ENTRIES = {'original64': {'source_sha256': '6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2', 'source_variables': 15672, 'source_rows': 15107}, 'target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-4a82d9a8dc1b': {'source_id': 'target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-4a82d9a8dc1b', 'source_sha256': '94f8a1972cbfc0cf6493d418e628a18482307dec5c427db72e86d3eacb1a6f5d', 'uncompressed_sha256': '4a82d9a8dc1b5c92eb40a49751c0a6aae073c8f765ca5e276a74802fd56b84be', 'source_variables': 4935, 'source_rows': 4513, 'source_header': {'witnesses': 4934, 'residuals': 4513, 'degree': 8, 'modules': {'q_anchor': [4, 2], 'q_primeparity': [7, 4], 'q_height_batch': [33, 30], 'q_linearnormalpole': [10, 8], 'q_conic13': [62, 59], 'q_compare4': [159, 146], 'q_conic6': [35, 32], 'q_compare_beta': [62, 55], 'q_conic10': [49, 46], 'q_compare_lucas': [131, 120], 'Z_definition': [4908, 4487]}, 'stored_residuals': 560, 'stored_calls': 46, 'anchor_squarings': 25, 'chart': 'general_E_mixed', 'prime_parity_witnesses': 7, 'unit_scale': True, 'base_gates': True, 'curve_droot': [3, -1], 'curve_d2': [11, -6], 'log_block': 2}, 'source_audit_sha256': 'e4b93b2da1babcdc3fcf4a63123fd813143d559358fdf4c76f3880733977333f', 'source_audit_checker_sha256': '58bf1da4007247bc4558eacce6bdbbc83d2394ac2a47f128390f20f26567d50a', 'construction_map_sha256': '3d1e002eee34f4917605da1ddc7227e43bfaf4a5044d30d9a77f50fabc7380d2', 'inspected_files_sha256': {'CONIC_POLE_CONTRACT_ADDON.json': '44bcef6a37f57a847f963313b146614b56ecf3fdb101e5443c2c65321494e4a4', 'CONIC_SOURCE.json': '0a0df805b2e0b2d7102278c4b20a8d584249c7f8b203fe9acd745bf76d4dcabc', 'FIRST_NORM_CONTRACT.json': 'b327fcc99625f09c36509c6b22cb12edc4fdeb40c2f8a7b70f65f2509c75570c', 'FIRST_NORM_PROOF.md': 'b18b32854d4ef6e8c49495ce404f7c96566a0a1926baca6f4ee1ed4cbedcba05', 'JOINT_CHART_CONTRACT_ADDON.json': '1793c7bdf798365247f04100d22c30490fa8e7e0df4f80534aaec8e2e775ffb3', 'JOINT_SOURCE_CONTRACT.json': 'e658843c6ba95dc797f10e7c25c086189f9694a0689a88c203979c38f05ed79e', 'LOCAL_LUCAS_CONTRACT_ADDON.json': '13ebcdd31363e8d482a8daac988da75ac314d66a1d989926e39bdf01d4418048', 'LOCAL_LUCAS_POLE_CONTRACT.json': 'cd7e4039c533eed79afd75fea9ba6abb53f10b7a26ea990b195b9f2c15badd8b', 'LOCAL_LUCAS_SOURCE_CONTRACT.json': '233ea7424864fb0d828346cfbfe29459cbc09e801d3d5cd327675b5ea3d95ad8', 'MIXED_MODE_DENOMINATOR_CLARIFICATION.md': '2a1eb8ed9a7175995afa665a08035728c1714b5fa30e1ba52030b6adf7b8ba34', 'NORMALIZED10_CONTRACT.json': '19c3f7d65aae9f38aeaea9cc9c079d0ec7ca9918123d96d1744813ae81e61869', 'NORMALIZED_LUCAS_CONTRACT_ADDON.json': 'af365079cce1bd502dc2d683fc1f76fa2a2ca85c396c22be888dbd9fb3237cb0', 'NORMALIZED_PARENT_PINS.json': 'd94bf88c98b5c3e5110ed9ab58c587ba83a7cda17b736f1a0d9d226e0b415e59', 'NORMALIZED_POLE_CONTRACT.json': '0ad8288dd3a44daa524e753dfba04b0b788de46d84bfa63d3f34a71d3272dd10', 'NORMALIZED_SOURCE_CONTRACT.json': 'b038a32f4b22de7a43680857dc693d5614d25c6d0f432841bbafd2a8577898d6', 'PARENT_SOURCE_PINS.json': '003211cbd8995b9b251596d56411a2c51ca7121176ada686c22591f333f56bac', 'ROOT_COMPOSITION_CONTRACT.json': '4e41f830938c3bdf8b5361b410a2fb639bd74299f0461fb356afe2efb012f2b7', 'ROOT_SHARED_CONTRACT.json': '73e17ecc19a797ce442412549931ff11e43f42ebff9c48e1b2c636ff2d839a8c', 'ROOT_SOURCE_CONTRACT.json': '505b3a743585187ebde58642bb02237dbb45bc55b328b5b88bd84a0724cf1d5c', 'SELECTED_PARENT.json': '248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0', 'SHARED_SQUARE_CONTRACT.json': '13f97f687a15f1d0bf283b608c8c00b425c2c4797eb9b4dc0df14fa2a93c3750', 'TANGENT_PROOF.md': '3591709058c666a1dd2786d46039b408a04f1908b644c16c6f722a72788a50c8', 'TANGENT_SOURCE_CONTRACT.json': 'd9ef1fedd0703377747353f44619d73eca47c160634757de7c477fc02c887e70', 'TARGET2_COMPOSITION_CONTRACT.json': '77e26c27804a00701306c115984df84129e26431ff285468a8e8f14cd8b217dd', 'TARGET_TWO_CONTRACT.md': '8e42299e4d281ecab724868d39eeb21589957c971516296500b942605ac0b711', 'TARGET_TWO_PROOF.md': 'cfc62097ffdbf072fe77524f7e0448356812712689394ca22dfc4a0fd64b7feb', 'TARGET_TWO_SOURCE_CONTRACT.json': '510ee91c4777c4e8ae4343622817b90e30a20e7507ec83fa7a26bc8b50d581c7', 'compiler/anchor_four_kernel.py': '4f5944cfe3dd16f5a38ab7113e54a5ecba1faccfecac0d23b7c2f36b76a00dcb', 'compiler/archive_build.py': 'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912', 'compiler/beta_kernel.py': '38f5524c9e87a9a7baea0e83b78a77c0f7e32230f52cbe1e3270806094d8c1e5', 'compiler/build_source.py': '2f973408d8f022fdf178606bc42a6ce41ec68aa0272b0e7186df2e5fff00bd61', 'compiler/combined_kernel.py': 'f41dc82a5dd451b3196bd20f46c14bb5a2ace4a29d6d22bc898725f1eba6e9f5', 'compiler/compress_doublings.py': 'a136e6cce43277ed63351fd1989c428c48b811b9a8682d213f6609d6a95f5cb2', 'compiler/conic_lucas.py': '42fcb55ec95be9ee34e98c5d0b0e672062b7cce6c5f9f9d0e676edff72e5ed86', 'compiler/emit_linear.py': '19e7dc5b5516674dc972aa4b1e15c6b10725192d3f5e8bf48419dbdb93446878', 'compiler/first_norm.py': 'badaa92471df68d9250f77d8584fee0eecafd8641d3873ab0f8babbf0d1d7438', 'compiler/joint_chart.py': 'f6868d7fc6f6898388288d4f088966220158e888aa47def53cd21c599ef7ff85', 'compiler/linear_pole_kernel.py': '01622f4c3f126d2c6bb190c0a4f87e7a22d45546baee99a33837c6ba60e96f1d', 'compiler/local_lucas.py': 'fc85b3c3a8a307bfa7113dc163790092b13738baef7e7431e071f31730f2b280', 'compiler/lowprecision_kernel.py': '66854ff3ee24d8dd6f4b3b54fa5ca627d87b5d0da09cafa35e3d05d47d0d5c31', 'compiler/normalized_lucas.py': '3e1e420306de2fbe51c17aeb8f24169e23a9d74f47601262d3333360e7c7d921', 'compiler/rational_difference.py': 'be766e35b06d8f334c326dedfddc7c200d226a4c70af6a73fe66242aa4ccc898', 'compiler/shared_square.py': '5a4b325c86255beb9f6271b0638822656c31ce46b8fa67997629ecd3e8887c73', 'compiler/target2_rewrite.py': 'fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799', 'counts.json': '8125c7db12e018fcff85ff849d13f5b24a7323e25c94a11d905ec7be42c9ca72', 'modules/Z_definition.json': '221e5ee5b95d18081941dd4ecd6977990bb170e583b182b2fbe329726ab35d59', 'modules/q_anchor.json': '3edef11d7871866f6224bf9a6e4a6f2d99d5c8f535eef2d3c2c57f98a33f0f6f', 'modules/q_compare4.json': '32b774216d8404d4a046d64bff9d51280e83c6b63699012d20f852f90a3c1301', 'modules/q_compare_beta.json': 'c3f5f3895d805ae4027d53c437440bb9666ebc74e48e2c656dd8e27618b7781c', 'modules/q_compare_lucas.json': '418277c6d6f4187ed10cb721a219dd561d3580150fd3320384e9f1f1cac69cdb', 'modules/q_conic10.json': '1a72243de8cc0de56d9a1b90922bbb8637ba447f033999821ac5c4a74afefaf0', 'modules/q_conic13.json': '6c8ae40d31ac835612fc2ae980e27e6bc6338190e4f4282b14637d08782a52a5', 'modules/q_conic6.json': 'aff175c604c523f88741cf6a2024cfd1d06edbb8984f5edf591ed06cbc7deaed', 'modules/q_height_batch.json': '22e3074cafdc80a71d39baf69d2012a8b039533d665f85f76da7f889dfe25761', 'modules/q_linearnormalpole.json': 'b3f86d819e831eb6970ab4249cea9337a874a0adcdbc4bd13efef9678fba547d', 'modules/q_primeparity.json': 'df89176d00ab6cc61e86416c5d1209554fcf87f45f30a866177c76683c2a306a', 'polynomial.json': '1d644b27d173b2467576e404eba009345cc5f98cc43bba4a9936193c489190c1', 'residuals.jsonl': '4a82d9a8dc1b5c92eb40a49751c0a6aae073c8f765ca5e276a74802fd56b84be', 'shared.json': 'f879f79eb7e8072176c8204df4c07a0097a219b7c2452c7c09bd52ca04abe83e'}, 'high': 40, 'label': 12, 'compressed': True, 'source_layout_sha256': '50c518b1f7e5a69bda243c8b027c2ddd88193cd20d15b3f3ddcb4deffead1006', 'layout_counts': {'comparisons': 37, 'norm_guards': 0, 'uncompressed_charts': 0, 'parity': 1, 'batches': 37, 'batch_pairs': 0, 'conic_fields': 377, 'private_conics': 37, 'conic_poles': 37, 'conic_evaluations': 340, 'conic_first_numerators': 37, 'conic_norm_fields': 340}, 'proposal': {'anchor_encoding': 'homogeneous trace 9+3(a^2+b^2) in S_2_3', 'anchor_private_coordinates': 4, 'anchor_residuals': 2, 'anchor_squarings': 25, 'arithmetic_acceptance': False, 'baseline_module_sha256': {'Z_definition': '26b6b8674056bb3e7b4ba8ca75bd5b2b47cba7a58c1d84db78ba108a2f264117', 'q_anchor': 'e5b74df60328d739e94224f199efb16dd817c994658c95d5dd781704bcf94fb1', 'q_batch41': 'a45569adc62e09ce254b01cb38a3b31eb891842a73f515f21732eeeb24799985', 'q_compare4': 'ef3aba59c082b9dc312993cc5ea8d0298cc1c81b21e58d4762186bb9a53d4eb2', 'q_height_batch': '22e3074cafdc80a71d39baf69d2012a8b039533d665f85f76da7f889dfe25761', 'q_primeparity': 'df89176d00ab6cc61e86416c5d1209554fcf87f45f30a866177c76683c2a306a'}, 'baseline_source_id': 'combined-k40-beta12-a25-h19-s32-502e3ed250f7', 'baseline_source_sha256': '3bad8b614f1593ab84f068bb42e0b5e0bd6877fa6d315cc6f72f48d57b22df43', 'beta_field_orders': [1, 1, 1, 12, 12, 12], 'beta_input_selection': [0, 4, 5, 6, 7, 8, 9, 10, 11, 24, 25, 26, 27, 28, 29, 30], 'beta_only_positions': [5, 6, 7, 8, 9, 10, 11, 12], 'comparison_contact_inverse_emitted': False, 'comparison_free_counts': {'q_compare4': 58, 'q_compare_beta': 28, 'q_compare_lucas': 47}, 'comparison_legacy_counts': {'q_compare4': 28, 'q_compare_beta': 16, 'q_compare_lucas': 23}, 'comparison_norm': 'private conic field norm v1', 'comparison_target_multiplier': 2, 'compiler_sha256': {'anchor_four_kernel.py': '4f5944cfe3dd16f5a38ab7113e54a5ecba1faccfecac0d23b7c2f36b76a00dcb', 'archive_build.py': 'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912', 'beta_kernel.py': '38f5524c9e87a9a7baea0e83b78a77c0f7e32230f52cbe1e3270806094d8c1e5', 'build_source.py': '2f973408d8f022fdf178606bc42a6ce41ec68aa0272b0e7186df2e5fff00bd61', 'combined_kernel.py': 'f41dc82a5dd451b3196bd20f46c14bb5a2ace4a29d6d22bc898725f1eba6e9f5', 'compress_doublings.py': 'a136e6cce43277ed63351fd1989c428c48b811b9a8682d213f6609d6a95f5cb2', 'conic_lucas.py': '42fcb55ec95be9ee34e98c5d0b0e672062b7cce6c5f9f9d0e676edff72e5ed86', 'emit_linear.py': '19e7dc5b5516674dc972aa4b1e15c6b10725192d3f5e8bf48419dbdb93446878', 'first_norm.py': 'badaa92471df68d9250f77d8584fee0eecafd8641d3873ab0f8babbf0d1d7438', 'joint_chart.py': 'f6868d7fc6f6898388288d4f088966220158e888aa47def53cd21c599ef7ff85', 'linear_pole_kernel.py': '01622f4c3f126d2c6bb190c0a4f87e7a22d45546baee99a33837c6ba60e96f1d', 'local_lucas.py': 'fc85b3c3a8a307bfa7113dc163790092b13738baef7e7431e071f31730f2b280', 'lowprecision_kernel.py': '66854ff3ee24d8dd6f4b3b54fa5ca627d87b5d0da09cafa35e3d05d47d0d5c31', 'normalized_lucas.py': '3e1e420306de2fbe51c17aeb8f24169e23a9d74f47601262d3333360e7c7d921', 'rational_difference.py': 'be766e35b06d8f334c326dedfddc7c200d226a4c70af6a73fe66242aa4ccc898', 'shared_square.py': '5a4b325c86255beb9f6271b0638822656c31ce46b8fa67997629ecd3e8887c73', 'target2_rewrite.py': 'fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799'}, 'conic_batch_modules': {'q_compare4': 'q_conic13', 'q_compare_beta': 'q_conic6', 'q_compare_lucas': 'q_conic10'}, 'conic_evaluations': 340, 'conic_field_nodes': 377, 'conic_norm_fields': 340, 'difference_formal_tests': False, 'difference_model': 'joint f,p,A,K curve and complete z graph; no difference formal tests', 'direct_tangent_doublings': 4, 'final_root_chart': 'general_E_mixed', 'first_norm_arithmetic_change': True, 'first_norm_field_order': 1, 'first_norm_field_role': 'H.f', 'first_norm_instances': 37, 'first_norm_virtual_denominator_exponent': 1, 'full_field_orders': [1, 1, 1, 1, 1, 1, 12, 40, 40, 12, 40, 40, 40], 'full_positions': [0, 1, 2, 3, 4, 21, 22, 23, 24, 25, 26, 27, 28], 'global_lucas_proxies_removed': True, 'global_root_error_retained_but_unused': True, 'height_exponent': 19, 'height_parity_instances': 1, 'high': 40, 'inherited_pole_contract_scope': 'preservation pins and reference audit only; pole arithmetic superseded', 'jacobi_primary_pair_count': 145, 'joint_chart_contract_sha256': '1793c7bdf798365247f04100d22c30490fa8e7e0df4f80534aaec8e2e775ffb3', 'joint_chart_extra_target_coordinates': 40, 'joint_contract_sha256': 'e658843c6ba95dc797f10e7c25c086189f9694a0689a88c203979c38f05ed79e', 'joint_primary_difference_chart': True, 'label': 12, 'linear_pole_contract_sha256': '19c3f7d65aae9f38aeaea9cc9c079d0ec7ca9918123d96d1744813ae81e61869', 'local_lucas_residual': True, 'local_lucas_source_contract_sha256': '233ea7424864fb0d828346cfbfe29459cbc09e801d3d5cd327675b5ea3d95ad8', 'local_lucas_typed_addon_sha256': '13ebcdd31363e8d482a8daac988da75ac314d66a1d989926e39bdf01d4418048', 'lucas_field_orders': [1, 1, 1, 1, 1, 40, 40, 40, 40, 40], 'lucas_input_selection': [1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'lucas_only_positions': [13, 14, 15, 16, 17, 18, 19, 20, 29, 30, 31, 32, 33, 34, 35, 36], 'normalized_global_nonzero_scope': 'Lambda,B_s,B_t,B_z,p_H,p_t; all numerator p_i locally at consumed primes', 'normalized_lucas_addon_sha256': 'af365079cce1bd502dc2d683fc1f76fa2a2ca85c396c22be888dbd9fb3237cb0', 'normalized_lucas_contract_sha256': 'b038a32f4b22de7a43680857dc693d5614d25c6d0f432841bbafd2a8577898d6', 'normalized_lucas_formula': 'F(C_s,C_t,C_z)/C_s^2', 'normalized_lucas_occurrences': 29, 'normalized_lucas_proof_sha256': 'e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811', 'normalized_lucas_residual': True, 'normalized_parent_pins_sha256': 'd94bf88c98b5c3e5110ed9ab58c587ba83a7cda17b736f1a0d9d226e0b415e59', 'normalized_pole_contract_sha256': '0ad8288dd3a44daa524e753dfba04b0b788de46d84bfa63d3f34a71d3272dd10', 'old_gpoint_rewrite_instances': 0, 'ordinary_pole_full_Psi_projection': False, 'ordinary_pole_input_layout': ['r', 'theta', 'W'], 'ordinary_pole_instances': 37, 'ordinary_pole_module': 'q_linearnormalpole', 'ordinary_pole_parent_manifest': '07ded5a9a1fb0dcdd2e0f1e0930268841fcdc79bf4b1335189a952fef024963b', 'ordinary_pole_private_coordinates': 10, 'ordinary_pole_residuals': 8, 'ordinary_pole_soundness': 'negative odd exclusion; no full Psi projection', 'parent_unchanged_pins_sha256': '003211cbd8995b9b251596d56411a2c51ca7121176ada686c22591f333f56bac', 'primary_square_transfer': False, 'private_conics': 37, 'private_index_group': '(1/2)Z via doubling', 'rational_difference_four_fields': False, 'removed_comparison_proxy_slots': {'q_compare4': [1, 2, 3], 'q_compare_beta': [], 'q_compare_lucas': [0, 1, 2]}, 'root_beta_comparison_scale': 2, 'root_doubling_model': 'direct tangent with retained square coordinates', 'root_index_semantics': '2Q=n_Q Pstar, n_Q integer', 'root_shared_contract_sha256': '73e17ecc19a797ce442412549931ff11e43f42ebff9c48e1b2c636ff2d839a8c', 'scalar_orders': [1, 1, 1, 1, 32, 32], 'scope': 'New arithmetic source requiring the general-root, direct-tangent, shared-square, first-norm arithmetic, normalized-Lucas, private-conic, linear-unit pole and anchor4 proofs; no old-source projection equivalence asserted', 'selected_parent_pins_sha256': '248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0', 'shared_square_fields': 37, 'source_family': 'H19-root37-target2-tangent-first-norm-normalized-linear-pole-v1', 'source_pin_authorized': False, 'x_squareclass_membership': False}, 'arithmetic_status': 'EXPLORATORY SOURCE; arithmetic acceptance is outside this algebraic checker'}}

def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode('ascii')
def decode(terms):
    result={}
    for coefficient,variables in terms:
        assert type(coefficient) is int and coefficient!=0
        assert all(type(v) is int and v>=0 for v in variables)
        m=tuple(variables);assert m==tuple(sorted(m)) and m not in result
        result[m]=coefficient
    return result
def encode(row):return [[c,list(m)] for m,c in row.items()]
def add(*summands):
    result=defaultdict(Fraction)
    for scalar,poly in summands:
        for m,c in poly.items():result[m]+=scalar*c
    return {m:c for m,c in result.items() if c}
def mul(f,g):
    result=defaultdict(Fraction)
    for m,c in f.items():
        for n,d in g.items():result[tuple(sorted(m+n))]+=c*d
    return {m:c for m,c in result.items() if c}
def normal(row):
    if not row:return ()
    common=math.lcm(*(Fraction(c).denominator for c in row.values()))
    terms={m:int(c*common) for m,c in row.items() if c}
    divisor=math.gcd(*terms.values())
    if terms[min(terms)]<0:divisor=-divisor
    return tuple(sorted((m,c//divisor) for m,c in terms.items()))
def substitute(row,v,replacement):
    result={}
    for m,c in row.items():
        value={():Fraction(c)}
        for variable in m:value=mul(value,replacement if variable==v else {(variable,):1})
        result=add((1,result),(1,value))
    return result
def variables(row):return {v for m in row for v in m}

def expand_definitions(row,definitions):
    result={}
    for monomial,coefficient in row.items():
        term={():Fraction(coefficient)}
        for v in monomial:term=mul(term,definitions.get(v,{(v,):1}))
        result=add((1,result),(1,term))
    return result

def decode_affine(obj):
    denominator=obj['denominator']
    assert type(denominator) is int and denominator>0
    row=decode(obj['terms'])
    assert all(len(mon)<=1 for mon in row)
    return {m:Fraction(c,denominator) for m,c in row.items()}

def unit_scale_expected(rows,d,nextvar):
    """Use the rational nonsquareness proof in UNIT_SCALING.md, not a field axiom."""
    E,theta,proof=d['unit'],d['root'],d['root_row']
    assert all(type(v) is int and 0<v<nextvar for v in (E,theta)) and E!=theta
    assert type(proof) is int and 0<=proof<len(rows)
    assert normal(rows[proof])==normal({(E,):1,(theta,theta):-1,():2})
    pairs=d['weights'];weights={v:k for v,k in pairs}
    assert len(weights)==len(pairs) and weights
    assert all(type(v) is int and 0<v<nextvar and v not in (E,theta)
               and type(k) is int and 1<=k<=8 for v,k in pairs)
    replacements=defaultdict(dict);bridges=[];aliased=set()
    for v,a,consumers in d['aliases']:
        assert type(v) is int and weights.get(v)==1 and v not in aliased
        aliased.add(v)
        assert type(a) is int and a==nextvar;nextvar+=1
        assert consumers and len(consumers)==len(set(consumers))
        for j in consumers:
            assert type(j) is int and 0<=j<len(rows) and j!=proof
            assert v in variables(rows[j])
            replacements[j][v]=a
        bridges.append({(v,):1,tuple(sorted((E,a))):-1})
    expected={}
    for j,row in enumerate(rows):
        if not variables(row)&weights.keys():continue
        laurent=defaultdict(Fraction);aliases=replacements[j]
        for mon,c in row.items():
            exponent=0;other=[]
            for v in mon:
                if v==E:exponent+=1
                elif v in aliases:other.append(aliases[v])
                else:other.append(v);exponent-=weights.get(v,0)
            laurent[(tuple(sorted(other)),exponent)]+=c
        laurent={m:c for m,c in laurent.items() if c}
        least=min((power for (_,power) in laurent),default=0)
        transformed={tuple(sorted(mon+(E,)*(power-least))):c
                     for (mon,power),c in laurent.items()}
        assert all(len(mon)<=2 for mon in transformed),'Unit scaling exceeds quadratic degree'
        expected[j]=transformed
    assert proof not in expected
    for k,row in enumerate(bridges):expected[len(rows)+k]=row
    return expected,nextvar

def redundant_inverse_expected(rows,d,nextvar,incidence):
    """Discard a private inverse using R*H=E^2 and E=theta^2-2 != 0."""
    i,u=d['row'],d['inverse'];nz=d['nonzero']
    assert type(i) is int and 0<=i<len(rows)
    assert type(u) is int and 0<u<nextvar and incidence[u]=={i}
    assert nz['kind']=='root_error'
    j,k=nz['root_row'],nz['relation_row']
    assert all(type(n) is int and 0<=n<len(rows) for n in (j,k))
    assert len({i,j,k})==3
    R,theta,E,H=[decode_affine(obj) for obj in
                 (d['factor'],nz['root'],nz['error'],nz['cofactor'])]
    for form in (R,theta,E,H):
        assert all(v<nextvar and v!=u for v in variables(form))
    assert normal(rows[i])==normal(add((1,mul({(u,):1},R)),(-1,{():1})))
    assert normal(rows[j])==normal(add((1,E),(-1,mul(theta,theta)),(2,{():1})))
    assert normal(rows[k])==normal(add((1,mul(R,H)),(-1,mul(E,E))))
    return {i:{}}


_rules_chart={'__name__':'embedded_chart'}
exec(compile('"""Independent verifier for the seven-field-coordinate sparse 2E chart.\n\nThis file imports no producer code. See PROOF.md for the solution maps.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction\nfrom functools import reduce\nfrom math import gcd, lcm\n\n\ndef add(*terms):\n    answer = defaultdict(Fraction)\n    for scalar, polynomial in terms:\n        for monomial, coefficient in polynomial.items():\n            answer[monomial] += scalar * coefficient\n    return {m: c for m, c in answer.items() if c}\n\n\ndef multiply(left, right):\n    answer = defaultdict(Fraction)\n    for m, c in left.items():\n        for n, d in right.items():\n            answer[tuple(sorted(m + n))] += c * d\n    return {m: c for m, c in answer.items() if c}\n\n\ndef normalize(polynomial):\n    if not polynomial:\n        return ()\n    denominator = lcm(*(Fraction(c).denominator for c in polynomial.values()))\n    integer = {m: int(c * denominator) for m, c in polynomial.items()}\n    common = reduce(gcd, integer.values())\n    if integer[min(integer)] < 0:\n        common = -common\n    return tuple(sorted((m, c // common) for m, c in integer.items()))\n\n\ndef variables(polynomial):\n    return {v for m in polynomial for v in m}\n\n\ndef fadd(left, right, scalar=1):\n    return tuple(add((1, a), (scalar, b)) for a, b in zip(left, right))\n\n\ndef fmul(left, right):\n    a, b = left\n    c, d = right\n    return add((1, multiply(a, c)), (2, multiply(b, d))), add((1, multiply(a, d)), (1, multiply(b, c)))\n\n\ndef chart_expected(rows, data, nextvar, incidence):\n    """Return exact replacement rows and next unused variable, or reject."""\n    names = (\'u\', \'v\', \'w\', \'z\', \'f\', \'h\', \'x\', \'y\')\n    blocks = (\'f=u^2\', \'v2+df=1\', \'w2+v2=2\', \'h=vw\', \'zh+u=0\', \'xf=1\', \'yz+x=0\')\n    assert set(data) == {\'coordinates\', \'rows\', \'new_variables\', \'droot\'}\n    assert data[\'droot\'] == [3, -1], \'Unexpected pinned curve parameter\'\n    coordinates = data[\'coordinates\']\n    assert set(coordinates) == set(names)\n    old_variables = []\n    for name in names:\n        pair = coordinates[name]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(v) is int and 0 < v < nextvar for v in pair)\n        old_variables.extend(pair)\n    assert len(set(old_variables)) == 16, \'Aliased chart coordinates\'\n    row_ids = data[\'rows\']\n    assert set(row_ids) == set(blocks)\n    selected = []\n    for block in blocks:\n        pair = row_ids[block]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(i) is int and 0 <= i < len(rows) for i in pair)\n        selected.extend(pair)\n    assert len(set(selected)) == 14, \'Duplicate proof row\'\n    u, v, w, z, f, h, x, y = [tuple({(i,): 1} for i in coordinates[name]) for name in names]\n    one, two = ({(): 1}, {}), ({(): 2}, {})\n    droot, dsquare = ({(): 3}, {(): -1}), ({(): 11}, {(): -6})\n    old = (\n        fadd(f, fmul(u, u), -1),\n        fadd(fadd(fmul(v, v), fmul(droot, f)), one, -1),\n        fadd(fadd(fmul(w, w), fmul(v, v)), two, -1),\n        fadd(h, fmul(v, w), -1),\n        fadd(fmul(z, h), u),\n        fadd(fmul(x, f), one, -1),\n        fadd(fmul(y, z), x),\n    )\n    for block, pair in zip(blocks, old):\n        for index, expected in zip(row_ids[block], pair):\n            assert normalize(rows[index]) == normalize(expected), (\'Chart proof row differs\', block, index)\n    changed = set(row_ids[\'w2+v2=2\'] + row_ids[\'h=vw\'] + row_ids[\'zh+u=0\'])\n    removed = set(coordinates[\'w\'] + coordinates[\'h\'])\n    for v in removed:\n        assert incidence.get(v, set()) <= changed, (\'Removed chart coordinate used outside\', v)\n    fresh = data[\'new_variables\']\n    assert type(fresh) is list and len(fresh) == 2\n    assert all(type(v) is int for v in fresh)\n    assert fresh == [nextvar, nextvar + 1], \'Nonfresh p coordinate\'\n    p = tuple({(i,): 1} for i in fresh)\n    new = (fadd(p, fmul(y, f), -1), fadd(fadd(fmul(p, p), x, -1), fmul(dsquare, f)))\n    patches = {i: {} for i in changed}\n    for block, pair in zip((\'w2+v2=2\', \'h=vw\'), new):\n        for index, expected in zip(row_ids[block], pair):\n            assert all(len(m) <= 2 for m in expected)\n            assert not variables(expected) & removed\n            patches[index] = expected\n    return patches, nextvar + 2\n\n\ndef ordinate_expected(rows, data, nextvar, incidence):\n    """Eliminate y=x*p, using xf=1 to preserve the two chart relations."""\n    assert set(data) == {\'coordinates\', \'rows\'}\n    coordinates, row_ids = data[\'coordinates\'], data[\'rows\']\n    names = (\'x\', \'y\', \'z\', \'f\', \'p\')\n    blocks = (\'xf=1\', \'p=yf\', \'yz+x=0\')\n    assert set(coordinates) == set(names) and set(row_ids) == set(blocks)\n    flat = []\n    for name in names:\n        pair = coordinates[name]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(v) is int and 0 < v < nextvar for v in pair)\n        flat.extend(pair)\n    assert len(set(flat)) == 10, \'Aliased ordinate proof coordinates\'\n    indices = []\n    for block in blocks:\n        pair = row_ids[block]\n        assert type(pair) is list and len(pair) == 2\n        assert all(type(i) is int and 0 <= i < len(rows) for i in pair)\n        indices.extend(pair)\n    assert len(set(indices)) == 6, \'Duplicate ordinate proof row\'\n    x, y, z, f, p = [tuple({(i,): 1} for i in coordinates[name]) for name in names]\n    one = ({(): 1}, {})\n    old = (fadd(fmul(x, f), one, -1), fadd(p, fmul(y, f), -1), fadd(fmul(y, z), x))\n    for block, pair in zip(blocks, old):\n        for i, expected in zip(row_ids[block], pair):\n            assert normalize(rows[i]) == normalize(expected), (\'Ordinate proof row differs\', block, i)\n    removed = set(coordinates[\'y\'])\n    replacements = dict(zip(coordinates[\'y\'], fmul(x, p)))\n    affected = set().union(*(incidence.get(v, set()) for v in removed))\n    assert set(row_ids[\'p=yf\'] + row_ids[\'yz+x=0\']) <= affected\n    patches = {}\n    for i in affected:\n        if i in row_ids[\'p=yf\']:\n            patches[i] = {}\n            continue\n        if i in row_ids[\'yz+x=0\']:\n            k = row_ids[\'yz+x=0\'].index(i)\n            patches[i] = fadd(fmul(p, z), one)[k]\n            continue\n        replacement = {}\n        for monomial, coefficient in rows[i].items():\n            term = {(): coefficient}\n            for v in monomial:\n                term = multiply(term, replacements.get(v, {(v,): 1}))\n            replacement = add((1, replacement), (1, term))\n        assert all(len(m) <= 2 for m in replacement), \'Ordinate substitution exceeds quadratic degree\'\n        assert not variables(replacement) & removed\n        patches[i] = replacement\n    return patches, nextvar\n','<embedded-chart>','exec'),_rules_chart)
_rules_parity={'__name__':'embedded_parity'}
exec(compile('"""Independent checker for the exact q_primeparity conic replacement.\n\nNo producer or repository modules are imported. See PROOF.md for rational\nsolution maps, including both zero and exceptional-chart cases.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction as F\nfrom math import gcd, lcm\n\n\ndef add(*terms):\n    out = defaultdict(F)\n    for k, row in terms:\n        for mon, c in row.items():\n            out[mon] += k*c\n    return {m: c for m, c in out.items() if c}\n\n\ndef mul(left, right):\n    out = defaultdict(F)\n    for m, c in left.items():\n        for n, d in right.items():\n            out[tuple(sorted(m+n))] += c*d\n    return {m: c for m, c in out.items() if c}\n\n\ndef var(v):\n    return {(v,): F(1)}\n\n\ndef norm(row):\n    if not row:\n        return ()\n    den = lcm(*(F(c).denominator for c in row.values()))\n    ints = {m: int(c*den) for m, c in row.items() if c}\n    divisor = gcd(*ints.values())\n    if ints[min(ints)] < 0:\n        divisor = -divisor\n    return tuple(sorted((m, c//divisor) for m, c in ints.items()))\n\n\ndef variables(row):\n    return {v for m in row for v in m}\n\n\ndef expand(row, definitions):\n    result = {}\n    for mon, c in row.items():\n        term = {(): c}\n        for v in mon:\n            term = mul(term, definitions.get(v, var(v)))\n        result = add((1, result), (1, term))\n    return result\n\n\ndef source_rows(b, witnesses):\n    b = var(b)\n    t, u, e, p, q, s, h = map(var, witnesses)\n    tt, uu, ss = mul(t,t), mul(u,u), mul(s,s)\n    return [\n        add((1,u),(-1,b),(1,mul(mul(b,b),tt)),(1,mul(mul(b,u),tt))),\n        add((1,mul(p,p)),(-17,b),(-34,mul(b,e)),(51,mul(b,mul(e,e)))),\n        add((1,h),(-17,mul(b,e)),(1,mul(e,uu))),\n        add((17,mul(b,mul(q,q))),(-1,mul(ss,ss)),\n            (-34,mul(mul(b,h),ss)),(867,mul(mul(b,b),mul(h,h))))]\n\n\ndef replacement_rows(b, fresh):\n    b = var(b)\n    u,v,a,z,e,p,c,w,s,q,j,k = map(var, fresh)\n    return [\n        add((1,z),(-1,mul(u,u))),\n        add((1,a),(-1,mul(b,v))),\n        add((1,z),(1,mul(v,a)),(-1,mul(b,b))),\n        add((1,c),(-1,mul(b,e))),\n        add((1,mul(p,p)),(-17,b),(-34,c),(51,mul(e,c))),\n        add((1,w),(-17,mul(b,c)),(1,mul(c,z))),\n        add((1,j),(-1,mul(s,s))),\n        add((1,k),(-1,mul(b,q))),\n        add((1,mul(j,j)),(34,mul(j,w)),(-867,mul(w,w)),(-17,mul(q,k)))]\n\n\ndef check_rule(rows, incidence, data, nextvar):\n    """Return expected patches and new allocation count; fail closed."""\n    b = data[\'input\']\n    old = data[\'old_witnesses\']\n    ids = data[\'residual_rows\']\n    defs = data[\'definitions\']\n    new = data[\'new_variables\']\n    assert type(b) is int and 0 <= b < nextvar\n    assert len(old) == len(set(old)) == 7\n    assert all(type(v) is int and 0 < v < nextvar and v != b for v in old)\n    assert len(ids) == len(set(ids)) == 4\n    assert all(type(i) is int and 0 <= i < len(rows) for i in ids)\n    assert len(new) == 12 and new == list(range(nextvar, nextvar+12))\n    assert all(isinstance(d, list) and len(d) == 2 for d in defs)\n    di = [i for i,v in defs]\n    dv = [v for i,v in defs]\n    assert len(di) == len(set(di)) and len(dv) == len(set(dv))\n    assert not set(di)&set(ids)\n    assert all(type(i) is int and 0 <= i < len(rows) for i in di)\n    assert all(type(v) is int and 0 < v < nextvar for v in dv)\n    assert not set(dv)&(set(old)|{b})\n    selected = set(ids)|set(di)\n    removed = set(old)|set(dv)\n    assert len(selected) >= 9\n    for v in removed:\n        assert incidence.get(v,set()) <= selected, \'Outside use of removed parity coordinate\'\n    expanded = {}\n    for i,v in defs:\n        row = rows[i]\n        coefficient = row.get((v,),0)\n        assert coefficient\n        rhs = add((-1/F(coefficient),row),(1,var(v)))\n        assert v not in variables(rhs)\n        assert variables(rhs) <= set(old)|{b}|set(expanded), \'Non-acyclic or external definition\'\n        expanded[v] = expand(rhs,expanded)\n    expected_source = source_rows(b,old)\n    for i,source in zip(ids,expected_source):\n        assert norm(expand(rows[i],expanded)) == norm(source), \'Wrong source parity residual\'\n    expected = {i:{} for i in selected}\n    for i,row in zip(sorted(selected),replacement_rows(b,new)):\n        assert all(len(m)<=2 for m in row)\n        expected[i] = dict(norm(row))\n    return expected,nextvar+12\n\n\ndef check_patches(expected, supplied):\n    assert len(supplied) == len({i for i,row in supplied})\n    actual = {i:{tuple(m):c for c,m in row} for i,row in supplied}\n    assert actual.keys() == expected.keys()\n    for i,row in actual.items():\n        assert all(type(c) is int and c and len(m)<=2 for m,c in row.items())\n        assert norm(row) == norm(expected[i]), \'Incorrect supplied replacement\'\n\n\ndef old_to_new(b, old):\n    t,u,e,p,q,s,h = map(F,old)\n    b = F(b)\n    denominator = 1+b*t*t\n    assert denominator != 0\n    v = 2*b*t/denominator\n    return [u,v,b*v,u*u,e,p,b*e,b*h,s,q,s*s,b*q]\n\n\ndef new_to_old(b, new):\n    b = F(b)\n    u,v,a,z,e,p,c,w,s,q,j,k = map(F,new)\n    if not b:\n        assert u == 0\n        t = F(0)\n    elif u+b:\n        t = v/(u+b)\n    else:\n        assert u == -b and v == 0\n        u = b\n        t = F(0)\n    return [t,u,e,p,q,s,e*(17*b-z)]\n','<embedded-parity>','exec'),_rules_parity)
_rules_batch={'__name__':'embedded_batch'}
exec(compile('"""Independent checker for root-error absorption in a quadratic norm batch.\n\nIntegration: import batch_absorb_expected; dispatch the event kind\n``batch_absorb`` to expected,nextvar=batch_absorb_expected(rows,d,nextvar,incidence).\nThe caller must check every supplied patch against ``expected`` up to a nonzero\nrational scalar and retain the usual final expansion checks.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction\nfrom math import gcd, lcm\n\n\ndef dec(terms):\n    p = {}\n    for c, m in terms:\n        assert type(c) is int and c != 0\n        assert type(m) is list and all(type(v) is int and v >= 0 for v in m)\n        t = tuple(m)\n        assert t == tuple(sorted(t)) and t not in p\n        p[t] = Fraction(c)\n    return p\n\n\ndef vs(p):\n    return {v for m in p for v in m}\n\n\ndef add(*parts):\n    out = defaultdict(Fraction)\n    for c, p in parts:\n        for m, a in p.items():\n            out[m] += c*a\n    return {m: a for m, a in out.items() if a}\n\n\ndef mul(p, q):\n    out = defaultdict(Fraction)\n    for m, a in p.items():\n        for n, b in q.items():\n            out[tuple(sorted(m+n))] += a*b\n    return {m: a for m, a in out.items() if a}\n\n\ndef v(i):\n    return {(i,): Fraction(1)}\n\n\ndef canon(p):\n    if not p:\n        return ()\n    den = lcm(*(Fraction(c).denominator for c in p.values()))\n    q = {m: int(c*den) for m, c in p.items()}\n    g = gcd(*q.values())\n    if q[min(q)] < 0:\n        g = -g\n    return tuple(sorted((m, c//g) for m, c in q.items()))\n\n\ndef expand(p, defs):\n    out = {}\n    for m, a in p.items():\n        term = {(): a}\n        for i in m:\n            term = mul(term, defs.get(i, v(i)))\n        out = add((1, out), (1, term))\n    return out\n\n\ndef batch_absorb_expected(rows, d, nextvar, incidence):\n    old_limit = nextvar\n    def old(i):\n        assert type(i) is int and 0 < i < old_limit\n        return v(i)\n    def row(i):\n        assert type(i) is int and 0 <= i < len(rows)\n        return rows[i]\n    def eq(i, p):\n        assert p and canon(row(i)) == canon(p)\n    E, T = old(d[\'error\']), old(d[\'root\'])\n    assert d[\'error\'] != d[\'root\']\n    root_row = d[\'root_row\']\n    eq(root_row, add((1, E), (-1, mul(T, T)), (2, {(): 1})))\n    # Over Q the retained root row implies E != 0: sqrt(2) is irrational.\n    # Every retained first-leaf row then proves its R != 0.\n    proofs = {}\n    proof_rows = {root_row}\n    for r, f, i in d[\'first_leaves\']:\n        R, F = old(r), old(f)\n        assert r not in proofs and i not in proof_rows\n        eq(i, add((1, mul(R, F)), (-1, R), (-1, mul(E, E))))\n        proofs[r] = f\n        proof_rows.add(i)\n    assert proofs\n\n    items = d[\'definitions\']\n    targets = [t for _, t in items]\n    indices = [i for i, _ in items]\n    assert len(targets) == len(set(targets))\n    assert len(indices) == len(set(indices))\n    assert not set(indices) & proof_rows\n    target_set = set(targets)\n    expanded = {}\n    for i, t in items:\n        old(t)\n        rr = row(i)\n        c = rr.get((t,), 0)\n        assert c\n        rhs = add((-Fraction(1, c), rr), (1, v(t)))\n        assert t not in vs(rhs)\n        assert vs(rhs) & target_set <= expanded.keys()\n        expanded[t] = expand(rhs, expanded)\n\n    removed_list = d[\'removed\']\n    removed = set(removed_list)\n    assert len(removed) == len(removed_list) and removed <= target_set\n    pair_rows = [p[\'row\'] for p in d[\'pairs\']]\n    assert pair_rows and len(pair_rows) == len(set(pair_rows))\n    assert not set(pair_rows) & (set(indices) | proof_rows)\n    changed = set(pair_rows) | {i for i, t in items if t in removed}\n    for t in removed:\n        assert incidence.get(t, set()) <= changed\n    expected = {i: {} for i in changed}\n\n    # Every new coordinate is explicitly defined. Odd powers use the proved\n    # unit R; squares use a polynomial definition. No square root is chosen.\n    new_rows = []\n    odds = {}\n    squares = {}\n    def fresh(t):\n        nonlocal nextvar\n        assert type(t) is int and t == nextvar\n        nextvar += 1\n    for spec in d[\'new_variables\']:\n        kind = spec[\'kind\']; t = spec[\'variable\']; fresh(t)\n        if kind == \'odd_power\':\n            r, p = spec[\'factor\'], spec[\'even\']\n            R, P = old(r), old(p)\n            assert r in proofs and (r, p) not in odds\n            assert not {r, p} & removed\n            odds[r, p] = t\n            new_rows.append(add((1, mul(R, v(t))), (-1, P)))\n        else:\n            assert kind == \'square\'\n            B = dec(spec[\'base\'])\n            assert B and all(len(m) <= 1 for m in B)\n            assert all(i < old_limit for i in vs(B)) and not vs(B) & removed\n            squares[t] = B\n            new_rows.append(add((1, v(t)), (-1, mul(B, B))))\n    low = {}\n    for r, p, i in d[\'low_powers\']:\n        R, P = old(r), old(p)\n        assert r in proofs and (r, p) not in low and (r, p) not in odds\n        assert i not in changed and not {r, p} & removed\n        eq(i, add((1, P), (-1, mul(R, R))))\n        low[r, p] = r\n    used_odds = set(); used_squares = set(); used_proofs = set(); used_low = set()\n    for pair in d[\'pairs\']:\n        i, r, f, p, o, n, t, q = (pair[k] for k in\n            (\'row\', \'factor\', \'first\', \'even\', \'odd\', \'norm\', \'test\', \'square\'))\n        R, F, P, N, U = (old(j) for j in (r, f, p, n, t))\n        assert proofs.get(r) == f\n        assert o == (odds | low).get((r, p))\n        B = dec(pair[\'base\'])\n        assert B and all(len(m) <= 1 for m in B)\n        assert all(j < old_limit for j in vs(B))\n        assert q in squares and mul(B, B) == mul(squares[q], squares[q])\n        assert not (vs(B) | {r, f, p, n, t}) & (removed | target_set)\n        want = add((1, mul(P, N)), (-1, mul(mul(E, E), mul(B, B))),\n                   (-1, mul(R, mul(U, U))))\n        assert canon(expand(row(i), expanded)) == canon(want)\n        expected[i] = add((1, mul(v(o), N)), (-1, mul(F, v(q))),\n                          (1, v(q)), (-1, mul(U, U)))\n        used_proofs.add(r); used_squares.add(q)\n        (used_odds if (r, p) in odds else used_low).add((r, p))\n    assert used_proofs == proofs.keys()\n    assert used_odds == odds.keys() and used_low == low.keys()\n    assert used_squares == squares.keys()\n    for k, rr in enumerate(new_rows):\n        expected[len(rows)+k] = rr\n    assert not set(expected) & proof_rows\n    assert all(not vs(rr) & removed and all(len(m) <= 2 for m in rr)\n               for rr in expected.values())\n    return expected, nextvar\n\n\nif __name__ == \'__main__\':\n    import argparse\n    import gzip\n    import json\n    from pathlib import Path\n    parser = argparse.ArgumentParser(description=\'Check one batch-absorb event against its parent rows.\')\n    parser.add_argument(\'--parent\', type=Path, required=True)\n    parser.add_argument(\'--event\', type=Path, required=True)\n    args = parser.parse_args()\n    rr = [dec(x) for x in json.loads(gzip.decompress((args.parent/\'candidate-rows.json.gz\').read_bytes()))]\n    records = [json.loads(line) for line in gzip.decompress((args.parent/\'certificate.jsonl.gz\').read_bytes()).splitlines()]\n    limit = records[-1][\'allocated_variables\']\n    incidence = defaultdict(set)\n    for i, poly in enumerate(rr):\n        for t in vs(poly):\n            incidence[t].add(i)\n    event = json.loads(args.event.read_bytes())\n    assert event[\'kind\'] == \'batch_absorb\'\n    want, limit = batch_absorb_expected(rr, event[\'data\'], limit, incidence)\n    patches = {i: dec(poly) for i, poly in event[\'patches\']}\n    assert len(patches) == len(event[\'patches\']) and patches.keys() == want.keys()\n    assert all(canon(patches[i]) == canon(poly) for i, poly in want.items())\n    print(json.dumps({\'status\': \'PASS\', \'scope\': \'one exact event; parent certificate and final expansion not checked here\',\n                      \'pairs\': len(event[\'data\'][\'pairs\']), \'patches\': len(patches), \'allocated_variables\': limit}))\n','<embedded-batch>','exec'),_rules_batch)

_relation_rules = {'__name__': 'independent_elimination_rule'}
exec('"""Independent exact checker for elimination modulo untouched equations.\n\nNo producer/search module is imported. Integrate relation_eliminate_expected\nas the handler for ``relation_eliminate`` and retain all ordinary patch,\ndegree, allocated-coordinate, source, and final expansion checks.\n"""\nfrom collections import defaultdict\nfrom fractions import Fraction\n\nif not __debug__:\n    raise RuntimeError(\'Assertion-based certificate checks require normal Python mode\')\nfrom math import gcd, lcm\n\n\ndef variables(p):\n    return {v for mon in p for v in mon}\n\n\ndef decode(terms):\n    p = {}\n    for c, mon in terms:\n        assert type(c) is int and c != 0\n        assert type(mon) is list and all(type(v) is int and v >= 0 for v in mon)\n        key = tuple(mon)\n        assert key == tuple(sorted(key)) and key not in p\n        p[key] = Fraction(c)\n    return p\n\n\ndef add(*parts):\n    p = defaultdict(Fraction)\n    for scalar, poly in parts:\n        for mon, c in poly.items():\n            p[mon] += scalar*c\n    return {mon: c for mon, c in p.items() if c}\n\n\ndef multiply(p, q):\n    r = defaultdict(Fraction)\n    for mon, c in p.items():\n        for other, d in q.items():\n            r[tuple(sorted(mon+other))] += c*d\n    return {mon: c for mon, c in r.items() if c}\n\n\ndef substitute(poly, variable, replacement):\n    result = {}\n    for mon, coefficient in poly.items():\n        term = {(): coefficient}\n        for v in mon:\n            term = multiply(term, replacement if v == variable else {(v,): 1})\n        result = add((1, result), (1, term))\n    return result\n\n\ndef normalize(poly):\n    if not poly:\n        return ()\n    denominator = lcm(*(Fraction(c).denominator for c in poly.values()))\n    integer = {mon: int(c*denominator) for mon, c in poly.items()}\n    divisor = gcd(*integer.values())\n    if integer[min(integer)] < 0:\n        divisor = -divisor\n    return tuple(sorted((mon, c//divisor) for mon, c in integer.items()))\n\n\ndef rational_polynomial(data, limit, excluded, degree):\n    denominator = data[\'denominator\']\n    assert type(denominator) is int and denominator > 0\n    p = decode(data[\'terms\'])\n    assert all(len(mon) <= degree for mon in p)\n    assert all(v < limit for v in variables(p))\n    assert not variables(p) & excluded\n    return {mon: c/denominator for mon, c in p.items()}\n\n\ndef relation_eliminate_expected(rows, data, nextvar, incidence):\n    i, v = data[\'row\'], data[\'variable\']\n    assert type(i) is int and 0 <= i < len(rows)\n    assert type(v) is int and 0 < v < nextvar\n    replacement = rational_polynomial(data[\'replacement\'], nextvar, {v}, 2)\n    defining = add((1, {(v,): 1}), (-1, replacement))\n    assert normalize(rows[i]) == normalize(defining)\n    affected = set(incidence.get(v, set())) - {i}\n    assert i in incidence.get(v, set())\n    reductions = data[\'reductions\']\n    ids = [r[\'row\'] for r in reductions]\n    assert all(type(j) is int and 0 <= j < len(rows) for j in ids)\n    assert len(ids) == len(set(ids)) and set(ids) == affected\n    frozen_forbidden = affected | {i}\n    expected = {i: {}}\n    for reduction in reductions:\n        j = reduction[\'row\']\n        transformed = substitute(rows[j], v, replacement)\n        support_ids = []\n        for term in reduction[\'terms\']:\n            k = term[\'support\']\n            assert type(k) is int and 0 <= k < len(rows)\n            assert k not in frozen_forbidden\n            assert v not in variables(rows[k]) and rows[k]\n            multiplier = rational_polynomial(term[\'multiplier\'], nextvar, {v}, 2)\n            assert multiplier\n            support_ids.append(k)\n            transformed = add((1, transformed), (-1, multiply(multiplier, rows[k])))\n        assert len(support_ids) == len(set(support_ids))\n        assert all(len(mon) <= 2 for mon in transformed)\n        assert v not in variables(transformed)\n        expected[j] = transformed\n    return expected\n\n\ndef verify_event(rows, event, nextvar):\n    assert event[\'kind\'] == \'relation_eliminate\'\n    incidence = defaultdict(set)\n    for i, poly in enumerate(rows):\n        for v in variables(poly):\n            incidence[v].add(i)\n    expected = relation_eliminate_expected(rows, event[\'data\'], nextvar, incidence)\n    supplied = {i: decode(poly) for i, poly in event[\'patches\']}\n    assert len(supplied) == len(event[\'patches\']) and supplied.keys() == expected.keys()\n    assert all(normalize(supplied[i]) == normalize(poly) for i, poly in expected.items())\n    return supplied\n\n\n', _relation_rules)
relation_eliminate_expected = _relation_rules['relation_eliminate_expected']
_localized_rules = {'__name__': 'independent_elimination_rule'}
exec('"""Independent checker for one localized_eliminate certificate operation.\n\nDoes not import the producer. Add the dispatcher hook documented in RESULT.md\nto the main certificate checker to validate full candidate artifacts.\n"""\nfrom collections import Counter, defaultdict\nfrom fractions import Fraction\nimport itertools\nimport math\n\nif not __debug__:\n    raise RuntimeError(\'Assertion-based certificate checks require normal Python mode\')\n\n\ndef decode(terms):\n    out = {}\n    for c, m in terms:\n        assert type(c) is int and c != 0\n        assert all(type(v) is int and v >= 0 for v in m)\n        key = tuple(m)\n        assert key == tuple(sorted(key)) and key not in out\n        out[key] = Fraction(c)\n    return out\n\n\ndef vars_in(poly):\n    return {v for term in poly for v in term}\n\n\ndef combine(terms):\n    out = defaultdict(Fraction)\n    for scale, poly in terms:\n        for m, c in poly.items():\n            out[m] += scale * c\n    return {m: c for m, c in out.items() if c}\n\n\ndef product(*polys):\n    out = defaultdict(Fraction)\n    for terms in itertools.product(*(tuple(p.items()) for p in polys)):\n        coefficient = Fraction(1)\n        monomial = []\n        for m, c in terms:\n            coefficient *= c\n            monomial.extend(m)\n        out[tuple(sorted(monomial))] += coefficient\n    return {m: c for m, c in out.items() if c}\n\n\ndef proportional(a, b):\n    if not a or not b:\n        return not a and not b\n    if set(a) != set(b):\n        return False\n    anchor = min(a)\n    return all(a[m] * b[anchor] == b[m] * a[anchor] for m in a)\n\n\ndef prove_unit(rows, factor, proof, removed, allocated, ancestors=()):\n    assert factor and all(len(m) <= 1 for m in factor)\n    assert removed not in vars_in(factor)\n    assert all(v < allocated for v in vars_in(factor))\n    i = proof["row"]\n    assert type(i) is int and 0 <= i < len(rows)\n    row = rows[i]\n    assert len(ancestors) <= 256\n    # Retaining the proof without the eliminated coordinate is essential.\n    assert removed not in vars_in(row)\n    if proof["kind"] == "inverse":\n        w = proof["witness"]\n        assert type(w) is int and 0 <= w < allocated\n        assert row.get((), 0) != 0\n        nonconstant = {m: c for m, c in row.items() if m}\n        assert proportional(nonconstant, product(factor, {(w,): Fraction(1)}))\n    elif proof["kind"] == "root_error":\n        e, t = proof["error"], proof["root"]\n        assert all(type(v) is int and 0 <= v < allocated for v in (e, t))\n        assert e != t\n        assert proportional(factor, {(e,): Fraction(1)})\n        assert proportional(row, {(e,): Fraction(1), (t, t): Fraction(-1), (): Fraction(2)})\n        # For rational t, t^2 != 2 by the usual coprime numerator/denominator proof.\n    elif proof["kind"] == "product_unit":\n        # The retained row states factor*cofactor = c*monomial. All\n        # variables in monomial are independently nonzero and c != 0.\n        # This includes R*(F-1)=E^2, without assuming F is nonzero.\n        certified_factor = decode(proof["factor"])\n        assert certified_factor and all(len(m) <= 1 for m in certified_factor)\n        assert proportional(factor, certified_factor)\n        cofactor = decode(proof["cofactor"])\n        monomial = tuple(proof["monomial"])\n        assert monomial == tuple(sorted(monomial))\n        assert all(type(w) is int and 0 <= w < allocated for w in monomial)\n        assert cofactor and all(len(m) <= 1 for m in cofactor)\n        assert removed not in vars_in(cofactor)\n        assert all(w < allocated for w in vars_in(cofactor))\n        coefficient = proof["coefficient"]\n        assert type(coefficient) is int and coefficient != 0\n        assert (i, tuple(sorted(factor.items()))) not in ancestors\n        expected_row = combine([(1, product(certified_factor, cofactor)),\n                                (-coefficient, {monomial: Fraction(1)})])\n        assert expected_row and proportional(row, expected_row)\n        known = {w: child for w, child in proof["known"]}\n        assert len(known) == len(proof["known"]) and set(known) == set(monomial)\n        for w, child in known.items():\n            assert type(w) is int\n            prove_unit(rows, {(w,): Fraction(1)}, child, removed, allocated,\n                       ancestors + ((i, tuple(sorted(factor.items()))),))\n    elif proof["kind"] == "binomial":\n        v = proof["variable"]\n        assert type(v) is int and 0 <= v < allocated\n        assert proportional(factor, {(v,): Fraction(1)})\n        assert len(row) == 2\n        left = [m for m in row if v in m]\n        right = [m for m in row if v not in m]\n        assert len(left) == len(right) == 1\n        assert (i, v) not in ancestors\n        known = {w: child for w, child in proof["known"]}\n        assert len(known) == len(proof["known"]) and set(known) == set(right[0])\n        for w, child in known.items():\n            assert type(w) is int\n            prove_unit(rows, {(w,): Fraction(1)}, child, removed, allocated, ancestors + ((i, v),))\n        # Both binomial coefficients are nonzero. The right monomial is\n        # nonzero, hence so is the left monomial and each of its factors.\n    else:\n        raise AssertionError("unknown nonzero proof")\n\n\ndef expected(rows, data, allocated, incidence, patches, relations=False):\n    """Validate and return the complete patch map; no mutation occurs here."""\n    i, v = data["row"], data["variable"]\n    assert type(i) is int and 0 <= i < len(rows)\n    assert type(v) is int and 0 < v < allocated\n    a, n = decode(data["denominator"]), decode(data["numerator"])\n    assert a and max(map(len, a)) == 1\n    assert all(len(m) <= 2 for m in n)\n    assert v not in vars_in(a) | vars_in(n)\n    assert all(w < allocated for w in vars_in(a) | vars_in(n))\n    assert proportional(rows[i], combine([(1, product(a, {(v,): Fraction(1)})), (-1, n)]))\n    prove_unit(rows, a, data["nonzero"], v, allocated)\n    affected = sorted(incidence[v] - {i})\n    assert data["affected"] == affected\n    assert len(patches) == len(affected) + 1\n    supplied = {j: decode(poly) for j, poly in patches}\n    assert len(supplied) == len(patches) and set(supplied) == set(affected) | {i}\n    assert supplied[i] == {}\n    factors_by_row = {entry["row"]: entry["factors"] for entry in data["cancellations"]}\n    assert len(factors_by_row) == len(data["cancellations"])\n    assert set(factors_by_row) == set(affected)\n    reductions = {}\n    if relations:\n        reductions = {entry[\'row\']: entry[\'terms\'] for entry in data[\'reductions\']}\n        assert len(reductions) == len(data[\'reductions\'])\n        assert set(reductions) == set(affected)\n    for j in affected:\n        new = supplied[j]\n        assert all(len(m) <= 2 for m in new)\n        assert v not in vars_in(new)\n        assert all(w < allocated for w in vars_in(new))\n        original = rows[j]\n        exponent = max((Counter(m)[v] for m in original), default=0)\n        assert 0 <= exponent <= 2\n        summands = []\n        for monomial, coefficient in original.items():\n            occurrences = Counter(monomial)[v]\n            other = tuple(w for w in monomial if w != v)\n            summands.append((coefficient, product({other: Fraction(1)},\n                             *([n] * occurrences), *([a] * (exponent - occurrences)))))\n        cleared = combine(summands)\n        if relations:\n            used = set()\n            for term in reductions[j]:\n                support = term[\'support\']\n                assert type(support) is int and 0 <= support < len(rows)\n                assert support not in supplied and support not in used\n                used.add(support)\n                assert rows[support] and v not in vars_in(rows[support])\n                denominator = term[\'multiplier\'][\'denominator\']\n                assert type(denominator) is int and denominator > 0\n                numerator = decode(term[\'multiplier\'][\'terms\'])\n                assert all(len(m) <= 2 for m in numerator)\n                assert v not in vars_in(numerator)\n                assert all(w < allocated for w in vars_in(numerator))\n                cleared = combine([(1, cleared),\n                                   (-Fraction(1, denominator), product(numerator, rows[support]))])\n        factors = []\n        assert len(factors_by_row[j]) <= 8\n        for entry in factors_by_row[j]:\n            factor = decode(entry["factor"])\n            assert factor and max(map(len, factor)) == 1\n            prove_unit(rows, factor, entry["proof"], v, allocated)\n            factors.append(factor)\n        assert proportional(cleared, product(new, *factors)), ("failed identity", j)\n    return supplied\n\n\ndef relation_expected(rows, data, allocated, incidence, patches):\n    return expected(rows, data, allocated, incidence, patches, relations=True)\n', _localized_rules)
localized_expected = _localized_rules['expected']
relation_expected = _localized_rules['relation_expected']

def verify(root,write_report=True):
    start=time.monotonic();source_bytes=(root/'source-residuals.jsonl.gz').read_bytes()
    with gzip.open(root/'certificate.jsonl.gz','rt',encoding='ascii') as seed:
        first=json.loads(next(seed))
    source_id=first.get('source_id','original64')
    assert source_id in SOURCE_ENTRIES
    entry=SOURCE_ENTRIES[source_id]
    SOURCE_SHA=entry['source_sha256'];SOURCE_VARIABLES=entry['source_variables'];SOURCE_ROWS=entry['source_rows']
    if source_id!='original64':
        assert first['source_entry_sha256']==hashlib.sha256(canonical(entry)+b'\n').hexdigest()
        assert json.loads(gzip.decompress(source_bytes).splitlines()[0])==entry['source_header']
        assert hashlib.sha256(gzip.decompress(source_bytes)).hexdigest()==entry['uncompressed_sha256']
    assert hashlib.sha256(source_bytes).hexdigest()==SOURCE_SHA
    source=[decode(json.loads(line)) for line in gzip.decompress(source_bytes).splitlines()[1:]]
    assert len(source)==SOURCE_ROWS and set.union(*(variables(r) for r in source))==set(range(SOURCE_VARIABLES))
    counts=defaultdict(int)
    with gzip.open(root/'certificate.jsonl.gz','rt',encoding='ascii') as stream:
        initial=json.loads(next(stream));assert initial['kind']=='initial'
        assert initial['source_sha256']==SOURCE_SHA and initial['source_variables']==SOURCE_VARIABLES and initial['source_rows']==SOURCE_ROWS
        rows=[decode(r) for r in initial['rows']]
        rules={};anchors=set()
        for rule in initial['reuse']:
            pair=tuple(rule['product']);v=rule['variable'];scale=Fraction(*rule['scale']);index=rule['anchor']
            assert len(pair)==2 and pair==tuple(sorted(pair)) and pair not in rules and v not in pair and scale
            assert 0<=index<len(source) and 0<=v<SOURCE_VARIABLES
            assert normal(source[index])==normal({pair:1,(v,):-scale})
            rules[pair]=(v,scale);anchors.add(index)
        def reduce_anchor_terms(row):
            result={}
            for monomial,coefficient in row.items():
                current=list(monomial);coefficient=Fraction(coefficient)
                while True:
                    choices=sorted(set(itertools.combinations(current,2))&rules.keys())
                    if not choices:break
                    pair=choices[0];v,scale=rules[pair]
                    for w in pair:current.remove(w)
                    current.append(v);current.sort();coefficient*=scale
                key=tuple(current);result[key]=result.get(key,0)+coefficient
            return {m:c for m,c in result.items() if c}
        expanded_vars={v:(v,) for v in range(SOURCE_VARIABLES)};nextvar=SOURCE_VARIABLES
        gates=initial['gates'];assert len(rows)==SOURCE_ROWS+len(gates)
        for position,gate in enumerate(gates):
            v=gate['variable'];pair=tuple(gate['product'])
            assert v==nextvar and len(pair)==2 and all(w in expanded_vars for w in pair)
            expanded_vars[v]=tuple(sorted(expanded_vars[pair[0]]+expanded_vars[pair[1]]));nextvar+=1
            assert rows[SOURCE_ROWS+position]=={pair:-1,(v,):1}
        for i,original in enumerate(source):
            expanded=defaultdict(int)
            for monomial,coefficient in rows[i].items():
                assert all(v in expanded_vars for v in monomial)
                key=tuple(sorted(v for w in monomial for v in expanded_vars[w]));expanded[key]+=coefficient
            expanded={m:c for m,c in expanded.items() if c}
            if i in anchors:assert normal(expanded)==normal(original),('anchor',i)
            else:assert normal(reduce_anchor_terms(expanded))==normal(reduce_anchor_terms(original)),('source',i)
        assert all(len(m)<=2 for r in rows for m in r)
        incidence=defaultdict(set)
        for i,r in enumerate(rows):
            for v in variables(r):incidence[v].add(i)
        def fresh(v):
            nonlocal nextvar
            assert type(v) is int and v==nextvar;nextvar+=1
        def patch(data,expected):
            supplied={i:decode(r) for i,r in data}
            assert len(supplied)==len(data) and supplied.keys()==expected.keys()
            for i,r in supplied.items():
                assert normal(r)==normal(expected[i]),('incorrect row',i)
                assert all(len(m)<=2 for m in r) and all(v<nextvar for v in variables(r))
                assert 0<=i<=len(rows)
                if i==len(rows):rows.append({})
                for v in variables(rows[i]):incidence[v].remove(i)
                rows[i]=r
                for v in variables(r):incidence[v].add(i)
        final=None;weights=None;circuit_cache=set()
        for line in stream:
            event=json.loads(line);kind=event['kind']
            if kind=='final':
                assert final is None;final=event
                assert not stream.read().strip(),'Data after final record'
                break
            if kind=='weights':
                assert weights is None
                weights=event['values'];assert len(weights)==len(rows) and all(type(w) is int and w>0 for w in weights)
                continue
            assert weights is None,'Transformations after final weights are not supported'
            assert final is None
            d=event['data'];expected={};counts[kind]+=1
            if kind=='cse':
                v=d['variable'];fresh(v);definition=decode(d['definition']);assert v not in variables(definition)
                for i,factor in d['rows']:
                    assert 0<=i<len(rows) and i not in expected and type(factor) is int
                    expected[i]=add((1,rows[i]),(-factor,definition),(factor,{(v,):1}))
                expected[len(rows)]=add((1,definition),(-1,{(v,):1}))
            elif kind=='split':
                v=d['variable'];fresh(v);i=d['row'];assert 0<=i<len(rows)
                left=decode(d['left']);assert v not in variables(left)
                right=add((1,rows[i]),(-1,left))
                expected={i:add((1,left),(-1,{(v,):1})),len(rows):add((1,right),(1,{(v,):1}))}
            elif kind=='eliminate':
                i=d['row'];v=d['variable'];assert v!=0 and 0<=i<len(rows)
                replacement=decode(d['replacement']);assert v not in variables(replacement)
                denominator=d.get('denominator',1)
                assert type(denominator) is int and denominator>0
                replacement={m:Fraction(c,denominator) for m,c in replacement.items()}
                assert normal(rows[i])==normal(add((1,{(v,):1}),(-1,replacement)))
                affected=d['affected'];assert len(set(affected))==len(affected) and set(affected)==incidence[v]-{i}
                expected={j:substitute(rows[j],v,replacement) for j in affected};expected[i]={}
            elif kind=='linear':
                i,j=d['target'],d['other'];a,b=d['a'],d['b']
                assert 0<=i<len(rows) and 0<=j<len(rows) and i!=j and type(a) is int and a!=0 and type(b) is int
                expected={i:add((a,rows[i]),(b,rows[j]))}
            elif kind=='relation_eliminate':
                expected=relation_eliminate_expected(rows,d,nextvar,incidence)
            elif kind=='localized_eliminate':
                expected=localized_expected(rows,d,nextvar,incidence,event['patches'])
            elif kind=='localized_relation':
                expected=relation_expected(rows,d,nextvar,incidence,event['patches'])
            elif kind=='unit_scale':
                expected,nextvar=unit_scale_expected(rows,d,nextvar)
            elif kind=='redundant_inverse':
                expected=redundant_inverse_expected(rows,d,nextvar,incidence)
            elif kind=='gpoint_chart':
                expected,nextvar=_rules_chart['chart_expected'](rows,d,nextvar,incidence)
            elif kind=='field_ordinate':
                expected,nextvar=_rules_chart['ordinate_expected'](rows,d,nextvar,incidence)
            elif kind=='parity_conic':
                expected,nextvar=_rules_parity['check_rule'](rows,incidence,d,nextvar)
            elif kind=='batch_absorb':
                expected,nextvar=_rules_batch['batch_absorb_expected'](rows,d,nextvar,incidence)
            elif kind=='norm_inverse':
                i=d['row'];u=d['inverse'];definitions=d['definitions']
                assert type(i) is int and 0<=i<len(rows)
                assert type(u) is int and 0<u<nextvar
                indices=[pair[0] for pair in definitions];targets=[pair[1] for pair in definitions]
                assert definitions and len(indices)==len(set(indices)) and len(targets)==len(set(targets))
                assert i not in indices and u not in targets
                assert all(type(j) is int and 0<=j<len(rows) for j in indices)
                assert all(type(v) is int and 0<v<nextvar for v in targets)
                target_set=set(targets);expanded={}
                for j,v in definitions:
                    coefficient=rows[j].get((v,),0);assert coefficient
                    rhs=add((Fraction(-1,coefficient),rows[j]),(1,{(v,):1}))
                    assert v not in variables(rhs)
                    assert variables(rhs)&target_set<=expanded.keys(),'Non-acyclic norm-guard definitions'
                    expanded[v]=expand_definitions(rhs,expanded)
                removed={u}|{v for v in targets if u in variables(expanded[v])}
                assert len(d['removed'])==len(set(d['removed'])) and set(d['removed'])==removed
                changed={i}|{j for j,v in definitions if v in removed}
                assert len(changed)>=2
                for v in removed:assert incidence[v]<=changed,'Removed norm coordinate has outside uses'
                for j,v in definitions:
                    if v not in removed:assert not variables(rows[j])&removed
                components=d['components'];assert len(components)==2
                A,B=map(decode,components)
                for component in (A,B):
                    assert all(len(m)<=1 for m in component)
                    assert all(v<nextvar for v in variables(component))
                    assert not variables(component)&(target_set|{u})
                N=add((1,mul(A,A)),(-2,mul(B,B)))
                assert normal(expand_definitions(rows[i],expanded))==normal(add((1,mul({(u,):1},N)),(-1,{():1})))
                new=d['new_variables'];assert len(new)==2
                s,t=new;fresh(s);fresh(t)
                S,T={(s,):1},{(t,):1}
                real=add((1,mul(A,S)),(2,mul(B,T)))
                imag=add((1,mul(A,T)),(1,mul(B,S)))
                # Exact norm multiplicativity supplies the reverse solution map.
                assert mul(N,add((1,mul(S,S)),(-2,mul(T,T))))==add((1,mul(real,real)),(-2,mul(imag,imag)))
                second=min(changed-{i})
                expected={j:{} for j in changed}
                expected[i]=add((1,real),(-1,{():1}));expected[second]=imag
            elif kind=='circuit':
                old_ids=d['old_rows'];old_targets=d['old_targets'];outputs=d['outputs'];new_targets=d['new_targets']
                assert len(old_ids)==len(set(old_ids))==len(old_targets)==len(set(old_targets))
                assert all(type(i) is int and 0<=i<len(rows) for i in old_ids)
                assert all(type(v) is int and 0<v<nextvar for v in old_targets)
                assert outputs and len(outputs)==len(set(outputs)) and set(outputs)<=set(old_targets)
                assert all(type(v) is int for v in outputs+new_targets)
                assert 0<len(new_targets)<=len(old_ids) and len(new_targets)==len(set(new_targets))
                assert set(outputs)<=set(new_targets) and set(new_targets)&set(old_targets)==set(outputs)
                for v in set(old_targets)-set(outputs):
                    assert incidence[v]<=set(old_ids),'Removed circuit variable used outside selected rows'
                for v in new_targets:
                    if v not in outputs:fresh(v)
                supplied={i:decode(r) for i,r in event['patches']}
                assert len(supplied)==len(event['patches']) and set(supplied)==set(old_ids)
                assert all(not supplied[i] for i in old_ids[len(new_targets):])
                old_defs=[rows[i] for i in old_ids]
                new_defs=[supplied[i] for i in old_ids[:len(new_targets)]]
                external=set().union(*(variables(r) for r in old_defs))-set(old_targets)
                assert (set().union(*(variables(r) for r in new_defs))-set(new_targets))<=external
                ext=sorted(external)
                def normalized_circuit(defs,targets):
                    mapping={v:i for i,v in enumerate(ext+targets)}
                    assert len(mapping)==len(ext)+len(targets)
                    seen=set(ext);normalized=[]
                    for target,row in zip(targets,defs):
                        assert row.get((target,),0)!=0
                        assert all(target not in mon for mon in row if mon!=(target,))
                        assert variables(row)-{target}<=seen,'Circuit is cyclic or has a forward reference'
                        assert all(len(mon)<=2 for mon in row)
                        renamed={tuple(sorted(mapping[v] for v in mon)):c for mon,c in row.items()}
                        normalized.append((mapping[target],normal(renamed)))
                        seen.add(target)
                    return normalized,[mapping[v] for v in outputs]
                old_norm,old_outputs=normalized_circuit(old_defs,old_targets)
                new_norm,new_outputs=normalized_circuit(new_defs,new_targets)
                # The cache key is the complete normalized data, not a digest.
                cache_key=canonical([len(ext),old_norm,old_outputs,new_norm,new_outputs])
                if cache_key not in circuit_cache:
                    def evaluate(defs):
                        env={i:{(i,):Fraction(1)} for i in range(len(ext))}
                        for target,terms in defs:
                            row=dict(terms);leading=row[(target,)];value={}
                            for mon,c in terms:
                                if mon==(target,):continue
                                term={():Fraction(-c,leading)}
                                for v in mon:term=mul(term,env[v])
                                value=add((1,value),(1,term))
                            env[target]=value
                        return env
                    old_values=evaluate(old_norm);new_values=evaluate(new_norm)
                    assert all(old_values[a]==new_values[b] for a,b in zip(old_outputs,new_outputs)),'Circuit outputs differ'
                    circuit_cache.add(cache_key)
                expected=supplied
            elif kind in ('translate','shear'):
                v=d['variable'];assert 0<v<nextvar
                affected=d['affected'];assert len(set(affected))==len(affected) and set(affected)==incidence[v]
                if kind=='translate':replacement={(v,):1,():Fraction(*d['shift'])}
                else:
                    w=d['other'];assert 0<=w<nextvar and w!=v
                    replacement={(v,):1,(w,):Fraction(*d['scalar'])}
                expected={i:substitute(rows[i],v,replacement) for i in affected}
            else:raise AssertionError(('unknown operation',kind))
            patch(event['patches'],expected)
        assert final is not None and final['allocated_variables']==nextvar
        if weights is None:weights=[1]*len(rows)
        assert hashlib.sha256(canonical([encode(r) for r in rows])).hexdigest()==final['rows_sha256']
    saved=[decode(r) for r in json.loads(gzip.decompress((root/'candidate-rows.json.gz').read_bytes()))];assert saved==rows
    active=json.loads((root/'variable-map.json').read_bytes())
    assert active[0]==0 and len(active)==len(set(active))
    assert set(active)=={v for v,indices in incidence.items() if indices}
    mapping={v:i for i,v in enumerate(active)}
    compact=[{tuple(sorted(mapping[v] for v in m)):coefficient for m,coefficient in r.items()} for r in rows if r]
    assert compact==[decode(r) for r in json.loads(gzip.decompress((root/'residuals.json.gz').read_bytes()))]
    compact_weights=[w for r,w in zip(rows,weights) if r]
    if (root/'weights.json').exists():assert json.loads((root/'weights.json').read_bytes())==compact_weights
    else:assert all(w==1 for w in compact_weights)
    # All ordered products, independent of the producer's triangular expansion.
    polynomial=defaultdict(int)
    for row,weight in zip(compact,compact_weights):
        for m,coefficient in row.items():
            for n,other in row.items():polynomial[tuple(sorted(m+n))]+=weight*coefficient*other
    polynomial={m:c for m,c in polynomial.items() if c}
    expanded_bytes=(root/'polynomial.expanded.txt').read_bytes()
    assert gzip.decompress((root/'polynomial.expanded.txt.gz').read_bytes())==expanded_bytes
    supplied={}
    for line in expanded_bytes.decode('ascii').splitlines():
        if line.startswith('#'):continue
        coefficient,*m=map(int,line.split());m=tuple(m)
        assert coefficient and m not in supplied and m==tuple(sorted(m));supplied[m]=coefficient
    assert polynomial==supplied
    degree=max(map(len,polynomial));maximum=max(map(abs,polynomial.values()))
    assert degree==4 and set.union(*(set(m) for m in polynomial))==set(range(len(active)))
    assert maximum<2**80,'Expanded coefficient reaches the strict 2^80 bound'
    stats={'witnesses':len(active)-1,'variables':len(active),'rows':len(compact),'monomials':len(polynomial),'degree':degree,'max_abs_coefficient':maximum}
    for key in ('variables','witnesses','rows','monomials','degree','max_abs_coefficient'):assert stats[key]==final['report'][key],key
    report={'status':'PASS','scope':'Exact projection-preserving algebraic equivalence to the pinned source system; exact full integer expansion. The source arithmetic theorem is not checked here.',
            **stats,'source_id':source_id,'source_sha256':SOURCE_SHA,'operations':dict(counts),'total_operations':sum(counts.values()),'weights_greater_than_one':sum(w>1 for w in compact_weights),
            'expanded_bytes':len(expanded_bytes),'compressed_bytes':(root/'polynomial.expanded.txt.gz').stat().st_size,
            'expanded_sha256':hashlib.sha256(expanded_bytes).hexdigest(),
            'certificate_sha256':hashlib.sha256((root/'certificate.jsonl.gz').read_bytes()).hexdigest(),
            'distinct_circuit_identities_checked':len(circuit_cache),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':round(time.monotonic()-start,3)}
    if write_report:(root/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);arguments=parser.parse_args()
    print(json.dumps(verify(arguments.directory),indent=2))
