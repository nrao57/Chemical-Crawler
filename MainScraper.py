from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import pymysql
import datetime

#Connect to the mySQL server
#all data will go into the chemcrawler database and the chemdata table
conn = pymysql.connect(
host='mytestdbinstance.cfhyp6bq5apl.us-east-1.rds.amazonaws.com', 
unix_socket='/tmp/mysql.sock', 
user='mainuser',
passwd="unQ4it12", 
db='mysql', 
charset='utf8')
#start cursor  
cur = conn.cursor()
cur.execute('USE chemcrawler')



def getSubTableNames(bsObj):
    #find subtable names
    subtablenames=[]
    maintable = bsObj.find('table',{'class':'infobox bordered'}) #only finds first table
    for header in maintable.findAll('th'):
        if header.get_text():
            subtablenames.append(header.get_text())
    return subtablenames

def getFieldNames(bsObj):
    #find all field titles from wiki page table
    fieldnames = []
    maintable = bsObj.find('table',{'class':'infobox bordered'}) #only finds first table
    for row in maintable.findAll('tr'):
        for cell in row:
            if type(cell.find('a'))==type(bsObj.h1):
                if 'title' in cell.find('a').attrs:
                    fieldnames.append(cell.find('a').attrs['title'])
    return fieldnames

def getChemicalProperties(bsObj):
    #Gets the field name and values from wiki page table 
    allcells=[]
    for row in bsObj.find('table').tr.next_siblings: #loop through rows of wiki page table
        c1=[] #this will be a list of the row's [field, value]
        for cell in row:
            if cell!='\n':
                if cell.find('a') != None:
                    if 'title' in cell.find('a').attrs:
                        c1.append(forUnicode(cell.find('a').attrs['title']))
                else:
                    c1.append(forUnicode(cell.get_text())) #these are the values that are numbers 
        if len(c1)>1:
            allcells.append(c1)
    return allcells

	
def forUnicode(string):
    #for unicode conversions
    string2 = bytes(string, "UTF-8")
    string3 = string2.decode("UTF-8")
    return string3
	
	
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
	
	#get the name of the chemical we are scraping
    chemicalproperties['name'] = bsObj.find('table',{'class':'infobox bordered'}).caption.get_text()
    chemicalproperties['name'] = forUnicode(chemicalproperties['name'])
    
    properties = getChemicalProperties(bsObj) #returns a nested list [[field1, value1],...]

    for a in properties:
        chemicalproperties[a[0]]=a[1]#right side throws error
    
    return chemicalproperties  #feed into "store" function
	

def store(title, content):
	cur.execute("INSERT INTO chemdata (title, content) VALUES (\"%s\",\"%s\")", (title, content))
	cur.connection.commit()
   

cur.close()
conn.close()
