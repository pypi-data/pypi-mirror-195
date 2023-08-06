
--create_tables
DROP TABLE IF EXISTS rta_matches;
DROP TABLE IF EXISTS player_info;
DROP TABLE IF EXISTS unit_info;

CREATE TABLE player_info (
    player_id BIGINT PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    player_country VARCHAR(50) NOT NULL,
    player_rank INTEGER NOT NULL,
    player_score INTEGER NOT NULL
);

CREATE TABLE unit_info (
    unit_id INTEGER PRIMARY KEY,
    unit_name VARCHAR(50) NOT NULL,
    unit_element VARCHAR(50) NOT NULL,
    unit_nat_stars SMALLINT NOT NULL
);

CREATE TABLE rta_matches (
    replay_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    winner SMALLINT NOT NULL,
    player1_id BIGINT REFERENCES player_info(player_id) NOT NULL,
    player2_id BIGINT REFERENCES player_info(player_id) NOT NULL,
    p1_unit1_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p1_unit2_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p1_unit3_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p1_unit4_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p1_unit5_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p1_unit_leader INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p1_unit_banned INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit1_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit2_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit3_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit4_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit5_id INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit_leader INTEGER REFERENCES unit_info(unit_id) NOT NULL,
    p2_unit_banned INTEGER REFERENCES unit_info(unit_id) NOT NULL
);

--drop_table


--insert_row


--delete_row


--insert_file


--return_data



