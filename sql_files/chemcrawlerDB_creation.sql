CREATE database chemcrawler;
use chemcrawler;

CREATE TABLE chemdata (
	id BIGINT(7) NOT NULL AUTO_INCREMENT,
	title VARCHAR(200), 
	content TEXT, 
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY(id)
	);