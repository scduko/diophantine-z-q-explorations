"""Locate and render changed manuscript pages for visual inspection."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pdf', type=Path, default=ROOT / 'quartic_1272.pdf')
parser.add_argument('--pypdf', action='store_true', help='Extract text with optional pypdf instead of pdftotext')
parser.add_argument('--pdftoppm', default='pdftoppm', help='Poppler renderer executable')
args = parser.parse_args()
PDF = args.pdf.resolve()
OUT = ROOT / 'build/pdf-review'
OUT.mkdir(parents=True, exist_ok=True)
if args.pypdf:
    from pypdf import PdfReader
    (OUT / 'paper.txt').write_text('\f'.join(page.extract_text() for page in PdfReader(PDF).pages), encoding='utf-8')
else:
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT / 'paper.txt')], check=True)
pages = (OUT / 'paper.txt').read_text(encoding='utf-8').split('\f')
normalized = [re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text)) for text in pages]
starts = [i for i, text in enumerate(normalized) if i > 10 and 'This is the second final polynomial' in text]
ends = [i for i, text in enumerate(normalized) if i > 10 and 'The finite checks do not replace' in text]
assert len(starts) == len(ends) == 1, (starts, ends)
last = max(i for i, text in enumerate(normalized) if text.strip())
theta_pages = [i for i, text in enumerate(normalized) if 'We check every theta convolution term' in text]
selected = sorted(set([0, 1, 2, last] + theta_pages + list(range(starts[0], ends[0] + 1))))
# Inspect every page of the new source and the prime-pattern appendix.
# Match body headings away from the table of contents.
new_starts = [i for i, text in enumerate(normalized) if i > 10 and
              'Arithmetic interfaces for the smaller quartic' in text]
new_ends = [i for i, text in enumerate(normalized) if i > 10 and
            'Dependency order in the arithmetic argument' in text]
sun_starts = [i for i, text in enumerate(normalized) if i > 10 and
              'Simultaneous primes with coprime adjacent norms' in text]
assert len(new_starts) == len(new_ends) == len(sun_starts) == 1, (new_starts, new_ends, sun_starts)
selected = sorted(set(selected + list(range(new_starts[0], new_ends[0] + 1)) +
                      list(range(sun_starts[0], last + 1))))
for index in selected:
    subprocess.run([args.pdftoppm, '-png', '-r', '105', '-singlefile', '-f', str(index + 1),
                    '-l', str(index + 1), str(PDF), str(OUT / f'page-{index + 1:03}')], check=True)
report = {'pages': last + 1, 'changed_quartic_pages': [starts[0] + 1, ends[0] + 1],
          'new_source_pages': [new_starts[0] + 1, new_ends[0] + 1],
          'new_appendix_and_references_pages': [sun_starts[0] + 1, last + 1],
          'pdf_sha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
          'rendered_pages': [i + 1 for i in selected], 'visual_inspection': 'PENDING'}
(OUT / 'rendered.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
