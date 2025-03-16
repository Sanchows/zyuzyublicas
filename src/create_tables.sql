CREATE TABLE sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL CHECK(url LIKE 'http://%' OR url LIKE 'https://%'),
    xpath TEXT NOT NULL
);