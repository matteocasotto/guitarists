def check_guitarist(db_manager, guitar_player):
    if db_manager:
        bands = db_manager.get_guitarist_bands(guitar_player)
        if bands:
            if len(bands) == 1:
                return f'{guitar_player} plays for {bands[0]}.'
            return f'{guitar_player} plays for {", ".join(x for x in bands)}.'
        return f'Sorry, {guitar_player} does not seem to be a known guitarist.'
    return None


def check_band(db_manager, band_name):
    if db_manager:
        guitarists = db_manager.get_band_guitarists(band_name)
        if guitarists:
            if len(guitarists) == 1:
                return f'The guitar hero of {band_name} is {guitarists[0]}.'
            return f'The guitar hero of {band_name} are {", ".join(x for x in guitarists)}.'
        return f"Sorry, we don't know who is the guitar hero of {band_name}."
    return None
