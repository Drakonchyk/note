import unittest
from filters import Search, SearchAlgorithm, Filter, ValidateUser

class TestFiltersModule(unittest.TestCase):
    '''This class contains test for Search module'''
    def test_search(self):
        '''This method tests search class'''
        self.assertEqual(Search('Джонні деп в молодості').request, 'Джонні деп в молодості')
        self.assertEqual(Search('Давидко католик', tipe='both').tipe, 'both')
        self.assertEqual(Search('Чи може грек', ['kalimba']).instruments, ['kalimba'])
        self.assertIsNone(Search('та йой я не розбираюсь в машинах', ['kalimba']).find(), None)
        self.assertEqual(Search('ac dc', ['drums']).find()[0]['author'], 'AC/DC')
        self.assertEqual(Search('nirvana', ['drums']).find()[0]['title'], 'Come as You Are')

    def test_search_algorithm(self):
        '''This method test SearchAlgorithm class'''
        # Testing one_word_req function
        self.assertTrue(any(SearchAlgorithm('Kaene').one_word_req(song) for song in Filter(['kalimba'], 'tabs').get_filtered_songs())) # search by author
        self.assertTrue(any(SearchAlgorithm('скрябін').one_word_req(song) for song in Filter(['guitar'], 'chords').get_filtered_songs())) # search by author
        self.assertTrue(any(SearchAlgorithm('Джульетта').one_word_req(song) for song in Filter(['guitar'], 'chords').get_filtered_songs())) # search by title
        self.assertTrue(any(SearchAlgorithm('heard').one_word_req(song) for song in Filter(['piano'], 'chords').get_filtered_songs())) # search by text
        self.assertFalse(any(SearchAlgorithm('жфдіважлфоірвва').one_word_req(song) for song in Filter(['piano'], 'tabs').get_filtered_songs())) # huge mistake

        # Testing lots_word_req function

        # Testing search by title
        self.assertTrue(any(SearchAlgorithm('someone like you').lots_word_req(song) for song in Filter(['piano'], 'chords').get_filtered_songs())) # search by title: req is similiar length
        self.assertTrue(any(SearchAlgorithm('dancing on ma').lots_word_req(song) for song in Filter(['piano'], 'chords').get_filtered_songs())) # search by title: req is shorter
        self.assertFalse(any(SearchAlgorithm('цей запит має бути задовгим щоб наш пошук нічого не знайшов').lots_word_req(song) for song in Filter().get_filtered_songs())) # search: req is longer

        # Testing search by text
        self.assertFalse(any(SearchAlgorithm('коли біля тебе мене нема').lots_word_req(song) for song in Filter().get_filtered_songs())) # search by text: Song is not in database
        self.assertTrue(any(SearchAlgorithm('my life com-plete').lots_word_req(song) for song in Filter(['kalimba'], 'tabs').get_filtered_songs())) # search by texts
        self.assertTrue(any(SearchAlgorithm('не маючи нічого мати всьо').lots_word_req(song) for song in Filter(['guitar'], 'chords').get_filtered_songs())) # search by texts

        # Testing search by author
        self.assertTrue(any(SearchAlgorithm('foo fighters').one_word_req(song) for song in Filter().get_filtered_songs())) # search by author: req is similiar
        self.assertTrue(any(SearchAlgorithm('zeppelin').one_word_req(song) for song in Filter().get_filtered_songs())) # search by author: req is shorter


    def test_validate_user(self):
        """
        test validate_email and validate_password methods
        """
        # test validate_email
        self.assertTrue(ValidateUser().validate_email('naws@gmail.com'))
        self.assertFalse(ValidateUser().validate_email('na..ws@gmail.com'))
        self.assertFalse(ValidateUser().validate_email('naws.@gmail.com'))
        self.assertFalse(ValidateUser().validate_email('.dskdjfgh@gmail.com'))

        # test validate_password
        self.assertTrue(ValidateUser().validate_password('14917263549'))
        self.assertFalse(ValidateUser().validate_password('14919'))
        self.assertFalse(ValidateUser().validate_password('13546q34 4576919'))
        self.assertFalse(ValidateUser().validate_password('12345678901374569123745691273465293746591273465914691872346'))


def main():
    '''This function tests module filters'''
    unittest.main()

if __name__ == '__main__':
    main()
