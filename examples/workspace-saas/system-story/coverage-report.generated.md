# System Story Coverage Report

> GENERATED FILE. Do not edit by hand.

- Registry generated at: `not recorded (deterministic output)`
- Flow files scanned: `7`
- Coverage-required IDs: `58`
- Covered IDs: `58`
- Deferred IDs: `0`
- Uncovered IDs: `0`
- Unknown IDs: `0`
- Invalid category claims: `0`

## Flow Inventory

| Flow | Title | Actor |
| --- | --- | --- |
| `P1-F01` | Create workspace | `public_signup` |
| `P1-F02` | Invite admin user | `workspace_owner` |
| `P1-F03` | Admin first login | `workspace_admin` |
| `P2-F01` | Invite member | `workspace_admin` |
| `P2-F02` | Disable member | `workspace_admin` |
| `P2-F03` | Logout session revoke | `workspace_user` |
| `P2-F04` | Suspend workspace | `system` |

## Uncovered IDs

None.

## Unknown IDs

None.

## Invalid Category Claims

None.

## Covered IDs By Category

### `actor_sets`

- `T.user_account.email`: P1-F01, P1-F02, P2-F01
- `T.user_account.full_name`: P1-F01, P1-F02, P2-F01
- `T.workspace.name`: P1-F01
- `T.workspace.slug`: P1-F01

### `app_sets`

- `E.account_status.active`: P1-F03
- `E.account_status.disabled`: P2-F02
- `E.audit_action.create`: P1-F01, P1-F02, P2-F01
- `E.audit_action.disable`: P2-F02, P2-F04
- `E.audit_action.login`: P1-F03
- `E.audit_action.revoke`: P2-F03
- `E.audit_actor_type.system`: P1-F01, P2-F04
- `E.audit_actor_type.user`: P1-F02, P1-F03, P2-F01, P2-F02, P2-F03
- `E.audit_object_type.session`: P2-F03
- `E.audit_object_type.user_account`: P1-F02, P1-F03, P2-F01, P2-F02
- `E.audit_object_type.workspace`: P1-F01, P2-F04
- `E.session_status.revoked`: P2-F03
- `E.user_role.admin`: P1-F02
- `E.user_role.member`: P2-F01
- `E.user_role.owner`: P1-F01
- `E.workspace_status.suspended`: P2-F04
- `T.audit_event.action`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.actor_id`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.actor_type`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.correlation_id`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.object_id`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.object_type`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.summary`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.workspace_id`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.session.access_token_hash`: P1-F03
- `T.session.expires_at`: P1-F03
- `T.session.refresh_expires_at`: P1-F03
- `T.session.refresh_token_hash`: P1-F03
- `T.session.revoked_at`: P2-F03
- `T.session.status`: P2-F03
- `T.session.user_account_id`: P1-F03
- `T.session.workspace_id`: P1-F03
- `T.user_account.last_login_at`: P1-F03
- `T.user_account.password_changed_at`: P1-F03
- `T.user_account.password_hash`: P1-F03
- `T.user_account.role`: P1-F01, P1-F02, P2-F01
- `T.user_account.status`: P1-F03, P2-F02
- `T.user_account.workspace_id`: P1-F01, P1-F02, P2-F01
- `T.workspace.status`: P2-F04

### `db_sets`

- `E.account_status.invited`: P1-F01, P1-F02, P2-F01
- `E.session_status.active`: P1-F03
- `E.workspace_status.active`: P1-F01
- `T.audit_event.id`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.audit_event.occurred_at`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.session.created_at`: P1-F03
- `T.session.id`: P1-F03
- `T.session.issued_at`: P1-F03
- `T.session.status`: P1-F03
- `T.session.updated_at`: P1-F03, P2-F03
- `T.user_account.created_at`: P1-F01, P1-F02, P2-F01
- `T.user_account.id`: P1-F01, P1-F02, P2-F01
- `T.user_account.status`: P1-F01, P1-F02, P2-F01
- `T.user_account.updated_at`: P1-F01, P1-F02, P1-F03, P2-F01, P2-F02
- `T.workspace.created_at`: P1-F01
- `T.workspace.id`: P1-F01
- `T.workspace.status`: P1-F01
- `T.workspace.updated_at`: P1-F01, P2-F04

### `reads`

- `E.account_status.active`: P1-F02, P2-F01, P2-F02, P2-F03
- `E.account_status.invited`: P1-F03
- `E.session_status.active`: P2-F03
- `E.user_role.admin`: P1-F03, P2-F01, P2-F02
- `E.user_role.member`: P2-F02
- `E.user_role.owner`: P1-F02
- `E.workspace_status.active`: P1-F02, P1-F03, P2-F01, P2-F02, P2-F04
- `T.session.id`: P2-F03
- `T.session.status`: P2-F03
- `T.session.user_account_id`: P2-F03
- `T.session.workspace_id`: P2-F03
- `T.user_account.email`: P1-F03
- `T.user_account.id`: P1-F02, P1-F03, P2-F01, P2-F02, P2-F03
- `T.user_account.role`: P1-F02, P1-F03, P2-F01, P2-F02
- `T.user_account.status`: P1-F02, P1-F03, P2-F01, P2-F02, P2-F03
- `T.user_account.workspace_id`: P1-F02, P1-F03, P2-F01, P2-F02
- `T.workspace.id`: P1-F02, P1-F03, P2-F01, P2-F02, P2-F03, P2-F04
- `T.workspace.status`: P1-F02, P1-F03, P2-F01, P2-F02, P2-F04

### `deferred`

None.
