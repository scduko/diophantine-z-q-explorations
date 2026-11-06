"""Freeze an audited reciprocal source and prepare an isolated research toolchain.

This creates a new named algebraic source entry. It does not approve the
arithmetic theorem, modify the original source entry, or publish a quartic.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil

from source_layout import MODULES, derive_layout
from adapt_absorb import adapt_mixed_absorb

ORIGINAL_SOURCE_SHA256 = '6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2'
ACCEPTED_ANCHORS = {40:25, 44:24, 48:23}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')+b'\n'


def replace_once(text, old, new):
    assert text.count(old) == 1, ('Unexpected pinned script shape', old)
    return text.replace(old, new)


def adapt_producer(name, text):
    """Change source locators only; retain the independent algebraic rule."""
    text = text.replace("str(args.repo / 'research/quartic-variables')", 'str(Path(__file__).resolve().parent)')
    text = text.replace("str(a.repo/'research/quartic-variables')", 'str(Path(__file__).resolve().parent)')
    text = text.replace("args.repo / 'degree8-original/modules'", "args.repo / 'source/modules'")
    text = text.replace("a.repo/'degree8-original/modules'", "a.repo/'source/modules'")
    text = text.replace("args.repo / 'degree8-original/construction-certificate.json'", "args.repo / 'construction-map.json'")
    text = text.replace("a.repo/'degree8-original/construction-certificate.json'", "a.repo/'construction-map.json'")
    text = replace_once(text, 'import sys\n', 'import sys\nfrom source_layout import load_layout\n')
    if name == 'replace_charts.py':
        text = replace_once(text, '    args = parser.parse_args()\n', '    args = parser.parse_args()\n    layout = load_layout(args.repo)\n')
        text = replace_once(text, "            prefix = label[:-4]\n", "            prefix = label[:-4]\n            if prefix + '.w.0' not in labels:\n                continue  # The audited compressed primary chart is already reduced.\n")
        text = replace_once(text, '        assert len(diagnostics) == 211', "        assert len(diagnostics) == layout['counts']['uncompressed_charts']\n        assert {(d['instance'],d['chart']) for d in diagnostics} == {(d['path'],d['prefix']) for d in layout['charts']}")
    elif name == 'remove_chart_ordinates.py':
        text = replace_once(text, '    args = parser.parse_args()\n', '    args = parser.parse_args()\n    layout = load_layout(args.repo)\n')
        text = replace_once(text, '    assert len(chart_data) == 211', "    assert len(chart_data) == layout['counts']['uncompressed_charts']")
    elif name == 'produce_parity.py':
        text = replace_once(text, '    a=p.parse_args()\n', "    a=p.parse_args()\n    layout=load_layout(a.repo)\n    parity_by_path={x['path']:x for x in layout['parity']}\n")
        text = replace_once(text, "        old=list(range(inst['first_local'],inst['first_local']+7))\n        ids=list(range(inst['first_residual'],inst['first_residual']+4))", "        locator=parity_by_path[inst['path']]\n        assert b==locator['input']\n        old=locator['witnesses']; ids=locator['rows']")
        text = replace_once(text, "    summary={'instances':len(report)", "    assert len(report)==layout['counts']['parity']\n    summary={'instances':len(report)")
    elif name == 'absorb_batch_error.py':
        text = replace_once(text, '    a = ap.parse_args()\n', '    a = ap.parse_args()\n    layout = load_layout(a.repo)\n')
        old = "    assert hashlib.sha256(source_bytes).hexdigest() == '"+ORIGINAL_SOURCE_SHA256+"'"
        new = "    entry = json.loads((a.repo/'source-entry.json').read_bytes())\n    assert hashlib.sha256(source_bytes).hexdigest() == entry['source_sha256']"
        text = replace_once(text, old, new)
        text = replace_once(text, "    root_i = root['first_residual']+erows[0]\n", "    root_i = root['first_residual']+erows[0]\n    assert root_i == layout['root_row']\n")
        text = replace_once(text, '    pair_ids = {p[\'row\'] for p in pair_records}\n', "    pair_ids = {p['row'] for p in pair_records}\n    assert len(first)==layout['counts']['batches']\n    assert len(pair_records)==layout['counts']['batch_pairs']\n    assert pair_ids=={i for b in layout['batches'] for i in b['pair_rows']}\n")
    assert 'degree8-original/' not in text
    if name == 'absorb_batch_error.py':
        text = adapt_mixed_absorb(text)
    return '# Generated locator adapter; --repo names the isolated adapter directory.\n'+text


def make_checker(base, entry, rules):
    """Retain the original registry entry and bind the new one by name and data."""
    original = dict(source_sha256=ORIGINAL_SOURCE_SHA256, source_variables=15672, source_rows=15107)
    registry = {'original64': original, entry['source_id']: entry}
    prelude = 'SOURCE_ENTRIES = '+repr(registry)+'\n'
    old = "    start=time.monotonic();source_bytes=(root/'source-residuals.jsonl.gz').read_bytes()\n"
    new = "    start=time.monotonic();source_bytes=(root/'source-residuals.jsonl.gz').read_bytes()\n    with gzip.open(root/'certificate.jsonl.gz','rt',encoding='ascii') as seed:\n        first=json.loads(next(seed))\n    source_id=first.get('source_id','original64')\n    assert source_id in SOURCE_ENTRIES\n    entry=SOURCE_ENTRIES[source_id]\n    SOURCE_SHA=entry['source_sha256'];SOURCE_VARIABLES=entry['source_variables'];SOURCE_ROWS=entry['source_rows']\n    if source_id!='original64':\n        assert first['source_entry_sha256']==hashlib.sha256(canonical(entry)+b'\\n').hexdigest()\n        assert json.loads(gzip.decompress(source_bytes).splitlines()[0])==entry['source_header']\n        assert hashlib.sha256(gzip.decompress(source_bytes)).hexdigest()==entry['uncompressed_sha256']\n"
    base = replace_once(base, old, new)
    # These exact source-size literals occur only in the initial lift contract.
    assert base.count('15107') == 4 and base.count('15672') == 5
    base = base.replace('15107', 'SOURCE_ROWS').replace('15672', 'SOURCE_VARIABLES')
    base = replace_once(base, "SOURCE_SHA='"+ORIGINAL_SOURCE_SHA256+"'\n", prelude)
    base = replace_once(base, "            **stats,'source_sha256':SOURCE_SHA,", "            **stats,'source_id':source_id,'source_sha256':SOURCE_SHA,")
    embedded = '\n'; dispatch = ''
    specifications = [
        ('chart', 'check_chart_replacement.py', [('gpoint_chart', "expected,nextvar=_rules_chart['chart_expected'](rows,d,nextvar,incidence)"), ('field_ordinate', "expected,nextvar=_rules_chart['ordinate_expected'](rows,d,nextvar,incidence)")]),
        ('parity', 'parity_rule.py', [('parity_conic', "expected,nextvar=_rules_parity['check_rule'](rows,incidence,d,nextvar)")]),
        ('batch', 'check_batch_absorb.py', [('batch_absorb', "expected,nextvar=_rules_batch['batch_absorb_expected'](rows,d,nextvar,incidence)")]),
    ]
    for name, filename, cases in specifications:
        embedded += f"_rules_{name}={{'__name__':'embedded_{name}'}}\nexec(compile({rules[filename]!r},'<embedded-{name}>','exec'),_rules_{name})\n"
        for kind, expression in cases:
            dispatch += f"            elif kind=='{kind}':\n                {expression}\n"
    base = replace_once(base, 'def verify(root,write_report=True):\n', embedded+'\ndef verify(root,write_report=True):\n')
    base = replace_once(base, "            elif kind=='norm_inverse':\n", dispatch+"            elif kind=='norm_inverse':\n")
    assert "kind=='log_inverse'" not in base and "kind=='field_ratio_fusion'" not in base
    return base


def main():
    if not __debug__:
        raise RuntimeError('Do not disable assertions')
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ('source', 'audit', 'construction-map', 'audit-checker', 'toolchain', 'rules', 'output'):
        p.add_argument('--'+flag, type=Path, required=True)
    a = p.parse_args()
    policy = json.loads(Path(__file__).with_name('AUDITOR_PIN.json').read_bytes())
    audit_sha = policy['checker_sha256']
    assert isinstance(audit_sha,str) and len(audit_sha)==64, 'Combined auditor has not been frozen'
    assert digest(a.audit_checker.read_bytes()) == audit_sha
    for name, expected_digest in policy['helper_files'].items():
        assert digest(a.audit_checker.with_name(name).read_bytes()) == expected_digest
    audit = json.loads(a.audit.read_bytes())
    assert audit['status'] == 'PASS: SOURCE CONSTRUCTION ONLY'
    assert audit['source_pin_authorized'] is False and audit['checker_sha256'] == audit_sha
    assert audit['checker_dependencies_sha256'] == policy['helper_files']
    assert audit['high'] in ACCEPTED_ANCHORS and audit['label']==12 and audit['compressed'] is True
    assert digest(a.construction_map.read_bytes()) == audit['construction_map_sha256']
    residual = audit['source_residual_file']
    assert residual in ('residuals.jsonl', 'residuals.jsonl.gz')
    expected = {'BETA_SOURCE.json', 'counts.json', 'polynomial.json', 'shared.json', residual}
    if residual=='residuals.jsonl' and 'residuals.jsonl.gz' in audit['inspected_files_sha256']:
        expected.add('residuals.jsonl.gz')
    expected |= {'modules/'+name+'.json' for name in MODULES}
    assert policy['compiler_files'] and len(set(policy['compiler_files']))==len(policy['compiler_files'])
    expected |= {'compiler/'+name for name in policy['compiler_files']}
    assert set(audit['inspected_files_sha256']) == expected
    source_files = {}
    for name, wanted in audit['inspected_files_sha256'].items():
        source_files[name] = (a.source/name).read_bytes()
        assert digest(source_files[name]) == wanted, ('Source changed since audit', name)
    if 'residuals.jsonl' in source_files and 'residuals.jsonl.gz' in source_files:
        assert gzip.decompress(source_files['residuals.jsonl.gz']) == source_files['residuals.jsonl']
    raw = source_files[residual]
    if residual.endswith('.gz'):
        raw = gzip.decompress(raw)
    header, *lines = raw.splitlines()
    header = json.loads(header)
    assert header == audit['counts'] and len(lines) == header['residuals']
    variables = {x for line in lines for _, mon in json.loads(line) for x in mon}
    assert variables == set(range(header['witnesses']+1))
    compressed_bytes = gzip.compress(raw, compresslevel=1, mtime=0)
    proposal = json.loads(source_files['BETA_SOURCE.json'])
    assert proposal['high']==audit['high']==40 and proposal['label']==audit['label']==12
    assert proposal['anchor_squarings']==25
    assert proposal['beta_only_positions']==list(range(5,13))
    assert proposal['scalar_orders']==[1,1,1,1,32,32] and proposal['height_exponent']==19
    assert proposal['source_pin_authorized'] is False
    name = 'selective-beta-k40-q12-a25-h19-s32-'+digest(raw)[:12]
    modules = {n: json.loads(source_files['modules/'+n+'.json']) for n in MODULES}
    visits = json.loads(a.construction_map.read_bytes())['instantiations']
    layout = derive_layout(modules,visits)
    assert layout['counts']['comparisons']==37
    assert layout['module_counts']['q_compare4']==29 and layout['module_counts']['q_compare_beta']==8
    entry = dict(source_id=name, source_sha256=digest(compressed_bytes), uncompressed_sha256=digest(raw),
                 source_variables=header['witnesses']+1, source_rows=header['residuals'], source_header=header,
                 source_audit_sha256=digest(a.audit.read_bytes()), source_audit_checker_sha256=audit_sha,
                 construction_map_sha256=audit['construction_map_sha256'], inspected_files_sha256=audit['inspected_files_sha256'],
                 high=audit['high'], label=audit['label'], compressed=audit['compressed'],
                 source_layout_sha256=digest(encoded(layout)), layout_counts=layout['counts'],
                 proposal=proposal,
                 arithmetic_status='EXPLORATORY SOURCE; arithmetic acceptance is outside this algebraic checker')
    pins = json.loads(Path(__file__).with_name('PINNED_INPUTS.json').read_bytes())
    inputs = {}
    for pin in pins:
        path = (a.toolchain if pin['family']=='toolchain' else a.rules)/pin['path']
        data = path.read_bytes(); assert digest(data) == pin['sha256'], ('Changed pinned tool', path)
        key = Path(pin['path']).name; assert key not in inputs
        inputs[key] = data
    a.output.mkdir(parents=True, exist_ok=False)
    for relative, data in source_files.items():
        target = a.output/'source'/relative; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    (a.output/'source-residuals.jsonl.gz').write_bytes(compressed_bytes)
    (a.output/'source-entry.json').write_bytes(encoded(entry))
    (a.output/'source-layout.json').write_bytes(encoded(layout))
    shutil.copyfile(a.audit, a.output/'source-audit.json')
    shutil.copyfile(a.construction_map, a.output/'construction-map.json')
    destination = a.output/'tools'; destination.mkdir()
    producers = {'replace_charts.py','remove_chart_ordinates.py','produce_parity.py','absorb_batch_error.py'}
    for filename, data in inputs.items():
        if filename == 'verify_certificate.py':
            continue
        text = data.decode('utf-8')
        (destination/filename).write_text(adapt_producer(filename,text) if filename in producers else text, encoding='utf-8', newline='\n')
    checker = make_checker(inputs['verify_certificate.py'].decode('utf-8'), entry, {k:v.decode('utf-8') for k,v in inputs.items()})
    (a.output/'verify_named_source.py').write_text(checker, encoding='utf-8', newline='\n')
    for filename in ('fresh_lift.py','reduce_norms.py','run_pipeline.py','source_layout.py'):
        shutil.copyfile(Path(__file__).with_name(filename), destination/filename)
    generated = {str(path.relative_to(a.output)).replace('\\','/'):digest(path.read_bytes()) for path in destination.iterdir()}
    generated['verify_named_source.py'] = digest((a.output/'verify_named_source.py').read_bytes())
    (a.output/'adapter-manifest.json').write_bytes(encoded(dict(status='PREPARED RESEARCH ADAPTER; NOT A SOURCE ACCEPTANCE', source_id=name, pinned_inputs=pins, generated_sha256=generated)))
    print(json.dumps(entry, indent=2))


if __name__ == '__main__':
    main()
