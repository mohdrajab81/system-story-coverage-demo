import json
from pathlib import Path

from tools.system_story.coverage_report import load_flows, load_registry, summarize


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "examples/workspace-saas/system-story/schema-registry.generated.json"
FLOWS_DIR = ROOT / "examples/workspace-saas/system-story/flows"


def test_schema_registry_ids_are_unique():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    ids = [entry["id"] for entry in registry["entries"]]

    assert len(ids) == len(set(ids))
    assert "T.workspace.id" in ids
    assert "E.user_role.admin" in ids


def test_registry_has_expected_ids():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in registry["entries"]}

    assert "E.audit_action.suspend" in ids, "suspend value must be in audit_action enum"
    assert "E.audit_action.disable" in ids, "disable value must remain in audit_action enum"
    assert registry["summary"]["coverage_required_entries"] == 59


def test_demo_coverage_is_strict_clean():
    registry = load_registry(REGISTRY_PATH)
    flows = load_flows(FLOWS_DIR)
    summary = summarize(registry, flows)

    assert len(flows) == 7
    assert not summary["unknown"]
    assert not summary["invalid_claims"]
    assert not summary["uncovered"]
