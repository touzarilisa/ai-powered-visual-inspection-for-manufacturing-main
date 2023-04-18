from fileinput import filename
import sqlite3
from sqlite3 import Error
import csv
import os
from datetime import datetime


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def insert_card(Name,DIE,classification_result,Confidence,Bounding_box):
    todays_date =  datetime.today().strftime('%Y-%m-%d-%Hh%Mm') #datetime(2021, 11, 1).strftime('%Y-%m-%d-%Hh%Mm')
    path = os.getcwd()
    path = path.replace(os.sep, '/')
    path = path + '/test.db'
    con = create_connection(path)
    cur = con.cursor()
    cur.execute("create table if not exists Carte (Name,DIE,Decision,Confidence,Bounding_box,Date)")
    cur.execute("insert into Carte values (?,?,?,?,?,?)", (Name,DIE,classification_result,Confidence,Bounding_box,todays_date))
    con.commit()
    con.close()

def generate_report(case=0, DIE=1, decision = "Defected",date ="2022"):
    # 0: generique  1: Par DIE  2: Par Class  3: Par Date
    path = os.getcwd()
    path = path.replace(os.sep, '/')
    path = path + '/test.db'
    con = create_connection(path)
    cur = con.cursor()
    if case == 0 :
        cur.execute("select * from carte order by Date DESC")
    elif case == 1 :
        cur.execute(f"select * from carte where DIE = {DIE} order by Date DESC")
    elif case == 2 :
        cur.execute(f"select * from carte where Decision LIKE '{decision}' order by Date DESC")
    elif case == 3 :
        cur.execute(f"select * from carte where Date LIKE '{date}%' order by Date DESC")
    results = cur.fetchall()
    con.close()
    return results


def save_report(case=0, DIE=1, decision = "Defected", date = "2022"):
    # 0: generique  1: Par DIE  2: Par Class  3: Par Date    
    res = generate_report(case, DIE, decision,date)
    filename = "report"+"_"+datetime.today().strftime('%Y-%m-%d')+".csv"
    fp = open(filename, "w", newline='')
    myFile = csv.writer(fp, delimiter = ',')
    myFile.writerow(['Card_Name','DIE','Decision','Confidence','Bounding_box','Date'])
    myFile.writerows(res)
    fp.close()

if __name__ == '__main__':
    
    insert_card("AE00005_124507_00_1_2_2001.jpg",1,"Not Defected",99,"0,100,21,57")
    insert_card("test_card_2",1,"Defected",97,"0,0,0,0")
    """
    insert_card("test_card_4",4,"NOT Defected",97,"0,0,0,0")
    insert_card("test_card_5",4,"NOT Defected",97,"0,0,0,0")
    insert_card("test_card_69",1,"Defected",97,"0,0,0,0")
    """
    # r = generate_report_date("2022-02-01")
    # print(r)
    # insert_card("test_card_7",4,"Defected",90,"0,0,0,10")
    # save_report(2,0)
    # r = generate_report()
    # print(r)
    save_report()