create database if not exists tournament;

use tournament;

create table if not exists participants (
    ID int not nULL,
    FirstName varchar(255) not Null,
    LastName varchar(255) not NULL,
    Age int,
    PRIMARY KEY(ID)
);

insert into participants (ID,FirstName,LastName,Age)
values (1,Tobias, Durchholz, 33),
(2,Max,Mustermann,30),
(3,Moana, Musterfrau,21);