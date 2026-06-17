# P2-F02 — Disable Member

An administrator disables a member account. The disabled user can no longer create new
sessions.

```json system-story
{
  "id": "P2-F02",
  "phase": "P2",
  "title": "Disable member",
  "actor": "workspace_admin",
  "actor_sets": [],
  "app_sets": [
    "T.user_account.status",
    "E.account_status.disabled",
    "T.audit_event.workspace_id",
    "T.audit_event.actor_type",
    "E.audit_actor_type.user",
    "T.audit_event.actor_id",
    "T.audit_event.action",
    "E.audit_action.disable",
    "T.audit_event.object_type",
    "E.audit_object_type.user_account",
    "T.audit_event.object_id",
    "T.audit_event.summary",
    "T.audit_event.correlation_id"
  ],
  "db_sets": [
    "T.user_account.updated_at",
    "T.audit_event.id",
    "T.audit_event.occurred_at"
  ],
  "reads": [
    "T.workspace.id",
    "T.workspace.status",
    "E.workspace_status.active",
    "T.user_account.id",
    "T.user_account.workspace_id",
    "T.user_account.role",
    "E.user_role.admin",
    "E.user_role.member",
    "T.user_account.status",
    "E.account_status.active"
  ],
  "deferred": []
}
```
