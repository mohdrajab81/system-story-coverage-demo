# P2-F03 — Logout Session Revoke

A logged-in user logs out. The backend revokes the session and records an audit event.

```json system-story
{
  "id": "P2-F03",
  "phase": "P2",
  "title": "Logout session revoke",
  "actor": "workspace_user",
  "actor_sets": [],
  "app_sets": [
    "T.session.status",
    "E.session_status.revoked",
    "T.session.revoked_at",
    "T.audit_event.workspace_id",
    "T.audit_event.actor_type",
    "E.audit_actor_type.user",
    "T.audit_event.actor_id",
    "T.audit_event.action",
    "E.audit_action.revoke",
    "T.audit_event.object_type",
    "E.audit_object_type.session",
    "T.audit_event.object_id",
    "T.audit_event.summary",
    "T.audit_event.correlation_id"
  ],
  "db_sets": [
    "T.session.updated_at",
    "T.audit_event.id",
    "T.audit_event.occurred_at"
  ],
  "reads": [
    "T.workspace.id",
    "T.session.id",
    "T.session.workspace_id",
    "T.session.user_account_id",
    "T.session.status",
    "E.session_status.active",
    "T.user_account.id",
    "T.user_account.status",
    "E.account_status.active"
  ],
  "deferred": []
}
```
