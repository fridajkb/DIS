from flask import Flask, request, jsonify, render_template
import sqlite3


app = Flask(__name__)
@app.route('/')

def hello():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run()

