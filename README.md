# System Story Coverage Demo

System Story Coverage is a simple way to answer one question:

> Can every database field be explained by a real system flow?

Most systems have fields that nobody can confidently explain later. A field may
exist because of an old screen, an old API, a one-time workaround, or a business
rule that was never written down.

Here, "field" means one piece of stored data, such as a user's email, an account
status, or the time a record was created. "Enum value" means one allowed state,
such as `active`, `disabled`, or `admin`.

This technique makes every important field and enum value traceable to the flow
that creates it, reads it, changes it, or depends on it.

This repository is a small public demo. It uses a fake SaaS workspace system so
the idea can be shared safely without exposing any private product schema.

## The Idea In Plain English

1. Start from the real database schema.
2. Give every field and enum value a stable ID.
3. Write one small story file for each system flow.
4. In each story, list which fields the flow touches.
5. Run a script that checks whether every required field is covered.

If a new field is added to the database but no story explains it, the coverage
report fails. That is the point: the schema and the product behavior stay in
sync.

## Small Example

Imagine this field:

```text
T.user_account.email
```

The ID means:

- `T` means table column.
- `user_account` is the table.
- `email` is the column.

Now imagine this enum value:

```text
E.user_role.admin
```

The ID means:

- `E` means enum value.
- `user_role` is the enum.
- `admin` is one allowed value.

A flow story can then say:

```text
In "Invite admin user", the actor supplies user_account.email,
and the application sets user_role to admin.
```

That makes the database field understandable through a real business action.

## What This Demo Contains

- Real SQL migration files.
- A script that creates a temporary PostgreSQL database.
- The script applies the migrations and asks PostgreSQL what the schema really is.
- Generated schema registry files with stable IDs.
- One Markdown story file per flow.
- A generated coverage report.
- Tests and GitHub Actions CI.

The registry is generated from PostgreSQL `pg_catalog`. The tool does not parse
SQL text by hand.

## Repository Layout

```text
examples/workspace-saas/schema/migrations/
  Real SQL migration files.

examples/workspace-saas/system-story/flows/
  One Markdown file per business flow.

examples/workspace-saas/system-story/schema-registry.generated.json
  Generated list of database fields and enum values.

examples/workspace-saas/system-story/coverage-report.generated.md
  Generated coverage report.

tools/system_story/extract_schema.py
  Builds the registry from PostgreSQL.

tools/system_story/coverage_report.py
  Checks the story files against the registry.

tests/
  Small regression tests.
```

## Prerequisites

You need:

- Python 3.11 or newer.
- PostgreSQL 13 or newer.
- `psql` available on your command line.

If you do not already have PostgreSQL running locally, Docker is the easiest
way to try the demo.

## Quick Start With Docker

Step 1: clone the repo.

```bash
git clone https://github.com/mohdrajab81/system-story-coverage-demo.git
cd system-story-coverage-demo
```

Step 2: start a temporary PostgreSQL database on port `5433`.

```bash
docker run --name sys-story-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  -d postgres:16
```

Step 3: generate the schema registry.

This creates a disposable database inside PostgreSQL, applies the SQL
migrations, reads the real schema from PostgreSQL, writes the generated registry,
and drops the disposable database.

```bash
python tools/system_story/extract_schema.py \
  --migrations-dir examples/workspace-saas/schema/migrations \
  --out-dir examples/workspace-saas/system-story \
  --host localhost \
  --port 5433 \
  --user postgres \
  --password postgres
```

Step 4: generate the strict coverage report.

```bash
python tools/system_story/coverage_report.py \
  --registry examples/workspace-saas/system-story/schema-registry.generated.json \
  --flows examples/workspace-saas/system-story/flows \
  --report examples/workspace-saas/system-story/coverage-report.generated.md \
  --strict
```

Step 5: run the tests.

```bash
python -m pip install pytest
python -m pytest
```

Step 6: stop the demo database when finished.

```bash
docker stop sys-story-postgres
docker rm sys-story-postgres
```

## Run With An Existing PostgreSQL Server

If you already have PostgreSQL running on port `5432`, use:

```bash
python tools/system_story/extract_schema.py \
  --migrations-dir examples/workspace-saas/schema/migrations \
  --out-dir examples/workspace-saas/system-story \
  --host localhost \
  --port 5432 \
  --user postgres \
  --password postgres
```

You can also avoid putting the password in the command by using `PGPASSWORD`.

PowerShell:

```powershell
$env:PGPASSWORD = "postgres"
python tools/system_story/extract_schema.py `
  --migrations-dir examples/workspace-saas/schema/migrations `
  --out-dir examples/workspace-saas/system-story `
  --host localhost `
  --port 5432 `
  --user postgres
```

Bash:

```bash
export PGPASSWORD=postgres
python tools/system_story/extract_schema.py \
  --migrations-dir examples/workspace-saas/schema/migrations \
  --out-dir examples/workspace-saas/system-story \
  --host localhost \
  --port 5432 \
  --user postgres
```

## What Success Looks Like

The coverage report should say:

```text
Flow files scanned: 7
Coverage-required IDs: 59
Covered IDs: 59
Deferred IDs: 0
Uncovered IDs: 0
Unknown IDs: 0
Invalid category claims: 0
```

That means every required field and enum value in this demo schema is explained
by at least one story file.

## How A Story Classifies Fields

Each flow file contains a small machine-readable block. The block uses the
`json system-story` info string. GitHub does not apply syntax highlighting to
this block because the info string is not a standard language tag, but the
content is valid JSON and is machine-readable by the coverage tool.

```json system-story
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

The categories mean:

- `actor_sets`: the user or client request provides this value.
- `app_sets`: backend logic writes or derives this value.
- `db_sets`: the database default, generated column, or trigger creates this value.
- `reads`: the flow checks or uses this value without changing it.
- `deferred`: the ID is intentionally not covered yet.

## Why This Is Useful

System Story Coverage helps teams answer:

- Why does this field exist?
- Who is allowed to set it?
- Is it entered by a user, calculated by code, or created by the database?
- Which screen or API needs it?
- Which tests should protect it?
- What breaks if we rename, remove, or change it?
- Which business state does each enum value represent?

It is especially useful when rebuilding a legacy system because it prevents
teams from blindly copying old tables into the new system.

## Why It Helps AI Work

This technique also helps AI-assisted engineering.

Instead of giving an AI assistant the whole database, all source code, and all
product notes, you can give it:

- the generated schema registry,
- the generated coverage report,
- and only the few story files related to the change.

That usually means fewer tokens, less irrelevant context, and fewer wrong
assumptions. The AI can reason from a focused map of the system instead of a
large pile of unrelated files.

It also makes AI review easier. A requested change can be checked against the
story files to see which fields, APIs, screens, and tests are likely affected.

## CI

GitHub Actions runs the same workflow automatically:

1. Start a PostgreSQL 16 container.
2. Install Python test dependencies.
3. Generate the schema registry from SQL migrations.
4. Generate the strict coverage report.
5. Run pytest.

If a migration adds a new required field and no story covers it, CI fails.

## What This Does Not Replace

System Story Coverage does not replace:

- user stories,
- BDD scenarios,
- event storming,
- database migrations,
- OpenAPI specifications,
- automated tests.

It connects those things to the database schema.

## Further Reading

See `docs/technique.md` for a more detailed explanation of the technique.
