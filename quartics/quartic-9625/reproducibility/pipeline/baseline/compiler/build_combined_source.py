"""Generate a provisional H19/root37/reciprocal source in a new directory.

The original builder and all six original modules must match their reviewed
pins before any source change is installed. No source is accepted here.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True

ORIGINAL_BUILDER_SHA256 = 'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912'
LOWPRECISION_KERNEL_SHA256 = '66854ff3ee24d8dd6f4b3b54fa5ca627d87b5d0da09cafa35e3d05d47d0d5c31'
ORIGINAL_MODULES = {
    'q_anchor': 'e4d8f1c9395d254fef83bddefdf304c520af8fee0575926be3aa7189376965cb',
    'q_batch41': '8963245225447a7065b67de902ad27b8820dbeba5562d13756fdf1f71902ae6a',
    'q_compare4': '639574951f42451345b3286a57ca922273567f20a548ee2426939c7a30a07212',
    'q_height_batch': '6682b1069de2edb5fe5ef5ffd5d53ac74652699d8166c509bccad63bf741860a',
    'q_primeparity': 'de1bd279f6ca85b6f4d972c36a4ad079cc9678c47a8672904c168eedbab17478',
    'Z_definition': '75fe909cbd7992c77ec99a2fe18495745362054d20083e4e6a3ff705bb17035e',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')+b'\n'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_original_modules(b):
    b.CURVE_DROOT = (3,-1); b.CURVE_D2 = (11,-6)
    b.BASE_POINT = ((b.F(57,8),b.F(-7,2)),(b.F(-165,8),b.F(417,32)))
    b.CHART = 10; b.PARITY = 7; b.LOG_BLOCK = 2
    b.BASE_GATES = True; b.UNIT_SCALE = True
    b.PELL_PRECISION = 64; b.ANCHOR_SQUARINGS = 24
    captured = {}; old_save = b.M.save
    def save(m, **metadata):
        assert m.name not in captured
        captured[m.name] = dict(name=m.name, free=m.free, locals=m.count-m.free,
                                residuals=m.rows, calls=m.calls, construction_log=m.operations, **metadata)
    b.M.save = save
    try:
        b.make_parity(); b.make_anchor()
        b.make_batch('q_batch41', [1]*23+[64]*18, 'q_primeparity')
        b.make_batch('q_height_batch', [1]*4+[48]*2, 'q_primeparity')
        b.make_multi_comparison(); b.make_root()
    finally:
        b.M.save = old_save
    assert set(captured) == set(ORIGINAL_MODULES)
    for name, expected in ORIGINAL_MODULES.items():
        if sha(canonical(captured[name])) != expected:
            raise ValueError('Original module did not regenerate exactly: '+name)
    assert b.MODULES == {}, 'Baseline check must not publish modules'
    return dict(ORIGINAL_MODULES)


def main():
    if not __debug__:
        raise RuntimeError('Do not disable checks with python -O')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--builder', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--high', type=int, choices=(40,44,48), default=40)
    p.add_argument('--label', type=int, choices=(12,), default=12)
    p.add_argument('--compressed-primary-charts', action='store_true',
                   help='The only supported chart mode; retained as an explicit invocation marker')
    args = p.parse_args()
    if sha(args.builder.read_bytes()) != ORIGINAL_BUILDER_SHA256:
        raise ValueError('Unreviewed original builder')
    here = Path(__file__).resolve().parent
    low_path = here/'lowprecision_kernel.py'
    if sha(low_path.read_bytes()) != LOWPRECISION_KERNEL_SHA256:
        raise ValueError('Unreviewed low-precision circuit producer')
    low = load_module('combined_reviewed_lowprecision', low_path)
    kernel = load_module('combined_reviewed_kernel', here/'combined_kernel.py')
    config = kernel.configuration(args.high, args.label)
    for name in ('high_log_profile', 'beta_log_profile'):
        profile = config[name]
        assert (profile['precision'],profile['scheme'],profile['normalization'],profile['hscale'],profile['bound_output']) in low.profiles()
    b = load_module('combined_original_builder', args.builder)
    original_hashes = check_original_modules(b)
    installed = kernel.install(b, low.emit_g, high=args.high, label=args.label)
    assert installed == config
    args.out.mkdir(parents=True, exist_ok=False)
    sys.argv = [str(args.builder), '--out', str(args.out.resolve()), '--chart', '10', '--parity', '7',
                '--base-gates', '--unit-scale', '--log-block', '2']
    b.main()
    assert set(b.MODULES) == set(ORIGINAL_MODULES)
    assert sum(call['module']=='q_compare4' for call in b.MODULES['Z_definition']['calls']) == 37
    assert b.MODULES['q_height_batch']['orders'] == [1,1,1,1,32,32]
    assert b.MODULES['q_batch41']['orders'] == config['rational_inequality_orders']
    compiler = args.out/'compiler'; compiler.mkdir()
    files = [args.builder.resolve(), Path(__file__).resolve(), here/'combined_kernel.py', low_path]
    hashes = {}
    for source in files:
        destination = compiler/source.name
        assert not destination.exists()
        shutil.copyfile(source, destination); hashes[destination.name] = sha(destination.read_bytes())
    contract = dict(
        status='PROPOSED COMBINED ARITHMETIC SOURCE; INDEPENDENT REVIEW AND SOURCE AUDIT REQUIRED',
        source_family='H19-root37-reciprocal-compressed-v1', source_pin_authorized=False,
        original_builder_digest_matched=ORIGINAL_BUILDER_SHA256,
        complete_original_comparison_regenerated=ORIGINAL_MODULES['q_compare4'],
        complete_original_modules_regenerated=original_hashes,
        compiler_sha256=hashes,
        lowprecision_kernel_sha256=LOWPRECISION_KERNEL_SHA256,
        height_constant_role='Proof-side height bound and parameter justification; H19 is not a literal coefficient of the source residuals',
        height_coordinate_coefficient=7,
        scalar_height_exponent={'numerator':19,'denominator':32},
        prime_pattern_proof_denominator_is_not_a_source_variable=True,
        curve={'field':'Q(sqrt(2))','d':[3,-1],'D':[11,-6]},
        original_input_variable=0,
        fixed_source_flags={'chart':10,'parity':7,'base_gates':True,'unit_scale':True,'log_block':2},
        source_projection_claim='Proposed integer-defining claim depends on the separately reviewed combined arithmetic proof',
        not_established=['accepted new arithmetic source','independent source-construction audit',
                         'fresh quadratic lift','final quartic variable count','full expanded coefficient bound'],
        **config)
    (args.out/'COMBINED_SOURCE.json').write_bytes(canonical(contract))
    print(json.dumps(contract, indent=2))


if __name__ == '__main__':
    main()
