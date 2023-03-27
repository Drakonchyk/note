from pymongo import MongoClient

client = MongoClient("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')

class Filter:
    def __init__(self, instruments=['kalimba', 'guitar', 'ukulele', 'piano', 'drums'], tipe='both'):
        self.instruments = instruments
        self.collections = []
        self.tipe = tipe

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


class Search(Filter):
    def __init__(self, request = '', instruments=['kalimba', 'guitar', 'ukulele', 'piano', 'drums'], tipe='both'):
        super().__init__(instruments, tipe)
        self.request = request

    def find(self):
        result = []
        collections = self.get_filtered_songs()
        for collection in collections:
            if self.tipe == 'both':
                file = list(collection.find({'$or': [{'title': {'$regex': self.request}}, {'author': {'$regex': self.request}}]}))
            elif self.tipe == 'chords':
                file = list(collection.find({'$and': [{'categories': 'chords'}, {'$or': [{'title': {'$regex': self.request}}, {'author': {'$regex': self.request}}]}]}))
            else:
                file = list(collection.find({'$and': [{'categories': 'tabs'}, {'$or': [{'title': {'$regex': self.request}}, {'author': {'$regex': self.request}}]}]}))

            for song in file:
                if song not in result:
                    result.append(song)

        if result:
            return result
        else:
            return 'Nothing found'

