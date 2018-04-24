-- CREATE database chemcrawler;
use chemcrawler;

drop table chemdata;

CREATE TABLE chemdata (
	id BIGINT(7) NOT NULL AUTO_INCREMENT,
	molname VARCHAR(200), 
	molarmass VARCHAR(200), 
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY(id)
	);
    
-- SELECT * FROM chemdata;