"""
flask code for our 'note' project
"""
import secrets #for secret_key, generates secure random numbers for cryptographic purposes.
from flask import Flask, render_template, request, abort, url_for, redirect, session
import pymongo
import bcrypt
from bson import ObjectId
from filters import Filter, Search

client = pymongo.MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) #secret_key, should not change that

@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    function which submits chosen filters to class Search
    """
    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            query = ''
        instrument_button = request.form.get('instrument_button')
        instrument_s = request.form.getlist('instrument_checkbox')
        if instrument_button:
            new_instrument = [instrument_button]
        elif instrument_s:
            new_instrument = instrument_s
        else:
            new_instrument = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums']
        tipe = request.form.getlist('categories')
        if not tipe or len(tipe) == 2:
            tipe = ['both']
        search_songs = Search(request=query, instruments=new_instrument, tipe=tipe[0])
        results = search_songs.find()
        return render_template('search.html', results=results)
    return render_template('search.html')


@app.route('/')
def welcome():
    """
    opens main page
    """
    return render_template('welcome.html')

@app.route('/welcome_loged')
def welcome_loged():
    """
    opens main page as loged user
    """
    return render_template('welcome_loged.html')

@app.route('/about')
def about():
    """
    opens page with information about the site
    """
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Opens registration page
    """
    if request.method == 'POST':
        user = request.form['username']
        mail = request.form['email']
        __password = request.form['pwd']
        __rep_password = request.form['pwd-repeat']
        hashed = bcrypt.hashpw(__password.encode('utf-8'), bcrypt.gensalt())
        if (not user or not mail or not __password
            or not __rep_password or __password != __rep_password
            or list(db.Users.find({"email": mail})) or list(db.Users.find({"name": user}))):
            return render_template('register.html')
        db.Users.insert_one({"name": user, "email": mail, "password": hashed})
        return render_template('login.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        __password = request.form['pswrd']
        user = db.Users.find_one({"name": username})
        if user:
            if bcrypt.checkpw(__password.encode('utf-8'), user['password']):
                return render_template('welcome.html')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    function for adding songs in the database
    all fields are required except for the checkbox 'I want_tabs!'
    """
    if request.method == 'POST':
        name = request.form['song_name']
        authr = request.form['author_name']
        instrument = request.form['instr']
        text = request.form['song_text'].split('\n')
        choice = request.form.get('want_tabs')
        if instrument == 'guitar':
            db.Guitar.insert_one({'title': name, 'author': authr,
                                  'categories': 'tabs' if choice else 'chords',
                                  'instrument': instrument, 'text': text})
        elif instrument == 'ukulele':
            db.Ukulele.insert_one({'title': name, 'author': authr,
                                   'categories': 'tabs' if choice else 'chords',
                                   'instrument': instrument, 'text': text})
        elif instrument == 'piano':
            db.Piano.insert_one({'title': name, 'author': authr,
                                 'categories': 'tabs', 
                                 'instrument': instrument, 'text': text})
        elif instrument == 'drums':
            db.Drums.insert_one({'title': name, 'author': authr,
                                 'categories': 'tabs',
                                 'instrument': instrument, 'text': text})
        else:
            db.Kalimba.insert_one({'title': name, 'author': authr,
                                   'categories': 'tabs',
                                   'instrument': instrument, 'text': text})
    return render_template('create.html')

@app.route('/object/<object_id>')
def object_detail(object_id):
    """
    function which finds an object in the database and
    renders a song page with its details
    """
    obj = []
    for collection in Filter().get_filtered_songs():
        obj = list(collection.find({ '_id': ObjectId(object_id) }))
        if obj:
            break
    if obj is None:
        abort(404)
    obj = obj[0]
    return render_template('song_pg.html', object=obj)

if __name__ == '__main__':
    app.run(debug=True)
