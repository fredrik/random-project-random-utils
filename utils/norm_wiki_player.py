from sports.models import Player
from utils.fifa_country_codes import codes_to_names

names_to_codes = dict((val, key) for key, val in codes_to_names)


# DUPE CODES!

def norm_position(pos):
    trans = dict((v, k) for k, v in Player.POSITION_CHOICES)
    return trans.get(pos) or pos


def normalise_wiki_player_data(player):
    """
    Takes data scraped from wikipedia player table, and parses/normalises
    it for consistancy

    Keys in resulting dictionary should match those in Player model.
    """
    norm_data = {}

    norm_data['name'] = player.get('name', '')
    norm_data['number'] = player.get('squad_no') or None
    player_wiki = player.get('wiki_title')
    if not player_wiki or player_wiki.endswith('(page does not exist)'):
        player_wiki = ''
    norm_data['wiki'] = player_wiki
    player_position = player.get('position')
    if player_position:
        player_position = norm_position(player_position)
    norm_data['position'] = player_position

    return norm_data
