from flask import Flask, render_template, request # We import render_template so we can render Jinja2 code, and request so we can handle POSTs
# We import sqlite, likely we don't need to install any new library because this is a default Python library
import sqlite3, csv, re, random

# This creates the connection to the database
def db_connection():
    # When we run this code we will this file being created. The file will persist between executations of the server.
    # Keep in mind that you may need to delete this file every time you change the schema of your database.
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

# This initializes our database with a schema, and some initial data
def init_db():
    conn = db_connection()
    empty_or_whitespace = r'^\s*$'
    # We create a table that has two fields: the id of the todo, and a todo_text that is unique
    conn.execute('''CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT NOT NULL, year INTEGER, gross INTEGER)''')

    # This cursor a database bureaucracy: it is a control structure that enables traversal over the records in a database.
    c = conn.cursor()
    with open('imdb_top_1000.csv', 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                title = row[1]
                year = row[2]
                gross = row[15].replace(',', '').replace('"', '')
                if re.match(empty_or_whitespace, title) or re.match(empty_or_whitespace, year) or re.match(empty_or_whitespace, gross):
                    continue
                c.execute('INSERT INTO movies (title, year, gross) VALUES (?, ?, ?)', 
                  (title, year, gross))
    conn.commit()
    conn.close()


# We initialize the database
init_db()

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# We have a new route to /todo
@app.route("/")
def random_movie():
    conn = db_connection()
    c = conn.cursor()

    movieID1 = random.randint(1, 1000)
    movieID2 = random.randint(1, 1000)
    if movieID1 == movieID2:
        movieID2 = random.randint(1, 1000)
    movie1 = c.execute('SELECT * FROM movies WHERE id = ?', (movieID1,)).fetchone()
    movie2 = c.execute('SELECT * FROM movies WHERE id = ?', (movieID2,)).fetchone()
    conn.close()

    return render_template(
        'testhtml.html', 
        movie1_title=movie1['title'],
        movie1_year=movie1['year'],
        movie1_gross=movie1['gross'],
        movie2_title=movie2['title'],
        movie2_year=movie2['year'],
        movie2_gross=movie2['gross'],)