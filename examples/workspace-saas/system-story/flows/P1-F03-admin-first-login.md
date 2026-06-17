# P1-F03 — Admin First Login

An invited admin completes first login. The backend stores the password hash, activates
the account, creates a session, and records the login audit event.

```json system-story
{
  "id": "P1-F03",
  "phase": "P1",
  "title": "Admin first login",
  "actor": "workspace_admin",
  "actor_sets": [],
  "app_sets": [
    "T.user_account.password_hash",
    "T.user_account.password_changed_at",
    "T.user_account.status",
    "E.account_status.active",
    "T.user_account.last_login_at",
    "T.session.workspace_id",
    "T.session.user_account_id",
    "T.session.access_token_hash",
    "T.session.refresh_token_hash",
    "T.session.expires_at",
    "T.session.refresh_expires_at",
    "T.audit_event.workspace_id",
    "T.audit_event.actor_type",
    "E.audit_actor_type.user",
    "T.audit_event.actor_id",
    "T.audit_event.action",
    "E.audit_action.login",
    "T.audit_event.object_type",
    "E.audit_object_type.user_account",
    "T.audit_event.object_id",
    "T.audit_event.summary",
    "T.audit_event.correlation_id"
  ],
  "db_sets": [
    "T.user_account.updated_at",
    "T.session.id",
    "T.session.status",
    "E.session_status.active",
    "T.session.issued_at",
    "T.session.created_at",
    "T.session.updated_at",
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
    "T.user_account.email",
    "T.user_account.status",
    "E.account_status.invited"
  ],
  "deferred": []
}
```
