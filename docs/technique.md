# System Story Coverage Technique

System Story Coverage is a flow-based way to validate a schema against real
product behavior.

## Core Idea

Create a stable registry of every coverage-relevant schema item:

- table columns: `T.workspace.name`
- enum values: `E.user_role.admin`
- view columns, if applicable: `V.report.active_user_count`

Then write one small system story per business flow. Each story classifies the
fields and enum values it touches:

- `actor_sets`: supplied by the human or client request.
- `app_sets`: explicitly written or derived by application/service logic.
- `db_sets`: produced by database defaults, generated columns, or triggers.
- `reads`: checked or used but not changed.
- `deferred`: intentionally in scope, but not covered yet.

## Why This Helps

It turns a schema into a product accountability map.

For every field, you can ask:

- Why does it exist?
- Who owns the value?
- When does it change?
- Which user journey depends on it?
- Which API contract should expose it?
- Which tests should cover it?

## Practical Workflow

1. Generate a schema registry.
2. Write flows one by one.
3. Run the coverage report in strict mode.
4. Investigate uncovered IDs.
5. Treat unknown IDs or invalid category claims as design errors.
6. Use the stories to design OpenAPI, UI journeys, and tests.
7. Re-run coverage after every schema change.

## What This Is Not

This is not a replacement for:

- BDD scenarios
- user stories
- event storming
- database migrations
- OpenAPI
- automated tests

It is a traceability layer that connects them.

## Naming

Useful names for the technique:

- System Story Coverage
- Flow-Based Schema Coverage
- Story-Driven Schema Traceability
