\c postgres;
DROP database quizup;
CREATE database quizup;

\c quizup;

CREATE TABLE quiz(
    quiz_id varchar(50) PRIMARY KEY,
    name varchar(50) ,
    times_played integer DEFAULT 0,
    num_questions integer DEFAULT 0
);

CREATE TABLE question(
	question_id varchar(50) PRIMARY KEY,
	question_statement varchar(500) NOT NULL ,
	options varchar(50) array[4] NOT NULL ,
	quiz_id varchar(50) REFERENCES quiz(quiz_id),
	difficulty integer NOT NULL ,
    time_to_solve integer NOT NULL ,
    points integer NOT NULL
);

CREATE TABLE users(
    user_id varchar(50) PRIMARY KEY,
    name varchar(50),
    email varchar(50) NOT NULL UNIQUE,
    password varchar(50) NOT NULL
);

CREATE TABLE leaderboard(
  user_id varchar(50) REFERENCES users(user_id),
  points integer
);