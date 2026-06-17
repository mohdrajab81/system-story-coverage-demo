import json
from pathlib import Path

from tools.system_story.coverage_report import load_flows, load_registry, summarize
from tools.system_story.extract_schema import build_entries, load_schema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "examples/workspace-saas/schema/source-schema.json"
REGISTRY_PATH = ROOT / "examples/workspace-saas/system-story/schema-registry.generated.json"
FLOWS_DIR = ROOT / "examples/workspace-saas/system-story/flows"


def test_schema_registry_ids_are_unique():
    schema = load_schema(SCHEMA_PATH)
    entries = build_entries(schema)
    ids = [entry["id"] for entry in entries]

    assert len(ids) == len(set(ids))
    assert "T.workspace.id" in ids
    assert "E.user_role.admin" in ids


def test_generated_registry_matches_source_schema():
    generated = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    schema = load_schema(SCHEMA_PATH)

    assert generated["generated_at"] == "not recorded (deterministic output)"
    assert generated["entries"] == build_entries(schema)


def test_demo_coverage_is_strict_clean():
    registry = load_registry(REGISTRY_PATH)
    flows = load_flows(FLOWS_DIR)
    summary = summarize(registry, flows)

    assert len(flows) == 7
    assert not summary["unknown"]
    assert not summary["invalid_claims"]
    assert not summary["uncovered"]

