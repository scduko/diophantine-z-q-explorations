"""Verify every file in a Version 9 supplement before optionally extracting it."""
import argparse,hashlib,json,zipfile
from pathlib import Path,PurePosixPath

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive',type=Path)
    ap.add_argument('--sha256',required=True,help='Archive digest from the repository SHA256SUMS')
    ap.add_argument('--extract',type=Path)
    a=ap.parse_args()
    if hashlib.sha256(a.archive.read_bytes()).hexdigest()!=a.sha256:
        raise ValueError('Archive digest differs')
    with zipfile.ZipFile(a.archive) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive paths')
        for name in names:
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
                raise ValueError('Unsafe member path')
        manifest=json.loads(z.read('MANIFEST.json'))
        if set(names)!=set(manifest['files'])|{'MANIFEST.json'}:raise ValueError('File coverage differs')
        for name,expected in manifest['files'].items():
            if hashlib.sha256(z.read(name)).hexdigest()!=expected:raise ValueError('File digest differs: '+name)
        if a.extract:
            if a.extract.exists():raise ValueError('Extraction directory must be new')
            a.extract.mkdir(parents=True)
            z.extractall(a.extract)
    print(json.dumps({'status':'PASS','files':len(names)-1,'scope':manifest['scope']}))

if __name__=='__main__':main()
