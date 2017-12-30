from flask import abort, Flask, redirect, render_template, request, url_for, session
from Crypto.Random import random
from datetime import datetime

import bcrypt
import mysql.connector
import os
import sys

from MySQLDriver import MySQLDriver
from config import flask_conf

sql = MySQLDriver()
app = Flask(__name__)
app.root_path = os.path.dirname(os.path.abspath(__file__))


def create_tables():
    print("creating tables")
    query = "SHOW TABLES LIKE '{}';"
    tables = ["Users", "Post"]

    # loop through table names
    try:
        sql.query("CREATE TABLE Users("
                  "  `UUID` VARCHAR(12) NOT NULL,"
                  "  `Username` varchar(20) NOT NULL,"
                  "  `EmailAddress` varchar(40) NOT NULL,"
                  "  `Password` varchar(64) NOT NULL,"
                  "  `Salt` varchar(64) NOT NULL,"
                  "  PRIMARY KEY (`UUID`)"
                  ") ENGINE=InnoDB;")
        print("created table: Users")
    except mysql.connector.errors.ProgrammingError as err:
        print(err)
    try:
        sql.query("CREATE TABLE Post("
                  "  `PostID` varchar(20) NOT NULL,"
                  "  `Post` varchar(20) NOT NULL,"
                  "  `PostDate` varchar(20) NOT NULL,"
                  "  `UUID` VARCHAR(12) NOT NULL,"
                  "  PRIMARY KEY (`PostID`),"
                  "  FOREIGN KEY (UUID) REFERENCES `Users`(`UUID`)"
                  ") ENGINE=InnoDB;")
        print("created table: Post")
    except mysql.connector.errors.ProgrammingError as err:
        print(err)


def validate_login(username: str, password: str) -> bool:
    if sql.exists(username, "Users", "Username"):

        sql.query("SELECT Password, Salt FROM Users WHERE Username = '{}'".format(username))
        hashed_password = None
        # print(sql.cursor)
        for (hashed_pw, salt) in sql.cursor:
            pw_check = bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8'))
            if (pw_check):
                return True
    return False


def validate_signup(email: str, username: str, password: str) -> bool:
    if sql.exists(username, "Users", "Username") or sql.exists(email, "Users", "EmailAddress"):
        return False
    return True


def create_user(username: str, password: str, email: str):
    uuid = 0
    unique = False
    while not unique:
        uuid_str = ""
        for i in range(12):
            uuid_str += str(random.randint(0,9))
        unique = not sql.exists(int(uuid_str), "Users", "UUID")
        if unique:
            uuid = int(uuid_str)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print(len(hashed_password), " ", len(salt))
    sql.insert("INSERT INTO Users(UUID, Username, EmailAddress, Password, Salt) VALUES (%s, %s, %s, %s, %s)", (uuid, username, email, hashed_password, salt))


# default route (index)
@app.route('/')
# dynamic route
@app.route('/<page>')
def route(page="index"):
    logged_in = False
    if 'username' in session:
        logged_in = True
    try:
        if logged_in:
            return render_template(page + ".html", title=page, user=logged_in, username=session['username']) # render the selected page
        else:
            return render_template(page + ".html", title=page, user=logged_in)
    except:
        if logged_in:
            return render_template("index.html", title="index", user=logged_in, username=session['username'])
        else:
            return render_template("index.html", title="index", user=logged_in)


# log in route - log in page and post to log in to system
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("user")
        password = data.get("password")
        valid = validate_login(username, password)
        if valid:
            session['username'] = username
            return redirect('/index')
        else:
            return render_template('login.html', title='login', invalid=True)
    elif request.method == "GET":
        return render_template('login.html', title='login')


# register  route - POST data from register form
@app.route("/signup", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        username = data.get("user")
        password = data.get("password")
        confirm_password = data.get("password_confirm")
        if password != confirm_password:
            return render_template('login.html', title='login', no_match=True)
        valid = validate_signup(email, username, password)
        if valid:
            create_user(username, password, email)
            return redirect('/index')
        else:
            return render_template('login.html', title='login', invalid_signup=True)


# main program
if __name__ == '__main__':
    # open sql connection
    sql.open()
    # create database tables
    create_tables()

    # start flask web server
    app.secret_key = bcrypt.gensalt().decode()
    app.run(**flask_conf)
    sql.close()
