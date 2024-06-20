CREATE DATABASE IF NOT EXISTS `wynndb`;
CREATE DATABASE IF NOT EXISTS `wynndb_test`;

CREATE USER IF NOT EXISTS 'fazbot'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `wynndb`.* TO 'fazbot'@'localhost';
GRANT ALL PRIVILEGES ON `wynndb_test`.* TO 'fazbot'@'localhost';
FLUSH PRIVILEGES;
