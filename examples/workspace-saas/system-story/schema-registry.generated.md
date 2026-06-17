# System Story Schema Registry

> GENERATED FILE. Do not edit by hand.
> Source: SQL migrations applied to a disposable PostgreSQL database,
> then introspected through `pg_catalog`.

- Domain tables: `4`
- Views: `0`
- Enum types: `7`
- Coverage-required IDs: `59`

## Stable ID Rules

- `T.<table>.<column>` — table column
- `T.<table>.~<column>` — generated/computed column (cannot appear in `actor_sets` or `app_sets`)
- `E.<enum>.<value>` — enum value
- `V.<view>.<column>` — view column

## Table Columns

| ID | Type | Null | Default | Trigger Written |
| --- | --- | --- | --- | --- |
| `T.audit_event.action` | `app.audit_action` | no | `none` | `none` |
| `T.audit_event.actor_id` | `uuid` | yes | `none` | `none` |
| `T.audit_event.actor_type` | `app.audit_actor_type` | no | `none` | `none` |
| `T.audit_event.correlation_id` | `uuid` | no | `none` | `none` |
| `T.audit_event.id` | `uuid` | no | `gen_random_uuid()` | `none` |
| `T.audit_event.object_id` | `uuid` | no | `none` | `none` |
| `T.audit_event.object_type` | `app.audit_object_type` | no | `none` | `none` |
| `T.audit_event.occurred_at` | `timestamp with time zone` | no | `now()` | `none` |
| `T.audit_event.summary` | `text` | no | `none` | `none` |
| `T.audit_event.workspace_id` | `uuid` | yes | `none` | `none` |
| `T.session.access_token_hash` | `text` | no | `none` | `none` |
| `T.session.created_at` | `timestamp with time zone` | no | `now()` | `none` |
| `T.session.expires_at` | `timestamp with time zone` | no | `none` | `none` |
| `T.session.id` | `uuid` | no | `gen_random_uuid()` | `none` |
| `T.session.issued_at` | `timestamp with time zone` | no | `now()` | `none` |
| `T.session.refresh_expires_at` | `timestamp with time zone` | no | `none` | `none` |
| `T.session.refresh_token_hash` | `text` | no | `none` | `none` |
| `T.session.revoked_at` | `timestamp with time zone` | yes | `none` | `none` |
| `T.session.status` | `app.session_status` | no | `'active'::app.session_status` | `none` |
| `T.session.updated_at` | `timestamp with time zone` | no | `now()` | `app.touch_updated_at()` |
| `T.session.user_account_id` | `uuid` | no | `none` | `none` |
| `T.session.workspace_id` | `uuid` | no | `none` | `none` |
| `T.user_account.created_at` | `timestamp with time zone` | no | `now()` | `none` |
| `T.user_account.email` | `text` | no | `none` | `none` |
| `T.user_account.full_name` | `text` | no | `none` | `none` |
| `T.user_account.id` | `uuid` | no | `gen_random_uuid()` | `none` |
| `T.user_account.last_login_at` | `timestamp with time zone` | yes | `none` | `none` |
| `T.user_account.password_changed_at` | `timestamp with time zone` | yes | `none` | `none` |
| `T.user_account.password_hash` | `text` | yes | `none` | `none` |
| `T.user_account.role` | `app.user_role` | no | `none` | `none` |
| `T.user_account.status` | `app.account_status` | no | `'invited'::app.account_status` | `none` |
| `T.user_account.updated_at` | `timestamp with time zone` | no | `now()` | `app.touch_updated_at()` |
| `T.user_account.workspace_id` | `uuid` | no | `none` | `none` |
| `T.workspace.created_at` | `timestamp with time zone` | no | `now()` | `none` |
| `T.workspace.id` | `uuid` | no | `gen_random_uuid()` | `none` |
| `T.workspace.name` | `text` | no | `none` | `none` |
| `T.workspace.slug` | `text` | no | `none` | `none` |
| `T.workspace.status` | `app.workspace_status` | no | `'active'::app.workspace_status` | `none` |
| `T.workspace.updated_at` | `timestamp with time zone` | no | `now()` | `app.touch_updated_at()` |

## Enum Values

| ID | Enum | Value |
| --- | --- | --- |
| `E.account_status.active` | `account_status` | `active` |
| `E.account_status.disabled` | `account_status` | `disabled` |
| `E.account_status.invited` | `account_status` | `invited` |
| `E.audit_action.create` | `audit_action` | `create` |
| `E.audit_action.disable` | `audit_action` | `disable` |
| `E.audit_action.login` | `audit_action` | `login` |
| `E.audit_action.revoke` | `audit_action` | `revoke` |
| `E.audit_action.suspend` | `audit_action` | `suspend` |
| `E.audit_actor_type.system` | `audit_actor_type` | `system` |
| `E.audit_actor_type.user` | `audit_actor_type` | `user` |
| `E.audit_object_type.session` | `audit_object_type` | `session` |
| `E.audit_object_type.user_account` | `audit_object_type` | `user_account` |
| `E.audit_object_type.workspace` | `audit_object_type` | `workspace` |
| `E.session_status.active` | `session_status` | `active` |
| `E.session_status.revoked` | `session_status` | `revoked` |
| `E.user_role.admin` | `user_role` | `admin` |
| `E.user_role.member` | `user_role` | `member` |
| `E.user_role.owner` | `user_role` | `owner` |
| `E.workspace_status.active` | `workspace_status` | `active` |
| `E.workspace_status.suspended` | `workspace_status` | `suspended` |

## Triggers

| Table | Trigger | Function |
| --- | --- | --- |
| `session` | `touch_updated_at` | `app.touch_updated_at()` |
| `user_account` | `touch_updated_at` | `app.touch_updated_at()` |
| `workspace` | `touch_updated_at` | `app.touch_updated_at()` |
