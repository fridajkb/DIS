from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3, csv, random, re

app = Flask(__name__)

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

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# We have a new route to /todo
@app.route("/")
def display():
    conn = db_connection()
    c = conn.cursor()

    movieID1 = random.randint(1, 1000)
    movieID2 = random.randint(1, 1000)
    if movieID1 == movieID2:
        movieID2 = random.randint(1, 1000)
    movie1 = c.execute('SELECT * FROM movies WHERE id = ?', (movieID1,)).fetchone()
    movie2 = c.execute('SELECT * FROM movies WHERE id = ?', (movieID2,)).fetchone()
    conn.close()

    return render_template("testhtml.html",
        movie1_title=movie1["title"],
        movie2_title=movie2["title"],
        result=None
    )

# @app.route('/')
# def display(movie1_title="Movie 00", movie2_title="Movie 2"):

#     return render_template('testhtml.html', movie1_title="Movie 00", movie2_title="Movie 2", result=False)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    m1 = request.form["movie1_title"]
    m2 = request.form["movie2_title"]
    choice = request.form["choice"]        # "higher" or "lower"
    is_correct = True
    # SQL to get the gross of the movies

    return render_template("testhtml.html",
                           movie1_title="movie1_title",
                           movie2_title="movie2_title",
                           result=is_correct)

if __name__ == "__main__":
    app.run()

