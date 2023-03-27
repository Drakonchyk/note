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
app.secret_key = secrets.token_hex(16)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        instruments = request.form.getlist('instruments')
        tipe = request.form['tipe']
        search_songs = Search(query if query else '',
                        instruments if instruments else ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'],
                        tipe if tipe else 'both')
        results = search_songs.find()
        return render_template('search.html', results=results)
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
    for collection_name in ['Guitar', 'Kalimba', 'Ukulele', 'Piano', 'Drums']:
        collection = db.get_collection(collection_name)
        obj = collection.find_one({ '_id': ObjectId(object_id) })
        if obj:
            break

    # If the object is not found, return a 404 error
    if obj is None:
        abort(404)

    # Render a template with the details of the object
    return render_template('song_pg.html', object=obj)

if __name__ == '__main__':
    app.run(debug=True)
