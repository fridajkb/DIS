from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3, csv, random, re

def db_connection():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

def format_gross(gross):
    return f"{gross:,}".replace(",", ".")

movie1_name = ""
movie2_name = ""
movie1_gross = -1
movie2_gross = 0
app = Flask(__name__)

@app.route("/")
def display():
    global movie1_name, movie2_name, movie1_gross, movie2_gross
    conn = db_connection()
    c = conn.cursor()
    result = c.execute('SELECT max(id) FROM movies;').fetchone()
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

    

    return render_template("higherorlower.html",
        movie1_title=movie1["title"],
        movie2_title=movie2["title"],
        result=None, movie1_gross =movie1_gross
    )

@app.route('/check_answer', methods=['POST'])
def check_answer():
    choice = request.form["choice"]        # "higher" or "lower"
    is_correct = ""
    
    if choice == "higher":
        if movie1_gross <= movie2_gross:
            is_correct = "correct"
        else:
            is_correct= "not correct"
    elif choice == "lower":
        if movie1_gross >= movie2_gross:
            is_correct = "correct"
        else:
            is_correct= "not correct"
    

    return render_template("higherorlower.html", movie1_title = movie1_name, movie2_title=movie2_name,
                           result=is_correct, movie1_gross = movie1_gross, movie2_gross=movie2_gross, next_avb = True)

@app.route('/next_pair', methods=['POST'])
def next_pair():
    return display()

if __name__ == "__main__":
    app.run()
