"""Freeze an explicit release copy plan from caller-selected verified inputs."""
import argparse,json
from pathlib import Path
from common import *

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('selection','source-run','pipeline','repository','final-artifact','final-checker','arithmetic-review','output'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--cleanup-packet',type=Path)
    a=p.parse_args();s=selection(load(a.selection));runtime=Path(__file__).resolve().parent
    runtime_manifest=load(runtime/'MANIFEST.json');manifest_files(runtime,runtime_manifest)
    roots=dict(source=a.source_run.resolve(),pipeline=a.pipeline.resolve(),repository=a.repository.resolve(),
        final=a.final_artifact.resolve(),checker=a.final_checker.resolve().parent,
        review=a.arithmetic_review.resolve().parent,selection=a.selection.resolve().parent,runtime=runtime)
    source=roots['source'];pipeline=roots['pipeline'];final=roots['final']
    need(sha(pipeline/'manifest.json')==s['source_pipeline_manifest_sha256'],'Pipeline pin')
    packet=load(pipeline/'manifest.json');manifest_files(pipeline,packet)
    need(len(packet['external_inputs'])==13,'Changed external input closure')
    for item in packet['external_inputs']:need(sha(child(roots['repository'],item['path']))==item['sha256'],'External input pin')
    summary=load(source/'SUMMARY.json');need(summary['status']=='ALGEBRAIC CANDIDATE VERIFIED','Incomplete source run')
    need(summary['manifest_sha256']==s['source_pipeline_manifest_sha256'],'Source run packet differs')
    entry_path=source/'adapter/source-entry.json';entry=load(entry_path)
    need(sha(entry_path)==s['source_entry_sha256'],'Source entry pin')
    need(entry['source_sha256']==s['source_archive_sha256'],'Source archive entry pin')
    base=source/'adapter/verify_named_source.py'
    need(sha(base)==s['base_checker_sha256'],'Base checker pin');inspect_registry(base,entry)
    need(sha(a.final_checker)==s['final_checker_sha256'],'Final checker pin');inspect_registry(a.final_checker,entry)
    need(sha(a.arithmetic_review)==s['arithmetic_review_sha256'],'Arithmetic review pin')
    need(entry['source_id'] in a.arithmetic_review.read_text(encoding='utf-8'),'Review does not name selected source')
    report=load(final/'verification.json');expected=expected_report(report,entry,s)
    for field,key in [('source_id',None),('source_sha256','source_archive_sha256'),('checker_sha256','final_checker_sha256'),
                      ('certificate_sha256','final_certificate_sha256'),('expanded_sha256','final_expansion_sha256')]:
        need(report[field]==(entry['source_id'] if key is None else s[key]),'Final report pin: '+field)
    for name,key in [('source-residuals.jsonl.gz','source_archive_sha256'),('certificate.jsonl.gz','final_certificate_sha256'),
                     ('polynomial.expanded.txt','final_expansion_sha256')]:
        need(sha(final/name)==s[key],'Final file pin: '+name)
    inspect_certificate(final/'certificate.jsonl.gz',entry,s['source_entry_sha256'])
    for name,key in [('source-audit.json','source_audit_sha256'),('construction-map.json','construction_map_sha256'),('source-layout.json','source_layout_sha256')]:
        need(sha(source/'adapter'/name)==entry[key],'Adapter metadata pin: '+name)
    need(sha(pipeline/'check_source.py')==entry['source_audit_checker_sha256'],'Source auditor pin')
    for name,pin_value in entry['inspected_files_sha256'].items():need(sha(child(source/'source',name))==pin_value,'Inspected source file: '+name)
    cleanup=None
    if s['cleanup_manifest_sha256'] is not None:
        need(a.cleanup_packet is not None,'Cleanup root required');roots['cleanup']=a.cleanup_packet.resolve();cleanup=roots['cleanup']
        need(sha(cleanup/'MANIFEST.json')==s['cleanup_manifest_sha256'],'Cleanup manifest pin')
        manifest_files(cleanup,load(cleanup/'MANIFEST.json'))
        need(sha(cleanup/'inputs/base-checker.py')==s['base_checker_sha256'],'Cleanup base checker')
        need(sha(cleanup/'tools/verify_elimination.py')==s['final_checker_sha256'],'Cleanup final checker')
        need(load(cleanup/'BINDING.json')['source_id']==entry['source_id'],'Cleanup source identity')
        need(load(cleanup/'BINDING.json')['explicit_input_pins']['source_entry']==s['source_entry_sha256'],'Cleanup entry identity')
    else:need(a.cleanup_packet is None,'Unselected cleanup root')
    rows=[];destinations=set()
    def add(family,name,destination,pinned=None):
        path=child(roots[family],name);need(path.is_file(),'Missing input '+name)
        need(destination.casefold() not in destinations,'Duplicate destination');destinations.add(destination.casefold())
        digest=sha(path);need(pinned is None or pinned==digest,'Copy pin '+name)
        rows.append(dict(input=family,source=name,destination=destination,sha256=digest,bytes=path.stat().st_size))
    for name in CANDIDATE:add('final',name,name)
    add('final','verification.json','evidence/final-verification.json')
    add('checker',a.final_checker.name,'verify_certificate.py',s['final_checker_sha256'])
    add('review',a.arithmetic_review.name,'evidence/arithmetic-source-review.md',s['arithmetic_review_sha256'])
    add('selection',a.selection.name,'reproducibility/selection.json')
    for name in ('source-entry.json','source-audit.json','construction-map.json','source-layout.json'):
        add('source','adapter/'+name,name)
    for name,pin_value in entry['inspected_files_sha256'].items():add('source','source/'+name,'source/'+name,pin_value)
    add('source','adapter/verify_named_source.py','reproducibility/base/verify_named_source.py',s['base_checker_sha256'])
    add('source','adapter/adapter-manifest.json','reproducibility/base/adapter-manifest.json')
    for name,pin_value in load(source/'adapter/adapter-manifest.json')['generated_sha256'].items():
        if name!='verify_named_source.py':add('source','adapter/'+name,'reproducibility/base/'+name,pin_value)
    for name,item in packet['files'].items():add('pipeline',name,'reproducibility/pipeline/'+name,item['sha256'])
    add('pipeline','manifest.json','reproducibility/pipeline/manifest.json',s['source_pipeline_manifest_sha256'])
    for item in packet['external_inputs']:add('repository',item['path'],'reproducibility/external-repository/'+item['path'],item['sha256'])
    for name in ('SUMMARY.json','RUN_INPUTS.json','source-mutations.json','inherited-source-mutations.json','named-source-mutations.json','source-determinism.json','proxy-removal-guards.json'):
        add('source',name,'evidence/source-run/'+name)
    for name in ('fresh-lift','parity','optimized','coordinates'):
        add('source','stages/'+name+'/verification.json','evidence/base-stages/'+name+'.json')
    if cleanup:
        for name,item in load(cleanup/'MANIFEST.json')['files'].items():add('cleanup',name,'reproducibility/cleanup/'+name,item['sha256'])
        add('cleanup','MANIFEST.json','reproducibility/cleanup/MANIFEST.json',s['cleanup_manifest_sha256'])
    for name,item in runtime_manifest['files'].items():
        add('runtime',name,'README.md' if name=='ROOT_README.md' else 'reproducibility/'+name,item['sha256'])
    add('runtime','MANIFEST.json','reproducibility/runtime-manifest.json')
    expected.update(source_id=entry['source_id'],source_sha256=s['source_archive_sha256'],
        checker_sha256=s['final_checker_sha256'],certificate_sha256=s['final_certificate_sha256'],expanded_sha256=s['final_expansion_sha256'])
    plan=dict(format='quartic-release-copy-plan/v2',expected=expected,files=rows,
        recipe=dict(profile='target2-tangent-first-norm/v1',selection=s,cleanup=cleanup is not None),
        source_arithmetic_acceptance=False,scope='Exact finite reproduction; separate pinned arithmetic review')
    need(not a.output.exists(),'Copy plan output must be fresh');a.output.parent.mkdir(parents=True,exist_ok=True);save(a.output,plan)
    print(json.dumps(dict(status='COPY PLAN FROZEN; no replay performed',files=len(rows),plan_sha256=sha(a.output))))
if __name__=='__main__':main()
