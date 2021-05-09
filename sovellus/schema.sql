CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    name TEXT,
    user_id INTEGER REFERENCES users,
    visible INTEGER
);

CREATE TABLE chains (
    id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES areas,
    subject TEXT,
    opening_message TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id SERIAL PRIAMRY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    chain_id INTEGER REFERENCES chains
);
