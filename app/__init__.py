# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run


from flask import Flask, g, render_template, request

# from .auth import auth_bp, close_auth_db, init_auth_db_command
from .messages import messages_bp, close_message_db

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)

# Create main page (fancy)

@app.route('/')
def main():
    return render_template('main_better.html')

# Show url matching

@app.route('/hello/<name>/')
def hello_name(name):
    return render_template('hello.html', name=name)

# Page with form

@app.route('/ask/', methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        try:
            return render_template('ask.html', name=request.form['name'], student=request.form['student'])
        except:
            return render_template('ask.html')


# @app.route('/submit/', methods=['POST', 'GET'])
# def submit():
#     if request.method == 'GET':
#         return render_template('submit.html')
#     else:
#         try:
#             # retrieve the image
#             message = request.files['message']


#             return render_template('submit.html')
#         except:
#             return render_template('submit.html', error=True)
        
app.register_blueprint(messages_bp)
app.teardown_appcontext(close_message_db)

# Sessions and logging in

# app.secret_key = b'h\x13\xce`\xd9\xde\xbex\xbd\xc3\xcc\x07\x04\x08\x88~'

# app.register_blueprint(auth_bp)
# app.teardown_appcontext(close_auth_db)
# app.cli.add_command(init_auth_db_command) # run with flask init-auth-db
