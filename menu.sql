CREATE Table restaurant
(


)

create table players(
	player_id int not null default nextval('player_id_seq') primary key ,
	name varchar(60) not null
);