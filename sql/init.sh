#!/bin/bash
/usr/bin/mysqld_safe --skip-grant-tables &
sleep 10
mysql -u root -e "
use db;

create table students(
    StudentID int not null AUTO_INCREMENT,
    FirstName varchar(100) not null,
    LastName varchar(100) not null,
    primary key(StudentID)
);

INSERT INTO students(FirstName,LastName)
VALUES ("Ada","Abel"),("Cane","Chenning");
"
