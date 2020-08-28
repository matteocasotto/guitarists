#! /usr/bin/env python3

from guitarists import check_guitarist, check_band
from database.database_manager import DatabaseManager

db_manager = DatabaseManager()

a = check_guitarist(db_manager, "Kirk Hammett")
b = check_guitarist(db_manager, "Young Signorino")
c = check_band(db_manager, "Guns N' Roses")
d = check_band(db_manager, "Ricchi e Poveri")

print(a, b, c, d)
db_manager.close_connection()
