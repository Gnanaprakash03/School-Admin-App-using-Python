create database school;
use school;
create table student(registration_number int primary key, full_name varchar(50), gender varchar(10), date_of_birth varchar(20),
age int, address varchar(500), phone_no varchar(50),email varchar(30),standard varchar(30));
select * from student;
alter table student drop column id;
select * from student where registration_number = "10";

create table
 marks(registration_number int primary key,exam_name varchar(30),language varchar(20),english varchar(20),maths varchar(20),science varchar(20),social varchar(20));
select * from marks;