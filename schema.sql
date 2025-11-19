CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE routes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    grade TEXT,
    grade_int INTEGER,
    gym_id INTEGER REFERENCES gyms
);

CREATE TABLE climbed (
    user_id INTEGER REFERENCES users,
    route_id INTEGER REFERENCES routes,
    date TEXT
);

CREATE TABLE gyms (
    id INTEGER PRIMARY KEY,
    name TEXT
);