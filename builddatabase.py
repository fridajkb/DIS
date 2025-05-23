from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3, csv, random, re
# This creates the connection to the database
def db_connection():
    # When we run this code we will this file being created. The file will persist between executations of the server.
    # Keep in mind that you may need to delete this file every time you change the schema of your database.
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

# This initializes our database with a schema, and some initial data
def init_db():
    is_digit = r'[0-9]+'
    conn = db_connection()
    # We create a table that has two fields: the id of the todo, and a todo_text that is unique
    conn.execute('''CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT NOT NULL, year INTEGER, gross INTEGER)''')

    c = conn.cursor()
    with open('imdb_top_1000.csv', 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                title = row[1]
                year = row[2]
                gross = row[15].replace(',', '').replace('"', '')
                if (re.match(is_digit, year) and re.match(is_digit, gross)) and (year != None and gross != None and title !=  None):
                    print(title, gross)
                    print(re.match(is_digit, gross))
                    c.execute('INSERT INTO movies (title, year, gross) VALUES (?, ?, ?)', 
                    (title, year, gross))
                else:
                    print("ERROR")
                    continue
    conn.commit()
    c.execute('SELECT max(id) from movies')
    conn.close()
    
init_db()