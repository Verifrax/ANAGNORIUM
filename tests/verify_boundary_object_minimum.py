#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    p = ROOT / rel
    if not p.exists():
        raise SystemExit(f"FAIL missing-file {rel}")
    try:
        return json.loads(p.read_text())
    except Exception as e:
        raise SystemExit(f"FAIL invalid-json {rel}: {e}")

def need(cond, msg):
    if not cond:
        raise SystemExit(f"FAIL {msg}")

policy = load("contracts/boundary-policy.json")
recognition_schema = load("schemas/recognition-object.schema.json")
output_schema = load("schemas/recognition-output.schema.json")
audit_schema = load("schemas/recognition-audit-record.schema.json")
current_obj = load("recognitions/current/recognition-object-0001.json")
current_idx = load("recognitions/current/index.json")
output_fixture = load("fixtures/recognition-output.valid.json")
audit_fixture = load("fixtures/recognition-audit-record.valid.json")

print("[VERIFY] files-present")

need(policy["object_type"] == "BOUNDARY_POLICY", "boundary policy object_type")
need(policy["surface"] == "ANAGNORIUM", "boundary policy surface")
need(policy["role"] == "terminal-recognition", "boundary policy role")

allowed = set(policy["allowed_output_classes"])
forbidden = set(policy["forbidden_output_classes"])
need(allowed.isdisjoint(forbidden), "allowed/forbidden overlap")

required_reasons = {
    "would-author-law",
    "would-mutate-accepted-state",
    "would-issue-authority",
    "would-execute-governed-action",
    "would-emit-verification-verdict",
    "would-assign-burden",
    "would-assign-remedy",
    "would-assign-closure",
    "would-assign-terminal-recourse"
}
need(required_reasons.issubset(set(policy["rejection_reasons"])), "missing rejection reasons")

print("[VERIFY] boundary-policy-core")

need(current_obj["object_type"] == "RecognitionObject", "current recognition object type")
need(current_obj["status"] == "ACTIVE_TRUTH", "current recognition object status")
need(current_obj["recognition_index_ref"] == "recognitions/current/index.json", "recognition index ref")
need(current_obj["historical_archive_ref"] == "recognitions/history/", "historical archive ref")
need(current_obj["recognition_status"] == "RECOGNIZED", "recognition status")
need(current_obj["admissibility_status"] == "ADMISSIBLE", "admissibility status")

assertions = set(current_obj["boundary_assertions"])
need("recognition does not assign burden" in assertions, "missing non-burden assertion")
need("recognition does not assign remedy" in assertions, "missing non-remedy assertion")
need("recognition does not perform closure" in assertions, "missing non-closure assertion")

print("[VERIFY] recognition-object-core")

need(current_idx["object_type"] == "RecognitionIndex", "current index type")
need(current_idx["status"] == "ACTIVE_TRUTH", "current index status")
need(current_idx["historical"] is False, "current index historical false")
need(current_idx["current_recognition_object_ref"] == "recognitions/current/recognition-object-0001.json", "current object ref")
need(current_idx["entries"][0]["path"] == "recognitions/current/recognition-object-0001.json", "index entry path")

print("[VERIFY] recognition-index-core")

need(output_fixture["object_type"] == "RECOGNITION_OUTPUT", "output fixture type")
need(output_fixture["boundary_assertions"]["not-recourse"] is True, "output fixture non-recourse")
need(audit_fixture["object_type"] == "RECOGNITION_AUDIT_RECORD", "audit fixture type")
need(audit_fixture["decision"] == "rejected", "audit fixture decision")
need(audit_fixture["rejection_reason"] == "would-assign-burden", "audit fixture reason")
need(audit_fixture["sovereign_collision_flags"]["burden"] is True, "audit fixture burden flag")
need(audit_fixture["sovereign_collision_flags"]["recourse"] is True, "audit fixture recourse flag")

print("[VERIFY] output-and-audit-core")

try:
    import jsonschema  # type: ignore
except Exception:
    print("[VERIFY] jsonschema-module absent -> structural verification only")
else:
    from jsonschema import Draft202012Validator, FormatChecker  # type: ignore
    Draft202012Validator(recognition_schema, format_checker=FormatChecker()).validate(current_obj)
    Draft202012Validator(output_schema, format_checker=FormatChecker()).validate(output_fixture)
    Draft202012Validator(audit_schema, format_checker=FormatChecker()).validate(audit_fixture)
    Draft202012Validator(load("schemas/boundary-policy.schema.json"), format_checker=FormatChecker()).validate(policy)
    print("[VERIFY] full-jsonschema-validation")

print("[PASS] PHASE 2 / STEP 7 boundary-object minimum verified")
