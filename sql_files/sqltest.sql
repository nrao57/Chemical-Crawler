
-- this mysql script shows how to create a simple table and switch to it
-- to run, type "source C:\Users\Nikhil Home Media\Downloads\WebCrawling\Chemical-Crawler\sql_files\sqltest.sql"

SHOW databases;
USE scraping;

CREATE TABLE pages (
	id BIGINT(7) NOT NULL AUTO_INCREMENT,
	title VARCHAR(200), 
	content TEXT, 
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY(id)
	);
	
DESCRIBE pages;