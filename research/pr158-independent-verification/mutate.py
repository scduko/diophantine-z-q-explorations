"""Negative controls: each mutation of a copy of the package must make verify_pr158.py fail."""
import json, shutil, subprocess, sys, tempfile, pathlib
pkg, here = pathlib.Path(sys.argv[1]), pathlib.Path(__file__).resolve().parent
inputs = ['--v19', sys.argv[2], '--brox', sys.argv[3], '--main', sys.argv[4]]
def edit_json(path, fn):
    d = json.load(open(path)); fn(d); open(path, 'w').write(json.dumps(d))
def bump(t): t['coefficient'] = str(int(t['coefficient']) + 1)
muts = {
  'final quadratic coefficient +1': ('quadratic.json', lambda d: bump(d['residuals'][100]['terms'][0])),
  'expanded coefficient +1': ('polynomial.json', lambda d: bump(d['terms'][1234])),
  'transformation exponent changed': ('transformation.json', lambda d: d['coordinate_powers'].__setitem__(104, d['coordinate_powers'][104] + 1)),
  'paper row-exponent table edited': ('paper.tex', None),
  'literal text: one digit changed': ('quartic229-N15.txt', None),
  'source table row edited (caught by hash pins)': ('source/quadratic229-v62.json', lambda d: bump(d['residuals'][23]['terms'][0])),
}
fails = 0
for name, (f, fn) in muts.items():
    with tempfile.TemporaryDirectory() as tmp:
        cp = pathlib.Path(tmp) / 'pkg'; shutil.copytree(pkg, cp)
        target = cp / f
        if f == 'paper.tex':
            s = target.read_text(); target.write_text(s.replace('-18 & 50', '-18 & 51', 1))
        elif f.endswith('.txt'):
            b = bytearray(target.read_bytes()); i = b.index(b'7'); b[i] = ord('8'); target.write_bytes(bytes(b))
        else:
            edit_json(target, fn)
        r = subprocess.run([sys.executable, '-I', '-B', str(here / 'verify_pr158.py'), '--pkg', str(cp)] + inputs, capture_output=True, text=True)
        first = next((l for l in r.stdout.splitlines() if l.startswith('FAIL')), r.stderr.strip()[-120:])
        print(('REJECTED' if r.returncode else 'ACCEPTED!'), '|', name, '|', first)
        fails += r.returncode == 0
sys.exit(1 if fails else 0)
