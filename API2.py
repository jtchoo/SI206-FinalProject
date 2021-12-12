from bs4 import BeautifulSoup
import unittest
import os
import requests as re
import sqlite3
import csv
import json

def create_country_table(cur, conn):
    base_url = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/2021-11-02/2021-11-03"
    r = re.get(base_url)
    data = r.text
    dict = json.loads(data) 

    # cur.execute('DROP TABLE IF EXISTS CountryCode')
    cur.execute('CREATE TABLE IF NOT EXISTS CountryCode ("code" TEXT, "confirmed" INTEGER, "deaths" INTEGER, "stringency" FLOAT, "stringency_legacy" FLOAT, "date" TEXT, UNIQUE("code", "date"))')
    # , UNIQUE("code", "date"))
    conn.commit()

    count = 0
    day_dict = dict['data']
    for dated in day_dict:
        country_dict=day_dict[dated]
        for country in country_dict:
            country_data = country_dict[country]
            code = country
            deaths = country_data['deaths']
            confirmed_num = country_data['confirmed']
            stringency = country_data['stringency']
            stringency_legacy = country_data['stringency_legacy']

            cur.execute('INSERT OR IGNORE INTO CountryCode (code, confirmed, deaths, stringency, stringency_legacy, date) VALUES (?,?,?,?,?,?)', (code, confirmed_num, deaths, stringency, stringency_legacy, dated))
            if cur.rowcount == 1:
                count = count + 1
                if count == 26:
                    exit()
    
    
            conn.commit()
"""
Takes the cursor and the connection to the database as inputs.
Loads the API data into the json file.
Create the "CountryCode" table
Insert the data into the table.
Returns nothing. 
"""
    

def setUpDatabase(covid_cond):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+"/"+covid_cond)
    cur = conn.cursor()
    return cur,conn
""" 
Set up the database and the input should be the name of your choice.
Returns the cursor and the connection to the database.
"""


def main():
    cur,conn= setUpDatabase('covid.db')
    data = create_country_table(cur,conn)
"""
Takes nothing as input and call the functions above
"""




if __name__ == '__main__':
    main()