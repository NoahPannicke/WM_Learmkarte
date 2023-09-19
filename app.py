from flask import Flask
from flask import request
from functions_laermkarte import map_func
app = Flask(__name__)
@app.route("/")
def index():
    Uhrzeit = request.args.get("Uhrzeit", "")
    if Uhrzeit:
        laermkarte = dynamic_page(Urhzeit)
    else:
        laermkarte = "10:00"
    return (
        """<form action="" method="get">
                Urhzeit: <input type="text" name="Uhrzeit">
                <input type="submit" value="Lärmkarte anzeigen">
            </form>"""
    )
#@app.route("/")
#def dynamic_page(Uhrzeit):
#    return test_app.map_func(Uhrzeit)
