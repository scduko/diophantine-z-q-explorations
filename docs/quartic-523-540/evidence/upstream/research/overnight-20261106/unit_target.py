"""Experimental shift-one targets; reuses the frozen V6 generator and checker."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('v6_experiment',ROOT/'research/v6-comparison/explore.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
original=v.variant

def direct_targets(s,level):
 if level!=4:raise ValueError('Use --only 4 for this experiment')
 s=original(s,level)
 s=v.h.replace_once(s,"let four={P:double('P2',P)};for(let n of ['A','S','T','Z'])four[n]=double(n+'2',points[n]);","let four={P};for(let n of ['A','S','T','Z'])four[n]=points[n];")
 s=v.h.replace_once(s,"start('doubled_targets',[2394,2399]);","start('direct_targets',[2394,2399]);")
 return s

if __name__=='__main__':
 v.variant=direct_targets
 v.main()
