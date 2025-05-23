from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3


app = Flask(__name__)
@app.route('/')
def display(movie1_title="Movie 00", movie2_title="Movie 2"):

    return render_template('testhtml.html', movie1_title="Movie 00", movie2_title="Movie 2", result=False)

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


@app.route("/next")
def next_pair():
    return redirect(url_for("display"))


if __name__ == "__main__":
    app.run()

