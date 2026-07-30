-- Personal AI Trainer: schema for the example package.
-- Table and enum names come from glossary.md. Applied against a live PostgreSQL 16 as the
-- validation step, so this file is proven to run, not only proofread.

create type goal as enum ('STRENGTH', 'ENDURANCE', 'WEIGHT_LOSS');
create type plan_status as enum ('DRAFT', 'ACTIVE', 'DONE');

create table users (
    id          uuid primary key,
    email       text        not null unique,
    created_at  timestamptz not null default now()
);

create table training_plans (
    id          uuid primary key,
    user_id     uuid        not null references users (id) on delete cascade,
    goal        goal        not null,
    status      plan_status not null default 'DRAFT',
    weeks       integer     not null check (weeks between 1 and 24),
    created_at  timestamptz not null default now(),
    adapted_at  timestamptz,
    -- A DONE plan is immutable, so it must have been adapted at least once or never at all;
    -- the rule that adaptation never touches past weeks lives in the Adaptation Engine.
    constraint adapted_after_created check (adapted_at is null or adapted_at >= created_at)
);

-- FR-7 and ADR-0002: at most one unfinished plan per User, enforced by the database so that two
-- concurrent creations or activations cannot both succeed. Covering DRAFT as well as ACTIVE is what
-- makes activation on first read safe: a second draft can never be waiting to take the same slot.
create unique index one_unfinished_plan_per_user
    on training_plans (user_id)
    where status <> 'DONE';

create index training_plans_user_id_idx on training_plans (user_id);

create table sessions (
    id                uuid        primary key,
    plan_id           uuid        not null references training_plans (id) on delete cascade,
    completed_at      timestamptz not null,
    duration_minutes  integer     not null check (duration_minutes between 1 and 600),
    perceived_effort  integer     check (perceived_effort between 1 and 10),
    created_at        timestamptz not null default now()
);

-- Adaptation loads the Sessions of a plan in completion order on every write (ADR-0001).
create index sessions_plan_completed_idx on sessions (plan_id, completed_at);
