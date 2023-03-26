""" Search class """
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

class Filter:
    def __init__(self, instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'], \
                 tipe = 'both') -> None:
        self.instruments = instruments
        self.tipe = tipe # 'chords', 'tabs' or 'both'

class Search (Filter):
    def __init__(self, request, instruments = ['kalimba', 'guitar', 'ukulele', \
'piano', 'drums'], tipe = 'both') -> None:
        super().__init__(instruments, tipe)
        self.request = request

    def find(self):
        result = []
        collections = []
        if 'guitar' in self.instruments:
            collections.append(db.Guitar)
        if 'kalimba' in self.instruments:
            collections.append(db.Kalimba)
        if 'ukulele' in self.instruments:
            collections.append(db.Ukulele)
        if 'piano' in self.instruments:
            collections.append(db.Piano)
        if 'drums' in self.instruments:
            collections.append(db.Drums)

        for collection in collections:
            if self.tipe == 'both':
                file = list(collection.find({'title': self.request}))
                file += (list(collection.find({'author': self.request})))
            elif self.tipe == 'chords':
                file = list(collection.find({'title': self.request, 'categories':'chords'}))
                file += (list(collection.find({'author': self.request, 'categories':'chords'})))
            else:
                file = list(collection.find({'title': self.request, 'categories':'tabs'}))
                file += (list(collection.find({'author': self.request, 'categories':'tabs'})))

            for song in file:
                if song not in result:
                    result.append(song)
        if result:
            return result
        return 'Nothing found'


# i = Search("Stairway to Heaven", ['guitar']) # example
# print(i.find())



