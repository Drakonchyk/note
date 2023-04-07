""" Search class """
import re
from pymongo import MongoClient

client = MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

class Filter:
    """
    class for filtering songs
    """
    def __init__(self, instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'],
                 tipe = 'both') -> None:
        self.instruments = instruments
        self.collections = []
        self.tipe = tipe # 'chords', 'tabs' or 'both'

    def get_filtered_songs(self) -> list:
        """
        add wanted collections to the list of collections (self.collections)
        and return the final list
        """

        if 'guitar' in self.instruments:
            self.collections.append(db.Guitar)
        if 'kalimba' in self.instruments:
            self.collections.append(db.Kalimba)
        if 'ukulele' in self.instruments:
            self.collections.append(db.Ukulele)
        if 'piano' in self.instruments:
            self.collections.append(db.Piano)
        if 'drums' in self.instruments:
            self.collections.append(db.Drums)

        return self.collections

class Search (Filter):
    """
    search for songs by author or title
    instruments - wanted instruments for songs (by default - all are chosen)
    tipe - type of notes
    """
    def __init__(self, request="",
                 instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'],
                 tipe = 'both') -> None:
        super().__init__(instruments, tipe)
        self.request = request

    def find(self) -> list:
        """
        search for songs by instrument and by type of notes
        (it can be chords, tabs or both) if request is given, \
searches for songs which title or author mathicng the request  
        """
        result = []
        collections = Filter(self.instruments).get_filtered_songs()
        if self.request == "":
            for collection in collections:
                if self.tipe == 'both':
                    file = list(collection.find({'$or': [{'categories': 'chords'},
                                                         {'categories': 'tabs'}]}))
                elif self.tipe == 'chords':
                    file = list(collection.find({'categories': 'chords'}))
                else:
                    file = list(collection.find({'categories': 'tabs'}))
                for song in file:
                    if song not in result:
                        result.append(song)
            return result
        for collection in collections:
            if self.tipe == 'both':
                file = list(collection.find({'title': self.request}))
                file += (list(collection.find({'author': self.request})))
            elif self.tipe == 'chords':
                file = list(collection.find({'title': self.request, 'categories': 'chords'}))
                file += (list(collection.find({'author': self.request, 'categories': 'chords'})))
            else:
                file = list(collection.find({'title': self.request, 'categories': 'tabs'}))
                file += (list(collection.find({'author': self.request, 'categories': 'tabs'})))

            for song in file:
                if song not in result:
                    result.append(song)
        if result:
            return result
        return None

class ValidateUser:
    """
    check if email is appropriate
    """

    def validate_email(self, email:str)-> bool:
        """
        validate email
        """
        if '..' in email:
            return False
        pattern = r"^[^\.\s][^\s]{0,63}(?<!\.)@[a-z]+(\.[a-z]+)*\.(com|org|edu|gov|net|ua)$"
        if re.fullmatch(pattern, email):
            return True
        return False

    def validate_password(self, password:str)-> bool:
        """
        validate password
        """
        if len(password) < 8:
            return False
        pattern = r'[^\s]{0,32}[\!\@\#\$\%\^\&\*]{1,9}[^\s]{0,32}'
        if re.fullmatch(pattern, password):
            return True
        return False
