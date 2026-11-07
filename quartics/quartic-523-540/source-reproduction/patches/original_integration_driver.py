from pathlib import Path
import importlib.util,shutil,sys
HERE=Path(__file__).resolve().parent
ARCH=HERE.parent
TASK=ARCH.parent

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def build(base,out):
 s=(base/'build_source.cjs').read_text()
 s=load('odd_chart',ARCH/'odd_chart/patch.py').patch(s)
 s=load('product_scales',HERE/'patch_product_scales.py').patch(s)
 s=load('odd_scalar',ARCH/'integer_encoding/odd_scalar_patch.py').patch(s)
 out.mkdir(exist_ok=True);shutil.copytree(base/'sources',out/'sources',dirs_exist_ok=True)
 (out/'build_source.cjs').write_text(s)
 print(out)

if __name__=='__main__':
 base=TASK/'circuit/laurent_noy_scalar'
 out=HERE/'integrated'
 if len(sys.argv)>1 and sys.argv[1]=='asymmetric':
  base=ARCH/'logarithms/candidate';out=HERE/'integrated_asymmetric'
 build(base,out)
