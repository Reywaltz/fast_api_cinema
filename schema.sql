CREATE TABLE IF NOT EXISTS film (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    description TEXT,
    film_path TEXT,
    poster_path TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    access_token TEXT,
    valid_to TIMESTAMP WITH TIME ZONE
)