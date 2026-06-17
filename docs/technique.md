# System Story Coverage

System Story Coverage is a flow-based way to connect a database schema to real
product behavior.

The purpose is simple:

> Every important field should have a reason to exist.

It is useful **before, during, and after** development — not only when rebuilding
a legacy system.

- **Before and during a new build**, it stops the schema from growing by
  accident. Every new field must earn its place from day one, so the new system
  does not quietly become the next legacy mess.
- **After the fact, on an existing system**, it recovers the lost "why" behind
  fields nobody can confidently explain anymore.

The strongest use is the new-build case, because the cheapest time to explain a
field is the moment it is created — not two years later when the person who added
it has gone.

## Core Idea

First, generate a stable registry from the real database schema.

Example IDs:

- `T.workspace.name`: a table column.
- `E.user_role.admin`: an enum value.
- `T.trip.~duration_seconds`: a database-generated column. The `~` marks a
  value computed by the database.
- `V.report.active_user_count`: a view column, if the project chooses to cover
  views.

Then write one small story per business flow.

Each story classifies the fields and enum values it touches:

- `actor_sets`: supplied by the user or client request.
- `app_sets`: written or derived by application code.
- `db_sets`: created by database defaults, generated columns, or triggers.
- `reads`: checked or used but not changed.
- `deferred`: intentionally in scope but not covered yet.

## Why Both Column And Enum Value?

A column token says which field is involved:

```text
T.workspace.status
```

An enum token says which state is involved:

```text
E.workspace_status.suspended
```

Together they say:

```text
This flow sets workspace.status to suspended.
```

Without the enum value, you only know that the field changed. You do not know
which business state the flow produced.

This is why the technique is more useful than a normal field list. It shows the
business meaning of the data.

## Why This Helps

For every field, the team can ask:

- Why does it exist?
- Who owns it?
- Who can change it?
- When does it change?
- Which user journey depends on it?
- Which API contract should expose it?
- Which tests should cover it?
- Which screens or workers may be affected by a future change?

## Why It Helps AI-Assisted Work

AI assistants work better when the context is small, specific, and structured.

System Story Coverage creates that context.

Instead of loading a whole repository into an AI conversation, you can provide:

- the generated schema registry,
- the generated coverage report,
- and the few story files related to the change.

That can reduce token usage and reduce confusion. It also gives the AI a clear
map of ownership:

- user-provided values,
- backend-derived values,
- database-generated values,
- read-only dependencies,
- and intentionally deferred items.

This makes it easier to ask focused questions such as:

- "Which fields are affected if we change this flow?"
- "Which OpenAPI endpoint should expose these fields?"
- "Which tests should be updated?"
- "Is this new column justified by any story?"

## Benefits You Might Not Expect

The five categories were designed to answer "who sets this field?" But the same
classification turns out to be useful for several things the technique was not
originally built for.

### A built-in security map

`actor_sets` is more than "fields the user enters." It is the complete list of
every field that untrusted input can influence, across the whole system, in one
place. That is an attack-surface map you normally have to build by hand.

This makes two security questions easy to answer:

- **What can an attacker reach?** Read every `actor_sets` entry.
- **Which fields must never be settable from a request body?** Anything in
  `db_sets` or `app_sets`. A request that lets a client write one of those is a
  mass-assignment bug. The registry tells you exactly which fields to lock down.

For systems that hold sensitive or regulated data, this is a real safety benefit,
not a side effect.

### A privacy and compliance trace

The registry already records where every field is set and where it is read. Mark
which fields hold personal data and you have a trace of exactly which flows touch
it — which is what data-retention, consent, and right-to-be-forgotten work all
need. The coverage report becomes evidence that you know where sensitive data
flows, instead of a promise that you do.

### Dead-field detection

A field that appears in `db_sets` but never in any `reads` is written but never
consumed — stored data that no flow uses. The classification surfaces this
write-only dead weight so it can be removed instead of carried forever.

### A shared language for product and engineering

Flow files describe business journeys, not SQL. A non-technical product owner can
read one and confirm that the engineering understanding matches the business
intent. Very few artifacts are readable and verifiable by both sides at once.

### Durable institutional memory

When the person who designed the schema leaves, the reasoning usually leaves with
them. Story files keep the "why" in the repository, so the next engineer — or the
next AI session — does not have to reverse-engineer intent from column names.

> Note: the security map, the privacy trace, and dead-field detection are
> capabilities the classification makes possible. The demo tool in this repo
> checks coverage, unknown references, and invalid category claims; the other
> uses build on the same registry but are applied by the team, not automated
> here.

## Practical Workflow

1. Write or update SQL migrations.
2. Apply the migrations to a disposable PostgreSQL database.
3. Introspect PostgreSQL using `pg_catalog`.
4. Generate the schema registry.
5. Write or update one story file per flow.
6. Run the coverage report in strict mode.
7. Investigate uncovered IDs.
8. Treat unknown IDs or invalid category claims as design errors.
9. Use the stories to guide OpenAPI, UI journeys, tests, and authorization.
10. Re-run the same checks in CI.

## What This Is Not

System Story Coverage is not a replacement for:

- BDD scenarios,
- user stories,
- event storming,
- database migrations,
- OpenAPI specifications,
- automated tests.

It is a traceability layer that connects them.

## Schema Source

In production, generate the registry from live contracts.

For this demo, that means:

1. Apply SQL migrations to a real PostgreSQL instance.
2. Ask PostgreSQL what schema it created.
3. Generate the registry from that answer.

This is stronger than hand-maintaining a registry file because hand-maintained
documents drift quickly. The registry should be generated by scripts and checked
in CI.
