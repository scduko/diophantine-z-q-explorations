"""Prepare a private TeX candidate from explicit accepted endpoint metadata.

No defaults for endpoint values, no polynomial computation, no PDF build,
and no writes to the published checkout. This checks bindings, not proofs.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

BASE = Path(__file__).resolve().parent
WORKSPACE = next(p for p in BASE.parents if (p/'work/quartic-sub10000-20261106').is_dir())
RESEARCH = WORKSPACE/'work/quartic-sub10000-20261106'
APPENDIX = BASE.parent/'publication-draft/revision-3/CONTENT.tex'
PLAN = RESEARCH/'charts/sub5000/publication-review/SPLICE_PLAN.md'
INVENTORY = PLAN.with_name('SPLICE_INVENTORY.json')
PINS = {
    'v3': 'dc77c88b5cc0819201343dc85d0891d4dad81d97ac3267ec1df34eb38003b552',
    'appendix': 'e67b256be73b41fca2e74958ebf0f9749e78f5d98f0c05c06118d3d156defc85',
    'plan': '9c2d96907d294aa212d63d6e6fe8cb1993b64a1b2bce13bc4e37a60640907a9d',
    'inventory': 'e500797a712e7a62294319900da7d5096d95743e9c2926a2bb829268cd4350b0',
}
SELECTION = dict(GeneralRoots=True, TargetTwo=True, TangentFusion=True,
                 SharedSquare=True, FirstNorm=True, ScalarFusion=False)
EVENT_NAMES = {
    'parity_conic': 'height-parity replacements',
    'circuit': 'contact-power circuit replacements',
    'linear': 'invertible linear row operations',
    'eliminate': 'rational definition eliminations',
    'shear': 'invertible rational shears',
    'relation_eliminate': 'eliminations modulo retained equations',
}
ARTIFACTS = ('expanded', 'expanded_gzip', 'source', 'source_entry',
             'source_audit', 'construction_map', 'verification', 'certificate',
             'verifier', 'source_auditor', 'residuals', 'weights', 'variable_map')
SOURCE_EXPECTED = {
    'source_family': 'H19-root37-target2-tangent-first-norm-normalized-linear-pole-v1',
    'comparison_target_multiplier': 2, 'final_root_chart': 'general_E_mixed',
    'root_index_semantics': '2Q=n_Q Pstar, n_Q integer',
    'direct_tangent_doublings': 4, 'first_norm_field_role': 'H.f',
    'first_norm_field_order': 1, 'first_norm_instances': 37,
    'first_norm_virtual_denominator_exponent': 1,
    'first_norm_arithmetic_change': True, 'root_beta_comparison_scale': 2,
    'shared_square_fields': 37, 'high': 40, 'label': 12,
    'anchor_squarings': 25, 'scalar_orders': [1,1,1,1,32,32],
    'height_exponent': 19, 'full_positions': list(range(5))+list(range(21,29)),
    'beta_only_positions': list(range(5,13)),
    'lucas_only_positions': list(range(13,21))+list(range(29,37)),
    'global_lucas_proxies_removed': True, 'normalized_lucas_residual': True,
    'ordinary_pole_module': 'q_linearnormalpole',
    'ordinary_pole_private_coordinates': 10, 'anchor_private_coordinates': 4,
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def gzip_digest(path):
    h = hashlib.sha256(); length = 0
    with gzip.open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            length += len(block)
            need(length <= 128 << 20, 'Compressed artifact exceeds binding-check size limit')
            h.update(block)
    return h.hexdigest(), length


def load_json(path):
    need(path.stat().st_size <= 8 << 20, 'JSON input exceeds binding-check size limit')
    def pairs(items):
        out = {}
        for k,v in items:
            need(k not in out, 'Duplicate JSON key: '+k)
            out[k] = v
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def keys(obj, expected, label):
    need(type(obj) is dict and set(obj) == set(expected), 'Wrong keys: '+label)


def integer(n, label, minimum=1):
    need(type(n) is int and n >= minimum, 'Invalid integer: '+label)


def sha(s):
    need(type(s) is str and re.fullmatch('[0-9a-f]{64}', s), 'Invalid SHA256')


def public_path(s):
    need(type(s) is str and re.fullmatch('[A-Za-z0-9_./-]+', s), 'Unsafe public path')
    p = PurePosixPath(s)
    need(not p.is_absolute() and '..' not in p.parts and str(p) == s, 'Unsafe public path')
    return s


def artifact(record):
    keys(record, ('local_path','public_path','sha256'), 'artifact')
    sha(record['sha256']); public_path(record['public_path'])
    path = Path(record['local_path'])
    need(path.is_absolute() and path.is_file(), 'Artifact must be an existing absolute file')
    need(file_digest(path) == record['sha256'], 'Artifact digest mismatch: '+str(path))
    return path


def validate_metadata(m):
    keys(m, ('schema','release','selection','acceptance','endpoint','source','events',
             'format','artifacts'), 'metadata')
    need(m['schema'] == 'quartic-manuscript-endpoint-v1', 'Wrong metadata schema')
    need(m['selection'] == SELECTION, 'This splice supports only the reviewed selected variant')
    r = m['release']
    keys(r, ('tex_basename','version','date','package_path'), 'release')
    need(re.fullmatch('[A-Za-z0-9_-]+', r['tex_basename']) is not None, 'Invalid basename')
    integer(r['version'], 'version')
    need(re.fullmatch('[A-Za-z]+ [0-9]{1,2}, [0-9]{4}', r['date']) is not None, 'Invalid displayed date')
    public_path(r['package_path'])
    a = m['acceptance']
    keys(a, ('arithmetic_source_accepted','full_source_audit_passed',
             'certificate_expansion_passed','reviews'), 'acceptance')
    for k in ('arithmetic_source_accepted','full_source_audit_passed','certificate_expansion_passed'):
        need(a[k] is True, 'Explicit acceptance is required: '+k)
    keys(a['reviews'], ('arithmetic','source','finite'), 'acceptance reviews')
    for rec in a['reviews'].values():
        artifact(rec)
    e = m['endpoint']
    keys(e, ('variables','witnesses','degree','monomials','rows','max_abs_coefficient',
             'coefficient_bound_exponent','weights_all_one',
             'input_coordinate','expanded_bytes'), 'endpoint')
    for k in ('variables','witnesses','degree','monomials','rows','coefficient_bound_exponent','expanded_bytes'):
        integer(e[k], k)
    need(e['variables'] == e['witnesses']+1 and e['degree'] == 4, 'Witness count or degree mismatch')
    need(e['input_coordinate'] == 0 and type(e['input_coordinate']) is int, 'Input must be coordinate zero')
    need(e['weights_all_one'] is True, 'All-one weight assertion required')
    need(type(e['max_abs_coefficient']) is str and re.fullmatch('[1-9][0-9]*',e['max_abs_coefficient']), 'Coefficient maximum must be a decimal string')
    need(int(e['max_abs_coefficient']) < 2**e['coefficient_bound_exponent'], 'Coefficient maximum exceeds stated strict bound')
    s = m['source']
    keys(s, ('source_id','uncompressed_sha256','variables','rows','module_names'), 'source')
    need(re.fullmatch('[A-Za-z0-9_-]+', s['source_id']) is not None, 'Unsafe source ID')
    sha(s['uncompressed_sha256']); integer(s['variables'],'source variables'); integer(s['rows'],'source rows')
    need(type(s['module_names']) is list and s['module_names'] and len(set(s['module_names'])) == len(s['module_names']), 'Invalid module list')
    need(type(m['events']) is dict and set(m['events']) <= set(EVENT_NAMES), 'Unsupported certificate rule requires an additional reviewed proof')
    for k,v in m['events'].items(): integer(v,'event '+k)
    keys(m['format'], ('expanded','variable_order','circuit_identities'), 'format')
    need(m['format']['expanded'] == 'comment-then-coefficient-sorted-index-list-lex-v1', 'Unsupported coefficient format')
    need(m['format']['variable_order'] == 'occurrence-frequency-input0-v1', 'Unsupported variable ordering')
    expected = ['contact-powers-2-24-80'] if m['events'].get('circuit',0) else []
    need(m['format']['circuit_identities'] == expected, 'Unsupported circuit identity family')
    keys(m['artifacts'], ARTIFACTS, 'artifacts')
    paths = {k:artifact(v) for k,v in m['artifacts'].items()}
    for k in ('expanded','expanded_gzip','source','source_entry','certificate','residuals','weights','variable_map'):
        need(m['artifacts'][k]['public_path'].startswith(r['package_path']+'/'), 'Artifact outside declared package: '+k)
    v = load_json(paths['verification']); entry = load_json(paths['source_entry'])
    need(v['status'] == 'PASS', 'Finite verification did not pass')
    for k in ('variables','witnesses','degree','monomials','rows','expanded_bytes'):
        need(v[k] == e[k], 'Verification mismatch: '+k)
    need(str(v['max_abs_coefficient']) == e['max_abs_coefficient'], 'Verification coefficient mismatch')
    need(v['weights_greater_than_one'] == 0, 'Verification reports nonunit weights')
    need(v['operations'] == m['events'] and v['total_operations'] == sum(m['events'].values()), 'Event census mismatch')
    for field,key in (('expanded_sha256','expanded'),('certificate_sha256','certificate'),('checker_sha256','verifier'),('source_sha256','source')):
        need(v[field] == m['artifacts'][key]['sha256'], 'Verification digest mismatch: '+field)
    need(v['source_id'] == s['source_id'] == entry['source_id'], 'Source name mismatch')
    need(entry['source_sha256'] == m['artifacts']['source']['sha256'], 'Source entry digest mismatch')
    need(entry['uncompressed_sha256'] == s['uncompressed_sha256'], 'Source entry uncompressed digest mismatch')
    need(entry['source_variables'] == s['variables'] and entry['source_rows'] == s['rows'], 'Source counts mismatch')
    need(set(entry['source_header']['modules']) == set(s['module_names']), 'Source module set mismatch')
    for k,x in SOURCE_EXPECTED.items():
        need(entry['proposal'].get(k) == x, 'Selected arithmetic interface mismatch: '+k)
    for field,key in (('source_audit_sha256','source_audit'),('source_audit_checker_sha256','source_auditor'),('construction_map_sha256','construction_map')):
        need(entry[field] == m['artifacts'][key]['sha256'], 'Source audit binding mismatch: '+field)
    need(paths['expanded'].stat().st_size == e['expanded_bytes'], 'Expanded byte count mismatch')
    need(gzip_digest(paths['expanded_gzip']) == (m['artifacts']['expanded']['sha256'],e['expanded_bytes']), 'Compressed expansion mismatch')
    need(gzip_digest(paths['source'])[0] == s['uncompressed_sha256'], 'Compressed source mismatch')
    weights = load_json(paths['weights'])
    need(type(weights) is list and len(weights) == e['rows'] and all(type(w) is int and w == 1 for w in weights), 'Weights file is not exactly the stated all-one list')
    return paths


def replace_once(text, old, new):
    need(text.count(old) == 1, 'Expected exactly one splice anchor: '+old[:90])
    return text.replace(old,new,1)


def select(text):
    token = re.compile(r'\\if('+ '|'.join(SELECTION)+r')\b|\\else\b|\\fi\b')
    out=[]; stack=[]; active=True; start=0
    for t in token.finditer(text):
        if active: out.append(text[start:t.start()])
        if t.group(1):
            value=SELECTION[t.group(1)]; stack.append((active,value,False)); active=active and value
        elif t.group() == r'\else':
            need(bool(stack),'Unmatched else'); outer,value,seen=stack.pop(); need(not seen,'Repeated else')
            stack.append((outer,value,True)); active=outer and not value
        else:
            need(bool(stack),'Unmatched fi'); outer,_,_=stack.pop(); active=outer
        start=t.end()
    need(not stack,'Unclosed selection')
    if active: out.append(text[start:])
    return ''.join(out)


def snippet(name):
    return (BASE/name).read_text(encoding='utf-8').rstrip()+'\n\n'


def selected_appendix():
    text = select(APPENDIX.read_text(encoding='utf-8'))
    text = re.sub(r'^%[^\n]*\n','',text,flags=re.M)
    text = text.replace(r'\subsection{',r'\subsubsection{').replace(r'\section{',r'\subsection{')
    changes = [
        ('Retain the field and curve of Version 3:',r'Retain the field and curve of Section~\ref{sec:degree8-original}:'),
        (r'\cite{v3}',r'Section~\ref{sec:degree8-original} and Appendix~\ref{app:sources}'),
        ('This is the same $H_{19}$ as in Version 3, not a new height bound.',r'This is $H_{19}$ of Theorem~\ref{thm:quartic-height19}.'),
        ('We also retain the reciprocal logarithm lemma of Version 3.',r'We also retain Lemma~\ref{lem:quartic-reciprocal-log}.'),
        (r'\cite{koenigsmann}',r'\cite{koenigsmann-defining}'),
        (r'\subsection{Optional general-root carrier}',r'\subsection{General root carrier}'),
        (r'\subsubsection{Optional doubled targets}',r'\subsubsection{Doubled targets}'),
        (r'\subsection{Optional exact implementation refinements}',r'\subsection{Exact implementation refinements}'),
        ("$\\beta'=\\beta=X^2+2$ for the Version 3 carrier, and\n$\\beta'=2\\beta$ for the general-root carrier.","$\\beta=X^2+2$ and $\\beta'=2\\beta$."),
        ("Put $H_*=H$ for the Version 3\nroot carrier, and $H_*=5H$ for the general-root variant below.","Put $H_*=5H$."),
        ("For the original\ncarrier $\\beta'=\\beta=X^2+2$, giving integral $X$ by the original\ndenominator argument. For the general-root carrier $\\beta'=2\\beta$;", "$\\beta'=2\\beta=2(X^2+2)$;"),
        ("For integral input first set $\\beta=X^2+2$. In the general-root branch\ntake $A=\\beta P_*$, whose doubled index is $2\\beta$; otherwise use the\nVersion 3 choice.", "For integral input first set $\\beta=X^2+2$ and\ntake $A=\\beta P_*$, whose doubled index is $2\\beta$."),
        ("In the general-root\nbranch their doubled-index ratio is unchanged.", "Their doubled-index ratio is unchanged."),
        ("and in that branch take $T=tR$,", "and take $T=tR$,"),
        ('the selected target-four or target-two CRT rule.', 'the target-two CRT rule.'),
        ('Optional exact fusions preserve the specified','The exact fusions preserve the specified'),
    ]
    for old,new in changes: text=replace_once(text,old,new)
    text=replace_once(text,r'\subsection{Selective comparisons and the local elliptic chart}',snippet('TRANSPLANTS.tex')+r'\subsection{Selective comparisons and the local elliptic chart}')
    text=replace_once(text,'Take $H_*=5H$ and $\\beta\'=2\\beta$.',snippet('SCALAR_BOUND.tex')+'Take $H_*=5H$ and $\\beta\'=2\\beta$.')
    return text


def span(lines,a,b):
    return ''.join(lines[a-1:b]).replace('\r\n','\n')


def contact_foundation(lines):
    text=span(lines,8910,9035)
    text=replace_once(text,"$G=2E(K)=\\Z P_*$ from Section~\\ref{sec:degree8-original}.\nLet $A=[n]P_*,S=[s]P_*,T=[t]P_*,Z=[z]P_*$ be nonidentity points.","$E:y^2=x^3-Dx$ from Section~\\ref{sec:degree8-original}.\nLet $A,S,T,Z$ be nontorsion points of $E(K)$.")
    text=replace_once(text,'The same pole-completeness construction applies to these values.',r'These contacts have the positivity and local squareclasses used by Lemmas~\ref{lem:quartic-conic-completeness} and \ref{lem:quartic-linear-pole}.')
    text=replace_once(text,"residue $c$ and the square factor $D_0^2$. Lemma~\\ref{hyp:o8-pole}\ntherefore supplies the pole witnesses.","residue $c$ and the square factor $D_0^2$.\nLemmas~\\ref{lem:quartic-conic-completeness} and\n\\ref{lem:quartic-linear-pole} supply the selected ordinary-pole witnesses.")
    return text


def num(x): return format(x,',').replace(',',r'\,')
def display_hash(h): return '\\begin{center}\\footnotesize\\ttfamily\n'+h+'\n\\end{center}\n'
def path_tex(s): return r'\nolinkurl{'+s+'}'


def literal_spec(m):
    e=m['endpoint']; n=e['variables']; w=e['witnesses']; arts=m['artifacts']
    return r'''\section{An explicit quartic defining the integers}
\label{sec:quartics}
This is the second final polynomial of the manuscript. The original huge
polynomial remains unchanged. The base residual compiler in
Section~\ref{sec:degree8-original} supplies construction machinery and
inherited arithmetic inputs; it is not a third final polynomial.

\begin{theorem}[An explicit quartic definition]\label{thm:quartic}
With precisely the inherited arithmetic hypotheses and qualifications of
Section~\ref{sec:degree8-original} and Appendix~\ref{app:sources}, the
coefficient file below defines one integer polynomial $\Phi$ of total
degree $4$, with $''' + num(e['monomials']) + '$ nonzero monomials in $'+num(n)+r'''$ variables.
For every $q\in\Q$,
\[
 q\in\Z\quad\Longleftrightarrow\quad
 \exists(w_1,\ldots,w_{'''+str(w)+r'''})\in\Q^{'''+str(w)+r'''},\qquad
 \Phi(q,w_1,\ldots,w_{'''+str(w)+r'''})=0.
\]
There are $'''+num(w)+r'''$ existential witnesses besides the original input.
The coefficient bound is
\[
 \|\Phi\|_\infty='''+e['max_abs_coefficient']+'<2^{'+str(e['coefficient_bound_exponent'])+r'''}.
\]
\end{theorem}

\subsection{Literal specification and coefficient file}
The complete coefficient table is '''+path_tex(arts['expanded']['public_path'])+r'''.
After one comment line, each line gives a nonzero signed integer coefficient
followed by a nondecreasing list of variable indices. Repeated indices give
their multiplicities as exponents; a coefficient alone is the constant.
Thus \texttt{-6 0 2 2} denotes $-6X_0X_2^2$. The original input is $X_0$.
Like terms are collected, and the rows are in lexicographic index-list order.
The occurrence-frequency relabeling is recorded in
'''+path_tex(arts['variable_map']['public_path'])+r''' and fixes index zero.
The gzip companion has exactly the same uncompressed bytes.
The coefficient table has $'''+num(e['expanded_bytes'])+r'''$ bytes, including
its comment and line endings, and SHA-256
'''+display_hash(arts['expanded']['sha256'])+r'''
This specifies every coefficient without an auxiliary choice of witnesses.

\subsection{Arithmetic source and retained foundations}
\label{subsec:quartic-source}
The selected source uses the following retained height, contact and
reciprocal-logarithm proofs before the new source equivalence is established.
An element of $K$ is represented by two rational coefficients, with
\[
 (a_0,a_1)(b_0,b_1)=(a_0b_0+2a_1b_1,a_0b_1+a_1b_0),\qquad
 a^{-1}=\frac{(a_0,-a_1)}{a_0^2-2a_1^2}\quad(a\ne0).
\]
The inverse denominator is nonzero by the irrationality of $\sqrt2$.

'''


def source_metadata(m):
    s=m['source']; arts=m['artifacts']
    out=r'''\subsection{Exact source specification and audit boundary}
The source just proved has $'''+num(s['variables'])+r'''$ rational coordinates,
including input zero, and $'''+num(s['rows'])+r'''$ residual equations.
Its distinct name in '''+path_tex(arts['source_entry']['public_path'])+' is\n'+display_hash(s['source_id'])
    out+='The compressed source '+path_tex(arts['source']['public_path'])+' has SHA-256\n'+display_hash(arts['source']['sha256'])
    out+='Its uncompressed bytes have SHA-256\n'+display_hash(s['uncompressed_sha256'])
    out+='The source contains $'+num(len(s['module_names']))+'$ modules. Its complete construction map is '+path_tex(arts['construction_map']['public_path'])+'.\n'
    out+=r'''The independent source audit checks the full module equations, exact
ordered expression lists and contact positions, root and scalar interfaces,
all retained guards, the anchor terminal coordinate and complete flattening.
It is recorded in '''+path_tex(arts['source_audit']['public_path'])+'. The source-auditor SHA-256 is\n'+display_hash(arts['source_auditor']['sha256'])
    out+=r'''Those checks establish finite source identities. The source's rational
input projection is proved in Theorem~\ref{thm:quartic-selected-source},
with the inherited qualifications unchanged. A source digest is not an
arithmetic proof, and the historical base compiler remains construction
machinery rather than another final polynomial.

'''
    return out


def reductions(lines,m):
    text=span(lines,9571,9605)
    text=replace_once(text,r'Theorem~\ref{thm:quartic-source-arithmetic}.',r'Theorem~\ref{thm:quartic-selected-source}.')
    if m['events'].get('relation_eliminate'): text+=snippet('RELATION_RULE.tex')
    if m['events'].get('circuit'): text+=snippet('POWER_RULE.tex')
    if m['events'].get('parity_conic'):
        text+=span(lines,9670,9711)
        text+=r'''This rule is applied only at the certificate's height-parity blocks;
the ordinary comparison pole is the linear-unit source predicate already
proved above. The actual multiplicity is given in the following census.

'''
    return text


def final_proof(m):
    e=m['endpoint']; a=m['artifacts']; w=e['witnesses']; count=sum(m['events'].values())
    text=r'''\subsection{Finite realization and proof of the quartic theorem}
The fresh quadratic lift introduces only defining product equations.
Their evaluation and forgetting maps preserve rational solutions while
fixing the original input. The certificate then applies exactly the
operations below, under the current-row and complete-incidence hypotheses
just proved. The resulting file '''+path_tex(a['residuals']['public_path'])+r'''
contains $'''+num(e['rows'])+r'''$ nonzero integer residuals of degree at most two.
Every weight in '''+path_tex(a['weights']['public_path'])+r''' is one, and
\[
 \Phi(X_0,\ldots,X_{'''+str(w)+r'''})=\sum_{i=1}^{'''+str(e['rows'])+r'''}R_i^2.
\]
At rational values each square is nonnegative, so this sum vanishes if and
only if all residuals vanish. Nonzero rational row normalization preserves
each row's zero set before this integral sum is formed.

The certificate '''+path_tex(a['certificate']['public_path'])+' records $'+num(count)+r'''$ transformations:
\[
\begin{array}{lr}
'''
    row_end=r'\\'+'\n'
    text+=row_end.join(r'\text{'+EVENT_NAMES[k]+'}&'+num(v) for k,v in m['events'].items())+row_end+'\\end{array}\n\\]\n'
    text+='Its SHA-256 is\n'+display_hash(a['certificate']['sha256'])
    text+='The independent verifier '+path_tex(a['verifier']['public_path'])+' has SHA-256\n'+display_hash(a['verifier']['sha256'])
    text+=r'''It checks the named source binding, fresh lift, every recorded
polynomial identity and reconstruction map, defining order, current-row
supports, every occurrence of each removed coordinate, final quadratic
degrees, and the bijective variable map fixing input zero. It then compares
the complete collected integer expansion, including every cross term.
The endpoint verification receipt is '''+path_tex(a['verification']['public_path'])+'.\n\n'
    text+=r'''\begin{proof}[Proof of Theorem~\ref{thm:quartic}]
Theorem~\ref{thm:quartic-selected-source} proves both rational-input
implications for the selected arithmetic source. For any fixed rational
input, every defining lift and every recorded transformation has the
forward and reverse solution maps proved above. Their composition preserves
the existence of rational witnesses and keeps that input fixed. Hence the
final residual system has rational input projection exactly $\Z$.
The all-one sum of its squares vanishes precisely on its simultaneous
zero set, so the same equivalence holds for $\Phi$.

The literal coefficient table is the verified complete integral expansion
of that sum. Its nonzero degree-four term makes its degree exactly four;
the collected coefficients give the stated monomial count and maximum.
The checked variable map gives the stated ambient coordinates, one of
which is the input. Thus all numerical
claims and the input-projection equivalence concern this one polynomial.
\end{proof}

The finite checks do not replace the inherited rank, height, prime-pattern,
formal-group, norm or pole arguments. Their qualifications remain those
stated in the source proof and Appendix~\ref{app:sources}.
'''
    return text


def source_body(lines):
    evaluator=span(lines,9509,9529)
    evaluator=replace_once(evaluator,r'$\Lambda p_0=G_0$ and $B_i\Lambda=G_i$.',r'$\Lambda p_H=G_H$ and the beta or normalized-Lucas equations $B_i\Lambda=G_i$.')
    return (span(lines,8752,8909)+contact_foundation(lines)+span(lines,9036,9130)
            +selected_appendix()+snippet('SOURCE_THEOREM.tex')+evaluator)


def check_tex(text):
    clean=re.sub(r'(?<!\\)%[^\n]*','',text)
    labels=re.findall(r'\\label\{([^}]+)\}',clean)
    duplicates=[k for k,v in Counter(labels).items() if v>1]
    need(not duplicates,'Duplicate labels: '+repr(duplicates))
    refs=set(re.findall(r'\\(?:ref|eqref|autoref|[Cc]ref)\{([^}]+)\}',clean))
    refs={x.strip() for r in refs for x in r.split(',')}
    need(not refs-set(labels),'Undefined references: '+repr(sorted(refs-set(labels))))
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',clean))
    cites={k.strip() for c in re.findall(r'\\cite\w*(?:\[[^]]*\])*\{([^}]+)\}',clean) for k in c.split(',')}
    need(not cites-bib,'Undefined citation keys: '+repr(sorted(cites-bib)))
    need(labels.count('thm:quartic') == 1 and labels.count('thm:target') == 1,'Two-result structure changed')
    need(text.count(r'\author{}') == 1,'Blank author not preserved')
    return dict(labels=len(labels),references=len(refs),citation_keys=len(cites))


def verify_inputs(v3):
    for key,path in (('v3',v3),('appendix',APPENDIX),('plan',PLAN),('inventory',INVENTORY)):
        need(file_digest(path) == PINS[key], 'Frozen input changed: '+key)
    raw=v3.read_bytes(); lines=raw.decode('utf-8').splitlines(keepends=True)
    inv=load_json(INVENTORY)
    for block in inv['quartic_blocks']:
        excerpt=span(lines,block['first_line'],block['last_line'])
        need(digest(excerpt.encode()) == block['normalized_excerpt_sha256'], 'Inventory span mismatch')
    return raw,lines,inv


def integrate(v3,m):
    raw,lines,inv=verify_inputs(v3)
    e=m['endpoint']; r=m['release']
    section=literal_spec(m)+source_body(lines)+source_metadata(m)+reductions(lines,m)+final_proof(m)
    need(not re.search(r'\\if(?:'+ '|'.join(SELECTION)+r')|\\else\b|\\fi\b',section),'Unresolved source option')
    need('Optional' not in section and 'target-four' not in section,'Unselected variant prose remains')
    for item in inv['metadata_updates']:
        if item['kind'] == 'sha256': need(item['value'] not in section,'Historical artifact digest remains active')
    newline='\r\n' if b'\r\n' in raw else '\n'
    def encoded(t): return t.rstrip('\n').replace('\n',newline)+newline
    header=(r'\providecommand{\LogE}{\log_E}'+'\n'
            +r'\title{$\mathbb{Z}$ is Diophantine in $\mathbb{Q}$\\[4pt]\large Version '+str(r['version'])+'.}\n'
            +r'\author{}'+'\n'+r'\date{'+r['date']+'}\n')
    abstract='We also specify a quartic with $'+num(e['variables'])+'$ variables, $'+num(e['monomials'])+'$ nonzero monomials, and coefficients of magnitude below $2^{'+str(e['coefficient_bound_exponent'])+'}$,\nwith rational zero projection exactly $\\Z$.\n'
    intro=(r'% Begin quartic introduction addition'+'\nSection~\\ref{sec:quartics} gives the explicit $'+num(e['variables'])+r'''$-variable quartic.
Its arithmetic source revises the base residual compiler of
Section~\ref{sec:degree8-original}, with a separate proof of soundness and
completeness. The complete coefficient table and exact algebraic conversion
certificate are included with this manuscript.
% End quartic introduction addition
''')
    replacements=[(35,37,header),(47,48,abstract),(94,100,intro),(8679,9830,section)]
    output=[]; cursor=0; receipt=[]
    for lo,hi,new in replacements:
        output.extend(lines[cursor:lo-1]); output.append(encoded(new))
        receipt.append(dict(first_line=lo,last_line=hi,old_sha256=digest(''.join(lines[lo-1:hi]).encode()),new_sha256=digest(encoded(new).encode())))
        cursor=hi
    output.extend(lines[cursor:]); result=''.join(output)
    checks=check_tex(result)
    for protected in inv['protected_spans']:
        old=''.join(lines[protected['first_line']-1:protected['last_line']])
        need(result.count(old) == 1,'Protected span was changed or duplicated')
    need(span(lines,8752,8909).replace('\n',newline) in result,'H19 proof was changed')
    need(span(lines,9036,9130).replace('\n',newline) in result,'Reciprocal proofs were changed')
    return result.encode('utf-8'),dict(replacements=receipt,static_checks=checks,
        protected_spans_preserved=True,unchanged_bytes_outside_replacements=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--v3',type=Path,required=True)
    p.add_argument('--metadata',type=Path,required=True)
    p.add_argument('--out-dir',type=Path,required=True)
    a=p.parse_args()
    out=a.out_dir.resolve(); allowed=(BASE/'generated').resolve()
    need(out != allowed and out.is_relative_to(allowed),'Output must be a fresh subdirectory of manuscript-integration/generated')
    need(not out.exists(),'Output directory already exists; use a fresh candidate name')
    m=load_json(a.metadata); validate_metadata(m)
    result,receipt=integrate(a.v3,m)
    receipt.update(schema='quartic-manuscript-splice-receipt-v1',candidate_only=True,
        no_pdf_created=True,source_acceptance_not_inferred=True,
        input_pins=PINS,metadata_sha256=file_digest(a.metadata),
        output_sha256=digest(result),selection=SELECTION,
        emitter_sha256=file_digest(Path(__file__)),
        snippet_sha256={x.name:file_digest(x) for x in BASE.glob('*.tex')})
    out.mkdir(parents=True)
    name=m['release']['tex_basename']+'.tex'
    (out/name).write_bytes(result)
    (out/'splice-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PRIVATE CANDIDATE WRITTEN; NO PDF OR PUBLICATION',path=str(out/name),sha256=digest(result))))


if __name__ == '__main__': main()
