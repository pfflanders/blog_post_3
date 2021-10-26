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
    db = get_message_db()
    c = db.cursor()
    name = request.form["name"]
    message = request.form["message"]
    new_id = 0 # get number of messages

    c.execute(f"INSERT INTO messages VALUES ({new_id}, {name}, {message})" )


messages_bp = Blueprint('messages', __name__, url_prefix='/messages')


@messages_bp.route('/survey/', methods=['POST', 'GET'])
def survey():
    if request.method == 'GET':
         return render_template('submit.html')
    else:
        try:
            insert_message(request)
            render_template('submit.html')
        except:
            return render_template('submit.html', error=True)

@messages_bp.route('/view/', methods=['GET']) 
def list():
    result = []
    #db = get_message_db()
    #c = db.cursor()
    #c.execute("SELECT DISTINCT * FROM messages LIMIT 5")
    #result = [elem[0] for elem in c.fetchall()]
    return render_template('list.html', messages=result)
