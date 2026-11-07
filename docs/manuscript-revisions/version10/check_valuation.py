"""Bounded regression for Issue2 item6. The manuscript proves the general inequalities."""
import json
count=0
for delta in range(1,100,2):
    for alpha in range(-201,delta+1,2):
        for k in (1,25):
            failed=alpha+2*(k-1)-2*k*delta
            if not failed<=alpha-2*delta<0:raise ValueError('Failed-factor inequality')
            lower=2*delta-alpha
            pole=alpha-2*lower
            if not (pole==3*alpha-4*delta and pole<=-delta<0 and pole%2==1):raise ValueError('Pole contradiction')
            count+=1
# At delta=alpha=3 a normalized test valuation -2 makes one factor have
# valuation -1. Inverse products can all have positive valuation; there
# need not be an all-unit group. The repaired inference does not need one.
if min(0,3+2*(-2))!=-1:raise ValueError('Old shortcut counterexample')
print(json.dumps({'status':'PASS','bounded_inequality_cases':count,'universal_proof':'manuscript Section6','certifies_entire_proof':False}))
