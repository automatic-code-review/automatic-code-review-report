CREATE TABLE IF NOT EXISTS merge
(
    id_merge_internal  SERIAL PRIMARY KEY,
    id_merge           INTEGER      NOT NULL,
    id_project         INTEGER      NOT NULL,
    id_group           INTEGER      NOT NULL,
    ds_author_username VARCHAR(256) NOT NULL,
    dh_merge           TIMESTAMP    NOT NULL,
    CONSTRAINT un_merge_external UNIQUE (id_merge, id_project, id_group)
);

CREATE TABLE IF NOT EXISTS comment
(
    id_comment_internal SERIAL PRIMARY KEY,
    id_merge_internal   INTEGER      NOT NULL REFERENCES merge (id_merge_internal),
    id_comment          VARCHAR(128) NOT NULL,
    lk_comment          VARCHAR(512) NOT NULL,
    ds_type             VARCHAR(256) NOT NULL,
    tx_comment          TEXT         NOT NULL,
    tp_status           INTEGER      NOT NULL DEFAULT 0,
    constraint un_comment_external UNIQUE (id_merge_internal, id_comment)
);

ALTER TABLE comment
    ADD COLUMN IF NOT EXISTS dh_insercao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
