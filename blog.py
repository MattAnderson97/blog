from flask import abort, Flask, redirect, render_template, request, url_for
import mysql.connector
import json

from MySQLDriver import MySQLDriver
from config import flask_conf


sql = MySQLDriver()
app = Flask(__name__)


def create_tables():
    print("creating tables")
    query = "SHOW TABLES LIKE '{}';"
    tables = ["Users", "Post"]

    # loop through table names
    for table in tables:
        try:
            sql.query("CREATE TABLE `" + table + "`("
                                                 "  `UUID` int(12) NOT NULL,"
                                                 "  `Username` varchar(20) NOT NULL,"
                                                 "  `EmailAddress` varchar(40) NOT NULL,"
                                                 "  `Password` varchar(20) NOT NULL,"
                                                 "  `Salt` varchar(64) NOT NULL,"
                                                 "  PRIMARY KEY (`UUID`)"
                                                 ") ENGINE=InnoDB;")
            print("created table: " + table)

        except mysql.connector.errors.ProgrammingError as err:
            print(err)


def validate(username: str, password: str) -> bool:
    return False


# default route (index)
@app.route('/')
# dynamic route
@app.route('/<page>')
def route(page="index"):
    print(page)
    return render_template(page + ".html", title=page) # render the selected page


# log in route - log in page and post to log in to system
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("user")
        password = data.get("password")
        print(username, password)
        valid = validate(username, password)
        if valid:
            return redirect('/index')
        else:
            return render_template('login.html', title='login', invalid=True)
    elif request.method == "GET":
        return render_template('login.html', title='login')


# main program
if __name__ == '__main__':
    # open sql connection
    sql.open()
    # create database tables
    create_tables()

    # start flask web server
    app.run(**flask_conf)
    sql.close()
