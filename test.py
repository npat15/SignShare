# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 00:04:51 2020

@author: nickp
"""


from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # stuff

    # temporary redirect 
    return redirect("/login.html")

# consider adding login_required aspect (http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/)
@app.route('/login', methods=["GET", "POST"])
def login():
    # setup login page
    return render_template("login")


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)