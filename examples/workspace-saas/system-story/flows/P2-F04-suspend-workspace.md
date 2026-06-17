# P2-F04 — Suspend Workspace

A system process suspends a workspace, for example because the billing or compliance state
requires temporary lockout.

```json system-story
{
  "id": "P2-F04",
  "phase": "P2",
  "title": "Suspend workspace",
  "actor": "system",
  "actor_sets": [],
  "app_sets": [
    "T.workspace.status",
    "E.workspace_status.suspended",
    "T.audit_event.workspace_id",
    "T.audit_event.actor_type",
    "E.audit_actor_type.system",
    "T.audit_event.actor_id",
    "T.audit_event.action",
    "E.audit_action.disable",
    "T.audit_event.object_type",
    "E.audit_object_type.workspace",
    "T.audit_event.object_id",
    "T.audit_event.summary",
    "T.audit_event.correlation_id"
  ],
  "db_sets": [
    "T.workspace.updated_at",
    "T.audit_event.id",
    "T.audit_event.occurred_at"
  ],
  "reads": [
    "T.workspace.id",
    "T.workspace.status",
    "E.workspace_status.active"
  ],
  "deferred": []
}
```
