# System Story Coverage

System Story Coverage is a flow-based technique for validating a schema against
real product behavior.

## Core Idea

Create a stable registry of every coverage-relevant schema item:

- table columns: `T.workspace.name`
- generated/computed columns: `T.trip.~duration_seconds` (the `~` prefix marks columns the database computes — flow stories cannot claim them in `actor_sets` or `app_sets`)
- enum values: `E.user_role.admin`
- view columns, if applicable: `V.report.active_user_count`

Then write one small system story per business flow. Each story classifies the
fields and enum values it touches:

- `actor_sets`: supplied by the human or client request
- `app_sets`: explicitly written or derived by application or service logic
- `db_sets`: produced by database defaults, generated columns, or triggers
- `reads`: checked or used but not changed
- `deferred`: intentionally in scope but not covered yet

## Why Both Column and Enum Value?

A column token (`T.workspace.status`) tells you which field changes.
An enum value token (`E.workspace_status.suspended`) tells you which state the
flow transitions to.

Together they give you: "this flow sets workspace.status to suspended." Without
the enum token, you only know the field was written — not what value it received
or which business state it represents. This is what makes the registry a product
accountability map rather than just a field list. It lets you trace which flows
produce each state, and which tests need to protect each transition.

## Why This Helps

For every field you can answer:

- Why does it exist?
- Who owns the value?
- When does it change?
- Which user journey depends on it?
- Which API contract should expose it?
- Which tests should cover it?

## Practical Workflow

1. Generate a schema registry from live SQL migrations via pg_catalog.
2. Write flows one by one.
3. Run the coverage report in strict mode.
4. Investigate uncovered IDs.
5. Treat unknown IDs or invalid category claims as design errors — fix the story or fix the schema.
6. Use the stories to drive OpenAPI design, UI journeys, and test cases.
7. Re-run coverage after every schema migration.

## What This Is Not

System Story Coverage is not a replacement for:

- BDD scenarios
- user stories
- event storming
- database migrations
- OpenAPI specifications
- automated tests

It is a traceability layer that connects them.

## Schema Source

In production, always generate the registry from live contracts — SQL migrations
applied to a real PostgreSQL instance and introspected through `pg_catalog`. This
guarantees the registry reflects exactly what the database engine sees, including
computed defaults, trigger-written columns, and generated expressions.

Avoid hand-maintaining the registry. A hand-maintained file drifts from the real
schema within days. The registry should be a CI artifact, not a document.
