from os import error
from flask import Blueprint, current_app, g, render_template, url_for, abort, request
import sqlite3

def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('message.sqlite')
        with current_app.open_resource('init.sql') as f:
            g.message_db.executescript(f.read().decode('utf8'))
    return g.message_db

def close_message_db(e=None):
    db = g.pop('message_db', None)
    if db is not None:
        db.close()

def insert_message(request):
    print('inserting message')
    
    db = get_message_db()
    if db:
        print('database succeded')
    
    c = db.cursor()
    name = request.form["name"]
    message = request.form["message"]
    print(f"name is {name} and message is {message}")

    length = c.execute("SELECT COUNT(id) FROM messages").fetchone()[0]
    print(f'length is {length}')

    sql = f"""
    INSERT INTO messages VALUES({length+1}, '{name}', '{message}');
    """
    print(sql)
    
    c.execute(sql)
    print('insert statement succeeded')
    
    db.commit()

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')


@messages_bp.route('/', methods=['POST', 'GET'])
def survey():
    if request.method == 'GET':
         return render_template('submit.html')
    else:
        print('got a post request for survey')
        try:
            insert_message(request)
            return render_template('submit.html')
        except:
            print('error in submitting survey')
            return render_template('submit.html', error=True)

def random_messages(n):
    result = []
    db = get_message_db()
    c = db.cursor()
    length = c.execute("SELECT COUNT(id) FROM messages").fetchone()[0] + 1 
    results = c.execute(f"SELECT * FROM messages ORDER BY RANDOM() LIMIT {min(n, length, 5)}").fetchall()
    print('sql method in view exectued succuessfully')
    return results
        

@messages_bp.route('/view/', methods=['GET']) 
def view():
    print('enter view method')
    try:
        results = random_messages(5)
        names = [elem[1] for elem in results]
        messages = [elem[2] for elem in results]
        return render_template('list.html', names=names, messages=messages)
    except:
        print('error in /view/')
        return render_template('list.html', error=True)