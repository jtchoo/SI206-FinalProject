from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json
import os


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
""" 
Set up the database and the input should be the name of your choice.
Returns the cursor and the connection to the database.
"""

def get_country():
    country = {}

    r = requests.get("https://www.iban.com/country-codes")
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find('table')
    countries = result.find_all('tr')
    for i in range(1, len(countries)):
        for data in countries[i].find('td'):
            # print(data.text)
            # print(countries[i].select("td")[1])
            country[str(data)] = countries[i].select("td")[2].text

    return country
""" 
No inputs. Request the website url that we are going to scrape from.
Return a dictionary that has the country full name as the key and Alpha-3 code as the value. 
"""


def setUpCountryTable(data, cur, conn):

    data_key = list(data.keys())
    # print(data_key)
    # print(data)

    cur.execute("DROP TABLE IF EXISTS COUNTRY")
    cur.execute("CREATE TABLE Country (Country TEXT PRIMARY KEY, threeDigits TEXT)")
    for i in data_key:
        cur.execute("INSERT INTO Country (Country, threeDigits) VALUES (?,?)",(i,data[i]))
    conn.commit()
"""
Takes the dictionary that we got from get_country(), the cursor, and the connection of the database as inputs.
Will create the "Country" table.
Insert countries' full name and their Alpha-3 code into the table. 
Returns nothing. 
"""



def main():
    cur, conn = setUpDatabase('covid.db')
    list = get_country()
    setUpCountryTable(list, cur, conn)
"""
Takes nothing as input and call the functions above
"""



if __name__ == '__main__':
    main()