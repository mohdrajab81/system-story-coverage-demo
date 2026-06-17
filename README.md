# System Story Coverage Demo

System Story Coverage is a lightweight technique for connecting schema fields
and enum values to real business flows.

The basic rule:

> Every field and enum value should be justified by at least one system story,
> or explicitly excluded from the current scope.

This repo is a public-safe demo. It uses a small synthetic SaaS workspace
system, not a real product schema.

## What This Demonstrates

- A machine-readable schema registry with stable IDs such as `T.workspace.name`
  and `E.account_status.active`.
- One Markdown file per business flow.
- A strict `json system-story` block inside each flow.
- A coverage report showing which schema IDs are covered, deferred, uncovered,
  unknown, or incorrectly categorized.
- Scripts and tests that can run in CI.

## Example Flow Fragment

```json
{
  "id": "P1-F02",
  "phase": "P1",
  "title": "Invite admin user",
  "actor": "workspace_owner",
  "actor_sets": [
    "T.user_account.email",
    "T.user_account.full_name"
  ],
  "app_sets": [
    "T.user_account.workspace_id",
    "T.user_account.role",
    "E.user_role.admin"
  ],
  "db_sets": [
    "T.user_account.id",
    "T.user_account.status",
    "E.account_status.invited"
  ],
  "reads": [
    "T.workspace.id",
    "T.workspace.status",
    "E.workspace_status.active"
  ],
  "deferred": []
}
```

## Repository Layout

```text
examples/workspace-saas/schema/source-schema.json
examples/workspace-saas/system-story/schema-registry.generated.json
examples/workspace-saas/system-story/coverage-report.generated.md
examples/workspace-saas/system-story/flows/
tools/system_story/extract_schema.py
tools/system_story/coverage_report.py
tests/
```

## Run The Demo

Generate the registry from the example schema manifest:

```bash
python tools/system_story/extract_schema.py \
  --schema examples/workspace-saas/schema/source-schema.json \
  --out-dir examples/workspace-saas/system-story
```

Generate the coverage report:

```bash
python tools/system_story/coverage_report.py \
  --registry examples/workspace-saas/system-story/schema-registry.generated.json \
  --flows examples/workspace-saas/system-story/flows \
  --report examples/workspace-saas/system-story/coverage-report.generated.md \
  --strict
```

Run tests:

```bash
python -m pytest
```

## Why It Is Useful

System Story Coverage helps answer:

- Why does this field exist?
- Who sets it: actor, application, or database?
- Which flows read it?
- Which API endpoint or screen needs it?
- Which tests should protect it?
- What changes if this field changes?

It does not replace user stories, BDD, event storming, or OpenAPI. It connects
them to the schema.

## Public Demo Note

This repository intentionally uses a synthetic example. In real systems, the
registry should preferably be generated from live contracts such as SQL
migrations, not hand-maintained.
