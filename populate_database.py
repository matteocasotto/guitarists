
import argparse
import os
import json
import requests
import re

from utils.database.database_manager import DatabaseManager

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delete', dest='delete',
                    default=False, action='store_true', help='Delete database')
args = parser.parse_args()

database_file = 'guitarists.db'
db_manager = DatabaseManager(database_file)

if args.delete:
    db_manager.clear()
    db_manager.close_connection()
    os.remove(database_file)
else:

    r = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=list_of_guitarists&rvslots=*&rvprop=content&formatversion=2&format=json')

    r = r.json()
    content = r['query']['pages'][0]['revisions'][0]['slots']['main']['content']

    guitarist_bands_dict = {}

    valid_entry_pattern = r'\*\[\[(.+)\]\] \((.+)\)'
    find_band_names_pattern = r'\[\[(.+?)\]\]'

    entries = re.finditer(valid_entry_pattern, content)

    for person in entries:
        name = person.group(1)
        bands = person.group(2)

        if '|' in name:
            name = name.split('|')[1].strip()
        bands = re.findall(find_band_names_pattern, bands)
        for y in range(0, len(bands)):
            if '|' in bands[y]:
                bands[y] = bands[y].split('|')[1].strip()
        guitarist_bands_dict[name] = bands

    for k, v in guitarist_bands_dict.items():
        db_manager.add_guitarist_and_bands(k, v)
    db_manager.close_connection()
