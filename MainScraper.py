from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import pymysql
import datetime

conn = pymysql.connect(
host='mytestdbinstance.cfhyp6bq5apl.us-east-1.rds.amazonaws.com', 
unix_socket='/tmp/mysql.sock', 
user='mainuser',
passwd="unQ4it12", 
db='mysql', 
charset='utf8')

cur = conn.cursor()
cur.execute('USE chemcrawler')#make chemcrawler database 

#make chemdata table


def getSubTableNames(bsObj):
    #find subtable names
    subtablenames=[]
    maintable = bsObj.find('table',{'class':'infobox bordered'}) #only finds first table
    for header in maintable.findAll('th'):
        if header.get_text():
            subtablenames.append(header.get_text())
    return subtablenames

def getFieldNames(bsObj):
    #find all field titles
    fieldnames = []
    maintable = bsObj.find('table',{'class':'infobox bordered'}) #only finds first table
    for row in maintable.findAll('tr'):
        for cell in row:
            if type(cell.find('a'))==type(bsObj.h1):
                if 'title' in cell.find('a').attrs:
                    fieldnames.append(cell.find('a').attrs['title'])
    return fieldnames

def getChemicalProperties(bsObj):
    allcells=[]
    for row in bsObj.find('table').tr.next_siblings:
        c1=[]
        for cell in row:
            if cell!='\n':
                if cell.find('a') != None:
                    if 'title' in cell.find('a').attrs:
                        c1.append(cell.find('a').attrs['title'])
                else:
                    c1.append(cell.get_text())
        if len(c1)>1:
            allcells.append(c1)
    return allcells

def ChemCrawler(pageUrl):

    #Create Dictionary to hold info
    chemicalproperties = {}

    try:
        html = urlopen(pageUrl)
        bsObj = BeautifulSoup(html, "html.parser")
        print("Opened Page: {}".format(pageUrl))

    except ValueError as e:
        print("Could not open: {}".format(pageUrl))
        return
    except URLError as e:
        print(e)
        return

    chemicalproperties['name'] = bsObj.find('table',{'class':'infobox bordered'}).caption.get_text()

    properties = getChemicalProperties(bsObj)
    for a in properties:
        chemicalproperties[a[0]]=a[1]
    
    return chemicalproperties  #feed into "store" function
	

def store(title, content):
	cur.execute("INSERT INTO chemdata (title, content) VALUES (\"%s\",\"%s\")", (title, content))
	cur.connection.commit()
   
   
 finally:
	cur.close()
	conn.close()
