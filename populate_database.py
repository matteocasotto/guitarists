
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


db_manager = DatabaseManager('guitarists.db')

for k, v in list_of_guitarists.items():
    db_manager.add_guitarist_and_bands(k, v)
db_manager.close_connection()
