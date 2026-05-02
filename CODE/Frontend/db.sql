drop database if exists mediplus;
create database mediplus;
use mediplus;


create table users(id INT PRIMARY KEY AUTO_INCREMENT, email VARCHAR(50), password VARCHAR(50));