import sqlite3

create_guitarist_table = '''CREATE TABLE IF NOT EXISTS guitarists (
                            id INTEGER PRIMARY KEY,
                            full_name TEXT NOT NULL UNIQUE
                            );'''

create_bands_table = '''CREATE TABLE IF NOT EXISTS bands (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL UNIQUE
                        );'''

create_combined_table = '''CREATE TABLE IF NOT EXISTS guitarists_and_bands (
                            guitarist_id INTEGER NOT NULL,
                            band_id INTEGER NOT NULL,
                            FOREIGN KEY(guitarist_id)
                            REFERENCES guitarists (id),
                            FOREIGN KEY(band_id) REFERENCES bands (id)
                        );'''


class DatabaseManager:
    def __init__(self, filename='guitarists.db'):
        self._conn = None
        self._filename = filename
        self._create_connection()
        self._create_tables()

    def _create_connection(self):
        try:
            self._conn = sqlite3.connect(self._filename, isolation_level=None)
        except Exception:
            pass

    def close_connection(self):
        """Close the database's connection"""
        self._conn.close()

    def clear(self):
        """Delete all tables from the database"""
        cursor = self._conn.cursor()

        cursor.execute('DROP TABLE guitarists')
        cursor.execute('DROP TABLE bands')
        cursor.execute('DROP TABLE guitarists_and_bands')

    def _create_tables(self):
        cursor = self._conn.cursor()
        cursor.execute(create_guitarist_table)
        cursor.execute(create_bands_table)
        cursor.execute(create_combined_table)

    def _add_guitarist(self, guitarist_name):
        cursor = self._conn.cursor()
        try:
            cursor.execute('INSERT INTO guitarists(full_name) VALUES(?)',
                           (guitarist_name,))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return self._get_guitarist_id_by_name(guitarist_name)

    def _add_band(self, band_name):
        cursor = self._conn.cursor()
        try:
            cursor.execute('INSERT INTO bands(name) VALUES(?)',
                           (band_name,))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return self._get_band_id_by_name(band_name)

    def add_guitarist_and_bands(self, guitarist_name, bands):
        """Add a guitarists and its bands to the database

        Parameters:
            guitarist_name (str): the name of the guitarist
            bands Union[list(str), str]: a list of bands
        """
        if (not isinstance(guitarist_name, str) or
                not isinstance(bands, (str, list))):
            return
        if not guitarist_name:
            return
        if isinstance(bands, list):
            if not all(isinstance(x, str) for x in bands):
                return
        cursor = self._conn.cursor()
        guitarist_id = self._add_guitarist(guitarist_name)
        if guitarist_id:
            if isinstance(bands, str):
                bands = [bands]
            for band in bands:
                band_id = self._add_band(band)
                if band_id:
                    cursor.execute(
                        ('INSERT INTO guitarists_and_bands'
                         '(guitarist_id, band_id) VALUES(?, ?)'),
                        (guitarist_id, band_id)
                    )

    def _get_guitarist_id_by_name(self, guitarist_name):
        cursor = self._conn.cursor()
        try:
            guitarist = cursor.execute(
                'SELECT id FROM guitarists WHERE full_name=?',
                (guitarist_name,)
            )
            guitarist = guitarist.fetchone()
            if guitarist:
                return guitarist[0]
            return None
        except sqlite3.Error:
            return None

    def _get_band_id_by_name(self, band_name):
        cursor = self._conn.cursor()
        try:
            band = cursor.execute('SELECT id FROM bands WHERE name=?',
                                  (band_name,))
            band = band.fetchone()
            if band:
                return band[0]
            return None
        except sqlite3.Error:
            return None

    def _get_guitarist_name_by_id(self, id):
        cursor = self._conn.cursor()
        try:
            guitarist = cursor.execute(
                'SELECT full_name FROM guitarists WHERE id=?',
                (id,)
            )
            guitarist = guitarist.fetchone()
            if guitarist:
                return guitarist[0]
            return None
        except sqlite3.Error:
            return None

    def _get_band_name_by_id(self, id):
        cursor = self._conn.cursor()
        try:
            band = cursor.execute('SELECT name FROM bands WHERE id=?',
                                  (id,))
            band = band.fetchone()
            if band:
                return band[0]
            return None
        except sqlite3.Error:
            return None

    def get_guitarist_bands(self, guitarist_name):
        """Retrieve the bands of a guitarist

        Parameters:
            guitarist_name (str): the name of the guitarist
        """
        if not isinstance(guitarist_name, str):
            return None
        cursor = self._conn.cursor()
        guitarist = self._get_guitarist_id_by_name(guitarist_name)
        band_list = []
        if guitarist:
            try:
                bands = cursor.execute(
                    ('SELECT band_id FROM guitarists_and_bands '
                     'WHERE guitarist_id=?'),
                    (guitarist,)
                )
                bands = bands.fetchall()

                for band in bands:
                    band_name = self._get_band_name_by_id(band[0])
                    if band_name:
                        band_list.append(band_name)
            except sqlite3.Error:
                return None
        if not band_list:
            return None
        return band_list

    def get_band_guitarists(self, band_name):
        """Retrieve the guitarists of a band

        Parameters:
            band_name (str): the name of the band
        """
        if not isinstance(band_name, str):
            return None
        cursor = self._conn.cursor()
        band = self._get_band_id_by_name(band_name)
        guitarist_list = []
        if band:
            try:
                guitarists = cursor.execute(
                    ('SELECT guitarist_id FROM guitarists_and_bands '
                     'WHERE band_id=?'),
                    (band,)
                )
                guitarists = guitarists.fetchall()

                for guitarist in guitarists:
                    guitarist_name = self._get_guitarist_name_by_id(
                        guitarist[0])
                    if guitarist_name:
                        guitarist_list.append(guitarist_name)
            except sqlite3.Error:
                return None
        if not guitarist_list:
            return None
        return guitarist_list
