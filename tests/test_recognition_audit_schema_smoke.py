import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_recognition_audit_fixture():
    obj = json.loads((ROOT / "fixtures/recognition-audit-record.valid.json").read_text())
    assert obj["object_type"] == "RECOGNITION_AUDIT_RECORD"
    assert obj["decision"] == "rejected"
    assert obj["rejection_reason"] == "would-assign-burden"
