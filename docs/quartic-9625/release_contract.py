"""Immutable finite target; not a proof of the source's arithmetic theorem."""
DOCS='docs/quartic-9625'
PACKAGE='quartics/quartic-9625'
MANUSCRIPT='quartic_9625.tex'
REGISTRY_SHA='e06b377ecedd1bb42e0443606dd85cc54743e98a98188dfd2ddf9db4e06f29c1'
PATCH_SHA='da4d0239d33a344152481958a5e09d6737691dec40f5e78d6d654a08fd89172b'
BASE_INVENTORY_SHA='ab8507d4efc538e48675857320def4ffb43c0d62fafe46c44589d2ac6f6db4e4'
SOURCE_ID='selective-beta-k40-q12-a25-h19-s32-d68d86cdf995'
SOURCE_SHA='97b7bc300084afaefe9980f1feea760be8b4dedaf6eb788fcc4c3af440262579'
SOURCE_RAW_SHA='d68d86cdf995a0e80c38953f1ad03262733f81145b949a0501b143eca6ac0a9c'
ENTRY_SHA='8b45e266b0b4692320bb4f4924a2d3216d5f17fdc47a5c7fb9cdf6010a9a36f7'
AUDIT_SHA='9020dcfdcfab0b05a1b26d9f73713369bde40dae3fe5f179fab77bafcc5f0b40'
MAP_SHA='bcefd99b40537c59c422e9e44ebc6e444469ddb873909239e8a21d3e9d82f7f9'
AUDITOR_SHA='41a3d780636c1f28852762ee0ce7a252e207ec74e7367da275676200a6068ffa'
EXPECTED=dict(variables=9625,witnesses=9624,rows=9161,monomials=82476,degree=4,
 max_abs_coefficient=685783949153203534233601,total_operations=1246,
 expanded_sha256='6d67d45f3d615b7fd2242e3a9404dd9f5da570fc711a29ebe77f613e80ebbf99',
 certificate_sha256='8aaa2249eda6972c441d58b212ec64a53e1202d5e9f74ea4cbc53e7e3f71a0bd',
 checker_sha256='cf587ff9c28af5593e346eb7484d1713bd3f1ff77d28aa5ada06b2b92909d6f4',
 operations={'norm_inverse':161,'redundant_inverse':37,'gpoint_chart':6,'field_ordinate':2,
 'parity_conic':38,'batch_absorb':1,'linear':312,'eliminate':685,'shear':4})
RETAINED=['quadratic_field_and_rational_inverse','constant_definition_equivalence',
 'invertible_row_equivalence','acyclic_circuit_equivalence','scalar_norm_inverse_equivalence',
 'root_error_and_contact_nonvanishing','private_contact_inverse_removal','point_chart_equivalence',
 'ordinate_elimination_equivalence','parity_block_existential_equivalence',
 'bottom_norm_absorption_equivalence','normalization_and_sum_of_squares','rational_coordinate_shear']
NEW=['V3_H19','V3_ROOT37','V3_RECIPROCAL','V3_NONZERO','V3_LOCAL','V3_ANCHOR',
 'V3_LUCAS','V3_BETA','V3_SOURCE','V3_COMPRESSED','V3_CIRCUIT']
PUBLICATION_KEYS={'P_DETERMINANT':['diamond-im'],
 'P_MODULAR_FACTOR':['baker-et-al-finiteness','mascot-moduli','shimura-factors'],
 'P_BELYI':['javanpeykar','vonKaenel2021'],'P_TRANSFER':['GaudronRemond2023']}
LAYOUT_TRANSFORM=dict(id='split-contact-constants-display',
 old=' \\qquad A_i=R_{\\rm c}a_i+3,\\quad w_i=A_iv-u.',
 new='\\]\n\\[\n A_i=R_{\\rm c}a_i+3,\\quad w_i=A_iv-u.',
 reason='Split one overflowing display; remove only its leading horizontal-space command. Mathematical tokens unchanged.')
