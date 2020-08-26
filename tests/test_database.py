import os
import unittest
import sqlite3

from database.database_manager import DatabaseManager


class TestDatabase(unittest.TestCase):
    """Test case for correct creation and retrieval of
    guitarists and bands from the database"""

    def setUp(self):
        self.test_db_file = 'test.db'
        self.test_db = DatabaseManager(self.test_db_file)
        self.tables_names = ['guitarists', 'bands', 'guitarists_and_bands']
        try:
            self.alt_conn = sqlite3.connect(self.test_db_file)
        except Exception:
            pass

    def test_table_creation(self):
        """Test tables are created successfully by the DatabaseManager"""
        for table in self.tables_names:
            select_str = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table}';"
            self.assertTrue(self.alt_conn.execute(select_str).fetchone()[0])

    def test_valid_add(self):
        """Test guitarists and bands are added to the database successfully by the DatabaseManager"""
        self.test_db.add_guitarist_and_bands('guitarist1', ['band1', 'band2'])
        self.test_db.add_guitarist_and_bands('guitarist2', 'band3')

        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[0]} WHERE full_name='guitarist1'").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[0]} WHERE full_name='guitarist2'").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[1]} WHERE name='band1'").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[1]} WHERE name='band2'").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[1]} WHERE name='band3'").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[2]} WHERE guitarist_id=1 AND band_id=1").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[2]} WHERE guitarist_id=1 AND band_id=2").fetchone()[0])
        self.assertTrue(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[2]} WHERE guitarist_id=2 AND band_id=3").fetchone()[0])

    def test_invalid_add(self):
        """Test invalid guitarists and bands are not added to the database successfully by the DatabaseManager"""
        self.test_db.add_guitarist_and_bands('guitarist1', None)
        self.test_db.add_guitarist_and_bands('guitarist2', 53)
        self.test_db.add_guitarist_and_bands('', 'band1')

        self.assertFalse(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[0]}").fetchone()[0])
        self.assertFalse(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[1]}").fetchone()[0])
        self.assertFalse(self.alt_conn.execute(
            f"SELECT COUNT(*) FROM {self.tables_names[2]}").fetchone()[0])

    def test_valid_get(self):
        """Test guitarists and bands are retrieved from the database successfully by the DatabaseManager"""
        guitarist_name = 'guitarist1'
        bands = ['band1', 'band2']
        self.test_db.add_guitarist_and_bands(guitarist_name, bands)

        self.assertEqual(
            [guitarist_name], self.test_db.get_band_guitarists(bands[0]))
        self.assertEqual(
            [guitarist_name], self.test_db.get_band_guitarists(bands[1]))
        self.assertEqual(
            bands, self.test_db.get_guitarist_bands(guitarist_name))

    def test_invalid_get(self):
        """Test invalid guitarists and bands return None"""
        guitarist_name = 'guitarist1'
        bands = ['band1', 'band2']
        self.test_db.add_guitarist_and_bands(guitarist_name, bands)

        self.assertEqual(None, self.test_db.get_band_guitarists(3))
        self.assertEqual(None, self.test_db.get_band_guitarists(None))
        self.assertEqual(None, self.test_db.get_band_guitarists(bands))
        self.assertEqual(None, self.test_db.get_band_guitarists(''))

        self.assertEqual(None, self.test_db.get_guitarist_bands(3))
        self.assertEqual(None, self.test_db.get_guitarist_bands(None))
        self.assertEqual(
            None, self.test_db.get_guitarist_bands([guitarist_name]))
        self.assertEqual(
            None, self.test_db.get_guitarist_bands(''))

    def test_clear(self):
        """Test the tables are deleted by the DatabaseManager"""
        self.test_db.clear()
        for table in self.tables_names:
            select_str = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table}';"
            self.assertFalse(self.alt_conn.execute(select_str).fetchone()[0])

    def tearDown(self):
        self.test_db.close_connection()
        os.remove(self.test_db_file)
