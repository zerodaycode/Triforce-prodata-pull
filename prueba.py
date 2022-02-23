import pprint
from time import sleep, time
from lolesportapi import LoLEsportApi

from utils.json_files_manipulation import load_data,save_data
import logging
log = logging.getLogger(__name__)


lcs_id = 98767991299243165
lcs_spring_2013 = 107620592294752774
lec_id = 98767991302996019
lfl_league = 105266103462388553
eu_2018_summer = 100205575629449176

lec_2019_summer = 102147201778412187
lec_2020_split1 = 103462459318635408
lec_summer_2020 = 104169295253189561
lec_2021_split1 = 105522958532258735
lec_2021_summer = 106269680921022418
lec_2022_spring = 107417059262120466

lcs_2019_summer = 102147201296669914
lcs_2020_split1 = 103462439438682788
lcs_summer_2020 = 104174992692075107
lcs_2021_lockin = 105522217230238828
lcs_2021 = 105658534671026792
mss_2021 = 105788932118361426
lcs_2022_lock_in = 107458335260330212
lcs_spring_2022 = 107458367237283414

api = LoLEsportApi()

def handle_livematches():
    while True:
        live_matches = api.get_live()
        for live_match in live_matches['schedule']['events']:

            if live_match['state'] == 'inProgress' and 'match' in live_match.keys():
                print(f"{live_match['match']['teams'][0]['code']} vs {live_match['match']['teams'][1]['code']}")

                get_games_match = api.get_event_details(live_match['id'])
                # save_data("LCK_get_event_details",get_games_match)
                get_live_game(get_games_match)

        sleep(60)


def get_live_game(games):
    for game in games['event']['match']['games']:
        if game['state'] == 'inProgress':
            current_game = api.get_window(game['id'])
            get_details_player(game)
            # save_data("LCK_get_window", current_game)
            # pprint.pprint(current_game)


def get_details_player(game):
    if game['state'] == 'inProgress':
        players_details = api.get_details(game['id'])
        print("HERE")
        # save_data("LCK_get_details", players_details)
        pprint.pprint(players_details)

def load_LCK_player_details():
    log.info("Firing load_LCK_player_details()")
    return load_data("json_examples","LCK_get_details")


