CREATE database sumers_history;
USE sumers_history;
GRANT ALL on sumers_history to root;
CREATE table sumers_history (
	ID int auto_increment,
	Area enum('Free Weight Area', 'Cardio Area', 'Weight Machine Area', 'Rec Courts', 'Pool', 'South 40 Fitness Center'),
	TS timestamp,
	Open_Closed boolean,
	Count int,
	constraint sumers_history_pk
		primary key (ID)
);