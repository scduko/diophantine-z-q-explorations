"""Run the pinned independent tangent probe with packet-local input paths.

Only five file-path expressions in its main function are substituted. The
literal checker, mutation logic, expected counts and assertion guard are
loaded byte-for-byte from the independently reviewed helper.
"""
if not __debug__:
    raise RuntimeError('Assertions required')
import ast
import hashlib
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
PIN='75299d5a1118dd7d75892786079003cd8588dc0b814017ae33c82672d00b80b0'

def main():
    path=HERE/'probe_tangents.py'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('pinned_tangent_probe',path)
    probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
    text=path.read_text(encoding='utf-8')
    node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    body=ast.get_source_segment(text,node)
    substitutions={
        "base=Path(__file__).resolve().parents[3]":"base=Path(__file__).resolve().parent",
        "base/'charts/sub5000/half-generator-review/audit_root_rewrite.py'":"base/'audit_root_rewrite.py'",
        "base/'charts/sub5000/root-target2/audit_target2.py'":"base/'audit_target2.py'",
        "base/'elimination/sub5000/doubling-target-two/compress_doublings.py'":"base/'compress_doublings.py'",
        "base/'charts/sub5000/root-target2/FIXED_TARGET2.json'":"base/'FIXED_TARGET2.json'",
    }
    for old,new in substitutions.items():
        assert body.count(old)==1,old
        body=body.replace(old,new)
    namespace=dict(probe.__dict__)
    exec(compile(body,'<packet-local-pinned-tangent-probe>','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
