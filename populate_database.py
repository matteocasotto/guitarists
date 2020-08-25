
import argparse
import os

from database.database_manager import DatabaseManager

list_of_guitarists = {'Eric Clapton': 'Cream',
                      'Jimmy Page': 'Led Zeppelin',
                      'Keith Richards': 'Rolling Stones',
                      'Eddie Van Halen': 'Van Halen',
                      'David Gilmour': 'Pink Floyd',
                      'Angus Young': 'AD/DC',
                      'Brian May': 'Queen',
                      'Johnny Ramone': 'Ramones',
                      'Tom Morello': 'Rage Against the Machine',
                      'Slash': "Guns'n Roses",
                      'Jim Root': 'Slipknot',
                      'Kirk Hammet': 'Metallica'
                      }


parser = argparse.ArgumentParser()
parser.add_argument('d', '--delete', dest='delete',
                    default=False, action='store_true', help='Delete database')
args = parser.parse_args()

database_file = 'guitarists.db'
db_manager = DatabaseManager(database_file)

if args.delete:
    db_manager.clear()
    db_manager.close_connection()
    os.remove(database_file)
else:
    for k, v in list_of_guitarists.items():
        db_manager.add_guitarist_and_bands(k, v)
    db_manager.close_connection()
