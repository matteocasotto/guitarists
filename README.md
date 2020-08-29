## Implementation of a Database of guitar heroes

In this repository you can find an interface to a database of guitarists and their bands. An user can query the database by providing a name of a guitarist or of a band. 

### How to run

Run ```python3 main.py``` and follow the on-screen instruction to query the database. The program will automatically cache all the queries and their answers. This behaviour can be avoided by including a ```-nc/--no-csv``` argument.

Of course the database will be empty at the fist run. Please read the following section to understand how to populate or delete the database.

### How to populate/delete the database.

Run ```python3 populate_database.py``` to populate the database. This program will query the Wikipedia API for a list of guitarists and filter them. The corresponding Wikipedia page can be found [here](https://en.wikipedia.org/wiki/List_of_guitarists).

Running ```python3 populate_database.py -d``` or ```python3 populate_database.py --delete``` will clear the database and delete the file.

### Testing
To prove our framework works as expected, we developed a test suite to test our database manager and our caching system. Test can be run by typing ```python3 -m unittest```

## Requirements
The framework requires the ```json```, ```sqlite3```, ```requests``` modules to be installed.