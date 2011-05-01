# -*- coding: utf-8 -*-

from django.test import TestCase
from japanese import generate_reading, _furiganaize, _furiganaize_complex_compound_word
from cache import make_key, cached_function, cached_method


class CacheHelperTest(TestCase):
    def test_short_key(self):
        args = ['foo', 'bar', 'b1z', 'qu ux']
        key = make_key(*args)
        for arg in args:
            self.assertTrue(arg.replace(' ', '') in key)

    def test_long_key(self):
        args = range(2000)
        key = make_key(*args)
        self.assertTrue(len(key) <= 250)
        self.assertTrue('1.2.3.4.5.6.7.8.9.10.11.12' not in key, 'key is not hashed')

    def test_function_decorator(self):
        foo = 10
        
        @cached_function
        def my_func(invalidate_cache=None):
            return foo

        ret = my_func()
        self.assertEqual(ret, foo)

        foo = 20
        ret = my_func()
        self.assertNotEqual(ret, foo)

    def test_method_decorator(self):
        foo = 10
        
        class Bar(object):
            @cached_method
            def my_func(self, invalidate_cache=None):
                return foo

        bar = Bar()
        ret = bar.my_func()
        self.assertEqual(ret, foo)

        foo = 20
        ret = bar.my_func()
        self.assertNotEqual(ret, foo)

        


class ReadingGenerationTest(TestCase):

    def test_compound_word(self):
        word = u'曲がり角'
        reading = generate_reading(word)
        self.assertTrue(u'かど' in reading)
        self.assertEqual(u'曲[ま]がり　角[かど]', reading)

    def test_furiganaize(self):
        word = u'角'
        reading = u'かど'
        translit = _furiganaize(word, reading, False)
        self.assertTrue(u'かど' in translit)

    def test_complex_compound_word_furiganaize(self):
        word = u'曲がり角'
        reading = u'まがりかど'
        ret = _furiganaize_complex_compound_word(word, reading)
        self.assertEqual(u'曲[ま]がり　角[かど]', ret)


