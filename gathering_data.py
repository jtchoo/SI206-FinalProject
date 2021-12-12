from bs4 import BeautifulSoup
import unittest
import os
import requests as re
import sqlite3
import csv
import json
import matplotlib.pyplot as plt

def join_table(cur,conn):
    cur.execute("SELECT Country.Country, CountryCode.deaths, CountryCode.confirmed, CountryCode.stringency FROM Country JOIN CountryCode WHERE Country.threeDigits = CountryCode.code")
    rows=cur.fetchall()
    return rows
"""
Takes the cursor and the connection to the database as imputs.
Join the two tables and select the data that we need for the later calculations. 
Return a tuple of the data that we need. 
"""

def join_table2(cur,conn):
    cur.execute("SELECT Country.Country, CountryCode.stringency, CountryCode.stringency_legacy FROM Country JOIN CountryCode WHERE Country.threeDigits = CountryCode.code")
    rows=cur.fetchall()
    return rows
"""
Takes the cursor and the connection to the database as inputs.
Join the two tables and select the data that we need for the later calculations. 
Return a tuple of the data that we need.
(The difference between this join and the previous join is - we select different datas.)
"""

def calculation(cur,conn):
    lst=[]
    results= join_table(cur,conn)
    for result in results:
        country = result[0]
        death = result[1]
        confirm = result[2]
        rate = str(round(death/confirm,2))
        lst.append(country + "'s death rate is " + rate)
    return lst
"""
Takes the cursor and the connection to the database as inputs.
Returns a list of the result of our calculations.
"""

def write_data_file(file_name, cur, conn):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    outFile = open(path + file_name, "w")
    outFile.write("The death rate\n")
    outFile.write("=======================================================================\n\n")
    rate = calculation(cur, conn)
    for i in rate:
        outFile.write(str(i) + '\n' + '\n')
    outFile.close()
"""
Takes the file name, the cursor and the connection to the database as inputs.
Write things into the file.
Return nothing.
"""

def country_list(cur,conn):
    lst = []
    results = join_table(cur,conn)
    for i in results:
        country = i[0]
        lst.append(country)
    
    return lst
"""
Takes the cursor and the connection to the database as inputs.
Returns a list of country that we are going to use in later visualizations.
"""

def death_rate_list(cur,conn):
    lst = []
    results = join_table(cur,conn)
    for i in results:
        death = i[1]
        confirm = i[2]
        rate = round(death/confirm,2)
        lst.append(rate)
    
    return lst
"""
Takes the cursor and the connection to the database as inputs.
Returns a list of death rate that we are going to use in later visualizations.
"""

def calculation_stringency(cur,conn):
    legacy = 0
    non_legacy = 0
    others = 0
    lst = []
    results= join_table2(cur,conn)
    for result in results:
        stringency = result[1]
        stringency_legacy = result[2]
        if stringency == None:
            stringency = 0
            others = others + 1
        
        elif stringency_legacy - stringency > 0:
            legacy = legacy + 1
        
        else:
            non_legacy = non_legacy + 1
    lst.append(others)
    lst.append(legacy)
    lst.append(non_legacy)

    return lst
"""
Takes the cursor and the connection to the database as inputs.
Calculate whether the legacy_stringency is larger than the actual_stringency.
Return a list of amounts for both. 
"""


def visualization1(cur, conn):
    fig = plt.figure(figsize=(100,5))
    country = country_list(cur,conn)
    death = death_rate_list(cur,conn)
    stringency = calculation_stringency(cur,conn)
    labels = 'Others', "Stringency_Legacy > Stringency", "Stringency_Legacy < Stringency"
    # colors = ["blue", "red", "green"]
    ax2 = fig.add_subplot(211)
    ax1 = fig.add_subplot(212)

    ax2.set_title("If legacy > stringency, it means that gatherings and moving between cities are not currently the main causes of covid in the country")
    ax2.set_xlabel("Stringency_Legacy > Stringency or Stringency_Legacy < Stringency?")
    ax2.set_ylabel("The amount of country")
    ax2.bar(labels, stringency, color ='maroon', width = 0.4)

    ax1.set_xlabel("Name of the country")
    ax1.set_ylabel("Death rate")
    ax1.bar(country, death, color ='maroon', width = 0.4)
    plt.xticks(rotation=90)

    plt.show()
"""
Takes the cursor and the connection to the database as inputs.
Create both stringency chart and the death rate chart.
Return nothing.
Pop up the two visualizations.
"""


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/covid.db')
    cur = conn.cursor()

    calculation(cur, conn)
    # print(calc)
    write_data_file("country_death_rate.txt", cur, conn)
    # stringency_list = calculate_stringency(cur,conn)
    # print(stringency_list)
    visualization1(cur, conn)
    # visualization2(cur,conn)
    conn.close()
"""
Takes nothing as input and call the functions above
"""




if __name__ == '__main__':
    main()