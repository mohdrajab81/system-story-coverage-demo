-- System Story Coverage Demo — initial schema
-- Uses the 'app' schema to keep domain tables separate from public.
-- Compatible with PostgreSQL 13+ (uses gen_random_uuid() built-in).

CREATE SCHEMA IF NOT EXISTS app;

-- Trigger function: refreshes updated_at on every UPDATE.
CREATE OR REPLACE FUNCTION app.touch_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- ------------------------------------------------------------------ enums

CREATE TYPE app.workspace_status AS ENUM ('active', 'suspended');

CREATE TYPE app.user_role AS ENUM ('owner', 'admin', 'member');

CREATE TYPE app.account_status AS ENUM ('invited', 'active', 'disabled');

CREATE TYPE app.session_status AS ENUM ('active', 'revoked');

-- 'suspend' records workspace suspension; 'disable' records account disable.
-- Keeping them separate in the enum makes audit queries unambiguous.
CREATE TYPE app.audit_action AS ENUM ('create', 'login', 'disable', 'suspend', 'revoke');

CREATE TYPE app.audit_actor_type AS ENUM ('system', 'user');

CREATE TYPE app.audit_object_type AS ENUM ('workspace', 'user_account', 'session');

-- ------------------------------------------------------------------ tables

CREATE TABLE app.workspace (
  id         uuid                 NOT NULL DEFAULT gen_random_uuid(),
  name       text                 NOT NULL,
  slug       text                 NOT NULL,
  status     app.workspace_status NOT NULL DEFAULT 'active',
  created_at timestamptz          NOT NULL DEFAULT now(),
  updated_at timestamptz          NOT NULL DEFAULT now()
);

CREATE TABLE app.user_account (
  id                  uuid               NOT NULL DEFAULT gen_random_uuid(),
  workspace_id        uuid               NOT NULL,
  email               text               NOT NULL,
  full_name           text               NOT NULL,
  role                app.user_role      NOT NULL,
  status              app.account_status NOT NULL DEFAULT 'invited',
  password_hash       text,
  password_changed_at timestamptz,
  last_login_at       timestamptz,
  created_at          timestamptz        NOT NULL DEFAULT now(),
  updated_at          timestamptz        NOT NULL DEFAULT now()
);

CREATE TABLE app.session (
  id                 uuid                NOT NULL DEFAULT gen_random_uuid(),
  workspace_id       uuid                NOT NULL,
  user_account_id    uuid                NOT NULL,
  status             app.session_status  NOT NULL DEFAULT 'active',
  access_token_hash  text                NOT NULL,
  refresh_token_hash text                NOT NULL,
  issued_at          timestamptz         NOT NULL DEFAULT now(),
  expires_at         timestamptz         NOT NULL,
  refresh_expires_at timestamptz         NOT NULL,
  revoked_at         timestamptz,
  created_at         timestamptz         NOT NULL DEFAULT now(),
  updated_at         timestamptz         NOT NULL DEFAULT now()
);

CREATE TABLE app.audit_event (
  id             uuid                   NOT NULL DEFAULT gen_random_uuid(),
  workspace_id   uuid,
  actor_type     app.audit_actor_type   NOT NULL,
  actor_id       uuid,
  action         app.audit_action       NOT NULL,
  object_type    app.audit_object_type  NOT NULL,
  object_id      uuid                   NOT NULL,
  summary        text                   NOT NULL,
  correlation_id uuid                   NOT NULL,
  occurred_at    timestamptz            NOT NULL DEFAULT now()
);

-- ------------------------------------------------------------------ triggers

CREATE TRIGGER touch_updated_at
  BEFORE UPDATE ON app.workspace
  FOR EACH ROW EXECUTE FUNCTION app.touch_updated_at();

CREATE TRIGGER touch_updated_at
  BEFORE UPDATE ON app.user_account
  FOR EACH ROW EXECUTE FUNCTION app.touch_updated_at();

CREATE TRIGGER touch_updated_at
  BEFORE UPDATE ON app.session
  FOR EACH ROW EXECUTE FUNCTION app.touch_updated_at();
