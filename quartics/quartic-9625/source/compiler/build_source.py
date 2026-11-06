"""Build the selective beta-only proposal from the exact measured high40 source."""
import argparse,hashlib,importlib.util,json,shutil,sys
from pathlib import Path
import beta_kernel
HERE=Path(__file__).resolve().parent
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def configure(b):
    b.CURVE_DROOT=(3,-1);b.CURVE_D2=(11,-6)
    b.BASE_POINT=((b.F(57,8),b.F(-7,2)),(b.F(-165,8),b.F(417,32)))
    b.CHART=10;b.PARITY=7;b.LOG_BLOCK=2;b.BASE_GATES=True;b.UNIT_SCALE=True
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    pins=json.loads((HERE/'BASELINE.json').read_bytes())
    for relative,pin in pins['files'].items():assert digest(a.baseline/relative)==pin,relative
    compiler=a.baseline/'compiler'
    def fresh(tag):
        b=load(compiler/'archive_build.py',tag+'_builder');configure(b)
        c=load(compiler/'combined_kernel.py',tag+'_combined');low=load(compiler/'lowprecision_kernel.py',tag+'_low')
        return b,c,low
    b,c,low=fresh('baseline');c.install(b,low.emit_g,high=40,label=12)
    b.write=lambda name,data:None
    b.make_parity();b.make_anchor();b.make_batch('q_batch41',[1]*23+[40]*18,'q_primeparity')
    b.make_batch('q_height_batch',[1]*4+[48]*2,'q_primeparity');b.make_multi_comparison();b.make_root()
    originals={name:json.loads((a.baseline/'modules'/(name+'.json')).read_bytes()) for name in pins['modules']}
    assert b.MODULES==originals,'Measured baseline modules did not regenerate exactly'
    b,c,low=fresh('selective');beta_kernel.install(b,c,low)
    a.out.mkdir(parents=True,exist_ok=False)
    sys.argv=[str(compiler/'archive_build.py'),'--out',str(a.out.resolve()),'--chart','10','--parity','7','--base-gates','--unit-scale','--log-block','2']
    b.main()
    for name in pins['modules']:
        if name!='Z_definition':assert b.MODULES[name]==originals[name],name
    destination=a.out/'compiler';destination.mkdir();hashes={}
    for path in [compiler/'archive_build.py',compiler/'combined_kernel.py',compiler/'lowprecision_kernel.py',HERE/'beta_kernel.py',Path(__file__)]:
        shutil.copyfile(path,destination/path.name);hashes[path.name]=digest(path)
    contract=dict(source_family='H19-root37-selective-beta12-high40-v1',arithmetic_acceptance=False,source_pin_authorized=False,
      high=40,label=12,anchor_squarings=25,scalar_orders=[1,1,1,1,32,32],height_exponent=19,
      beta_only_positions=beta_kernel.POSITIONS,full_positions=[i for i in range(37) if i not in beta_kernel.POSITIONS],
      beta_input_selection=beta_kernel.SELECTION,beta_rational_orders=beta_kernel.ORDERS,
      baseline_source_id=pins['source_id'],baseline_source_sha256=pins['source_sha256'],
      baseline_module_sha256=pins['modules'],compiler_sha256=hashes,
      scope='New arithmetic source requiring selective-contact proof; no old-source projection equivalence asserted')
    (a.out/'BETA_SOURCE.json').write_text(json.dumps(contract,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(contract,indent=2))
if __name__=='__main__':main()
