"""Bounded syntax/template check; no source generation or polynomial expansion."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

from prepare_adapter import adapt_producer, make_checker
from source_layout import norm_row, normalize


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--toolchain', type=Path, required=True)
    p.add_argument('--rules', type=Path, required=True)
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    for path in here.glob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    inputs={}
    for pin in json.loads((here/'PINNED_INPUTS.json').read_bytes()):
        source=(a.toolchain if pin['family']=='toolchain' else a.rules)/pin['path']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==pin['sha256']
        inputs[Path(pin['path']).name]=source.read_text(encoding='utf-8')
    entry=dict(source_id='reciprocal-syntax-fixture',source_sha256='1'*64,
               source_variables=17,source_rows=13,source_header={'witnesses':16,'residuals':13},
               uncompressed_sha256='2'*64)
    checker=make_checker(inputs['verify_certificate.py'],entry,inputs)
    tree=ast.parse(checker)
    registry,=[node.value for node in tree.body if isinstance(node,ast.Assign)
               and any(isinstance(t,ast.Name) and t.id=='SOURCE_ENTRIES' for t in node.targets)]
    values=ast.literal_eval(registry)
    assert values[entry['source_id']]==entry
    assert values['original64']['source_variables']==15672
    assert values['original64']['source_rows']==15107
    assert values['original64']['source_sha256']=='6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2'
    assert 'log_inverse' not in checker and 'field_ratio_fusion' not in checker
    for filename in ('replace_charts.py','remove_chart_ordinates.py','produce_parity.py','absorb_batch_error.py'):
        ast.parse(adapt_producer(filename,inputs[filename]),filename=filename)
    # A concrete asymmetric norm row checks signs and off-diagonal factors
    # without importing the producer or expanding a source artifact.
    expected=normalize({():-1,(1,1,9):1,(1,3,9):-2,(3,3,9):1,
                        (2,2,9):-2,(2,4,9):4,(4,4,9):-2})
    assert norm_row(9,(1,2),(3,4))==expected
    assert norm_row(9,(1,2),(4,3))!=expected
    assert norm_row(8,(1,2),(3,4))!=expected
    print('PASS: packet syntax, exact pinned-template shape, and generated source registry. No arithmetic acceptance.')


if __name__=='__main__':
    main()
