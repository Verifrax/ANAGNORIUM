import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_recognition_object_minimum():
    data = json.loads((ROOT / "recognitions/current/recognition-object-0001.json").read_text())
    index = json.loads((ROOT / "recognitions/current/index.json").read_text())

    assert data["object_type"] == "RecognitionObject"
    assert data["status"] == "ACTIVE_TRUTH"
    assert data["recognition_object_id"] == "recognition-object-0001"
    assert data["recognition_index_ref"] == "recognitions/current/index.json"
    assert data["historical_archive_ref"] == "recognitions/history/"
    assert data["claim_class_ref"].endswith("/claim-classes/recognition-object.json")
    assert data["governing_law_version_ref"].endswith("/law/versions/current/law-version-0001.json")
    assert data["accepted_epoch_ref"].endswith("/epochs/current/accepted-epoch-0001.json")
    assert data["authority_object_ref"].endswith("/authorities/current/authority-object-0001.json")
    assert data["execution_receipt_ref"].endswith("/receipts/current/execution-receipt-0001.json")
    assert data["verification_result_ref"].endswith("/verification/results/current/verification-result-0001.json")
    assert data["recognition_status"] == "RECOGNIZED"
    assert data["admissibility_status"] == "ADMISSIBLE"

    assert index["object_type"] == "RecognitionIndex"
    assert index["status"] == "ACTIVE_TRUTH"
    assert index["current_recognition_object_ref"] == "recognitions/current/recognition-object-0001.json"
    assert index["entries"][0]["recognition_object_id"] == data["recognition_object_id"]
    assert index["entries"][0]["path"] == "recognitions/current/recognition-object-0001.json"
