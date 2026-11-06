"""Small negative tests for Version3 inventory metadata; no polynomial replay."""
import argparse,copy,hashlib,importlib.util,json,shutil,sys,tempfile
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();repo=a.repo.resolve();docs=repo/'docs/quartic-9625'
    sys.path.insert(0,str(docs))
    spec=importlib.util.spec_from_file_location('version3_inventory_validator',docs/'validate.py')
    validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
    baseline=validator.validate(repo);cases=[]
    def mutate(name,filename,change,wanted):
        with tempfile.TemporaryDirectory(prefix='v3-inventory-negative-') as temp:
            target=Path(temp)/'docs';shutil.copytree(docs,target)
            file=target/filename
            value=json.loads(file.read_text(encoding='utf-8-sig'));change(value)
            file.write_text(json.dumps(value,ensure_ascii=False)+'\n',encoding='utf-8')
            try:validator.validate(repo,target)
            except ValueError as error:
                if str(error)!=wanted:raise RuntimeError(name+': wrong rejection: '+str(error)) from error
                cases.append(name);return
            raise RuntimeError(name+': malformed inventory accepted')
    inv='theorem-applications.json'
    mutate('drop arithmetic node',inv,lambda x:x['arithmetic_lemmas'].pop(),'Dropped/added arithmetic lemma')
    mutate('change height statement',inv,lambda x:x['arithmetic_lemmas'][0].update(statement='False substituted statement'),
           'Changed arithmetic statement/dependencies V3_H19')
    mutate('drop published application',inv,lambda x:x['additional_published_applications'].pop(),'Dropped published application')
    mutate('drop inherited application',inv,lambda x:x['inherited_applications'].pop(),'Changed inherited applications')
    mutate('drop retained algebraic rule',inv,lambda x:x['retained_algebraic_lemmas'].pop(),'Dropped retained algebraic rule')
    mutate('erase source version limits',inv,lambda x:x.update(source_version_requirements=[]),'Lost source-version qualification')
    mutate('wrong finite target',inv,lambda x:x['certificate_binding'].update(variables=9624),'Wrong finite target')
    mutate('drop dependency edge','dependency-closure.json',lambda x:x['edges'].pop(),'Dependency edge set changed')
    mutate('duplicate dependency edge','dependency-closure.json',lambda x:x['edges'].append(copy.deepcopy(x['edges'][0])),'Dependency edge set changed')
    mutate('drop historical anchor','baseline-bridge.json',lambda x:x['anchors'].pop(),'Historical anchor coverage')
    mutate('drop historical citation','baseline-bridge.json',lambda x:x['citation_paragraphs'].pop(),'Historical citation coverage')
    mutate('change historical scope','baseline-bridge.json',lambda x:x['anchors'][0].update(earlier_review_scope_preserved=False),'Historical anchor retargeted')
    mutate('wrong registry target','inventory-spec.json',lambda x:x.update(source_id='old-source'),'Inventory specification changed')
    mutate('unapproved layout change','layout-transform.json',lambda x:x['transformations'][0].update(new='changed formula'),
           'Unapproved proof layout transformation')
    result=dict(status='PASS',baseline=baseline,malformed_cases=cases,count=len(cases),
                validator_sha256=hashlib.sha256((docs/'validate.py').read_bytes()).hexdigest(),
                scope='Metadata/binding rejection tests only; source and quartic replay are separate')
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',count=len(cases))))
if __name__=='__main__':main()
