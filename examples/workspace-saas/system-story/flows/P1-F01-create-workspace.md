# P1-F01 — Create Workspace

A platform sign-up creates a workspace tenant and its initial owner account. The actor
supplies both the workspace display name and the URL slug — the slug is chosen by the
user, not auto-generated from the name. The owner account starts as `invited`; first
login and password setup are handled by a separate flow.

```json system-story
{
  "id": "P1-F01",
  "phase": "P1",
  "title": "Create workspace",
  "actor": "public_signup",
  "actor_sets": [
    "T.workspace.name",
    "T.workspace.slug",
    "T.user_account.email",
    "T.user_account.full_name"
  ],
  "app_sets": [
    "T.user_account.workspace_id",
    "T.user_account.role",
    "E.user_role.owner",
    "T.audit_event.workspace_id",
    "T.audit_event.actor_type",
    "E.audit_actor_type.system",
    "T.audit_event.actor_id",
    "T.audit_event.action",
    "E.audit_action.create",
    "T.audit_event.object_type",
    "E.audit_object_type.workspace",
    "T.audit_event.object_id",
    "T.audit_event.summary",
    "T.audit_event.correlation_id"
  ],
  "db_sets": [
    "T.workspace.id",
    "T.workspace.status",
    "E.workspace_status.active",
    "T.workspace.created_at",
    "T.workspace.updated_at",
    "T.user_account.id",
    "T.user_account.status",
    "E.account_status.invited",
    "T.user_account.created_at",
    "T.user_account.updated_at",
    "T.audit_event.id",
    "T.audit_event.occurred_at"
  ],
  "reads": [],
  "deferred": []
}
```
