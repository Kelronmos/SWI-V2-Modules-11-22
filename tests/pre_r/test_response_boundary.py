from datetime import datetime, timedelta, timezone
import pytest
from experimental.response_boundary import *
from experimental.response_boundary.core import IntegrityVerifier, build_response

NOW = datetime(2026, 9, 19, 8, 0, tzinfo=timezone.utc)

def fixtures():
    request = RequestBinding("R1","alice","read","record-1","alice-ui",NOW+timedelta(minutes=10))
    authority = AuthorityScope("alice",frozenset({"read"}),frozenset({"record-1"}),frozenset({"alice-ui"}),NOW+timedelta(minutes=10))
    evidence = EvidenceCarrier("E1","execution-result",{"source":"test"})
    response = build_response(response_id="RESP1",request=request,authority=authority,result={"value":42},
                              evidence=evidence,destination="alice-ui",issued_at=NOW,expires_at=NOW+timedelta(minutes=5))
    return request, authority, response

def admit(response, request, authority, **kwargs):
    return ReturnGate().evaluate(response,request,authority,NOW,expected_destination="alice-ui",
                                 action="read",resource="record-1",principal="alice",**kwargs)

def replace(obj, **changes):
    data = {**obj.__dict__, **changes}
    return obj.__class__(**data)

def test_valid_response_admitted():
    r,a,x=fixtures(); assert admit(x,r,a)==BoundaryDecision.ADMIT

@pytest.mark.parametrize("mutation",[
    lambda r,a: replace(r,result={"value":43}),
    lambda r,a: replace(r,destination="bob-ui"),
    lambda r,a: replace(r,integrity_digest=""),
])
def test_integrity_mutations_rejected(mutation):
    r,a,x=fixtures(); assert admit(mutation(x,a),r,a)==BoundaryDecision.REJECT

def test_wrong_request_rejected():
    r,a,x=fixtures(); other=RequestBinding("R2","alice","read","record-1","alice-ui",r.expires_at)
    assert admit(x,other,a)==BoundaryDecision.REJECT

def test_authority_expansion_rejected():
    r,a,x=fixtures()
    expanded=AuthorityScope("alice",frozenset({"read","delete"}),a.resources,a.destinations,a.expires_at)
    assert admit(replace(x,authority=expanded).with_integrity(),r,a)==BoundaryDecision.REJECT

def test_wrong_destination_rejected():
    r,a,x=fixtures()
    assert ReturnGate().evaluate(x,r,a,NOW,expected_destination="bob-ui",action="read",resource="record-1",principal="alice")==BoundaryDecision.REJECT

def test_missing_evidence_rejected():
    r,a,x=fixtures(); assert admit(replace(x,evidence=None).with_integrity(),r,a)==BoundaryDecision.REJECT

def test_expired_response_rejected():
    r,a,x=fixtures()
    assert ReturnGate().evaluate(x,r,a,NOW+timedelta(minutes=6),expected_destination="alice-ui",action="read",resource="record-1",principal="alice")==BoundaryDecision.REJECT

def test_revoked_authority_rejected():
    r,a,x=fixtures()
    revoked=AuthorityScope(a.principal,a.actions,a.resources,a.destinations,a.expires_at,True)
    assert ReturnGate().evaluate(x,r,revoked,NOW,expected_destination="alice-ui",action="read",resource="record-1",principal="alice")==BoundaryDecision.REJECT

def test_policy_denial_rejected():
    r,a,x=fixtures(); assert admit(x,r,a,policy_allows=False)==BoundaryDecision.REJECT

@pytest.mark.parametrize("principal,action,resource",[
    ("bob","read","record-1"),("alice","delete","record-1"),("alice","read","record-2")
])
def test_scope_mismatch_rejected(principal,action,resource):
    r,a,x=fixtures()
    assert ReturnGate().evaluate(x,r,a,NOW,expected_destination="alice-ui",action=action,resource=resource,principal=principal)==BoundaryDecision.REJECT

def test_certificate_is_scoped():
    c=CertificateScope("C1",frozenset({"read"}),frozenset({"record-1"}),frozenset({"alice-ui"}))
    assert c.permits("read","record-1","alice-ui")
    assert not c.permits("delete","record-1","alice-ui")

def test_receipt_is_not_authority():
    receipt=Receipt("RC1","R1","digest")
    assert receipt.request_id=="R1"
    assert not hasattr(receipt,"authorize")

def test_response_does_not_create_new_privileged_action():
    r,a,x=fixtures(); assert admit(x,r,a)==BoundaryDecision.ADMIT
    assert not hasattr(x,"execute")

def test_transformation_requires_new_integrity():
    r,a,x=fixtures()
    transformed=replace(x,result={"summary":"42"})
    assert admit(transformed,r,a)==BoundaryDecision.REJECT

def test_nan_is_rejected_by_canonicalization():
    r,a,x=fixtures()
    with pytest.raises(ValueError): replace(x,result={"value":float("nan")}).with_integrity()

def test_integrity_is_deterministic():
    r,a,x=fixtures()
    assert IntegrityVerifier.digest(x.protected_material())==x.integrity_digest
