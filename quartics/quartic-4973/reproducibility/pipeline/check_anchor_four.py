"""Independent literal source specification for the four-witness anchor.

No producer import or symbolic builder is used. The caller must pin and audit
the other source modules, external interfaces and shared nonzero C chain.
"""
import json


def expected_anchor():
    return dict(name='q_anchor',free=2,locals=4,
        residuals=[
            [[-9,[-26,-26]],[1,[-26,2]],[-3,[0,0]],[-3,[1,1]]],
            [[-4,[-26,-26]],[1,[2,2]],[-8,[3,3]],[-12,[4,4]],[24,[5,5]]],
        ],calls=[],construction_log=[
            ['variable',2,'anchor homogeneous trace H'],
            ['variable',3,'anchor homogeneous trace U'],
            ['variable',4,'anchor homogeneous trace V'],
            ['variable',5,'anchor homogeneous trace W'],
            ['equation',0,'anchor trace of coefficient squares'],
            ['equation',1,'anchor homogeneous single trace'],
        ],anchor_squarings=25,anchor_constant_global_index=-26,
        inputs='two coordinates of f(S)=1/x(S)',
        encoding='homogeneous trace 9+3(a^2+b^2) in S_2_3',
        arithmetic_dependency='Koenigsmann Proposition 6 proof Facts (b),(e); explicit trace inclusion 4Z_2')


def check_anchor(module):
    encode=lambda value:json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)
    if encode(module)!=encode(expected_anchor()):
        raise ValueError('Anchor differs from the independent four-witness specification')
    return dict(status='PASS: SOURCE SPECIFICATION ONLY',free=2,locals=4,residuals=2,
                residual_degree=2,max_abs_residual_coefficient=24,
                arithmetic_acceptance=False)
