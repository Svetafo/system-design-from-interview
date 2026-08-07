-- DDL for [system]. Every line is a design decision: type, nullability, key, index, comment.
-- Table names come from glossary.md, the snake_case name in each entity entry.
-- It has to apply to a real database, not merely read well:
--   docker run --rm -e POSTGRES_PASSWORD=x -d --name sd-pg postgres:16
--   docker exec -i sd-pg psql -U postgres -v ON_ERROR_STOP=1 < schema.sql
--   docker rm -f sd-pg

CREATE TABLE IF NOT EXISTS [entities] (
    id          BIGSERIAL   PRIMARY KEY,
    owner_id    TEXT        NOT NULL,           -- [what it refers to]
    name        TEXT        NOT NULL,           -- [what it holds]
    status      TEXT        NOT NULL DEFAULT '[DEFAULT]',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Enum values are the glossary's, verbatim. A CHECK is what makes them true at runtime
    -- rather than true in a document.
    CONSTRAINT [entities]_status_check
        CHECK (status IN ('[VALUE_A]', '[VALUE_B]')),

    -- A business rule the requirements state belongs here, not only in application code:
    -- two concurrent requests can both pass a check that the database does not enforce.
    CONSTRAINT uq_[entities]_owner_name UNIQUE (owner_id, name)
);

CREATE INDEX IF NOT EXISTS idx_[entities]_owner ON [entities] (owner_id);

COMMENT ON TABLE  [entities]        IS '[What one row is]';
COMMENT ON COLUMN [entities].status IS '[VALUE_A], [VALUE_B]';
