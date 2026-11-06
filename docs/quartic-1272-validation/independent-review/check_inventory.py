"""Run the authored inventory validator read-only and retain its exact inputs."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / 'repository'
INVENTORY = REPO / 'docs/quartic-1272'
EXPECTED_INPUT = '695769c38917efa35b6256132cd8b77807d6384ab6d27c38f250ff8947ae6c10'

def digest(path): return sha256(path.read_bytes()).hexdigest()
def pins():
    paths = [REPO/'quartic_1272.tex'] + sorted(INVENTORY.glob('*.json')) + [INVENTORY/'inventory.py']
    return {p.relative_to(REPO).as_posix(): digest(p) for p in paths}

def main():
    before = pins()
    assert before['docs/quartic-1272/new-applications.json'] == EXPECTED_INPUT
    args = [sys.executable, '-E', '-B', str(INVENTORY/'inventory.py'), 'validate', '--repo', str(REPO),
            '--expected-input-sha256', EXPECTED_INPUT]
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8')
    (HERE/'inventory-validation.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    after = pins()
    receipt = {'status': 'PASS' if result.returncode == 0 and before == after else 'FAIL',
               'scope': 'Execution of the authored read-only inventory validator, with an externally selected input-register hash and before/after file pins.',
               'exitCode': result.returncode, 'inputsUnchangedDuringValidation': before == after,
               'inputPins': before, 'log': 'inventory-validation.log'}
    (HERE/'inventory-validation.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))
    return result.returncode or (0 if before == after else 1)

if __name__ == '__main__': sys.exit(main())
