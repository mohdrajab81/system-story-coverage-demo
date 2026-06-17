# P1-F02 — Invite Admin User

The workspace owner invites a second administrator. The invited admin gets a login
account scoped to the same workspace.

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
    "E.user_role.admin",
    "T.audit_event.workspace_id",
    "T.audit_event.actor_type",
    "E.audit_actor_type.user",
    "T.audit_event.actor_id",
    "T.audit_event.action",
    "E.audit_action.create",
    "T.audit_event.object_type",
    "E.audit_object_type.user_account",
    "T.audit_event.object_id",
    "T.audit_event.summary",
    "T.audit_event.correlation_id"
  ],
  "db_sets": [
    "T.user_account.id",
    "T.user_account.status",
    "E.account_status.invited",
    "T.user_account.created_at",
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
    "E.user_role.owner",
    "T.user_account.status",
    "E.account_status.active"
  ],
  "deferred": []
}
```
