"""Hash the explicit runtime file set after its bounded tests pass."""
if not __debug__:raise RuntimeError('Assertions required')
from pathlib import Path
from common import load,save,sha,need,PIPELINE_SHA

def main():
    root=Path(__file__).resolve().parent
    files=('common.py','plan_release.py','prepare_package.py','run.py','test_binding.py',
           'freeze_runtime.py','README.md','ROOT_README.md','BINDING_TESTS.json')
    need(load(root/'BINDING_TESTS.json')['status']=='PASS','Run bounded tests first')
    need(sha(root/'prepare_package.py')=='2a009fdb951329418aa384b3bc54b0e06faf187b87eb3b70f647cd047750e173','Reviewed installer changed')
    obj=dict(format='quartic-release-runtime/v1',source_pipeline_manifest_sha256=PIPELINE_SHA,
        scope='Runtime and copy-plan tooling only; final selection and full remote reproduction remain required',
        files={name:dict(sha256=sha(root/name),bytes=(root/name).stat().st_size) for name in files})
    save(root/'MANIFEST.json',obj);print(sha(root/'MANIFEST.json'))
if __name__=='__main__':main()
