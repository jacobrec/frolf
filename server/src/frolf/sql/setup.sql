-- :name clear-table-users
-- :command :execute
DROP TABLE IF EXISTS users;
-- :name clear-table-groups
-- :command :execute
DROP TABLE IF EXISTS groups;
-- :name clear-table-courses
-- :command :execute
DROP TABLE IF EXISTS courses;
-- :name clear-table-holes
-- :command :execute
DROP TABLE IF EXISTS holes;
-- :name clear-table-games
-- :command :execute
DROP TABLE IF EXISTS games;
-- :name clear-table-scores
-- :command :execute
DROP TABLE IF EXISTS scores;

-- :name clear-table-usergame
-- :command :execute
DROP TABLE IF EXISTS user_game;

-- :name create-table-groups
-- :command :execute
CREATE TABLE groups (
  id INT AUTO_INCREMENT,
  name VARCHAR(256),
  pass VARCHAR(256),
  PRIMARY KEY(id)
);

-- :name create-table-users
-- :command :execute
CREATE TABLE users (
  id INT AUTO_INCREMENT,
  gid INT,
  name VARCHAR(256),
  PRIMARY KEY(id)
);

-- :name create-table-courses
-- :command :execute
CREATE TABLE courses (
  id INT AUTO_INCREMENT,
  gid INT,
  name VARCHAR(256),
  PRIMARY KEY(id)
);

-- :name create-table-holes
-- :command :execute
CREATE TABLE holes (
  num INT,
  cid INT,
  par INT
);

-- :name create-table-games
-- :command :execute
CREATE TABLE games (
  id INT AUTO_INCREMENT,
  cid INT,
  gid INT,
  time LONG,
  PRIMARY KEY(id)
);

-- :name create-table-scores
-- :command :execute
CREATE TABLE scores (
  gid INT,
  pid INT,
  hole INT,
  score INT
);

-- :name create-table-usergame
-- :command :execute
CREATE TABLE user_game (
  pid INT,
  gid INT
);
