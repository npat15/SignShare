import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_mail import Mail, Message

# Configure application
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'signsharehelp@gmail.com',
	MAIL_PASSWORD = 'signshare123'
	)
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# TODO - change all cs50 stuff to sqlite3 import stuff
conn = sqlite3.connect(r"C:\Users\nickp\Downloads\signs.db")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/make", methods=["GET", "POST"])
def make():
    if request.method == "GET":
        return render_template("make.html")
    else:
        email = request.form.get("email")
        desc = request.form.get("message")
        loc = request.form.get("location")
        phone = request.form.get("phone")

        if email == "" or desc == "" or loc == "" or phone == "":
            return render_template("make_error.html")
        
        msg = Message("SignShare Important Info", sender="signsharehelp@gmail.com",recipients=[email])
        
        # some basic message with confirmation here
        msg.body = "Hi! Thank you for registering your sign! Once we find your sharer, we'll update you. Thanks!"
        mail.send(msg)

        conn = sqlite3.connect(r"C:\Users\nickp\Downloads\signs.db")
        db = conn.cursor()
        db.execute("INSERT INTO makers (email, descrip, location, phone) VALUES (?,?,?,?)", (email, desc, loc, phone,))
        conn.commit()
        
        return redirect("/confirmation")

@app.route("/receive", methods=["GET", "POST"])
def receive():
    if request.method == "GET":
        return render_template("receive.html")
    else:
        email = request.form.get("email")
        phone = request.form.get("phone")
        person = request.form.get("person_req")

        if email == "" or phone == "":
            return render_template("make_error.html")

        conn = sqlite3.connect(r"C:\Users\nickp\Downloads\signs.db")
        db = conn.cursor()
        
        # select list of people who's signs haven't been taken
        makers = db.execute("SELECT * FROM makers WHERE taken = 0")

        # quick check to see if requested person is in system
        # TODO - fix matchup error - has to do with maker[0] -- correct index?
        flag = 0
        for maker in makers:
            print(maker)
            if person == maker[0]:
                flag = 1

        if flag == 0:
            return render_template("take_error.html")

        db.execute("INSERT INTO takers (email, phone, person_req) VALUES (?,?,?)", (email, phone, person,))
        conn.commit()           
        
        # TODO - edit makers to have taken marked and send email

        return redirect("/confirmation")

@app.route("/confirmation")
def confirm():
    return render_template("confirm.html")

# run on localhost
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)