## to execute ##
#python -m flask --app .\app_laermkarte.py run
################
import functions_laermkarte
from flask import Flask
from flask import request, render_template
app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template('laermkarte.html')

@app.route('/', methods=['POST'])
def my_form_post():
    uhrzeit = str(request.form['variable'])
    return functions_laermkarte.map_func(uhrzeit)
@app.route('/foo', methods=['POST', 'GET'])
def index():
    return functions_laermkarte.hist_map_func()
if __name__ == "__main__":
    app.run(debug=True)

