-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS c2s_dev_db;
CREATE USER IF NOT EXISTS 'c2s_dev'@'localhost' IDENTIFIED BY 'c2s_dev_pwd';
GRANT ALL PRIVILEGES ON `c2s_dev_db`.* TO 'c2s_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'c2s_dev'@'localhost';
FLUSH PRIVILEGES;
