-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS c2s_test_db;
CREATE USER IF NOT EXISTS 'c2s_test'@'localhost' IDENTIFIED BY 'c2s_test_pwd';
GRANT ALL PRIVILEGES ON `c2s_test_db`.* TO 'c2s_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'c2s_test'@'localhost';
FLUSH PRIVILEGES;
