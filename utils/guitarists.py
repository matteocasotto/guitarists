from .database.database_manager import DatabaseManager


def check_guitarist(db_manager, guitar_player):
    """Check if a guitarist exits in the database

    Parameters:
        db_manager (DatabaseManager): the database's manager
        guitar_player (str): the full name of the guitarist
    """
    if not isinstance(db_manager, DatabaseManager):
        return
    if db_manager:
        bands = db_manager.get_guitarist_bands(guitar_player)
        if bands:
            if len(bands) == 1:
                return f'{guitar_player} plays for {bands[0]}.'
            return f'{guitar_player} plays for {", ".join(x for x in bands)}.'
        return f'Sorry, {guitar_player} does not seem to be a known guitarist.'
    return None


def check_band(db_manager, band_name):
    """Check if a band exits in the database

    Parameters:
        db_manager (DatabaseManager): the database's manager
        band_name (str): the name of the band
    """
    if not isinstance(db_manager, DatabaseManager):
        return
    if db_manager:
        guitarists = db_manager.get_band_guitarists(band_name)
        if guitarists:
            if len(guitarists) == 1:
                return f'The guitar hero of {band_name} is {guitarists[0]}.'
            return f'The guitar heroes of {band_name} are {", ".join(x for x in guitarists)}.'
        return f"Sorry, we don't know who is the guitar hero of {band_name}."
    return None
