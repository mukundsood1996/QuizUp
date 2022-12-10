\c postgres;
DROP database pricing_list;
CREATE database pricing_list;

\c quizup;

CREATE TABLE users(
    user_id varchar(50) PRIMARY KEY,
    name varchar(50),
    email varchar(50) NOT NULL UNIQUE,
    password varchar(50) NOT NULL
);