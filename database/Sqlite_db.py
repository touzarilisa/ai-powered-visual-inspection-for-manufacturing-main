"""
This program aims to create a class to manage Sqlite database to insert , and select data of the cards.
"""

# Importing libraries
import sqlite3
from sqlite3 import Error
import os
import sys
import argparse
import numpy as np
import pandas as pd
from datetime import datetime

# Implement a class to manage Sqlite database
class Sqlite_db:
    """
    This class is used to manage Sqlite database.
    """

    def __init__(self, db_path):
        """
        Initialize the Sqlite_db class.

        :param db_path: The path to the database.
        """
        self.db_path = db_path
        self.conn = self.create_connection(self.db_path)

    def create_connection(self, db_file):
        """
        Create a database connection to the SQLite database specified by db_file.

        :param db_file: The database path.
        :return: Connection to the database.
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def create_cards_table(self):
        """
        Create a table for cards.
        """
        sql = ''' CREATE TABLE IF NOT EXISTS cards (
                    name text PRIMARY KEY,
                    date text NOT NULL,
                    die text NOT NULL,
                    iml text NOT NULL,
                    label text NOT NULL,
                    confidence real NOT NULL,
                    x int NOT NULL,
                    y real NOT NULL,
                    width real NOT NULL,
                    height real NOT NULL,
                    today_date text NOT NULL
                ) '''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        cur.close()

    def insert_card(self, name, label, confidence, x, y, width, height):
        """
        Create a new card into the cards table.

        :param name: The name of the card.
        :param label: The label of the card.
        :param confidence: The confidence of the classification
        :param x: The x coordinate of the bounding box.
        :param y: The y coordinate of the bounding box.
        :param width: The width of the bounding box.
        :param height: The height of the bounding box.
        :return:
        """
        today_date =  datetime.today().strftime('%Y-%m-%d-%Hh%Mm')
        die = name.split('_')[3]
        date = name.split('_')[1]
        iml = name.split('_')[4]
        sql = ''' INSERT INTO cards(name, date, die, iml, label,confidence, x, y, width, height, today_date)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (name, date, die, iml, label, confidence, x, y, width, height, today_date))
        self.conn.commit()
        cur.close()


    def select_card(self, name):
        """
        Query all the cards in the cards table.

        :return: A list of cards.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cards WHERE name = ?", (name,))
        rows = cur.fetchall()
        cur.close()
        return rows
    
    def select_all_cards(self):
        """
        Query all the cards in the cards table.

        :return: A list of cards.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cards")
        rows = cur.fetchall()
        cur.close()
        return rows
    
    
if __name__ == '__main__':
    # Create a database
    db = Sqlite_db('../database/database.db')
    db.create_cards_table()
    # Insert a card
    db.insert_card('card_2019-11-05-17h00m_1_1_1_1_1', '1', 0.9, 0, 0, 0, 0)
    # Select a card
    print(db.select_card('card_2019-11-05-17h00m_1_1_1_1_1'))
    # Select all cards
    print(db.select_all_cards())

    

    
    

    
    

        

        

  

 