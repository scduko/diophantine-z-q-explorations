"""Generalize an already source-adapted, pinned absorption producer.

Call adapt_mixed_absorb after prepare_adapter.adapt_producer. This changes
source locators only. All source identities, acyclic alias expansion, current
gate checks, full-incidence closure and independent batch_absorb rules stay.
"""


def replace_once(text, old, new):
    assert text.count(old) == 1, ('Unexpected absorption template', old)
    return text.replace(old, new)


def adapt_mixed_absorb(text):
    text = replace_once(text, 'from source_layout import load_layout\n',
                        'from source_layout import BATCHES, COMPARISONS, load_layout\n')
    text = replace_once(text,
        "for name in ('Z_definition', 'q_compare4', 'q_batch41')}",
        "for name in ('Z_definition',)+tuple(COMPARISONS)+BATCHES}")
    text = replace_once(text,
        "    root = roots[0]; rm = modules['Z_definition']; bm = modules['q_batch41']\n",
        "    root = roots[0]; rm = modules['Z_definition']\n")
    text = replace_once(text,
        "        if inst['module'] != 'q_compare4':\n            continue\n"
        "        mod = modules['q_compare4']\n"
        "        call, = [c for c in mod['calls'] if c['module'] == 'q_batch41']\n",
        "        if inst['module'] not in COMPARISONS:\n            continue\n"
        "        mod = modules[inst['module']]\n"
        "        call, = [c for c in mod['calls'] if c['module'] == COMPARISONS[inst['module']]]\n")
    start = "    norm_vars = [x[1] for x in bm['construction_log'] if x[0] == 'variable' and x[2] == 'normalized bottom norm']\n"
    stop = "    for inst in instances:\n        if inst['module'] != 'q_batch41':\n            continue\n"
    assert text.count(start)==1 and text.count(stop)==1
    left=text.index(start);right=text.index(stop,left)
    block=text[left:right]
    assert len(block.splitlines())==7 and 'assert len(plan)*2+2 == bm[\'free\']' in block
    nested=''.join('    '+line+'\n' for line in block.splitlines())
    text=text[:left]+text[right:]
    text=replace_once(text,stop,
        "    for inst in instances:\n        if inst['module'] not in BATCHES:\n            continue\n"
        "        bm = modules[inst['module']]\n"+nested)
    assert "inst['module'] != 'q_compare4'" not in text
    assert "inst['module'] != 'q_batch41'" not in text
    return text
