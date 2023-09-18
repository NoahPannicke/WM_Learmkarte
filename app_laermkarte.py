import functions_laermkarte
from flask import Flask
from flask import request, render_template
from functions_laermkarte import map_func
app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template('laermkartelaermkarte.html')

@app.route('/', methods=['POST'])
def my_form_post():
    uhrzeit = str(request.form['variable'])
    return test_app.map_func(uhrzeit)
@app.route('/foo', methods=['POST', 'GET'])
def index():
    return test_app.hist_map_func()

