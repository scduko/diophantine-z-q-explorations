"""Bounded remote runner for a prepared combined-source research adapter.

Invoke only inside the root agent's established guarded remote job. Each
candidate must pass its named-source checker before the next stage runs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--stage-seconds', type=int, default=300)
    p.add_argument('--optimize', action='store_true')
    a=p.parse_args()
    assert 1<=a.stage_seconds<=1200
    a.adapter=a.adapter.resolve(); a.output=a.output.resolve()
    manifest=json.loads((a.adapter/'adapter-manifest.json').read_bytes())
    for relative,digest in manifest['generated_sha256'].items():
        assert hashlib.sha256((a.adapter/relative).read_bytes()).hexdigest()==digest, relative
    a.output.mkdir(parents=True,exist_ok=False)
    tools=a.adapter/'tools'; checker=a.adapter/'verify_named_source.py'
    steps=[]; started=time.monotonic()
    def run(script,*args):
        command=[sys.executable,str(script),*map(str,args)]
        print(json.dumps(dict(run=command)),flush=True)
        before=time.monotonic()
        try:
            result=subprocess.run(command,cwd=a.adapter,timeout=a.stage_seconds,check=False)
        except subprocess.TimeoutExpired:
            steps.append(dict(command=command,exit=None,status='TIMEOUT: NOT VERIFIED',seconds=round(time.monotonic()-before,3)))
            (a.output/'progress.json').write_text(json.dumps(steps,indent=2)+'\n')
            raise
        steps.append(dict(command=command,exit=result.returncode,seconds=round(time.monotonic()-before,3)))
        (a.output/'progress.json').write_text(json.dumps(steps,indent=2)+'\n')
        assert result.returncode==0, ('Failed stage; no continuation',command)
    def verify(candidate):
        run(checker,candidate)
        report=json.loads((candidate/'verification.json').read_bytes())
        assert report['status']=='PASS' and report['source_id']==manifest['source_id']
        assert report['degree']<=4 and report['max_abs_coefficient']<2**80
        return report
    current=a.output/'fresh-lift'
    run(tools/'fresh_lift.py','--adapter',a.adapter,'--output',current)
    final_verified=verify(current)
    for name,script in [('norms','reduce_norms.py'),('charts','replace_charts.py'),
                        ('ordinates','remove_chart_ordinates.py'),('parity','produce_parity.py'),
                        ('batch','absorb_batch_error.py')]:
        target=a.output/name
        options=['--adapter' if name=='norms' else '--repo',a.adapter,'--parent',current,'--output',target]
        if name=='charts':
            options+=['--diagnostic',a.output/'chart-diagnostic.json']
        run(tools/script,*options); final_verified=verify(target); current=target
    if a.optimize:
        target=a.output/'optimized'
        run(tools/'optimize.py','--parent',current,'--output',target,'--max-terms','96','--rounds','8',
            '--rational','--gaussian','--row-combine','--row-order','reverse')
        final_verified=verify(target); current=target
        target=a.output/'coordinates'
        run(tools/'merge_coordinates.py','--parent',current,'--output',target)
        final_verified=verify(target); current=target
    report=dict(status='ALL REQUESTED ALGEBRAIC STAGES VERIFIED; ARITHMETIC ACCEPTANCE REMAINS SEPARATE',
                source_id=manifest['source_id'],last_verified_candidate=str(current),
                verified_variables=final_verified['variables'],
                verified_max_abs_coefficient=final_verified['max_abs_coefficient'],
                verification_sha256=hashlib.sha256((current/'verification.json').read_bytes()).hexdigest(),
                seconds=round(time.monotonic()-started,3),steps=steps)
    (a.output/'SUMMARY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
