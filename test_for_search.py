'''test'''
from unittest import *
from search import *
class TestSearchModule(TestCase):
    '''This class contains test for Search module'''

    def testSearch(self):
        '''This method tests search class'''
        self.assertEqual(Search("Sweet Child O' Mine", ['guitar']).find(), [{'_id': 'ObjectId(\'641f428c016604bbbf9dc51b\')',
                                                                             'title': "Sweet Child O' Mine",
                                                                             'author': "Guns N' Roses",
                                                                             'categories': 'tabs',
                                                                             'instrument': 'guitar',
                                                                             'text': ['e|-----------------------------------------------------',
                                                                                      'B|-----------------------------------------------------',
                                                                                      'G|---------------------------------------0-------------',
                                                                                      'D|----2--0--2-----------------0--2--4--------4--2--0---',
                                                                                      'A|--------------2--0--2--3---------------------------',
                                                                                      'E|-----------------------------------------------------']}])
        self.assertEqual(Search('hehe i lowe men', ['guitar']).find(), None)
        self.assertEqual(Search('hehe i lowe men', ['pianino']).find(), None)
        self.assertEqual(Search('hehe i lowe men', ['ukulele']).find(), None)
        self.assertEqual(Search('hehe i lowe men', ['guitar'], tipe='chords').find(), None)
        self.assertEqual(Search('hehe i lowe men', ['guitar'], tipe='tabs').find(), None)
        self.assertEqual(Search('hehe i lowe men', ['drums']).find(), None)
        self.assertEqual(Search('hehe i lowe men', ['kalimba']).find(), None)
        self.assertTrue(isinstance(Filter(['kalimba']).collections, list))
        self.assertTrue(isinstance(Filter(['guitar']).instruments, list))