#! /usr/bin/env python3
import argparse
from utils.guitarists import check_guitarist, check_band
from utils.database.database_manager import DatabaseManager
from utils.cache.csv_cacher import CsvCacher

parser = argparse.ArgumentParser()
parser.add_argument('-nc', '--no-cache', dest='cache',
                    default=False, action='store_true', help='Do not save to csv the cache')
args = parser.parse_args()

write_cache = True

if args.cache:
    write_cache = False

db_manager = DatabaseManager()
if write_cache:
    cacher = CsvCacher()

print('Welcome to the guitarits database interface')

while True:
    input_str = input(
        "Do you want to search for a guitarist or a band? Type exit to quit. ")
    input_str = input_str.strip().lower()

    if input_str == 'guitarist':
        input_str = input("Please write the name of the guitarist. ")
        input_str = input_str.strip()

        answer = check_guitarist(db_manager, input_str)
        print(answer)

        if write_cache:
            cacher.add_to_cache(input_str, answer)
    elif input_str == 'band':
        input_str = input("Please write the name of the band. ")
        input_str = input_str.strip()

        answer = check_band(db_manager, input_str)
        print(answer)

        if write_cache:
            cacher.add_to_cache(input_str, answer)
    elif input_str == 'exit':
        break
    else:
        print('Cannot recognise the command')

if write_cache:
    cacher.write_cache()
db_manager.close_connection()
