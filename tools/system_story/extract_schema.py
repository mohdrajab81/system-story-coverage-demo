#!/usr/bin/env python3
"""Generate the System Story schema registry from SQL migration files.

Creates a disposable PostgreSQL database, applies every *.sql file in the
migrations directory in filename order, introspects pg_catalog, writes registry
files, then drops the database. Does not parse SQL text.

Usage:
    python tools/system_story/extract_schema.py \
        --migrations-dir examples/workspace-saas/schema/migrations \
        --out-dir        examples/workspace-saas/system-story \
        --host localhost --port 5432 --user postgres --password postgres
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMP_DB_PREFIX = "sys_story_extract_"
DB_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


# --------------------------------------------------------------------------- helpers

def _format_cmd(cmd: list[str]) -> str:
    """Return a redacted, space-joined command string safe to print."""
    out: list[str] = []
    redact_next = False
    for part in cmd:
        if redact_next:
            out.append("<redacted>")
            redact_next = False
            continue
        out.append(part)
        if part.lower() in {"-password", "--password"}:
            redact_next = True
    return " ".join(out)


def _run(cmd: list[str], *, env: dict, capture: bool = False, timeout: int = 120) -> str:
    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit(f"Command timed out after {timeout}s: {_format_cmd(cmd)}")
    if result.returncode != 0:
        if capture:
            sys.stderr.write(result.stdout or "")
            sys.stderr.write(result.stderr or "")
        raise SystemExit(f"Command failed ({result.returncode}): {_format_cmd(cmd)}")
    return result.stdout if capture else ""


# --------------------------------------------------------------------------- psql helpers

def _psql(args: argparse.Namespace, database: str, sql: str, *, capture: bool = False) -> str:
    env = os.environ.copy()
    env["PGPASSWORD"] = args.password
    return _run(
        [
            args.psql,
            "-h", args.host,
            "-p", str(args.port),
            "-U", args.user,
            "-d", database,
            "-v", "ON_ERROR_STOP=1",
            "-q", "-t", "-A",
            "-c", sql,
        ],
        env=env,
        capture=capture,
    )


def _psql_json(args: argparse.Namespace, database: str, sql: str) -> list[dict]:
    """Run sql wrapped in jsonb_agg and return the parsed result list."""
    wrapped = (
        f"SELECT COALESCE(jsonb_agg(to_jsonb(q)), '[]'::jsonb)::text FROM ({sql}) q"
    )
    raw = _psql(args, database, wrapped, capture=True).strip()
    return json.loads(raw or "[]")


def _quote_ident(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


# --------------------------------------------------------------------------- database lifecycle

def _validate_temp_db_name(db_name: str) -> None:
    if not DB_NAME_RE.match(db_name):
        raise SystemExit(f"Unsafe disposable DB name: {db_name!r}")
    if not db_name.startswith(TEMP_DB_PREFIX):
        raise SystemExit(
            f"Disposable DB name must start with {TEMP_DB_PREFIX!r}; "
            f"refusing to manage {db_name!r}."
        )


def _create_database(args: argparse.Namespace, db_name: str) -> None:
    exists = _psql(
        args, "postgres",
        f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';",
        capture=True,
    ).strip()
    if exists:
        raise SystemExit(
            f"Disposable DB already exists: {db_name!r}. "
            "Drop it manually after confirming it is not in use."
        )
    _psql(args, "postgres", f"CREATE DATABASE {_quote_ident(db_name)};")


def _drop_database(args: argparse.Namespace, db_name: str) -> None:
    _psql(args, "postgres", f"DROP DATABASE IF EXISTS {_quote_ident(db_name)} WITH (FORCE);")


def _apply_migrations(args: argparse.Namespace, db_name: str, migrations_dir: Path) -> None:
    migration_files = sorted(migrations_dir.glob("*.sql"))
    if not migration_files:
        raise SystemExit(f"No .sql files found in {migrations_dir}")
    env = os.environ.copy()
    env["PGPASSWORD"] = args.password
    for sql_file in migration_files:
        print(f"  Applying {sql_file.name}...", flush=True)
        _run(
            [
                args.psql,
                "-h", args.host,
                "-p", str(args.port),
                "-U", args.user,
                "-d", db_name,
                "-v", "ON_ERROR_STOP=1",
                "-f", str(sql_file),
            ],
            env=env,
        )


# --------------------------------------------------------------------------- pg_catalog introspection

def _collect_schema(args: argparse.Namespace, db_name: str) -> dict:
    relations = _psql_json(args, db_name, """
        SELECT
          c.relname                              AS name,
          c.relkind,
          c.relispartition                       AS is_partition,
          parent.relname                         AS partition_parent,
          obj_description(c.oid, 'pg_class')    AS comment
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        LEFT JOIN pg_inherits i      ON i.inhrelid  = c.oid
        LEFT JOIN pg_class   parent  ON parent.oid  = i.inhparent
        WHERE n.nspname = 'app'
          AND c.relkind IN ('r', 'p', 'v', 'm')
        ORDER BY c.relkind, c.relname
    """)

    columns = _psql_json(args, db_name, """
        SELECT
          c.relname                                     AS relation_name,
          c.relkind,
          c.relispartition                              AS is_partition,
          parent.relname                                AS partition_parent,
          a.attnum                                      AS ordinal_position,
          a.attname                                     AS column_name,
          format_type(a.atttypid, a.atttypmod)         AS data_type,
          NOT a.attnotnull                              AS nullable,
          CASE
            WHEN a.attgenerated = ''
            THEN pg_get_expr(d.adbin, d.adrelid)
            ELSE NULL
          END                                           AS default_expr,
          CASE
            WHEN a.attgenerated <> ''
            THEN pg_get_expr(d.adbin, d.adrelid)
            ELSE NULL
          END                                           AS generated_expr,
          CASE a.attgenerated
            WHEN 's' THEN 'stored'
            WHEN 'v' THEN 'virtual'
            ELSE ''
          END                                           AS generated,
          CASE a.attidentity
            WHEN 'a' THEN 'always'
            WHEN 'd' THEN 'by_default'
            ELSE ''
          END                                           AS identity,
          col_description(c.oid, a.attnum)              AS comment,
          CASE
            WHEN a.attname = 'updated_at' AND EXISTS (
              SELECT 1
              FROM pg_trigger   tg
              JOIN pg_proc       p  ON p.oid  = tg.tgfoid
              JOIN pg_namespace pn  ON pn.oid = p.pronamespace
              WHERE tg.tgrelid = c.oid
                AND NOT tg.tgisinternal
                AND pn.nspname = 'app'
                AND p.proname  = 'touch_updated_at'
            )
            THEN 'app.touch_updated_at()'
            ELSE ''
          END                                           AS trigger_written
        FROM pg_class     c
        JOIN pg_namespace n      ON n.oid      = c.relnamespace
        JOIN pg_attribute a      ON a.attrelid = c.oid
        LEFT JOIN pg_attrdef  d  ON d.adrelid  = c.oid AND d.adnum = a.attnum
        LEFT JOIN pg_inherits i  ON i.inhrelid  = c.oid
        LEFT JOIN pg_class parent ON parent.oid = i.inhparent
        WHERE n.nspname = 'app'
          AND c.relkind IN ('r', 'p', 'v', 'm')
          AND a.attnum > 0
          AND NOT a.attisdropped
        ORDER BY c.relkind, c.relname, a.attnum
    """)

    enums = _psql_json(args, db_name, """
        SELECT
          t.typname       AS enum_name,
          e.enumlabel     AS enum_value,
          e.enumsortorder AS sort_order
        FROM pg_type      t
        JOIN pg_namespace n ON n.oid       = t.typnamespace
        JOIN pg_enum      e ON e.enumtypid = t.oid
        WHERE n.nspname = 'app'
        ORDER BY t.typname, e.enumsortorder
    """)

    triggers = _psql_json(args, db_name, """
        SELECT
          c.relname                                AS table_name,
          tg.tgname                                AS trigger_name,
          pn.nspname || '.' || p.proname || '()'  AS function_name
        FROM pg_trigger    tg
        JOIN pg_class       c  ON c.oid   = tg.tgrelid
        JOIN pg_namespace   n  ON n.oid   = c.relnamespace
        JOIN pg_proc        p  ON p.oid   = tg.tgfoid
        JOIN pg_namespace  pn  ON pn.oid  = p.pronamespace
        WHERE n.nspname = 'app'
          AND NOT tg.tgisinternal
        ORDER BY c.relname, tg.tgname
    """)

    return {
        "relations": relations,
        "columns": columns,
        "enums": enums,
        "triggers": triggers,
    }


# --------------------------------------------------------------------------- registry assembly

def _entry_id_for_column(column: dict) -> str:
    name = column["column_name"]
    if column["relkind"] in {"v", "m"}:
        return f"V.{column['relation_name']}.{name}"
    # ~ marks GENERATED ALWAYS AS columns. Flow stories cannot claim them in
    # actor_sets or app_sets — the database computes their value automatically.
    marker = "~" if column.get("generated") else ""
    return f"T.{column['relation_name']}.{marker}{name}"


def build_registry(raw: dict) -> dict:
    """Assemble the registry dict from raw pg_catalog data."""
    entries: list[dict] = []
    relation_by_name = {r["name"]: r for r in raw["relations"]}

    for column in raw["columns"]:
        relkind = column["relkind"]
        is_partition = bool(column["is_partition"])
        is_view = relkind in {"v", "m"}
        if is_view:
            kind = "view_column"
        elif is_partition:
            kind = "physical_partition_column"
        else:
            kind = "table_column"
        entries.append(
            {
                "id": _entry_id_for_column(column),
                "kind": kind,
                "coverage_required": not is_partition,
                "relation": column["relation_name"],
                "column": column["column_name"],
                "data_type": column["data_type"],
                "nullable": bool(column["nullable"]),
                "default": column["default_expr"] or "",
                "generated_expr": column["generated_expr"] or "",
                "generated": column["generated"] or "",
                "identity": column["identity"] or "",
                "trigger_written": column["trigger_written"] or "",
                "is_partition": is_partition,
                "partition_parent": column["partition_parent"] or "",
                "relkind": relkind,
                "comment": column["comment"] or "",
            }
        )

    for enum in raw["enums"]:
        entries.append(
            {
                "id": f"E.{enum['enum_name']}.{enum['enum_value']}",
                "kind": "enum_value",
                "coverage_required": True,
                "enum": enum["enum_name"],
                "value": enum["enum_value"],
                "sort_order": enum["sort_order"],
            }
        )

    return {
        "generated_at": "not recorded (deterministic output)",
        "source": {
            "method": "disposable PostgreSQL database built from SQL migrations, introspected via pg_catalog",
            "schema": "app",
        },
        "summary": {
            "relations": len(raw["relations"]),
            "domain_tables": sum(
                1 for r in raw["relations"]
                if r["relkind"] in {"r", "p"} and not r["is_partition"]
            ),
            "physical_partitions": sum(1 for r in raw["relations"] if r["is_partition"]),
            "views": sum(1 for r in raw["relations"] if r["relkind"] in {"v", "m"}),
            "enum_types": len({e["enum_name"] for e in raw["enums"]}),
            "entries": len(entries),
            "coverage_required_entries": sum(1 for e in entries if e["coverage_required"]),
        },
        "relations": raw["relations"],
        "triggers": raw["triggers"],
        "entries": sorted(entries, key=lambda e: e["id"]),
        "relation_comments": {
            name: (relation.get("comment") or "")
            for name, relation in sorted(relation_by_name.items())
        },
    }


# --------------------------------------------------------------------------- markdown rendering

def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend(
        "| " + " | ".join(cell.replace("\n", " ") for cell in row) + " |"
        for row in rows
    )
    return out


def render_markdown(registry: dict) -> str:
    entries = registry["entries"]
    required = [e for e in entries if e["coverage_required"]]
    domain_columns = [e for e in required if e["kind"] == "table_column"]
    view_columns = [e for e in required if e["kind"] == "view_column"]
    enum_values = [e for e in required if e["kind"] == "enum_value"]
    physical = [e for e in entries if not e["coverage_required"]]

    lines: list[str] = [
        "# System Story Schema Registry",
        "",
        "> GENERATED FILE. Do not edit by hand.",
        "> Source: SQL migrations applied to a disposable PostgreSQL database,",
        "> then introspected through `pg_catalog`.",
        "",
        f"- Domain tables: `{registry['summary']['domain_tables']}`",
        f"- Views: `{registry['summary']['views']}`",
        f"- Enum types: `{registry['summary']['enum_types']}`",
        f"- Coverage-required IDs: `{registry['summary']['coverage_required_entries']}`",
        "",
        "## Stable ID Rules",
        "",
        "- `T.<table>.<column>` — table column",
        "- `T.<table>.~<column>` — generated/computed column (cannot appear in `actor_sets` or `app_sets`)",
        "- `E.<enum>.<value>` — enum value",
        "- `V.<view>.<column>` — view column",
        "",
        "## Table Columns",
        "",
    ]
    lines += _md_table(
        ["ID", "Type", "Null", "Default", "Trigger Written"],
        [
            [
                f"`{e['id']}`",
                f"`{e['data_type']}`",
                _yes_no(e["nullable"]),
                f"`{e['default'] or 'none'}`",
                f"`{e['trigger_written'] or 'none'}`",
            ]
            for e in domain_columns
        ],
    )

    if view_columns:
        lines += ["", "## View Columns", ""]
        lines += _md_table(
            ["ID", "Type", "Null"],
            [[f"`{e['id']}`", f"`{e['data_type']}`", _yes_no(e["nullable"])] for e in view_columns],
        )

    lines += ["", "## Enum Values", ""]
    lines += _md_table(
        ["ID", "Enum", "Value"],
        [[f"`{e['id']}`", f"`{e['enum']}`", f"`{e['value']}`"] for e in enum_values],
    )

    if physical:
        lines += ["", "## Physical Partition Columns", ""]
        lines += _md_table(
            ["ID", "Parent", "Type", "Null"],
            [
                [
                    f"`{e['id']}`",
                    f"`{e['partition_parent'] or 'none'}`",
                    f"`{e['data_type']}`",
                    _yes_no(e["nullable"]),
                ]
                for e in physical
            ],
        )

    lines += ["", "## Triggers", ""]
    if registry["triggers"]:
        lines += _md_table(
            ["Table", "Trigger", "Function"],
            [
                [f"`{t['table_name']}`", f"`{t['trigger_name']}`", f"`{t['function_name']}`"]
                for t in registry["triggers"]
            ],
        )
    else:
        lines.append("No non-internal triggers found in the app schema.")

    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- output

def write_outputs(registry: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    registry_json = out_dir / "schema-registry.generated.json"
    registry_md = out_dir / "schema-registry.generated.md"
    registry_json.write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    registry_md.write_text(render_markdown(registry), encoding="utf-8")
    def _display(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(ROOT))
        except ValueError:
            return str(p)

    print(f"Wrote {_display(registry_json)}", flush=True)
    print(f"Wrote {_display(registry_md)}", flush=True)


# --------------------------------------------------------------------------- CLI

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--migrations-dir", required=True, type=Path,
                        help="Directory containing *.sql migration files applied in filename order.")
    parser.add_argument("--out-dir", required=True, type=Path,
                        help="Directory where registry files are written.")
    parser.add_argument("--host",     default="localhost")
    parser.add_argument("--port",     default=5432, type=int)
    parser.add_argument("--user",     default="postgres")
    parser.add_argument("--password", default=os.environ.get("PGPASSWORD", "postgres"))
    parser.add_argument("--psql",     default="psql")
    parser.add_argument("--keep-db",  action="store_true",
                        help="Do not drop the disposable database after extraction.")
    parser.add_argument("--db-name",  help="Override the generated disposable database name.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    args.psql = shutil.which(args.psql) or args.psql

    migrations_dir = args.migrations_dir.resolve()
    if not migrations_dir.is_dir():
        raise SystemExit(f"Migrations directory not found: {migrations_dir}")

    db_name = args.db_name or (
        TEMP_DB_PREFIX + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
    )
    _validate_temp_db_name(db_name)

    created = False
    try:
        print(f"Creating disposable database {db_name!r}...", flush=True)
        _create_database(args, db_name)
        created = True

        print("Applying migrations...", flush=True)
        _apply_migrations(args, db_name, migrations_dir)

        print("Introspecting pg_catalog...", flush=True)
        raw = _collect_schema(args, db_name)

        registry = build_registry(raw)
        write_outputs(registry, args.out_dir)
    finally:
        if created and not args.keep_db:
            print(f"Dropping disposable database {db_name!r}...", flush=True)
            _drop_database(args, db_name)


if __name__ == "__main__":
    main()
