# Генератор фейковых внутриигровых событий для аналитики

1. Установка PostgeSQL
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service

2. Создание БД
sudo -u postgres psql
CREATE USER student WITH PASSWORD 'student';
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE game_events OWNER admin;

3. Выделение прав на объекты БД для преподавателя и студента
\connect game_events;
CREATE SCHEMA course;
GRANT ALL ON SCHEMA course TO admin;
GRANT ALL ON ALL TABLES IN SCHEMA course TO admin;

GRANT CONNECT ON DATABASE game_events TO student;
GRANT USAGE ON SCHEMA course TO student;
GRANT SELECT ON ALL TABLES IN SCHEMA course TO student;

psql -h localhost -p 5432 -U test -d test_db

4. Создание таблицы, загрузка данных из csv
CREATE TABLE course.red_robot_game (user_id VARCHAR, event_date TIMESTAMP, event_name VARCHAR, country VARCHAR, event_param_int INT NULL);
\copy course.red_robot_game from 'events.csv' delimiter ',' CSV HEADER;

5. Тестовое подключение
psql -h localhost -p 5432 -U student -d course
SELECT * FROM course.red_robot_game LIMIT 20;

6. Очистка таблица, загрузка новых данных
psql -h localhost -p 5432 -U admin -d game_events
drop table course.red_robot_game;
truncate course.red_robot_game;
\copy course.red_robot_game from 'events.csv' delimiter ',' CSV HEADER;