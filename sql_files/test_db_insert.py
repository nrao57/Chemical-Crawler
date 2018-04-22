#Testing an insert into the local database "scraping"
#this is testing python and mySQL integration

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re

conn = pymysql.connect(
host='mytestdbinstance.cfhyp6bq5apl.us-east-1.rds.amazonaws.com', 
unix_socket='/tmp/mysql.sock', 
user='mainuser',
passwd="unQ4it12", 
db='mysql', 
charset='utf8')

#DESKTOP-MRDG44P
						
cur = conn.cursor()
cur.execute('USE scraping')

random.seed(datetime.datetime.now())

def store(title, content):
	cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\",\"%s\")", (title, content))
	cur.connection.commit()
	
def getLinks(articleUrl):
	html = urlopen("http://en.wikipedia.org"+articleUrl)
	bsObj = BeautifulSoup(html)
	title = bsObj.find("h1").get_text()
	content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
	store(title, content)
	return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")

try:
	while len(links) > 0:
		newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
		print(newArticle)
		links = getLinks(newArticle)

finally:
	cur.close()
	conn.close()