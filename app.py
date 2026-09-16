# Import the necessary modules from Flask and sqlite3
from flask import Flask, render_template, request, redirect
import sqlite3

# Create the Flask app
app = Flask(__name__)

# Name of the database file (don't change this unless you also update it below)
DB_NAME = 'scores.db'

# This function sets up the database if it doesn't already exist
def init_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    with sqlite3.connect(DB_NAME) as conn:
        # Create the 'scores' table with three columns:
        # - id: an auto-incrementing number (primary key)
        # - first_name: the player's firstname
        # - last_name: the player's lastname
        # - score: the player's score
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')

# This specifies that the following function will run whenever there's any actions taken on the web page
@app.route('/leaderboard', methods=['GET', 'POST'])

# This function handles both displaying the leaderboard and submitting scores
def leaderboard():
    # If someone has submitted the form (POST request), save their data
    if request.method == 'POST':
        # Get the name and score that the player entered in the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        score = request.form['score']

        try:
            score = int(score)
            if score >= 0:
                with sqlite3.connect(DB_NAME) as conn:
                    # Save them cleanly as two separate fields
                    conn.execute('INSERT INTO scores (first_name, last_name, score) VALUES (?, ?, ?)', (first_name, last_name, score))
        except ValueError:
            pass
        
        # Redirect the user back to the main page after submitting
        return redirect('/leaderboard')

    # Defaults sorting selection to quickest time
    sort_by = request.args.get('sort_by', 'quickest')
    
    # Sorting options
    if sort_by == 'slowest':
        query = 'SELECT first_name, last_name, score FROM scores ORDER BY score DESC'
    elif sort_by == 'fn_az':
        query = 'SELECT first_name, last_name, score FROM scores ORDER BY first_name COLLATE NOCASE ASC'
    elif sort_by == 'fn_za':
        query = 'SELECT first_name, last_name, score FROM scores ORDER BY first_name COLLATE NOCASE DESC'
    elif sort_by == 'ln_az':
        query = 'SELECT first_name, last_name, score FROM scores ORDER BY last_name COLLATE NOCASE ASC'
    elif sort_by == 'ln_za':
        query = 'SELECT first_name, last_name, score FROM scores ORDER BY last_name COLLATE NOCASE DESC'
    else:  
        query = 'SELECT first_name, last_name, score FROM scores ORDER BY score COLLATE NOCASE ASC'

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(query)
        entries = cur.fetchall()
    
    return render_template('index.html', entries=entries, current_sort=sort_by)

# Allow the main game page to be access to and from the leaderboard page
@app.route('/cybermatch', methods=['GET', 'POST'])
def index ():
    return render_template('Muhammad-Main.html')

#----- Mainline program: This code executes when we run this file.-----

init_db()  # Set up the database before starting the web app

# Start the Flask server for local testing (Comment the version not being used)
app.run(debug=True)  
# Use this version when testing on your computer only

#app.run(debug=True, host='0.0.0.0') 
# Use this version if you want to test it on a phone/tablet connected to the same Wi-Fi