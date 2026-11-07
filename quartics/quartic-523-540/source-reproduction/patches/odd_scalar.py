"""Pointwise source changes for odd root labels; see ODD_ROOT_COMPLETENESS.md.

Only beta and the scalar/anchor point change. The comparison root S remains S.
"""
def replace_once(source,old,new):
    if source.count(old)!=1:
        raise ValueError((old,source.count(old)))
    return source.replace(old,new)

def patch(source):
    source=replace_once(source,
        "const beta=save('beta',add(rsq('inputSquare',X),C(2)));",
        "const beta=save('beta',add(scale(rsq('inputSquare',X),2),C(3)));")
    source=replace_once(source,
        "const PS=parameters('Sscalar',points.S),zRatio=",
        "const scalarPoint=subtract('scalar.shiftedS',points.S,P);\nconst PS=parameters('Sscalar',scalarPoint),zRatio=")
    return source

if __name__=='__main__':
    import sys
    from pathlib import Path
    Path(sys.argv[2]).write_text(patch(Path(sys.argv[1]).read_text()))
