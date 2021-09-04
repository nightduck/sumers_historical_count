/* EDIT ME */
CREATE database dms_db;
USE dms_db;
GRANT ALL on dms_db to root;
CREATE table birthdays (
	ID int auto_increment,
	FirstName varchar(255) null,
	LastName varchar(255) null,
	Birthday date null,
	constraint birthdays_pk
		primary key (ID)
);