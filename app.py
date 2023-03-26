from flask import Flask, render_template, session, request, url_for, redirect
from flask.helpers import make_response
from flask.json import jsonify
import pymongo
import json
from bson import ObjectId
import secrets
from backend.filters import Filter, Search


client = pymongo.MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) # should not change that

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) #not sure if that's useful

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         query = request.args.get('query')
#         # instrument = request.form.get('instrument')
#         # filtr = Filter()
#         # if instrument:
#         #     filtr = Filter([instrument])
#         # results = Filter().some_func(filtr)
#         result = Search(query).find()
#         # if instrument == 'kalimba':
#         #     # Do something when button_value_1 is pressed
#         # elif instrument == 'piano':
#         #     # Do something when button_value_2 is pressed
#         # elif instrument == 'drums':
#         # elif instrument == 'guitar':
#         # elif instrument == 'ukulele':
#     # Render the template with the form
#     return render_template('songs_choice.html')
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
