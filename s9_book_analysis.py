#!/usr/bin/env python3
"""Re-runs the computations behind Chapters 15-17 of the S9 Proof Book.
Usage: python s9_book_analysis.py /path/to/SWI-V2-Modules-11-22   (checked out at 44a6af9)
Prints the enumeration summary, the X1-X10 results and the P1-P14 probes. Pure: no writes."""
import sys, itertools
from collections import Counter
root = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, root)
from swi_v2.s9 import evaluate_s9
G = {"evidence_id":"E1","exists":True,"relevance":"PASS","freshness":"PASS","scope":"PASS","provenance":"PASS","integrity":"PASS"}
def base(**k):
    a = {"action_id":"A","constraints":["C1"],"law":["C1"],"governance":["C1"],"security":["C1"],"human":["C1"],
         "evidence":[dict(G)],"dependencies":[],"unknown_conditions":[],"authority":{"required":False,"present":False}}
    a.update(k); return a
EV = {"none":[], "adequate":[dict(G)], "unresolved":[{"evidence_id":"E1","exists":True}], "fail":[dict(G, freshness="FAIL")]}
AU = {"n/a":{"required":False,"present":False}, "req-absent":{"required":True,"present":False}, "req-present":{"required":True,"present":True}}
rows = []
for cne in (1, 0):
    for L, Gv, S, H in itertools.product((1, 0), repeat=4):
        for ek, ev in EV.items():
            for unk in (0, 1):
                for ak, au in AU.items():
                    r = evaluate_s9(base(constraints=["C1"] if cne else [], law=["C1"] if L else [], governance=["C1"] if Gv else [],
                        security=["C1"] if S else [], human=["C1"] if H else [], evidence=ev, unknown_conditions=["U"] if unk else [], authority=au))
                    rows.append((cne, L, Gv, S, H, ek, unk, ak, r.system_result, r.promotion_eligible))
print("states:", len(rows), dict(Counter(r[8] for r in rows)), "| promotion ever true:", any(r[9] for r in rows))
X = {"X1": base(evidence=[dict(G, evidence_id="E-OF-OTHER-ACTION-B")]), "X2a": base(evidence=[dict(G, freshness="FAIL")]),
     "X2b": base(evidence=[dict(G, freshness="PASS")]), "X3": base(evidence=[dict(G, evidence_id="MEM-previously_verified")]),
     "X4": base(constraints=["name","address"], law=["name"], governance=["name"], security=["name"], human=["name"]),
     "X5": base(evidence=[dict(G, evidence_id="E-bound-to-principal-B")]), "X6": base(authority={"required":True,"present":False}),
     "X7": base(authority={"required":True,"present":True,"expired":True}), "X8": base(authority={"required":True,"present":True,"path":"CLAIM->PRIVILEGED"}),
     "X9": base(constraints=[]), "X10": base(evidence=[{"evidence_id":"E1","exists":True}])}
for k, a in X.items(): print(k, evaluate_s9(a).system_result)
P = {"P1": base(dependencies=[{"id":"D","status":"FAILED"}]), "P2": base(dependencies=[{"id":"D","status":"unresolved"}]),
     "P3": base(dependencies=["D-unresolved"]), "P4": base(authority={"required":True,"present":"false"}),
     "P5": base(evidence=[dict(G, exists="false")]), "P6": base(evidence=[dict(G, integrity="pass")]),
     "P7": base(evidence=[dict(G, integrity=True)]), "P9": base(unknown_conditions="none"),
     "P11": {"evidence":[dict(G)]}, "P12": base(evidence=[{k:v for k,v in G.items() if k!="exists"}]),
     "P13": base(authority=None), "P14": base(evidence=dict(G))}
for k, a in P.items():
    try: print(k, evaluate_s9(a).system_result)
    except Exception as e: print(k, "raises", type(e).__name__)
