import logging

from config import API_KEY, API_BASE_URL, LIVE_STATS_API, LANGUAGE_CODES

from utils.lolesport_utilities import get_valid_date as window_date, check_correct_response
from Exceptions.lolesportsapi_exceptions import LoLEsportResponseError, LoLEsportStructureError
import json
import requests

log = logging.getLogger(__name__)


class LoLEsportApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(API_KEY)
        self.default_language = "es-ES"

    def set_default_language(self, language_code):
        # TODO implement language code error
        """Set a new default language

             Parameters
            ----------
            language_code : str
                The language code in which the information will be requested.
            """
        self.default_language = language_code

    def get_leagues(self, hl: str = 'es-ES') -> dict:
        """Retrieve leagues information (id, slug, name, region, image, priority, displayPriority).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES"

            Returns
             -------
            dict
                If the status code of the request is 200, the dictionary will have the following
                structure (keep in mind than multiple dictionary with the same structure are expected on the array level)::

                    {
                        'leagues': [
                            {
                            'id': (str)(no-empty) 'The name of the league',
                            'slug': 'URL friendly version of the league's name',
                            'name': 'The name of the league',
                            'region': 'EUROPA',
                            'image': 'URL to an image of the League's logo',
                            'priority': int,
                            'displayPriority': {
                                'position': int,
                                'status': 'Unknown value definition'
                                }
                            },
                            id': 'The league's ID',
                            'slug': 'URL friendly version of the league's name',
                            'name': 'The name of the league',
                            'region': 'EUROPA',
                            'image': 'URL to an image of the League's logo',
                            'priority': int,
                            'displayPriority': {
                                'position': int,
                                'status': 'Unknown value definition'
                                }
                            },
                            ...
                        ]

                    }

                Else (the status code of the request isn't 200) the dictionary will have the following structure::
                    {
                        'errors': [{
                            'message': 'Error message'
                            }]
                    }
                """
        response = self.session.get(
            API_BASE_URL + '/getLeagues',
            params={'hl': hl}
        )
        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_tournaments_for_league(self, hl: str = 'es-ES', league_id: int = None) -> dict:
        """Retrieve all splits/formats info for a given league (id, slug, startDate, endDate).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES"

            league_id: int (optional)
                The league ID of which splits will be requested. If not provided all tournaments for all leagues
                will be requested.

            Returns
             -------
            dict
                If the status code of the request is 200 and league ID exist, the dictionary will have the
                following structure (keep in mind than multiple dictionary with the same structure are expected on the
                array level)::

                    {
                       'leagues': [{
                            'tournaments': [
                                {
                                    'id': 'Tournament id',
                                    'slug': 'URL friendly name of the tournament',
                                    'startDate': 'Date the tournament start/started with format yyyy-mm-dd'
                                    'endDate': 'Date the tournament end/ended yyyy-mm-dd'
                                },
                                {
                                    'id': 'Tournament id',
                                    'slug': 'URL friendly name of the tournament',
                                    'startDate': 'Date the tournament start/started with format yyyy-mm-dd'
                                    'endDate': 'Date the tournament end/ended yyyy-mm-dd'
                                }.
                                ...
                            ]}

                    }

                If the status code of the request is 200 and the league ID doesn't exist, the value for the key "leagues"
                will be an empty array::
                    {'leagues': []}

                Else (the status code of the request isn't 200) the dictionary will have the following structure::
                    {
                        'errors': [{
                            'message': 'Error message'
                            }]
                    }
            """
        response = self.session.get(
            API_BASE_URL + '/getTournamentsForLeague',
            params={
                'hl': hl,
                'leagueId': league_id
            }
        )
        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_standings(self, tournament_id, hl: str = 'es-ES'):
        """Retrieve the position splits/formats info for a given league (id, slug, startDate, endDate).

                Parameters
                ----------
                hl : str
                    The language code in which the information will be requested. By default "es-ES"

                tournament_id: int,int[] (Optional)
                    The tournament(s) ID(s) of which splits will be requested. If not provided all tournaments for
                     all leagues will be requested.

                Returns
                 -------
                dict
                    If the status code of the request is 200 and league ID exist, the dictionary will have the
                    following structure (keep in mind than multiple dictionary with the same structure are expected on the
                    array level)::

                        {
                           'leagues': [{
                                'tournaments': [
                                    {
                                        'id': 'Tournament id',
                                        'slug': 'URL friendly name of the tournament',
                                        'startDate': 'Date the tournament start/started with format yyyy-mm-dd'
                                        'endDate': 'Date the tournament end/ended yyyy-mm-dd'
                                    },
                                    {
                                        'id': 'Tournament id',
                                        'slug': 'URL friendly name of the tournament',
                                        'startDate': 'Date the tournament start/started with format yyyy-mm-dd'
                                        'endDate': 'Date the tournament end/ended yyyy-mm-dd'
                                    }.
                                    ...
                                ]}

                        }

                    If the status code of the request is 200 and the league ID doesn't exist,
                    the value for the key "leagues" will be an empty array::
                        {'leagues': []}

                    Else (the status code of the request isn't 200) the dictionary will have the following structure::
                        {
                            'errors': [{
                                'message': 'Error message'
                                }]
                        }
                """
        response = self.session.get(
            API_BASE_URL + '/getStandings',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )
        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_schedule(self, hl='es-ES', league_id: int = None, pageToken: str = None):
        """Retrieve the schedule for a given league (blockName, league(name, slug), match(flags,id,strategy,teams),
            startTime,state,type).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            league_id:  int, optional
                The league(s) ID(s) of which schedule will be requested. If not provided all schedule for all leagues
                will be requested.

            pageToken: str, optional
                Base 64 encoded string used to determine the next "page" of data to pull.

            Returns
             -------
            dict
                If the status code of the request is 200 and league ID exist, the dictionary will have the
                following structure (keep in mind than multiple dictionary with the same structure are expected on the
                array level)::

                    {
                    'schedule':
                        {'events':
                            [
                                {
                                'blockName': 'Section/Black name',
                                'league': {
                                        'name': 'League  name',
                                        'slug': 'URL friendly name of the league'
                                         },
                                'match': {
                                        'flags': [],
                                        'id': 'Match ID',
                                        'strategy': {'count': (int) total match of the serie,
                                                    'type': 'Type of game example "bestOf"'},
                                        'teams': [{'code': 'Team short name',
                                                   'image': 'URL team logo',
                                                   'name': 'Team full name',
                                                  'record': {'losses': (int) Number of defeats,
                                                              'wins': (int) Number of victories},
                                                   'result': {'gameWins': (int) games win,
                                                              'outcome': 'win or loss'}}]},
                                                  {'code': 'Team short name',
                                                   'image': 'URL team logo',
                                                   'name': 'Team full name',
                                                   'record': {'losses': (int) Number of defeats,
                                                              'wins': (int) Number of victories},
                                                   'result': {'gameWins': (int) games win,
                                                              'outcome': 'win or loss'}}]},
                              'startTime': 'YYYY-MM-DDTHH:mm:ssZ',
                              'state': 'State of de match',
                              'type': 'match'}
                    }


                If the status code of the request is 200 and the league ID doesn't exist, the value for the key "leagues"
                will be an empty array::
                    {'schedule': {'events': [], 'pages': {'newer': None, 'older': None}}}

        """
        response = self.session.get(
            API_BASE_URL + '/getSchedule',
            params={
                'hl': hl,
                'leagueId': league_id,
                'pageToken': pageToken
            }
        )

        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_live(self, hl='es-ES'):
        """Retrieve the current live matches

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            Returns
             -------
            dict
                Example of a correct response::
            {
                    'schedule':
                        {'events':
                            [
                                {'blockName': 'Semana 4',
                              'id': '107439320898324934',
                              'league': {'displayPriority': {'position': 17,
                                                             'status': 'not_selected'},
                                         'id': '105709090213554609',
                                         'image': 'http://static.lolesports.com/leagues/lco-color-white.png',
                                         'name': 'LCO',
                                         'priority': 207,
                                         'slug': 'lco'},
                              'match': {'games': [{'id': '107439320898324935',
                                                   'number': 1,
                                                   'state': 'inProgress',
                                                   'teams': [{'id': '98767991921462763',
                                                              'side': 'blue'},
                                                             {'id': '101383792891050518',
                                                              'side': 'red'}],
                                                   'vods': []}],
                                        'id': '107439320898324934',
                                        'strategy': {'count': 1, 'type': 'bestOf'},
                                        'teams': [{'code': 'DW',
                                                   'id': '98767991921462763',
                                                   'image': 'http://static.lolesports.com/teams/direwolves.png',
                                                   'name': 'Dire Wolves',
                                                   'record': {'losses': 5,
                                                              'wins': 2},
                                                   'result': {'gameWins': 0,
                                                              'outcome': None},
                                                   'slug': 'dire-wolves'},
                                                  {'code': 'GRV',
                                                   'id': '101383792891050518',
                                                   'image': 'http://static.lolesports.com/teams/gravitas-logo.png',
                                                   'name': 'Gravitas',
                                                   'record': {'losses': 6,
                                                              'wins': 1},
                                                   'result': {'gameWins': 0,
                                                              'outcome': None},
                                                   'slug': 'gravitas'}]},
                              'startTime': '2022-02-15T09:00:00Z',
                              'state': 'inProgress',
                              'streams': [{'countries': ['AU', 'NZ'],
                                           'locale': 'en-AU',
                                           'offset': -200000,
                                           'parameter': 'lco',
                                           'provider': 'twitch'}],
                              'tournament': {'id': '107439320897210747'},
                              'type': 'match'}
                              ]
                    }
        """
        response = self.session.get(
            API_BASE_URL + '/getLive',
            params={'hl': hl}
        )

        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_completed_events(self, hl='es-ES', tournament_id=None):

        # TODO It seems data before summer 2019 isn't available, need more investigation

        """Get completed games for a tournament or last 300 completed games of all tournaments.
            DISCLAIMER ! Due to some inconsistency on the API, some tournaments don't return data.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            tournament_id: int (optional)
                The tournament(s) ID(s) of which splits will be requested. If not provided all tournaments for
                 all leagues will be requested.

            Returns
             -------
            dict
                Example of a correct response::
            {
                    'schedule': { 'events': [{'blockName': 'Semana 1',
                                  'games': [{'id': '104169295283008519',
                                             'vods': [{'parameter': 'f93tqKrcDqA'}]}],
                                  'league': {'name': 'LEC'},
                                  'match': {'id': '104169295283008518',
                                            'strategy': {'count': 1, 'type': 'bestOf'},
                                            'teams': [{'code': 'G2',
                                                       'image': 'http://static.lolesports.com/teams/G2-FullonDark.png',
                                                       'name': 'G2 Esports',
                                                       'result': {'gameWins': 1}},
                                                      {'code': 'MAD',
                                                       'image': 'http://static.lolesports.com/teams/1631819614211_mad-2021-worlds.png',
                                                       'name': 'MAD Lions',
                                                       'result': {'gameWins': 0}}],
                                            'type': 'normal'},
                                  'startTime': '2020-06-12T16:00:00Z'}
                            ]
                    }
        """
        response = self.session.get(
            API_BASE_URL + '/getCompletedEvents',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )

        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_event_details(self, match_id, hl='es-ES'):

        """Get information about a match metadata like league, teams, vods and who stream the game.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            match_id: int,str
                The match(s) ID(s) of which information will be requested.


            Returns
             -------
            dict
                Example of a correct response::
                {'event': {'id': '107468370561257634',
               'league': {'id': '105266103462388553',
                          'image': 'http://static.lolesports.com/leagues/LFL_Logo_2020_black1.png',
                          'name': 'La Ligue Française',
                          'slug': 'lfl'},
               'match': {'games': [{'id': '107468370561257635',
                                    'number': 1,
                                    'state': 'completed',
                                    'teams': [{'id': '105514907449611976',
                                               'side': 'blue'},
                                              {'id': '105515345386578249',
                                               'side': 'red'}],
                                    'vods': []}],
                         'strategy': {'count': 1},
                         'teams': [{'code': 'BDSA',
                                    'id': '105514907449611976',
                                    'image': 'http://static.lolesports.com/teams/1641944663689_bdslogo.png',
                                    'name': 'Team BDS Academy',
                                    'result': {'gameWins': 1}},
                                   {'code': 'SLY',
                                    'id': '105515345386578249',
                                    'image': 'http://static.lolesports.com/teams/LFL-SLY-logo.png',
                                    'name': 'Solary',
                                    'result': {'gameWins': 0}}]},
               'streams': [{'countries': [],
                            'locale': 'en-US',
                            'offset': -330000,
                            'parameter': 'northernarena',
                            'provider': 'twitch'},
                           {'countries': ['FR', 'CA'],
                            'locale': 'fr-FR',
                            'offset': -330000,
                            'parameter': 'otplol_',
                            'provider': 'twitch'}],
               'tournament': {'id': '107468370558963709'},
               'type': 'match'}}
        """

        response = self.session.get(
            API_BASE_URL + '/getEventDetails',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_games(self, hl='es-ES', match_id=None):

        """Get information about a completed or unneeded match (id,number,state,vods).
            If match_id is not provided all games will be requested

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            match_id: str, int (optional)
                The match_id(s) ID(s) of which information will be requested. If not provided all games for
                 all leagues will be requested.
                 Can be a single int, a string or a list of ids separate by coma(s) as a single string.

            Returns
             -------
            dict
                Example of a correct response::

                "games": [
                 {
                        "id": "100783238203695975",
                        "state": "completed",
                        "number": 1,
                        "vods": [
                            {
                                "locale": "cs-CZ",
                                "parameter": "FEIM1zlXcmI",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "de-DE",
                                "parameter": "k9zS682mNdI",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "en-US",
                                "parameter": "Vay2YGGv9CI",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "es-ES",
                                "parameter": "ofVeoAFHu38",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "es-MX",
                                "parameter": "lE_jtAbTnPM",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "fr-FR",
                                "parameter": "o28d5oPmQEw",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "it-IT",
                                "parameter": "Zxkw89qlIjc",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "pt-BR",
                                "parameter": "9DypUVTPjz0",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "ru-RU",
                                "parameter": "kmNwqpLlheI",
                                "provider": "youtube",
                                "offset": 0
                            },
                            {
                                "locale": "tr-TR",
                                "parameter": "8qiFpEugwio",
                                "provider": "youtube",
                                "offset": 0
                            }
                        ]
                    }
                ]
        """
        response = self.session.get(
            API_BASE_URL + '/getGames',
            params={
                'hl': hl,
                'id': match_id
            }

        )

        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_teams(self, hl='es-ES', team_slug=None):

        """Get information about a team a unneeded match (image,code,region,id,players,etc).
            If team_slug is not provided all teams will be requested.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            team_slug: str (optional)
                The team_slug of which information will be requested.
                If team_slug is not provided all teams will be requested.

            Returns
             -------
            dict
                Example of a correct response::

              {'teams': [{'alternativeImage': 'http://static.lolesports.com/teams/1592589079402_T1T1-03-SingleonLight.png',
                'backgroundImage': 'http://static.lolesports.com/teams/1596305556675_T1T1.png',
                'code': 'T1',
                'homeLeague': {'name': 'LCK', 'region': 'COREA'},
                'id': '98767991853197861',
                'image': 'http://static.lolesports.com/teams/1631819523085_t1-2021-worlds.png',
                'name': 'T1',
                'players': [{'firstName': 'Sanghyeok',
                             'id': '98767991747728851',
                             'image': 'http://static.lolesports.com/players/1642154893872_T1_Faker_F.png',
                             'lastName': 'Lee',
                             'role': 'mid',
                             'summonerName': 'Faker'},
                            {'firstName': 'Minhyung',
                             'id': '103495716775975785',
                             'image': 'http://static.lolesports.com/players/1642154901155_T1_Gumayusi_F.png',
                             'lastName': 'Lee',
                             'role': 'bottom',
                             'summonerName': 'Gumayusi'},
                            {'firstName': 'HYUNJUN',
                             'id': '105320682452092471',
                             'image': 'http://static.lolesports.com/players/1642154916489_T1_Oner_F.png',
                             'lastName': 'MUN',
                             'role': 'jungle',
                             'summonerName': 'Oner'},
                            {'firstName': 'Minseok',
                             'id': '103495716561790834',
                             'image': 'http://static.lolesports.com/players/1642154909657_T1_Keria_F.png',
                             'lastName': 'Ryu',
                             'role': 'support',
                             'summonerName': 'Keria'},
                            {'firstName': 'Taeki',
                             'id': '100205573453110710',
                             'image': 'http://static.lolesports.com/players/1642154884897_T1_Asper_F.png',
                             'lastName': 'Kim',
                             'role': 'support',
                             'summonerName': 'Asper'},
                            {'firstName': 'Wooje',
                             'id': '105320680474347057',
                             'image': 'http://static.lolesports.com/players/1642154923328_T1_Zeus_F.png',
                             'lastName': 'Choi',
                             'role': 'top',
                             'summonerName': 'Zeus'}],
                'slug': 't1',
                'status': 'active'}

                ]}
        """
        response = self.session.get(
            API_BASE_URL + '/getTeams',
            params={
                'hl': hl,
                'id': team_slug
            }
        )

        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_window(self, game_id):

        """Get information about a game, game stats (drakes, barons, etc) and players stats.

        Parameters
        ----------
        game_id : str
            The game id of which information will be requested.

        Returns
         -------
        dict
    """
        response = self.session.get(
            LIVE_STATS_API + f'/window/{game_id}',
            params={
                'startingTime': window_date()
            }
        )

        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=True)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")

    def get_details(self, game_id, participant_ids=None):

        """Get information about a player(s) on a game.
            Parameters
            ----------

            game_id : str
                The game id of which information will be requested.

            participant_ids : str, int, int[] (Optional)
                The participant(s) id of which information will be requested.
                Must be an int, string or list of int

            Returns
            -------
            dict
        """
        if type(participant_ids) == list:
            if all(isinstance(x, int) for x in participant_ids):
                participant_ids = "_".join(participant_ids)
            else:
                pass
                # TODO Error type not valid

        response = self.session.get(
            LIVE_STATS_API + f'/details/{game_id}',
            params={
                'startingTime': window_date(),
                'participantIds': participant_ids
            }
        )
        try:
            log.debug(f"Response content: {response.json()}")
            check_correct_response(response, live_stats_data=True)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError) as error:
            log.exception(f"Error on LoLEsport API response. Response: {response.json()}")
