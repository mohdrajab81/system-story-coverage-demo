# Schema Registry

> GENERATED FILE. Do not edit by hand.

- Project: `workspace-saas`
- Entries: `58`

| ID | Kind | Type/Value | Required |
| --- | --- | --- | --- |
| `E.account_status.active` | `enum_value` | `active` | `True` |
| `E.account_status.disabled` | `enum_value` | `disabled` | `True` |
| `E.account_status.invited` | `enum_value` | `invited` | `True` |
| `E.audit_action.create` | `enum_value` | `create` | `True` |
| `E.audit_action.disable` | `enum_value` | `disable` | `True` |
| `E.audit_action.login` | `enum_value` | `login` | `True` |
| `E.audit_action.revoke` | `enum_value` | `revoke` | `True` |
| `E.audit_actor_type.system` | `enum_value` | `system` | `True` |
| `E.audit_actor_type.user` | `enum_value` | `user` | `True` |
| `E.audit_object_type.session` | `enum_value` | `session` | `True` |
| `E.audit_object_type.user_account` | `enum_value` | `user_account` | `True` |
| `E.audit_object_type.workspace` | `enum_value` | `workspace` | `True` |
| `E.session_status.active` | `enum_value` | `active` | `True` |
| `E.session_status.revoked` | `enum_value` | `revoked` | `True` |
| `E.user_role.admin` | `enum_value` | `admin` | `True` |
| `E.user_role.member` | `enum_value` | `member` | `True` |
| `E.user_role.owner` | `enum_value` | `owner` | `True` |
| `E.workspace_status.active` | `enum_value` | `active` | `True` |
| `E.workspace_status.suspended` | `enum_value` | `suspended` | `True` |
| `T.audit_event.action` | `table_column` | `audit_action` | `True` |
| `T.audit_event.actor_id` | `table_column` | `uuid` | `True` |
| `T.audit_event.actor_type` | `table_column` | `audit_actor_type` | `True` |
| `T.audit_event.correlation_id` | `table_column` | `uuid` | `True` |
| `T.audit_event.id` | `table_column` | `uuid` | `True` |
| `T.audit_event.object_id` | `table_column` | `uuid` | `True` |
| `T.audit_event.object_type` | `table_column` | `audit_object_type` | `True` |
| `T.audit_event.occurred_at` | `table_column` | `timestamptz` | `True` |
| `T.audit_event.summary` | `table_column` | `text` | `True` |
| `T.audit_event.workspace_id` | `table_column` | `uuid` | `True` |
| `T.session.access_token_hash` | `table_column` | `text` | `True` |
| `T.session.created_at` | `table_column` | `timestamptz` | `True` |
| `T.session.expires_at` | `table_column` | `timestamptz` | `True` |
| `T.session.id` | `table_column` | `uuid` | `True` |
| `T.session.issued_at` | `table_column` | `timestamptz` | `True` |
| `T.session.refresh_expires_at` | `table_column` | `timestamptz` | `True` |
| `T.session.refresh_token_hash` | `table_column` | `text` | `True` |
| `T.session.revoked_at` | `table_column` | `timestamptz` | `True` |
| `T.session.status` | `table_column` | `session_status` | `True` |
| `T.session.updated_at` | `table_column` | `timestamptz` | `True` |
| `T.session.user_account_id` | `table_column` | `uuid` | `True` |
| `T.session.workspace_id` | `table_column` | `uuid` | `True` |
| `T.user_account.created_at` | `table_column` | `timestamptz` | `True` |
| `T.user_account.email` | `table_column` | `text` | `True` |
| `T.user_account.full_name` | `table_column` | `text` | `True` |
| `T.user_account.id` | `table_column` | `uuid` | `True` |
| `T.user_account.last_login_at` | `table_column` | `timestamptz` | `True` |
| `T.user_account.password_changed_at` | `table_column` | `timestamptz` | `True` |
| `T.user_account.password_hash` | `table_column` | `text` | `True` |
| `T.user_account.role` | `table_column` | `user_role` | `True` |
| `T.user_account.status` | `table_column` | `account_status` | `True` |
| `T.user_account.updated_at` | `table_column` | `timestamptz` | `True` |
| `T.user_account.workspace_id` | `table_column` | `uuid` | `True` |
| `T.workspace.created_at` | `table_column` | `timestamptz` | `True` |
| `T.workspace.id` | `table_column` | `uuid` | `True` |
| `T.workspace.name` | `table_column` | `text` | `True` |
| `T.workspace.slug` | `table_column` | `text` | `True` |
| `T.workspace.status` | `table_column` | `workspace_status` | `True` |
| `T.workspace.updated_at` | `table_column` | `timestamptz` | `True` |
