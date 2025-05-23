from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3, csv, random, re

def db_connection():
    # When we run this code we will this file being created. The file will persist between executations of the server.
    # Keep in mind that you may need to delete this file every time you change the schema of your database.
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

movie1_name = ""
movie2_name = ""
movie1_gross = -1
movie2_gross = 0
app = Flask(__name__)

# We have a new route to /todo
@app.route("/")
def display():
    global movie1_name, movie2_name, movie1_gross, movie2_gross
    conn = db_connection()
    c = conn.cursor()
    c.execute('SELECT max(id) FROM movies;')
    result = c.fetchone()
    maxid = result[0]
    movieID1 = random.randint(1, maxid)
    movieID2 = random.randint(1, maxid)
    if movieID1 == movieID2:
        movieID2 = random.randint(1, maxid)
    movie1 = c.execute('SELECT * FROM movies WHERE id = ?', (movieID1,)).fetchone()
    movie2 = c.execute('SELECT * FROM movies WHERE id = ?', (movieID2,)).fetchone()
    conn.close()

    try:
        movie1_name = movie1["title"]
        movie2_name = movie2["title"]
        movie1_gross = movie1["gross"]
        movie2_gross = movie2["gross"]
    except:
        print(movie1_name, movie2_name)


    return render_template("testhtml.html",
        movie1_title=movie1["title"],
        movie2_title=movie2["title"],
        result=None
    )

@app.route('/check_answer', methods=['POST'])
def check_answer():
    choice = request.form["choice"]        # "higher" or "lower"
    is_correct = False

    print(choice)

    print(movie1_gross, movie2_gross)
    
    if choice == "higher":
        if movie1_gross <= movie2_gross:
            is_correct = True
        else:
            is_correct= False
    elif choice == "lower":
        if movie1_gross >= movie2_gross:
            is_correct = True
        else:
            is_correct= False
    

    return render_template("testhtml.html", movie1_title = movie1_name, movie2_title=movie2_name,
                           result=is_correct)

if __name__ == "__main__":
    app.run()
