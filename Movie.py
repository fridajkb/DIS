from flask import Flask, render_template, request # We import render_template so we can render Jinja2 code, and request so we can handle POSTs
# We import sqlite, likely we don't need to install any new library because this is a default Python library
import sqlite3, csv, re

empty_or_whitespace = r'^\s*$'
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
    c.execute('SELECT * from movies')

    for row in c.fetchall():
        print(row['gross'])
    conn.close()

# We initialize the database
init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# We have a new route to /todo
@app.route('/todo', methods=['GET', 'POST'])
def list_todo():
    conn = db_connection()
    # This route has two functions: GET and POST.
    # If there is a POST, we do the insert in the database
    if request.method == 'POST':
        new_todo = request.form['new_todo']
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO todos (todo_text) VALUES (?)', (new_todo,))
        conn.commit()

    # But we always get all entries from the database
    db_todos = conn.execute('SELECT todo_text FROM todos').fetchall()
    conn.close()
    todos = []
    # The entries come in dictionary data structure, we need to convert it to a list
    for db_todo in db_todos:
        todos.append(db_todo['todo_text'])

    # We render the todo template with todos we fetched from the database
    return render_template('todo.html', todos=todos)