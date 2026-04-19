#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []

def need(cond, label):
    if cond:
        print(f"[VERIFY] {label}")
    else:
        print(f"[FAIL] {label}")
        errors.append(label)

def load(rel):
    return json.loads((root / rel).read_text(encoding="utf-8"))

obj_path = root / "recognitions/current/recognition-object-0001.json"
idx_path = root / "recognitions/current/index.json"
hist_path = root / "recognitions/history/README.md"
test_path = root / "tests/test_recognition_minimum.py"

need(obj_path.is_file(), "recognition-object-present")
need(idx_path.is_file(), "recognition-index-present")
need(hist_path.is_file(), "recognition-history-present")
need(test_path.is_file(), "outsider-recognition-test-present")

obj = load("recognitions/current/recognition-object-0001.json")
idx = load("recognitions/current/index.json")

need(obj.get("recognition_object_id") == "recognition-object-0001", "recognition-object-id")
need(obj.get("authority_object_ref") == "https://github.com/Verifrax/AUCTORISEAL/blob/main/authorities/current/authority-object-0001.json", "recognition-authority-ref")
need(obj.get("verification_result_ref") == "https://github.com/Verifrax/VERIFRAX/blob/main/verification/results/current/verification-result-0001.json", "recognition-verification-ref")
need(obj.get("execution_receipt_ref") == "https://github.com/Verifrax/CORPIFORM/blob/main/receipts/current/execution-receipt-0001.json", "recognition-receipt-ref")

non_role = obj.get("non_role_boundaries", {})
need("recourse" in non_role and "does not itself create recourse" in non_role["recourse"].lower(), "recognition-nonrole-recourse")
need("continuity_transfer" in non_role and "does not itself create continuity or transfer truth" in non_role["continuity_transfer"].lower(), "recognition-nonrole-continuity-transfer")

need(idx.get("object_type") == "RecognitionIndex", "recognition-index-type")
need(idx.get("status") == "ACTIVE_TRUTH", "recognition-index-status")
need(idx.get("historical") is False, "recognition-index-historical-false")
need(idx.get("current_recognition_object_ref") == "recognitions/current/recognition-object-0001.json", "recognition-index-binding")

entries = idx.get("entries", [])
need(len(entries) >= 1, "recognition-index-entry-present")
if entries:
    first = entries[0]
    need(first.get("recognition_object_id") == obj.get("recognition_object_id"), "recognition-index-entry-id")
    need(first.get("path") == "recognitions/current/recognition-object-0001.json", "recognition-index-entry-path")

if errors:
    print("[FAIL] PHASE 4 / STEP 75 recognition minimum verification failed")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("[PASS] PHASE 4 / STEP 75 recognition minimum verified")
