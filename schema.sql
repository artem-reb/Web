CREATE TABLE IF NOT EXISTS articles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT not null,
    content TExt not null,
    photo text not null
);

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT not null UNIQUE,
    phone text not null UNIQUE,
    password_hash text not null
)