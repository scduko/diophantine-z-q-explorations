"""Tiny resource-limit propagation tests, independent of a generated source."""
import json
import audit_shared_square as a
import shared_square_cases as cases


def main():
    deep=0
    for _ in range(50):deep={'nested':deep}
    fixtures=[{'nested':deep}, {'nested':{'monomial':[0]*16385}},
              {'nested':{'string':'x'*8193}}, {'nested':{'integer':1<<4097}}]
    count=0
    for bad in fixtures:
        try:cases.must_reject('resource',lambda _:a.preflight(bad),{})
        except a.SharedSquareResourceError:count+=1
        else:raise RuntimeError('Resource failure counted as semantic rejection')
    try:cases.must_reject('nodes',lambda _:a.preflight({'nested':list(range(25))},node_limit=10),{})
    except a.SharedSquareResourceError:count+=1
    else:raise RuntimeError('Node limit counted as semantic rejection')
    a.preflight({'valid':[1,None,True,'x',{'monomial':[0,1,2]}]})
    assert count==5
    print(json.dumps(dict(status='PASS: resource abort propagation',resource_cases=count,
                          semantic_rejections_claimed=0)))


if __name__=='__main__':main()
