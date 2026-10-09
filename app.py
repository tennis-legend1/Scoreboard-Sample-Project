from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


DB_NAME = 'scores.db'


def init_db():

    with sqlite3.connect(DB_NAME) as conn:

        conn.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')

@app.route('/leaderboard', methods=['GET', 'POST'])


def leaderboard():

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        score = request.form['score']

        try:
            score = int(score)
            if score >= 0:
                with sqlite3.connect(DB_NAME) as conn:
                    conn.execute('INSERT INTO scores (first_name, last_name, score) VALUES (?, ?, ?)', (first_name, last_name, score))
        except ValueError:
            pass
        
        return redirect('/leaderboard')

    sort_by = request.args.get('sort_by', 'quickest')
    
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

@app.route('/cybermatch', methods=['GET', 'POST'])
def index ():
    return render_template('Muhammad-Main.html')


init_db()  

# Start the Flask server for local testing (Comment the version not being used)
app.run(debug=True)  
# Use this version when testing on your computer only

#app.run(debug=True, host='0.0.0.0') 
# Use this version if you want to test it on a phone/tablet connected to the same Wi-Fi
