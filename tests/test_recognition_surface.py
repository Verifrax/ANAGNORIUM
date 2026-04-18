from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_surfaces_exist():
    required = [
        "README.md",
        "RECOGNITION_MODEL.md",
        "ADMISSIBILITY.md",
        "CLAIM_CLASSES.md",
        "INTERPRETIVE_BOUNDARY.md",
        "TERMINAL_RECOGNITION_RULES.md",
        "schemas/recognition-object.schema.json",
        "recognitions/current/index.json",
        "recognitions/history/README.md",
        "cases/README.md",
    ]
    for rel in required:
        assert (ROOT / rel).is_file(), rel

def test_current_index_shape():
    obj = json.loads((ROOT / "recognitions/current/index.json").read_text())
    assert obj["object_type"] == "RecognitionIndex"
    assert obj["status"] == "current"
    assert obj["historical"] is False
    assert isinstance(obj["entries"], list)
