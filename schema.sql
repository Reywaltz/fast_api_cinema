CREATE TABLE IF NOT EXISTS film (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    description TEXT,
    film_path TEXT,
    poster_path TEXT
)