"""Small hash/syntax freeze for the rational-difference packet."""
import argparse,ast,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);a=p.parse_args()
    assert 'PENDING_' not in (HERE/'check_source.py').read_text(encoding='utf-8'), 'Independent checker pins pending'
    for name,pin in load(HERE/'BASELINE.json')['files'].items():assert sha(HERE/'baseline'/name)==pin,name
    external=[]
    for item in load(HERE/'PINNED_INPUTS.json'):
        name='research/quartic-variables/'+('' if item['family']=='toolchain' else 'astra-wave11/')+item['path']
        assert sha(a.repo/name)==item['sha256'],name;external.append({'path':name,'sha256':item['sha256']})
    save(HERE/'AUDITOR_PIN.json',{'checker_sha256':sha(HERE/'check_source.py'),
      'helper_files':{name:sha(HERE/name) for name in ('core_audit.py','BASELINE.json','audit_normalized_lucas.py','check_lucas_batch.py','check_anchor_four.py','audit_conic_pole.py','check_conic_pole.py','audit_linear_pole.py','spec_linear.py','audit_root_shared.py','audit_root_rewrite.py','audit_target2.py','probe_tangents.py','audit_shared_square.py','audit_first_norm.py','SELECTED_PARENT.json')},
      'compiler_files':['archive_build.py','combined_kernel.py','lowprecision_kernel.py','beta_kernel.py','rational_difference.py','joint_chart.py','local_lucas.py','normalized_lucas.py','conic_lucas.py','anchor_four_kernel.py','linear_pole_kernel.py','emit_linear.py','target2_rewrite.py','compress_doublings.py','shared_square.py','first_norm.py','build_source.py'],
      'status':'EXPLORATORY FINITE CHECKER PIN; NO ARITHMETIC ACCEPTANCE'})
    files={}
    for path in sorted(HERE.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or path.name=='manifest.json':continue
        if path.suffix=='.py':ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
        files[path.relative_to(HERE).as_posix()]={'sha256':sha(path),'bytes':path.stat().st_size}
    save(HERE/'manifest.json',{'format':'target2-tangent-first-norm-normalized-linear-pole-source-pipeline/v1','arithmetic_acceptance':False,'files':files,'external_inputs':external})
    print(json.dumps({'status':'PASS','files':len(files),'external_inputs':len(external),'manifest_sha256':sha(HERE/'manifest.json')}))
if __name__=='__main__':main()
