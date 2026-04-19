import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text())

def test_forbidden_output_classes_do_not_overlap_allowed_output_classes():
    policy = load("contracts/boundary-policy.json")
    assert set(policy["allowed_output_classes"]).isdisjoint(set(policy["forbidden_output_classes"]))

def test_recognition_object_carries_non_recourse_boundary():
    obj = load("recognitions/current/recognition-object-0001.json")
    assertions = set(obj["boundary_assertions"])
    assert "recognition does not assign burden" in assertions
    assert "recognition does not assign remedy" in assertions
    assert "recognition does not perform closure" in assertions
    assert "recognition does not redefine law, epoch, authority, execution, or verification" in assertions

def test_current_index_shape_uses_active_truth():
    idx = load("recognitions/current/index.json")
    assert idx["object_type"] == "RecognitionIndex"
    assert idx["status"] == "ACTIVE_TRUTH"
    assert idx["historical"] is False

def test_boundary_policy_rejection_reasons_cover_terminal_non_recourse_split():
    policy = load("contracts/boundary-policy.json")
    reasons = set(policy["rejection_reasons"])
    assert "would-assign-burden" in reasons
    assert "would-assign-remedy" in reasons
    assert "would-assign-closure" in reasons
    assert "would-assign-terminal-recourse" in reasons
