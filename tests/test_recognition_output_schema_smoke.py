import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_recognition_output_fixture():
    obj = json.loads((ROOT / "fixtures/recognition-output.valid.json").read_text())
    assert obj["object_type"] == "RECOGNITION_OUTPUT"
    assert obj["output_class"] == "recognition-object"
    assert obj["boundary_assertions"]["not-recourse"] is True
