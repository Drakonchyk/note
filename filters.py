""" Search class """
import re
import difflib
from pymongo import MongoClient, ASCENDING, DESCENDING

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

class SearchAlgorithm:
    '''This class implements search algorithms.

    Uses:
    - regex library;
    - difflib library.

    Returns True or False'''
    def __init__(self, searching):
        '''This method contains variables'''
        self.searching = searching.strip()

    def without_mistakes(self, song):
        '''This method is True if search do not contain any mistakes and
        our database contains certain song'''
        return song['instrument'] in {'piano', 'guitar', 'ukulele'} and song['categories'] == 'chords' and any([bool(re.fullmatch(fr'(.*)?{self.searching}(.*)?', textline)) for textline in song['text']]) or\
            re.match(self.searching, song['title']) or\
            re.match(self.searching, song['author'])

    def one_word_req(self, song):
        '''This method handles mistakes in search request, if request consists of 1 word'''
        match_ratio = max([max([difflib.SequenceMatcher(None, element.lower(), self.searching.lower()).ratio() for element in re.split(r'\s+', textline)]) for textline in song['text']])
        return song['instrument'] in {'piano', 'guitar', 'ukulele'} and song['categories'] == 'chords' and match_ratio >= 0.75

    def lots_word_req(self, song):
        ''''This method handles requests with number of words > 1, that have mistakes'''
        number_of_words = len(re.findall(r'\s+', self.searching)) + 1
        if number_of_words == 1:
            return False
        for textline in song['text']:
            iter_space = 0
            spaces = [num for num, el in enumerate(textline) if el == ' ']
            cont = True # variable to continue
            if len(re.findall(r'\s+', self.searching)) > len(re.findall(r'\s+', textline)): # if our request is longer that line that we check
                continue
            elif number_of_words - 1 == len(re.findall(r'\s+', textline)): # if request and line have similiar length
                if difflib.SequenceMatcher(None, textline.lower(), self.searching.lower()).ratio() >= 0.75:
                                    return True
            else: # if request is shorter than line that we check
                try:
                    while cont and spaces != [] and textline != '':
                        if iter_space == 0: # first iteration
                            if len(spaces) != number_of_words-1:
                                check = textline[: spaces[number_of_words-1]]
                            else:
                                if difflib.SequenceMatcher(None, textline.lower(), self.searching.lower()).ratio() >= 0.75:
                                    return True
                                iter_space += 1
                                break

                            iter_space += 1
                        elif iter_space+number_of_words-1 >= len(spaces): # last iteration
                            check = textline[spaces[iter_space-1]+1:]
                            iter_space += 1
                            cont = False
                        else: # medium iteration
                            check = textline[spaces[iter_space-1]+1: spaces[iter_space+number_of_words-1]]
                            iter_space += 1
                        if difflib.SequenceMatcher(None, check.lower(), self.searching.lower()).ratio() >= 0.75:
                            return True
                except IndexError:
                    pass
        return False

    def find_matches(self, song):
        '''This method implements main search'''
        return self.without_mistakes(song) or self.one_word_req(song) or self.lots_word_req(song)

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
        Checker = SearchAlgorithm(self.request)
        result = []
        collections = Filter(self.instruments).get_filtered_songs()
        for collection in collections:
            if self.tipe == 'both':
                file = list(collection.find({'categories': 'chords'}))
                file += list(collection.find({'categories': 'tabs'}))
            elif self.tipe == 'chords':
                file = list(collection.find({'categories': 'chords'}))
            else:
                file = list(collection.find({'categories': 'tabs'}))
            for song in file:
                if Checker.find_matches(song):
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

class DateSort:
    '''This class sorts songs by dates'''
    def __init__(self, sort_position=1, instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'],\
                 tipe = 'both'):
        'This method contains variables'
        self.sort_position = sort_position
        self.instruments = instruments
        self.tipe = tipe

    def sort_by_dates(self):
        '''This method sorts songs and datesin
        ascending way if sort_position = 1
        in descending way if sort_position = 0'''
        collections = Filter(instruments=self.instruments, tipe=self.tipe).get_filtered_songs()
        sorted_songs = []
        for collection in collections:
            if self.sort_position:
                sort_order = [("date", ASCENDING)]
            else:
                sort_order = [("date", DESCENDING)]

            songs = collection.find().sort(sort_order)
            sorted_songs += songs

        sorted_songs = sorted(sorted_songs, key=lambda x: x["date"], reverse=self.sort_position)

        return sorted_songs
