from bs4 import BeautifulSoup
import unittest
import os
import requests as re
import sqlite3
import csv
import json

def join_table(cur,conn):
    """
    SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate
    FROM Orders
    INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;
    """
    cur.execute("SELECT Country.Country, CountryCode.deaths, CountryCode.confirmed, CountryCode.stringency FROM Country JOIN CountryCode WHERE Country.threeDigits = CountryCode.code")
    rows=cur.fetchall()
    return rows

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

def write_data_file(file_name, cur, conn):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    outFile = open(path + file_name, "w")
    outFile.write("The death rate\n")
    outFile.write("=======================================================================\n\n")
    rate = calculation(cur, conn)
    for i in rate:
        outFile.write(str(i) + '\n' + '\n')
    outFile.close()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/covid.db')
    cur = conn.cursor()

    calculation(cur, conn)
    # print(calc)
    write_data_file("country_death_rate.txt", cur, conn)
    conn.close()




if __name__ == '__main__':
    main()