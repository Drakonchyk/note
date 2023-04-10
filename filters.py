""" Filter, search, sort, validate_user algorithms"""
import re
import difflib
from pymongo import MongoClient, ASCENDING, DESCENDING


client = MongoClient\
("mongodb+srv://user:user-password@testcluster.tyin0tg.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SongDatabase')


class Filter:
    '''This class represents filter for instruments, chords or tabs'''
    def __init__(self,\
                 instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'],\
                 tipe = 'both') -> None:
        '''This method contains variables'''
        self.instruments = instruments
        self.collections = []
        self.tipe = tipe # 'chords', 'tabs' or 'both'

    def get_filtered_songs(self):
        '''This method returns filtered songs'''
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

        return DateSort(self.collections, 1).sort_by_dates()


class SearchAlgorithm:
    '''This class implements search algorithms.

    Uses:
    - regex library;
    - difflib library.

    Returns True or False'''
    def __init__(self, searching):
        '''This method contains variables'''
        self.searching = searching.strip()


    def one_word_req(self, song):
        '''This method handles mistakes in search request, if request consists of 1 word'''
        match_ratio_text = max([max([difflib.SequenceMatcher(None, elem.lower(),
                                                             self.searching.lower()).ratio()
                                                             for elem in re.split(r'\s+',textline)])
                                                             for textline in song['text']])
        match_ratio_title = difflib.SequenceMatcher(None, song['title'].lower(),
                                                    self.searching.lower()).ratio()
        match_ratio_author = difflib.SequenceMatcher(None, song['author'].lower(),
                                                     self.searching.lower()).ratio()
        return match_ratio_text >= 0.75 or max(match_ratio_author, match_ratio_title) >= 0.75

    def lots_word_req(self, song):
        ''''This method handles requests with number of words > 1, that have mistakes'''
        number_of_spaces = len(re.findall(r'\s+', self.searching))
        if number_of_spaces == 1:
            return False
        check_list = song['text']

        # check for title
        if len(re.findall(r'\s+', song['title'])) < number_of_spaces:
            pass
        elif len(re.findall(r'\s+', song['title'])) == number_of_spaces:
            if (difflib.SequenceMatcher(None, song['title'].lower(),
                                        self.searching.lower()).ratio() >= 0.75):
                return True
        else:
            if len(re.findall(r'\s+', song['title'])) != 1:
                check_list.append(song['title'])

        # check for author
        if len(re.findall(r'\s+', song['author'])) < number_of_spaces:
            pass
        elif len(re.findall(r'\s+', song['author'])) == number_of_spaces:
            if (difflib.SequenceMatcher(None, song['author'].lower(),
                                        self.searching.lower()).ratio() >= 0.75):
                return True
        else:
            if len(re.findall(r'\s+', song['author'])) != 1:
                check_list.append(song['author'])

        # check for text
        for textline in check_list:
            iter_space = 0
            spaces = [num for num, el in enumerate(textline) if el == ' ']
            cont = True # variable to continue

            # if our request is longer that line that we check
            if len(re.findall(r'\s+', self.searching)) > len(re.findall(r'\s+', textline)):
                pass

            # if request and line have similiar length
            elif number_of_spaces == len(re.findall(r'\s+', textline)):
                if difflib.SequenceMatcher(None, textline.lower(),
                                           self.searching.lower()).ratio() >= 0.75:
                    return True

            else: # if request is shorter than line that we check
                try:
                    while cont and spaces != [] and textline != '':
                        if iter_space == 0: # first iteration
                            if len(spaces) != number_of_spaces:
                                check = textline[: spaces[number_of_spaces]]
                            else:
                                if difflib.SequenceMatcher(None, textline.lower(),
                                                           self.searching.lower()).ratio() >= 0.75:
                                    return True
                                iter_space += 1
                                break

                            iter_space += 1
                        elif iter_space+number_of_spaces >= len(spaces): # last iteration
                            check = textline[spaces[iter_space-1]+1:]
                            iter_space += 1
                            cont = False
                        else: # medium iteration
                            check = textline[spaces[iter_space-1]+1:
                                             spaces[iter_space+number_of_spaces]]
                            iter_space += 1
                        if difflib.SequenceMatcher(None, check.lower(),
                                                   self.searching.lower()).ratio() >= 0.75:
                            return True
                except IndexError:
                    pass
        return False

    def find_matches(self, song):
        '''This method implements main search'''
        return self.one_word_req(song) or self.lots_word_req(song)


class Search(Filter):
    '''This class search songs by name, author, or text'''
    def __init__(self, request, instruments = ['kalimba', 'guitar', 'ukulele', 'piano', 'drums'],
                 tipe = 'both') -> None:
        '''This method contains variables'''
        super().__init__(instruments, tipe)
        self.request = request

    def find(self):
        '''This method finds song'''
        checker = SearchAlgorithm(self.request)
        result = []
        songs = Filter(self.instruments).get_filtered_songs()
        if self.request == "":
            for song in songs:
                if song not in result and self.tipe in (song['categories'], 'both'):
                    result.append(song)
            return result
        for song in songs:
            if checker.find_matches(song) and self.tipe in (song['categories'], 'both'):
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
        pattern = r'[^\s]{8,48}'
        if re.fullmatch(pattern, password):
            return True
        return False

class DateSort:
    '''This class sorts songs by dates'''
    def __init__(self, songs, sort_position=1):
        'This method contains variables'
        self.sort_position = sort_position
        self.songs = songs

    def sort_by_dates(self):
        '''This method sorts songs and datesin
        ascending way if sort_position = 1
        in descending way if sort_position = 0'''
        collections = self.songs
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
