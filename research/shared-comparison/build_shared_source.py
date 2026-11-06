"""Build the shared-comparison variant of the reciprocal source and check it.

Variant: the 41 per-contact `q_compare4` instances of `Z_definition` are
replaced by ONE comparison core (all private points, charts, logarithms,
ratios and field-test forms) and 41 per-contact `q_batch41` norm batches,
one for each ordinary-contact radical r_k, all fed the same 41 tests.

Checks performed (exact, no floating point):
  1. The flattener reproduces the pinned source residuals.jsonl row for row.
  2. The flattened variant equals the pinned flattened source after the
     substitution sigma that identifies each compare4 instance's private
     witnesses with those of the first instance, followed by removal of
     duplicate rows and dead variables.  Hence every rational zero of the
     variant yields a rational zero of the pinned source with the same X
     (soundness is inherited).  The converse is NOT claimed: it needs the
     cross-prime orientation lemma described in NOTE.md.

Usage: python3 -I build_shared_source.py SOURCE_DIR OUTPUT_DIR
"""
import json, sys, os, copy, hashlib

src, out = sys.argv[1], sys.argv[2]
NAMES = ['q_primeparity', 'q_anchor', 'q_batch41', 'q_height_batch', 'q_compare4', 'Z_definition']
MOD = {n: json.load(open(os.path.join(src, 'modules', n + '.json'))) for n in NAMES}
SHARED = json.load(open(os.path.join(src, 'shared.json')))


def flatten(mods):
    g = SHARED['witnesses']; rows = []; prov = {}; nxt = [g + 1]
    def emit(row, tr):
        rows.append([[c, sorted(tr(v) for v in mon)] for c, mon in row])
    for row in SHARED['residuals']:
        emit(row, lambda v: -v)
    for i in range(1, g + 1):
        prov[i] = ('shared', i)
    prov[0] = ('X',)
    def visit(name, args, path):
        d = mods[name]; start = nxt[0]; nxt[0] += d['locals']
        for v in range(d['locals']):
            prov[start + v] = (path, d['free'] + v)
        def tr(v):
            return -v if v < 0 else args[v] if v < d['free'] else start + v - d['free']
        for row in d['residuals']:
            emit(row, tr)
        for k, call in enumerate(d['calls']):
            visit(call['module'], [tr(v) for v in call['args']], path + '/' + str(k))
    visit('Z_definition', [0], 'Z')
    return rows, prov, nxt[0]


# ---- 1. reproduce pinned source -------------------------------------------
rows0, prov0, n0 = flatten(MOD)
with open(os.path.join(src, 'residuals.jsonl')) as fh:
    pinned = [json.loads(l) for l in fh.read().splitlines()[1:]]
assert rows0 == pinned, 'flattener does not reproduce the pinned source'
print('check 1: flattener reproduces pinned source:', len(rows0), 'rows,', n0, 'variables (incl. X)')

# ---- build variant modules ------------------------------------------------
c4 = MOD['q_compare4']; F = c4['free']; R_IN = F - 1          # r is the last input
(call,) = c4['calls']; assert call['module'] == 'q_batch41'
bargs = call['args']; assert bargs[0] == R_IN and bargs[1] == R_IN - 1   # [r, error, 40 test locals]
tests = bargs[2:]; assert len(tests) == 40 and all(t >= F for t in tests)
assert all(R_IN not in mon for row in c4['residuals'] for c, mon in row), 'r used outside the batch'
others = [F + v for v in range(c4['locals']) if F + v not in tests]
CF = R_IN + len(tests)                                          # core free: 30 inputs + 40 test outputs
ren = {v: v for v in range(R_IN)}
ren.update({t: R_IN + k for k, t in enumerate(tests)})
ren.update({v: CF + k for k, v in enumerate(others)})
core = {'name': 'q_compare4_core', 'free': CF, 'locals': len(others),
        'residuals': [[[c, [ren[v] if v >= 0 else v for v in mon]] for c, mon in row] for row in c4['residuals']],
        'calls': [],
        'semantics': 'q_compare4 without its norm batch; inputs as q_compare4 minus r, then its 40 bound field tests as outputs',
        'derived_from': 'q_compare4'}

