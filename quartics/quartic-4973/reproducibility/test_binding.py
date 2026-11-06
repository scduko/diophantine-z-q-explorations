"""Bounded metadata, parser and installer tests; never generate a research source."""
if not __debug__:raise RuntimeError('Assertions required')
import argparse,ast,copy,gzip,json,subprocess,sys,tempfile
from pathlib import Path
from common import *

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pipeline',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args();failures=[];accepted=[]
    def rejects(name,fn):
        try:fn()
        except (ValueError,AssertionError,KeyError,SyntaxError,TypeError,FileNotFoundError):failures.append(name)
        else:raise AssertionError('Invalid fixture accepted: '+name)
    with tempfile.TemporaryDirectory(prefix='quartic-release-bindings-') as tmp:
        root=Path(tmp);checker=root/'checker.py'
        s={k:'a'*64 for k in SELECTION_KEYS};s.update(format='quartic-release-selection/v1',source_pipeline_manifest_sha256=PIPELINE_SHA,cleanup_manifest_sha256=None)
        assert selection(s)==s;accepted.append('explicit selection')
        for field in sorted(SELECTION_KEYS-{'format','cleanup_manifest_sha256'}):
            bad=copy.deepcopy(s);bad[field]=None;rejects('missing pin '+field,lambda bad=bad:selection(bad))
        for name,delta in [('extra key',{'guessed_count':1}),('wrong format',{'format':'other'}),('short hash',{'source_entry_sha256':'a'}),('uppercase hash',{'source_entry_sha256':'A'*64}),('unreviewed family',{'source_pipeline_manifest_sha256':'b'*64}),('unbound extension',{'final_checker_sha256':'b'*64})]:
            bad=dict(s,**delta);rejects(name,lambda bad=bad:selection(bad))
        for name in ('../x','x/../y','/x','C:/x','x\\y','x//y','x/./y',''):
            rejects('path '+repr(name),lambda name=name:child(root,name))
        entry={'source_id':'synthetic-source','source_sha256':'a'*64}
        original=dict(source_sha256='6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2',source_variables=15672,source_rows=15107)
        values={'original64':original,'synthetic-source':entry}
        text='SOURCE_ENTRIES = '+repr(values)+'\n';checker.write_text(text)
        inspect_registry(checker,entry);accepted.append('exact two-entry registry')
        for name,text_bad in [('semicolon',text.strip()+'; sneaky = 1\n'),('chained assignment','alias = '+text),('duplicate registry',text+text),('annotated registry','SOURCE_ENTRIES: dict = '+repr(values)),('computed registry','SOURCE_ENTRIES = dict()\n')]:
            checker.write_text(text_bad);rejects(name,lambda:inspect_registry(checker,entry))
        for name,delta in [('extra source',{'third':{}}),('wrong selected entry',{'synthetic-source':{}}),('wrong historical entry',{'original64':{}})]:
            checker.write_text('SOURCE_ENTRIES = '+repr(dict(values,**delta)));rejects(name,lambda:inspect_registry(checker,entry))
        certificate=root/'certificate.jsonl.gz'
        def cert(obj):certificate.write_bytes(gzip.compress((json.dumps(obj)+'\n').encode(),mtime=0))
        cert(dict(source_id=entry['source_id'],source_entry_sha256='a'*64));inspect_certificate(certificate,entry,'a'*64);accepted.append('exact certificate header')
        for name,obj in [('wrong certificate source',dict(source_id='other',source_entry_sha256='a'*64)),('wrong certificate entry',dict(source_id=entry['source_id'],source_entry_sha256='b'*64))]:
            cert(obj);rejects(name,lambda:inspect_certificate(certificate,entry,'a'*64))
        report=dict(status='PASS',variables=2,witnesses=1,rows=1,degree=4,monomials=1,max_abs_coefficient=1,expanded_bytes=1,compressed_bytes=1,source_id=entry['source_id'],source_sha256='a'*64,checker_sha256='a'*64,certificate_sha256='a'*64,expanded_sha256='a'*64)
        assert expected_report(report,entry,s)['variables']==2;accepted.append('counts derived from report')
        for name,delta in [('non-pass',{'status':'FAIL'}),('boolean count',{'variables':True}),('float count',{'rows':1.0}),('zero rows',{'rows':0}),('input omitted',{'witnesses':2}),('threshold',{'variables':5000,'witnesses':4999}),('coefficient bound',{'max_abs_coefficient':2**80}),('wrong degree',{'degree':3}),('report source',{'source_id':'other'}),('report checker',{'checker_sha256':'b'*64}),('report certificate',{'certificate_sha256':'b'*64}),('report expansion',{'expanded_sha256':'b'*64})]:
            rejects(name,lambda delta=delta:expected_report(dict(report,**delta),entry,s))
        sample=root/'x';sample.write_text('sample')
        record={'files':{'x':dict(bytes=sample.stat().st_size,sha256=sha(sample))}}
        manifest_files(root,record);accepted.append('exact manifest file')
        for name,obj in [('empty files',{'files':{}}),('wrong bytes',{'files':{'x':dict(bytes=0,sha256=sha(sample))}}),('wrong file hash',{'files':{'x':dict(bytes=sample.stat().st_size,sha256='b'*64)}}),('missing file',{'files':{'absent':dict(bytes=0,sha256='b'*64)}})]:
            rejects(name,lambda obj=obj:manifest_files(root,obj))
        # Exercise the unchanged installer on one tiny file, including its exact
        # output-manifest/copy-plan convention. This performs no source replay.
        plan={'format':'quartic-release-copy-plan/v2','expected':{},'recipe':{},'files':[dict(input='tiny',source='x',destination='reproducibility/x',bytes=sample.stat().st_size,sha256=sha(sample))]}
        plan_path=root/'plan.json';save(plan_path,plan);target=root/'package'
        cmd=[sys.executable,'-E','-B',str(Path(__file__).with_name('prepare_package.py')),'--plan',str(plan_path),'--input','tiny='+str(root),'--output',str(target)]
        result=subprocess.run(cmd,capture_output=True,timeout=10);assert result.returncode==0,result.stderr
        manifest_files(target,load(target/'reproducibility/manifest.json'));accepted.append('unchanged installer tiny copy')
        result=subprocess.run(cmd,capture_output=True,timeout=10);assert result.returncode!=0 and b'Output must be fresh' in result.stderr;failures.append('existing installer output')
        result=subprocess.run([sys.executable,'-E','-B','-O','-c','import common'],cwd=Path(__file__).parent,capture_output=True,timeout=10)
        assert result.returncode!=0 and b'Assertions required' in result.stderr;failures.append('optimized import')
    here=Path(__file__).parent
    for path in here.glob('*.py'):ast.parse(path.read_text(encoding='utf-8'),filename=path.name)
    accepted.append('runtime syntax')
    if args.pipeline:
        def scripts(path):return {n.value for n in ast.walk(ast.parse(path.read_text())) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.endswith('.py')}
        frozen=scripts(args.pipeline/'run_candidate.py')-{'run_pipeline.py','tools/run_pipeline.py'}
        current=scripts(here/'run.py')
        assert frozen<=current,sorted(frozen-current)
        for name in frozen:assert (args.pipeline/name).is_file() or name=='compiler/archive_build.py'
        accepted.append('all frozen outer scripts retained')
    result=dict(status='PASS',scope='Synthetic bindings and tiny installer only; no source generation or certificate replay',negative_cases=len(failures),negative_names=failures,positive_checks=accepted)
    if args.report:save(args.report,result)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
