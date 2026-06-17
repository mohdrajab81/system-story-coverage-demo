#!/usr/bin/env python3
"""Generate a System Story schema registry from a small JSON schema manifest.

Real projects should usually generate the registry from live contracts such as
SQL migrations or OpenAPI files. This demo uses a JSON manifest so the repository
is self-contained and easy to run in CI.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_schema(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Schema manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_entries(schema: dict) -> list[dict]:
    entries: list[dict] = []

    for enum in schema.get("enums", []):
        enum_name = enum["name"]
        for index, value in enumerate(enum.get("values", []), start=1):
            entries.append(
                {
                    "id": f"E.{enum_name}.{value}",
                    "kind": "enum_value",
                    "coverage_required": True,
                    "enum": enum_name,
                    "value": value,
                    "sort_order": index,
                }
            )

    for table in schema.get("tables", []):
        table_name = table["name"]
        for index, column in enumerate(table.get("columns", []), start=1):
            entries.append(
                {
                    "id": f"T.{table_name}.{column['name']}",
                    "kind": "table_column",
                    "coverage_required": True,
                    "relation": table_name,
                    "column": column["name"],
                    "data_type": column["type"],
                    "nullable": bool(column.get("nullable", True)),
                    "default": column.get("default"),
                    "generated": column.get("generated"),
                    "trigger_written": column.get("trigger_written"),
                    "ordinal_position": index,
                }
            )

    return sorted(entries, key=lambda item: item["id"])


def render_markdown(schema: dict, entries: list[dict]) -> str:
    lines = [
        "# Schema Registry",
        "",
        "> GENERATED FILE. Do not edit by hand.",
        "",
        f"- Project: `{schema.get('project', 'unknown')}`",
        f"- Entries: `{len(entries)}`",
        "",
        "| ID | Kind | Type/Value | Required |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        type_or_value = entry.get("value") or entry.get("data_type") or ""
        lines.append(
            f"| `{entry['id']}` | `{entry['kind']}` | `{type_or_value}` | `{entry['coverage_required']}` |"
        )
    lines.append("")
    return "\n".join(lines)


def write_registry(schema: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = build_entries(schema)
    payload = {
        "generated_at": "not recorded (deterministic output)",
        "source": {
            "project": schema.get("project", "unknown"),
            "description": schema.get("description", ""),
        },
        "entries": entries,
    }
    (out_dir / "schema-registry.generated.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "schema-registry.generated.md").write_text(
        render_markdown(schema, entries),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()

    schema = load_schema(args.schema)
    write_registry(schema, args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
