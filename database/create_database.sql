\c postgres;
DROP database quizup;
CREATE database quizup;

\c quizup;

CREATE TABLE quiz(
    quiz_id varchar(50) PRIMARY KEY,
    name varchar(50),
    times_played integer,
    num_questions integer
);

CREATE TABLE question(
	question_id varchar(50) PRIMARY KEY,
	question_statement varchar(500),
	options varchar(50) array[4],
	quiz_id varchar(50) REFERENCES quiz(quiz_id),
	difficulty integer,
    time_to_solve integer,
    points integer
);

CREATE TABLE users(
    user_id varchar(50) PRIMARY KEY,
    name varchar(50),
    email varchar(50),
    password varchar(50)
);

CREATE TABLE leaderboard(
  user_id varchar(50) REFERENCES users(user_id),
  points integer
);