import os
import unittest

from cache.csv_cacher import CsvCacher


class Testcache(unittest.TestCase):
    """Test case for correct creation of a csv cache file"""

    def setUp(self):
        self.test_cache_file = 'test.csv'
        self.test_cacher = CsvCacher(self.test_cache_file)

    def test_add_valid_item(self):
        """Test question and answer are correctly added to cache"""
        self.test_cacher.add_to_cache('question', 'answer')

        self.assertEqual([('question', 'answer')], self.test_cacher._cache)

    def test_add_invalid_item(self):
        """Test invalid question and answer are not added to cache"""
        self.test_cacher.add_to_cache('question', 12)
        self.test_cacher.add_to_cache('question', None)
        self.test_cacher.add_to_cache('question', '')

        self.assertEqual([], self.test_cacher._cache)

    def test_write_with_valid_item(self):
        """Test file write cache correctly to file when there is one element in cache"""
        self.test_cacher.add_to_cache('question', 'answer')
        self.test_cacher.write_cache()

        self.assertTrue(os.path.exists(self.test_cache_file))

        with open(self.test_cache_file, 'r') as f:
            for i, _ in enumerate(f):
                pass
        self.assertEqual(i+1, 2)
        self.assertEqual(i, len(self.test_cacher._cache))

        self.test_cacher.add_to_cache('question2', 'answer2')
        self.test_cacher.write_cache()

        with open(self.test_cache_file, 'r') as f:
            for i, _ in enumerate(f):
                pass
        self.assertEqual(i+1, 3)
        self.assertEqual(i, len(self.test_cacher._cache))

    def test__write_with_no_item(self):
        """Test file write cache correctly to file when there are no elements in cache"""
        self.test_cacher.write_cache()

        self.assertTrue(os.path.exists(self.test_cache_file))

        with open(self.test_cache_file, 'r') as f:
            for i, _ in enumerate(f):
                pass
        self.assertEqual(i+1, 1)
        self.assertEqual(i, len(self.test_cacher._cache))

    def tearDown(self):
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)
