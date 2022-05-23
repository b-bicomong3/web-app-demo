#main.py

'''
Title: Flask contacts web app
Author: Beatrix Bicomong
Data: May 16, 2022
'''
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect

# --- GLOBAL VARIABLES --- #

DB_NAME = "flask.db"
FIRST_RUN = True
if (Path.cwd() / DB_NAME).exists():
    FIRST_RUN = False

# --- FLASK --- #
app = Flask(__name__)

### WEBPAGES
@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage of the website
    """
    ALERT=""
    if request.form:
        FIRST_NAME = request.form.get("first_name")
        LAST_NAME = request.form.get("last_name")
        EMAIL = request.form.get("email")
        if getOneContact(EMAIL) is None:
            createContacts(FIRST_NAME, LAST_NAME, EMAIL)
            ALERT = f"Successfully added a {FIRST_NAME} {LAST_NAME} to contacts! You did it :D"
        else:
            ALERT = f"{EMAIL} already used for another contact! Try again!"
            print("Email already exists")

    QUERY_CONTACTS = getAllContacts()

    return render_template("index.html", alert=ALERT, contacts=QUERY_CONTACTS)
    # alert is our html variable, ALERT is our python variable
@app.route('/help')
def help():
    """help page
    """
    return "<h1> HELP ME <h1>"

@app.route('/delete/<id>')
def deleteContactPage(id):
    deleteContact(id)
    return redirect('/')


# --- DATA BASE --- #

### --- INPUTS --- ###
def createContacts(F_NAME, L_NAME, EMAIL):
    """Creates a contact to add to the database

    Args:
        F_NAME (str): User's first name
        L_NAME (str): User's last name
        EMAIL (str): User's email
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
            INSERT INTO
                contacts
            VALUES(
                ?, ?, ?
            )
    ;''', [F_NAME, L_NAME, EMAIL])

    CONNECTION.commit()
    CONNECTION.close()

### --- PROCESSINGS --- ###
def createTable():
    """Creates the database table on first run
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
            CREATE TABLE
                contacts(
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    email TEXT PRIMARY KEY NOT NULL
                )
    ;''')

    CONNECTION.commit()
    CONNECTION.close()

def deleteContact(EMAIL):
    """Deletes a contact

    Args:
        EMAIL (str): primary key
    """
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
        DELETE FROM
            contacts
        WHERE
            email = ?
    ;''',[EMAIL])
    CONNECTION.commit()
    CONNECTION.close()

### --- OUTPUTS --- ###
def getOneContact(EMAIL):
    """Query and return a single contact from the database

    Args:
        EMAIL (str): 
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CONTACT = CURSOR.execute('''
            SELECT
                *
            FROM
                contacts
            WHERE
                email = ?
    ;''', [EMAIL]).fetchone()
    CONNECTION.close()
    return CONTACT

def getAllContacts():
    """Returns every row in the contacts database

    Returns:
        CONTACT (list):
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CONTACTS = CURSOR.execute('''
            SELECT
                *
            FROM
                contacts
            ORDER BY
                first_name
    ;''').fetchall()
    CONNECTION.close()
    return CONTACTS

if __name__ == "__main__":
    if FIRST_RUN:
        createTable()
    app.run(debug=True)