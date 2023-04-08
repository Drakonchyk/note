"""
flask code for our 'note' project
"""
import secrets
import datetime
import pymongo
import bcrypt
from flask import Flask, render_template, request, abort, url_for, redirect, session
from bson import ObjectId
from filters import Filter, Search, ValidateUser

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
        if "username" in session:
            return render_template('search.html', results=results, log=1)
        return render_template('search.html', results=results, log=0)
    return render_template('search.html', log=0)


@app.route('/')
def welcome():
    """
    opens main page
    """
    if "username" in session:
        return render_template('welcome.html', log = 1)
    return render_template('welcome.html', log = 0)


@app.route('/about')
def about():
    """
    opens page with information about the site
    """
    if "username" in session:
        return render_template('about.html', log = 1)
    return render_template('about.html', log = 0)

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
        user_list = [True, True, True, True]
        if not user or list(db.Users.find({"name": user})):
            user_list[0] = 0
        if not mail or list(db.Users.find({"email": mail})) or ValidateUser().validate_email(mail) is False:
            user_list[1] = 0
        if not __password or ValidateUser().validate_password(__password) is False:
            user_list[2] = 0
        if not __rep_password or __rep_password != __password:
            user_list[3] = 0
        if 0 in user_list:
            return render_template('register.html', troubles=user_list)
        db.Users.insert_one({"name": user, "email": mail, "password": hashed})
        return render_template('login.html', message="Registered succesfully!")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    opens login page
    """
    if request.method == 'POST':
        username = request.form['username']
        __password = request.form['pswrd']
        user = db.Users.find_one({"name": username})
        if not user:
            return render_template('login.html', troubles = 'user')
        if not __password or not bcrypt.checkpw(__password.encode('utf-8'), user['password']):
            return render_template('login.html', troubles = 'pswrd')
        session['username'] = username
        return redirect(url_for('user1'), )
    else:
        if "username" in session:
            return redirect(url_for('user1'))
        return render_template('login.html')

@app.route('/user')
def user1():
    """
    check if user logged in
    """
    if "username" in session:
        return render_template('welcome.html', log = 1)
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    function for adding songs in the database
    all fields are required except for the checkbox 'I want_tabs!'
    """
    if "username" not in session:
        return render_template('login.html')
    if request.method == 'POST':
        name = request.form['song_name']
        authr = request.form['author_name']
        instrument = request.form['instr']
        text = request.form['song_text'].split('\n')
        choice = request.form.get('want_tabs')
        username = session["username"]
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if instrument == 'guitar':
            db.Guitar.insert_one({'title': name, 'author': authr,
                                  'categories': 'tabs' if choice else 'chords',
                                  'instrument': instrument, 'text': text,
                                  'uploaded_by': username, 'date':date})
        elif instrument == 'ukulele':
            db.Ukulele.insert_one({'title': name, 'author': authr,
                                   'categories': 'tabs' if choice else 'chords',
                                   'instrument': instrument, 'text': text,
                                   'uploaded_by': username, 'date':date})
        elif instrument == 'piano':
            db.Piano.insert_one({'title': name, 'author': authr,
                                 'categories': 'tabs', 
                                 'instrument': instrument, 'text': text,
                                 'uploaded_by': username, 'date':date})
        elif instrument == 'drums':
            db.Drums.insert_one({'title': name, 'author': authr,
                                 'categories': 'tabs',
                                 'instrument': instrument, 'text': text,
                                 'uploaded_by': username, 'date':date})
        else:
            db.Kalimba.insert_one({'title': name, 'author': authr,
                                   'categories': 'tabs',
                                   'instrument': instrument, 'text': text, 
                                   'uploaded_by': username, 'date':date})
        return render_template('welcome.html', log = 1)
    return render_template('create.html')

@app.route('/object/<object_id>')
def object_detail(object_id):
    """
    function which finds an object in the database and
    renders a song page with its details
    """
    obj = []
    for song in Filter().get_filtered_songs():
        if song['_id'] == ObjectId(object_id):
            obj = song
            break
        # obj = list(collection.find({ '_id': ObjectId(object_id) }))
        # if obj:
        #     break
    if obj is None:
        abort(404)
    # obj = obj[0]
    if "username" in session:
        return render_template('song_pg.html', object=obj, log = 1)
    return render_template('song_pg.html', object=obj, log = 0)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('welcome.html', log = 0)

if __name__ == '__main__':
    app.run(debug=True)
