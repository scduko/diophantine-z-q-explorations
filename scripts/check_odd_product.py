"""Rebuild and check both odd-product sources without mutating pinned inputs."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'quartics/quartic-523-540'

def snapshot():
    return {p.relative_to(PACKAGE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PACKAGE.rglob('*')) if p.is_file()}

def run(cmd, out, env):
    with out.open('wb') as log:
        subprocess.run(cmd, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default=shutil.which('node'))
    parser.add_argument('--out', type=Path, default=ROOT/'build/odd-product')
    args = parser.parse_args()
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Run the exact certificate checkers without Python -O')
    if not args.node:
        parser.error('Node is required for source regeneration; pass --node PATH')
    out=args.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    if out.is_relative_to(PACKAGE):
        raise ValueError('Output directory must not be inside the pinned package')
    env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUTF8']='1'
    env['ODD_PRODUCT_OUTPUT']=str(out)
    before=snapshot()
    run([sys.executable, '-B', str(PACKAGE/'source-reproduction/reproduce.py'),
         '--node', args.node, '--packages', str(PACKAGE), '--work', str(out/'replay')],
        out/'source-replay.log', env)
    # Replay each final verifier again to catch mutation-on-first-run regressions.
    for name in ['final554_571','final523_540']:
        run([sys.executable,'-B',str(PACKAGE/name/'verify_all.py')],out/(name+'-second-run.log'),env)
    run([sys.executable,'-B',str(ROOT/'docs/quartic-523-540/independent_finite.py')],out/'independent-finite.log',env)
    run([sys.executable,'-B',str(ROOT/'docs/quartic-523-540/check_identities.py')],out/'identities.log',env)
    if snapshot()!=before:
        raise ValueError('A checker changed pinned input files')
    # Compare the convenient downloads with the complete JSON coefficient tables.
    for count, kind, rel in [
        (523,'symbolic-coefficients','symbolic523'),
        (540,'fully-expanded','ordinary540')]:
        raw=json.loads((PACKAGE/'final523_540'/rel/'polynomial/polynomial.json').read_bytes())
        terms=raw['terms']
        actual={}
        for line in (ROOT/f'quartics/quartic-{count}-{kind}.txt').read_text().splitlines():
            if not line or line.startswith('#'): continue
            tokens=line.split(); c=tokens[0]; sp=0
            if '*S' in c:
                c,s=c.split('*S'); sp=int(s[1:]) if s else 1
            key=(sp,tuple(map(int,tokens[1:])))
            if key in actual: raise ValueError('Duplicate monomial in download')
            actual[key]=int(c)
        expected={(t.get('sPower',0),tuple(t['monomial'])):int(t['coefficient']) for t in terms}
        if actual!=expected: raise ValueError('Text coefficient download does not match '+str(count))
    if (ROOT/'quartics/quartic-523-symbolic-coefficients.json').read_bytes() != (
        PACKAGE/'final523_540/symbolic523/polynomial/polynomial.json').read_bytes():
        raise ValueError('Symbolic JSON download differs')
    report={'status':'PASS','source_rebuilt':True,'final_verifier_runs_per_package':2,
            'input_files_unchanged':True,'independent_sparse_ring_check':True,
            'text_downloads_match':True,'arithmetic_theorem_proved_by_this_script':False}
    (out/'CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
