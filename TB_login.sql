DROP DATABASE IF EXISTS TrafficBoss_Login;
CREATE DATABASE IF NOT EXISTS TrafficBoss_Login DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE TrafficBoss_Login;

CREATE TABLE IF NOT EXISTS accounts (
	id int(10) NOT NULL AUTO_INCREMENT,
    username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
	salt varchar(35) NOT NULL,
    email varchar(100) NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
