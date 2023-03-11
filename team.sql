CREATE TABLE {table_name} (
	player_name varchar(255) NOT NULL,
    year_drafted int NOT NULL,
    position varchar(2),
    PRIMARY KEY (player_name, year_drafted)
)