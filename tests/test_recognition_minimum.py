import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_recognition_minimum():
    obj = load("recognitions/current/recognition-object-0001.json")
    idx = load("recognitions/current/index.json")

    assert obj["authority_object_ref"] == "https://github.com/Verifrax/AUCTORISEAL/blob/main/authorities/current/authority-object-0001.json"
    assert obj["verification_result_ref"] == "https://github.com/Verifrax/VERIFRAX/blob/main/verification/results/current/verification-result-0001.json"
    assert obj["execution_receipt_ref"] == "https://github.com/Verifrax/CORPIFORM/blob/main/receipts/current/execution-receipt-0001.json"

    assert idx["object_type"] == "RecognitionIndex"
    assert idx["status"] == "ACTIVE_TRUTH"
    assert idx["historical"] is False
    assert idx["current_recognition_object_ref"] == "recognitions/current/recognition-object-0001.json"

    first = idx["entries"][0]
    assert first["recognition_object_id"] == obj["recognition_object_id"]
    assert first["path"] == "recognitions/current/recognition-object-0001.json"

    non_role = obj["non_role_boundaries"]
    assert "does not itself create recourse" in non_role["recourse"].lower()
    assert "does not itself create continuity or transfer truth" in non_role["continuity_transfer"].lower()
