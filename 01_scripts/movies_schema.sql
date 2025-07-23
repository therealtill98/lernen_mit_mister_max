BEGIN;

-- Clean slate (safe to re-run)
DROP TABLE IF EXISTS movie_cast CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS movie CASCADE;

CREATE TABLE movie (
    movie_id     BIGINT PRIMARY KEY,
    title        TEXT NOT NULL,
    release_date DATE
);

CREATE TABLE person (
    person_id BIGINT PRIMARY KEY,
    name      TEXT NOT NULL,
    gender    INT
);

CREATE TABLE movie_cast (
    movie_id       BIGINT REFERENCES movie(movie_id) ON DELETE CASCADE,
    person_id      BIGINT REFERENCES person(person_id) ON DELETE CASCADE,
    character_name TEXT,
    cast_order     INT,
    PRIMARY KEY (movie_id, person_id)
);

CREATE INDEX idx_movie_title       ON movie (title);
CREATE INDEX idx_movie_cast_person ON movie_cast (person_id);

COMMIT;
