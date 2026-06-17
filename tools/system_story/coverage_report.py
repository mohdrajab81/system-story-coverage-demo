#!/usr/bin/env python3
"""Generate a coverage report from strict System Story JSON blocks."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


CATEGORIES = ("actor_sets", "app_sets", "db_sets", "reads", "deferred")
REQUIRED_FIELDS = ("id", "phase", "title", "actor", *CATEGORIES)
ALLOWED_FIELDS = set(REQUIRED_FIELDS)
BLOCK_RE = re.compile(r"```json system-story\s*(.*?)```", re.S)
TOKEN_RE = re.compile(r"^[TEV]\.[A-Za-z0-9_~.]+$")
FLOW_ID_RE = re.compile(r"^P\d+-F\d+$")


def load_registry(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Registry JSON not found: {path}")
    registry = json.loads(path.read_text(encoding="utf-8"))
    ids = [entry["id"] for entry in registry.get("entries", [])]
    duplicates = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
    if duplicates:
        raise SystemExit("Registry has duplicate IDs: " + ", ".join(duplicates))
    return registry


def validate_token(token: str, *, path: Path, flow_id: str, category: str) -> None:
    if not isinstance(token, str):
        raise SystemExit(f"{path}: {flow_id}.{category} has non-string token: {token!r}")
    if not TOKEN_RE.match(token):
        raise SystemExit(f"{path}: {flow_id}.{category} has invalid token: {token}")


def load_flows(flow_dir: Path) -> list[dict]:
    flows: list[dict] = []
    seen_ids: set[str] = set()
    for path in sorted(flow_dir.glob("P*-F*.md")):
        text = path.read_text(encoding="utf-8")
        matches = BLOCK_RE.findall(text)
        if len(matches) != 1:
            raise SystemExit(f"{path}: expected exactly one json system-story block, found {len(matches)}")
        try:
            data = json.loads(matches[0])
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}: invalid JSON system-story block: {exc}") from exc

        flow_id = data.get("id")
        if not isinstance(flow_id, str) or not FLOW_ID_RE.match(flow_id):
            raise SystemExit(f"{path}: flow id must match P<number>-F<number>")
        if not path.stem.startswith(flow_id):
            raise SystemExit(f"{path}: filename must start with flow id {flow_id}")
        if flow_id in seen_ids:
            raise SystemExit(f"{path}: duplicate flow id {flow_id}")
        seen_ids.add(flow_id)

        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            raise SystemExit(f"{path}: {flow_id} missing required fields: {', '.join(missing)}")
        extra = sorted(set(data) - ALLOWED_FIELDS)
        if extra:
            raise SystemExit(f"{path}: {flow_id} has unsupported fields: {', '.join(extra)}")
        if data["phase"] != flow_id.split("-")[0]:
            raise SystemExit(f"{path}: {flow_id}.phase must match id prefix")

        for category in CATEGORIES:
            if not isinstance(data[category], list):
                raise SystemExit(f"{path}: {flow_id}.{category} must be an array")
            for token in data[category]:
                validate_token(token, path=path, flow_id=flow_id, category=category)
            duplicates = sorted({token for token in data[category] if data[category].count(token) > 1})
            if duplicates:
                raise SystemExit(
                    f"{path}: {flow_id}.{category} contains duplicate tokens: " + ", ".join(duplicates)
                )
        data["_path"] = str(path)
        flows.append(data)
    return flows


def category_is_valid(entry: dict, category: str) -> tuple[bool, str]:
    if entry["kind"] == "enum_value":
        return True, ""
    if entry["kind"] != "table_column":
        return False, "only table columns and enum values are supported by this demo"
    if category == "db_sets":
        if entry.get("default") or entry.get("generated") or entry.get("trigger_written"):
            return True, ""
        return False, "db_sets requires a default, generated expression, or trigger writer"
    if category in {"actor_sets", "app_sets"}:
        if not entry.get("generated"):
            return True, ""
        return False, f"{category} cannot claim generated columns"
    return True, ""


def summarize(registry: dict, flows: list[dict]) -> dict:
    entries = {entry["id"]: entry for entry in registry.get("entries", [])}
    required_ids = {
        entry["id"] for entry in registry.get("entries", []) if entry.get("coverage_required", True)
    }
    used_by_category: dict[str, dict[str, list[str]]] = {
        category: defaultdict(list) for category in CATEGORIES
    }
    unknown: dict[str, list[str]] = defaultdict(list)
    invalid_claims: list[dict] = []

    for flow in flows:
        for category in CATEGORIES:
            for token in flow[category]:
                if token not in entries:
                    unknown[token].append(flow["id"])
                    continue
                ok, reason = category_is_valid(entries[token], category)
                if not ok:
                    invalid_claims.append(
                        {"id": token, "flow": flow["id"], "category": category, "reason": reason}
                    )
                    continue
                used_by_category[category][token].append(flow["id"])

    covered = set()
    for category in ("actor_sets", "app_sets", "db_sets", "reads"):
        covered.update(used_by_category[category].keys())
    deferred = set(used_by_category["deferred"].keys())
    uncovered = required_ids - covered - deferred
    return {
        "entries": entries,
        "required_ids": required_ids,
        "used_by_category": used_by_category,
        "unknown": dict(sorted(unknown.items())),
        "invalid_claims": invalid_claims,
        "covered": covered,
        "deferred": deferred,
        "uncovered": uncovered,
    }


def render_report(registry: dict, flows: list[dict], summary: dict) -> str:
    lines = [
        "# System Story Coverage Report",
        "",
        "> GENERATED FILE. Do not edit by hand.",
        "",
        f"- Registry generated at: `{registry.get('generated_at', 'unknown')}`",
        f"- Flow files scanned: `{len(flows)}`",
        f"- Coverage-required IDs: `{len(summary['required_ids'])}`",
        f"- Covered IDs: `{len(summary['covered'])}`",
        f"- Deferred IDs: `{len(summary['deferred'])}`",
        f"- Uncovered IDs: `{len(summary['uncovered'])}`",
        f"- Unknown IDs: `{len(summary['unknown'])}`",
        f"- Invalid category claims: `{len(summary['invalid_claims'])}`",
        "",
        "## Flow Inventory",
        "",
        "| Flow | Title | Actor |",
        "| --- | --- | --- |",
    ]
    for flow in flows:
        lines.append(f"| `{flow['id']}` | {flow['title']} | `{flow['actor']}` |")

    lines += ["", "## Uncovered IDs", ""]
    if summary["uncovered"]:
        for token in sorted(summary["uncovered"]):
            lines.append(f"- `{token}`")
    else:
        lines.append("None.")

    lines += ["", "## Unknown IDs", ""]
    if summary["unknown"]:
        for token, flow_ids in summary["unknown"].items():
            lines.append(f"- `{token}` used by {', '.join(flow_ids)}")
    else:
        lines.append("None.")

    lines += ["", "## Invalid Category Claims", ""]
    if summary["invalid_claims"]:
        for claim in summary["invalid_claims"]:
            lines.append(
                f"- `{claim['id']}` in `{claim['flow']}.{claim['category']}`: {claim['reason']}"
            )
    else:
        lines.append("None.")

    lines += ["", "## Covered IDs By Category", ""]
    for category in CATEGORIES:
        lines += [f"### `{category}`", ""]
        items = summary["used_by_category"][category]
        if not items:
            lines.append("None.")
        else:
            for token in sorted(items):
                lines.append(f"- `{token}`: {', '.join(items[token])}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--flows", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    flows = load_flows(args.flows)
    summary = summarize(registry, flows)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(registry, flows, summary), encoding="utf-8")

    if args.strict and (summary["unknown"] or summary["invalid_claims"] or summary["uncovered"]):
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
