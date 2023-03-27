""" Search class """
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

class Filter:
    def __init__(self, instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'], \
                 tipe = 'both') -> None:
        self.instruments = instruments
        self.collections = []
        self.tipe = tipe # 'chords', 'tabs' or 'both'

    def get_filtered_songs(self):

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
    def __init__(self, request="", instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'], tipe = 'both') -> None:
        super().__init__(instruments, tipe)
        self.request = request

    def find(self):
        result = []
        collections = Filter(self.instruments).get_filtered_songs()
        if self.request == "":
            for collection in collections:
                if self.tipe == 'both':
                    file = list(collection.find({'$or': [{'categories': 'chords'}, {'categories': 'tabs'}]}))
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
        return 'Nothing found'

# j = Filter(['guitar'])
# h = j.get_filtered_songs()
# i = Search("Скрябін", ["guitar"], tipe='tabs') # example
# print(i.find())
