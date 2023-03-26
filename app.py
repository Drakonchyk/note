from flask import Flask, render_template, session, request, url_for, redirect, abort
from flask.helpers import make_response
from flask.json import jsonify
import pymongo
from flask_pymongo import PyMongo
import json
from bson import ObjectId
import secrets
from filters import Filter, Search

client = pymongo.MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority"
# mongo = PyMongo(app)
app.secret_key = secrets.token_hex(16) # should not change that

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) #not sure if that's useful

@app.route('/search', methods=['GET', 'POST'])
def search_results():
    # if request.method == 'POST':
    #     query = request.args.get('query')
    #     # instrument = request.form.get('instrument')
    #     # filtr = Filter()
    #     # if instrument:
    #     #     filtr = Filter([instrument])
    #     # results = Filter().some_func(filtr)
    #     result = Search(query).find()
    #     # if instrument == 'kalimba':
    #     #     # Do something when button_value_1 is pressed
    #     # elif instrument == 'piano':
    #     #     # Do something when button_value_2 is pressed
    #     # elif instrument == 'drums':
    #     # elif instrument == 'guitar':
        # elif instrument == 'ukulele':
    # Render the template with the form
    if request.method == 'POST':
        search_text = request.form['search_text']
        search_options = request.form.getlist('search_option')

        # Use the search text and options to query the MongoDB database
        results = db.collection.find({'text': {'$regex': search_text}, 'options': {'$in': search_options}})
        return render_template('search.html', results=results, search_text=search_text, search_options=search_options)

    else:
        return render_template('search.html')

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/object/<object_id>')
def object_detail(object_id):
    # Look up the object in the database using the object_id parameter
    obj = db.objects.find_one({ '_id': ObjectId(object_id) })

    # If the object is not found, return a 404 error
    if obj is None:
        abort(404)

    # Render a template with the details of the object
    return render_template('song_pg.html', object=obj)

if __name__ == '__main__':
    app.run(debug=True)
