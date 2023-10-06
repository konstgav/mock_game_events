# Генератор фейковых внутриигровых событий для аналитики

sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service

sudo -u postgres psql
CREATE USER student WITH PASSWORD 'student';
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE game_events OWNER admin;

\connect game_events;
CREATE SCHEMA course;
GRANT ALL ON SCHEMA course TO admin;
GRANT ALL ON ALL TABLES IN SCHEMA course TO admin;

GRANT CONNECT ON DATABASE game_events TO student;
GRANT USAGE ON SCHEMA course TO student;
GRANT SELECT ON ALL TABLES IN SCHEMA course TO student;

psql -h localhost -p 5432 -U test -d test_db

CREATE TABLE course.red_robot_game (user_id VARCHAR, event_date TIMESTAMP, event_name VARCHAR, event_param_int INT NULL);
\copy course.red_robot_game from 'events.csv' delimiter ',' CSV HEADER;

psql -h localhost -p 5432 -U student -d course
SELECT * FROM course.red_robot_game LIMIT 20;