z = copy.deepcopy(MOD['Z_definition'])
c4calls = [c for c in z['calls'] if c['module'] == 'q_compare4']
common = c4calls[0]['args'][:R_IN]
assert all(c['args'][:R_IN] == common for c in c4calls), 'compare4 calls differ outside r'
T = [z['free'] + z['locals'] + k for k in range(len(tests))]
z['locals'] += len(tests)
newcalls = [c for c in z['calls'] if c['module'] != 'q_compare4']
newcalls.append({'module': 'q_compare4_core', 'args': common + T, 'label': 'shared comparison core'})
for c in c4calls:
    newcalls.append({'module': 'q_batch41', 'args': [c['args'][R_IN], common[R_IN - 1]] + T,
                     'label': 'per-contact norm batch'})
z['calls'] = newcalls
z['name'] = 'Z_definition'
z['variant'] = 'shared-comparison: one q_compare4_core and 41 per-contact q_batch41 calls'
VAR = dict(MOD); VAR['q_compare4_core'] = core; VAR['Z_definition'] = z; del VAR['q_compare4']
rows1, prov1, n1 = flatten(VAR)

# ---- 2. variant == sigma(pinned) -------------------------------------------
# instances of q_compare4 in the pinned flattening
zc = MOD['Z_definition']['calls']
c4paths = ['Z/' + str(k) for k, c in enumerate(zc) if c['module'] == 'q_compare4']
first = c4paths[0]
inst = {}
for gidx, p in prov0.items():
    if len(p) == 2 and p[0] in c4paths:
        inst[(p[0], p[1])] = gidx
sigma = {}
for (path, loc), gidx in inst.items():
    sigma[gidx] = inst[(first, loc)]
def sub(row, m):
    return tuple(sorted((c, tuple(sorted(m.get(v, v) if v >= 0 else v for v in mon))) for c, mon in row))
A = set(sub(r, sigma) for r in rows0)
# variant variables -> pinned variables via provenance
zpath_c4 = {k: 'Z/' + str(k) for k in range(len(zc))}
newz = VAR['Z_definition']['calls']
core_k = [k for k, c in enumerate(newz) if c['module'] == 'q_compare4_core'][0]
batch_ks = [k for k, c in enumerate(newz) if c['module'] == 'q_batch41']
inv_ren = {v: k for k, v in ren.items()}
pin_index = {p: g for g, p in prov0.items()}
tau = {}
for gidx, p in prov1.items():
    if len(p) != 2 or p[0] == 'shared':
        tau[gidx] = gidx if p[0] != 'shared' else gidx; continue
    path, loc = p; parts = path.split('/')
    if path == 'Z':
        if loc in T:                       # shared test value -> first instance's test local
            tau[gidx] = inst[(first, tests[T.index(loc)])]
        else:
            tau[gidx] = pin_index[('Z', loc)]
    elif parts[1] == str(core_k):
        assert len(parts) == 2
        tau[gidx] = inst[(first, inv_ren[loc])]
    elif int(parts[1]) not in batch_ks:      # anchor / height batch: same call index in both
        assert zc[int(parts[1])]['module'] == newz[int(parts[1])]['module'] != 'q_compare4'
        tau[gidx] = pin_index[(path, loc)]
    else:
        j = batch_ks.index(int(parts[1]))      # j-th contact batch -> batch inside j-th compare4
        tau[gidx] = pin_index[('/'.join([c4paths[j], '0'] + parts[2:]), loc)]
B = set(sub(r, tau) for r in rows1)
assert len(set(tau.values())) == len(tau), 'variable map not injective'
assert A == B, 'variant is not sigma(pinned)'
print('check 2: variant equals pinned source with the 41 private comparison blocks identified')
print('         distinct rows', len(B), '; variant rows', len(rows1))

# ---- write -------------------------------------------------------------------
os.makedirs(os.path.join(out, 'modules'), exist_ok=True)
for n, d in VAR.items():
    with open(os.path.join(out, 'modules', n + '.json'), 'w') as fh:
        json.dump(d, fh, separators=(',', ':'))
deg = 2 * max(len(m) for r in rows1 for c, m in r)
counts = {'witnesses': n1 - 1, 'residuals': len(rows1), 'degree': deg,
          'pinned_witnesses': n0 - 1, 'pinned_residuals': len(rows0)}
with open(os.path.join(out, 'residuals.jsonl'), 'w') as fh:
    fh.write(json.dumps(counts, separators=(',', ':')) + '\n')
    for r in rows1:
        fh.write(json.dumps(r, separators=(',', ':')) + '\n')
with open(os.path.join(out, 'counts.json'), 'w') as fh:
    json.dump(counts, fh, indent=1)
print(json.dumps(counts))
