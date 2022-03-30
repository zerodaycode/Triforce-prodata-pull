import datetime
import logging

from config import API_KEY, API_BASE_URL, LIVE_STATS_API

from utils.lolesport_utilities import get_valid_date as window_date, check_correct_response, unique_dicts
from Exceptions.lolesportsapi_exceptions import LoLEsportResponseError, LoLEsportStructureError
import requests

log = logging.getLogger(__name__)


class LoLEsportApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(API_KEY)
        self.default_language = "en-US"

    def set_default_language(self, language_code):
        # TODO implement language code error
        # TODO implement on class methods
        """Set a new default language

             Parameters
            ----------
            language_code : str
                The language code in which the information will be requested.
            """
        self.default_language = language_code

    def get_leagues(self, hl: str = "en-US") -> dict:
        """Retrieve leagues information (id, slug, name, region, image, priority, displayPriority).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US"

            Returns
             -------
            dict
                """
        response = self.session.get(
            API_BASE_URL + '/getLeagues',
            params={'hl': hl}
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_tournaments_for_league(self, hl: str = "en-US", league_id: int = None) -> dict:
        """Retrieve all splits/formats info for a given league (id, slug, startDate, endDate).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US"

            league_id: int (optional)
                The league ID of which splits will be requested. If not provided all tournaments for all leagues
                will be requested.

            Returns
             -------
            dict
            """
        response = self.session.get(
            API_BASE_URL + '/getTournamentsForLeague',
            params={
                'hl': hl,
                'leagueId': league_id
            }
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_standings(self, tournament_id, hl: str = "en-US"):
        """Retrieve the position splits/formats info for a given tournaments (id, slug, startDate, endDate).

                Parameters
                ----------
                hl : str
                    The language code in which the information will be requested. By default "en-US"

                tournament_id: int,int[] (Optional)
                    The tournament(s) ID(s) of which splits will be requested. If not provided all tournaments for
                     all leagues will be requested.

                Returns
                 -------
                dict
                """
        response = self.session.get(
            API_BASE_URL + '/getStandings',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_schedule(self, hl="en-US", league_id: int = None, pagetoken: str = None):
        """Retrieve the schedule for a given league (blockName, league(name, slug), match(flags,id,strategy,teams),
            startTime,state,type).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US".

            league_id:  int, optional
                The league(s) ID(s) of which schedule will be requested. If not provided all schedule for all leagues
                will be requested.

            pagetoken: str, optional
                Base 64 encoded string used to determine the next "page" of data to pull.

            Returns
             -------
            dict
        """
        response = self.session.get(
            API_BASE_URL + '/getSchedule',
            params={
                'hl': hl,
                'leagueId': league_id,
                'pageToken': pagetoken
            }
        )

        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_live(self, hl="en-US"):
        """Retrieve the current live matches

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US".

            Returns
             -------
            dict
        """
        response = self.session.get(
            API_BASE_URL + '/getLive',
            params={'hl': hl}
        )

        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_completed_events(self, hl="en-US", tournament_id=None):

        # TODO It seems data before summer 2019 isn't available, need more investigation

        """Get completed games for a tournament or last 300 completed games of all tournaments.
            DISCLAIMER ! Due to some inconsistency on the API, some tournaments don't return data.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default, "en-US".

            tournament_id: int (optional)
                The tournament(s) ID(s) of which splits will be requested. If not provided all tournaments for
                 all leagues will be requested.

            Returns
             -------
            dict
        """
        response = self.session.get(
            API_BASE_URL + '/getCompletedEvents',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )

        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_event_details(self, match_id, hl="en-US"):

        """Get information about a match metadata like league, teams, vods and who stream the game.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US".

            match_id: int,str
                The match(s) ID(s) of which information will be requested.


            Returns
             -------
            dict
        """

        response = self.session.get(
            API_BASE_URL + '/getEventDetails',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_games(self, hl="en-US", match_id=None):

        """Get information about a completed or unneeded match (id,number,state,vods).
            If match_id is not provided all games will be requested

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US".

            match_id: str, int (optional)
                The match_id(s) ID(s) of which information will be requested. If not provided all games for
                 all leagues will be requested.
                 Can be a single int, a string or a list of ids separate by coma(s) as a single string.

            Returns
             -------
            dict
        """
        response = self.session.get(
            API_BASE_URL + '/getGames',
            params={
                'hl': hl,
                'id': match_id
            }

        )

        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_teams(self, hl="en-US", team_identifier=None, only_active: bool = False):

        """Get information about a team a unneeded match (image,code,region,id,players,etc).
            If team_identifier is not provided all teams will be requested.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "en-US".

            team_identifier: str, id (optional)
                The team slug or id of which information will be requested.
                If team_slug is not provided all teams will be requested.

            only_active: bool (optional)
                True will return only teams with players and active

            Returns
             -------
            dict
        """
        response = self.session.get(
            API_BASE_URL + '/getTeams',
            params={
                'hl': hl,
                'id': team_identifier
            }
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            if only_active:
                teams = response.json()['data'].get("teams", None)
                if teams:
                    return {"teams": [team for team in teams if team["status"] == "active"]}
            return response.json()['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_window(self, game_id, valid_datetime=None):

        """Get information about a game, game stats (drakes, barons, etc) and players stats.

        Parameters
        ----------
        game_id : str
            The game id of which information will be requested.
        valid_datetime:
            A valid window time.

        Returns
         -------
        dict
    """
        if not valid_datetime:
            valid_datetime = window_date()
        response = self.session.get(
            LIVE_STATS_API + f'/window/{game_id}',
            params={
                'startingTime': window_date()
            }
        )

        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=True)
            if response.status_code == 204:
                return None
            else:
                return response.json()
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_details(self, game_id, participant_ids=None, valid_datetime=None):

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
        if not valid_datetime:
            valid_datetime = window_date()
        response = self.session.get(
            LIVE_STATS_API + f'/details/{game_id}',
            params={
                'startingTime': valid_datetime,
                'participantIds': participant_ids
            }
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=True)
            if response.status_code == 204:
                return None
            else:
                return response.json()
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_teams_for_tournament(self, tournament_id, hl="en-US", simplify_data_mode: bool = False):
        """
        Retrieve the list of participating teams in a tournament.
        If simplify_data_mode is False, teams will be separated by the phase
        in which they participate (quarterfinals, semifinals, etc.) and the result for that phase.

        Parameters
        ----------
        hl : str
            The language code in which the information will be requested. By default "en-US".

        tournament_id: str,int,int[] (Optional)
            The tournament(s) ID(s) of which splits will be requested.

        simplify_data_mode : bool (Optional)
            If true, the function only returns basic team information (id, name, slug, code, image)

        Returns
         -------
        dict
        """
        standings = self.get_standings(tournament_id=tournament_id, hl=hl)['standings']

        # Separate stages (Play-in, play-off, regular season, etc)
        stages = [stage for stages in standings for stage in stages['stages']]

        # Initialization of the dictionary that will contain the data with the custom format
        custom_stages = {'stages': []}

        for stage in stages:

            # Initialization of the stage dictionary
            stage_teams = {
                'name': stage['name'],
                'slug': stage['slug'],
                'type': stage['type'],
                'teams': []
            }

            # If the type of stage is group (for example a regular season) we process each team of the stage,
            # appending the position of the team on the competition and the group name to the team dictionary.
            # Once appended, the new information is appended to "teams" on the stage dictionary.
            if stage['type'] == "groups":
                for section in stage['sections']:
                    for position in section['rankings']:
                        for team in position['teams']:
                            team_dict = {
                                **team,
                                'group': section['name'],
                                'position': position['ordinal']
                            }
                            stage_teams['teams'].append(team_dict)

            # If the type of stage is bracket (for example a play-in phase) we process each match of the stage,
            # processing each team from those matches.
            # We extract the result of the team in that match, and relate it to the phase.
            # If the team is not yet in the stage dictionary, we add it,if it is already in the dictionary, we append
            # the match result to the "results" section of that team.
            elif stage['type'] == "bracket":
                for section in stage['sections']:
                    for match in section['matches']:
                        for team in match['teams']:

                            current_team = team

                            outcome = current_team.pop('result')
                            outcome = outcome['outcome'] if outcome else None

                            result = {'phase': section['name'], 'outcome': outcome}

                            if current_team['id'] == "0":
                                continue
                            elif current_team['id'] not in [team['id'] for team in stage_teams['teams']]:

                                team_dict = {
                                    **current_team,
                                    'results': [result]
                                }
                                stage_teams['teams'].append(team_dict)

                            else:

                                index_team = stage_teams['teams'].index(next(filter(lambda n:
                                                                                    n.get('id') == current_team['id'],
                                                                                    stage_teams['teams'])))
                                team_data = stage_teams['teams'].pop(index_team)

                                team_data['results'].append(result)

                                stage_teams['teams'].append(team_data)

            # Every processed stage is appended to the stage dictionary
            custom_stages['stages'].append(stage_teams)

        # If simplify_data_mode is True, the custom_stages dictionary is reprocessed to a new dictionary
        # to only return each team once with only 5 properties (id, name, slug, code, image)
        # Else the dictionary with all stages will be return
        if simplify_data_mode:
            teams_data_simplify = {'teams': []}
            for team in [team for stage in custom_stages['stages'] for team in stage['teams']]:
                team_dict = {
                    'id': team['id'],
                    'name': team['name'],
                    'slug': team['slug'],
                    'code': team['code'],
                    'image': team['image']
                }
                if team['id'] not in [team['id'] for team in teams_data_simplify['teams']]:
                    teams_data_simplify['teams'].append(team_dict)
            return teams_data_simplify
        else:
            return custom_stages

    def get_players(self, hl="en-US", team_identifier=None):

        """Get players for a team (id,summonerName,firstName,lastName,image,rol).
        If team_identifier is not provided all players will be requested, adding to the previous
        information to which team(s) the player belong(s).

            Parameters
            ----------
            hl : str
              The language code in which the information will be requested. By default "en-US".

            team_identifier: str, id (optional)
              The team slug or id of which information will be requested.
              If team_slug is not provided all teams will be requested.

            Returns
            -------
            dict
        """
        data = self.get_teams(hl=hl, team_identifier=team_identifier)

        # Removing placeholders team from the data
        data = [team for team in data['teams'] if
                (team['slug'] != "tbd" and team['name'] != "TBD") or team['id'] != "0"]

        # Initialization of the custom formatted dictionary
        players_dict = {'players': []}

        # Processing each player of each team on the retrieved data
        # Only players on active teams and who have a role in it will be added on the custom formatted dictionary.
        # The ID of the team to which the player belongs is added to his information.
        # the first time we add him to the dictionary means that he belongs to more than one team,
        # so we add the team's ID to the "teams" key of the player's information.
        for team in data:
            for player in team['players']:
                if team['status'] != "archived" and player['role'] != "none":
                    if player['id'] in [player['id'] for player in players_dict['players']]:
                        index_player = players_dict['players'].index(
                            next(filter(lambda n: n.get('id') == player['id'], players_dict['players'])))

                        player_data = players_dict['players'].pop(index_player)

                        player_data['teams'].append(team['id'])

                        players_dict['players'].append(player_data)
                    else:
                        custom_player_dict = {
                            **player,
                            'teams': [team['id']]
                        }
                        players_dict['players'].append(custom_player_dict)

        # If the user specify a team identifier, we remove the "teams" key from player's information
        if team_identifier:
            for player in players_dict['players']:
                player.pop('teams')

        return players_dict

    def get_live_games_info(self, only_ids: bool = False, hl="en-US"):

        live_data = self.get_live(hl=hl)['schedule']['events']

        live_games_data = {'games': []}

        # Processing matches in progress, discarding broadcasts without live games
        for match in [match for match in live_data if match['state'] == "inProgress" and match['type'] == 'match']:

            # Retrieve in progress game for the current iteration match
            in_progress_game = None
            for game in [game for game in match['match']['games'] if game['state'] == "inProgress"]:
                in_progress_game = game

            if not in_progress_game:
                continue

            # Retrieve previous completed games for the current iteration match
            previous_games = [game for game in match['match']['games'] if game['state'] == 'completed']

            # If there are completed games on the match, they are processed to retrieve their ID and game number.
            completed_games = []
            if previous_games:
                for game in previous_games:
                    game_data = {
                        'id': game['id'],
                        'number': game['number'],
                    }

                    completed_games.append(game_data)

            # Initialization of the custom formatted dictionary
            game_data_dict = {
                'match_id': match['id'],
                'game': {
                    'id': in_progress_game['id'],
                    'number': in_progress_game['number'],
                },
                'completedGames': completed_games,
                'blockName': match['blockName'],
                'type': match['match']['strategy']
            }

            # Removing unneeded data from league and adding the remaining info to the custom dictionary
            match['league'].pop('priority')
            match['league'].pop('displayPriority')

            game_data_dict['league'] = match['league']

            # Adding the tournament info to the custom dictionary
            # NOTE: We add this data now and not when initializing the custom dictionary so that the dictionary
            # is tidier and easier to read at a glance.
            game_data_dict['tournament'] = match['tournament']

            # Add team side to each team match dictionary, an add the result on the custom dictionary
            teams = []
            for team in in_progress_game['teams']:
                match_team_index = match['match']['teams'].index(next(filter(lambda n:
                                                                             n.get('id') == team['id'],
                                                                             match['match']['teams'])))

                match_team_dict = match['match']['teams'].pop(match_team_index)

                match_team_dict['side'] = team['side']

                teams.append(match_team_dict)

            game_data_dict['teams'] = teams

            live_games_data['games'].append(game_data_dict)

        if only_ids:
            return {'games': [game_info['game']['id'] for game_info in live_games_data['games']]}
        return live_games_data

    def get_window_details(self, game_id: str):
        valid_datetime = window_date()
        window = self.get_window(game_id, valid_datetime)
        details = self.get_details(game_id=game_id, valid_datetime=valid_datetime)

        return window, details

    @staticmethod
    def get_merged_window_details_frames(window, details):

        window['frames'] = unique_dicts(window['frames'], 'rfc460Timestamp')
        details['frames'] = unique_dicts(details['frames'], 'rfc460Timestamp')

        merged_window = {
            'frames': []
        }

        for i, window_frame in enumerate(window['frames']):
            players_details_frame = details['frames'][i]

            new_frame_dict = {
                'rfc460Timestamp': window_frame['rfc460Timestamp'],
                'gameState': window_frame['gameState']
            }

            if players_details_frame['rfc460Timestamp'] != window_frame['rfc460Timestamp']:
                log.warning(f"TimeStamp don't match.\r\n"
                            f"Details: {players_details_frame['rfc460Timestamp']}\r\n"
                            f"Window: {window_frame['rfc460Timestamp']}")

                log.warning(f"Window {window}")
                log.warning(f"Details {details}")
            else:
                for player in [player for player in window_frame['blueTeam']['participants']]:
                    [details_player] = list(filter(lambda n: n.get('participantId') == player['participantId'],
                                                   players_details_frame['participants']))

                    index_player = window_frame['blueTeam']['participants'].index(next(filter(lambda n:
                                                                                              n.get('participantId') ==
                                                                                              player['participantId'],
                                                                                              window_frame['blueTeam'][
                                                                                                  'participants'])))
                    window_frame['blueTeam']['participants'].pop(index_player)
                    window_frame['blueTeam']['participants'].append(details_player)

                for player in [player for player in window_frame['redTeam']['participants']]:
                    [details_player] = list(filter(lambda n: n.get('participantId') == player['participantId'],
                                                   players_details_frame['participants']))

                    index_player = window_frame['redTeam']['participants'].index(next(filter(lambda n:
                                                                                             n.get('participantId') ==
                                                                                             player['participantId'],
                                                                                             window_frame['redTeam'][
                                                                                                 'participants'])))
                    window_frame['redTeam']['participants'].pop(index_player)
                    window_frame['redTeam']['participants'].append(details_player)
                new_frame_dict['blue'] = window_frame['blueTeam']
                new_frame_dict['red'] = (window_frame['redTeam'])

            merged_window['frames'].append(new_frame_dict)

        return merged_window

    def get_tournaments_league_related(self, hl="en-US", league_id=None, mode="ongoing"):
        if not league_id:
            leagues = self.get_leagues(hl=hl)
            league_id = ",".join([league['id'] for league in leagues['leagues']])
        data = {
            'tournaments': []
        }
        today_date = datetime.datetime.utcnow().date()

        tournaments = self.get_tournaments_for_league(hl=hl, league_id=league_id)['leagues']
        for i, league in enumerate(leagues['leagues']):

            league.pop('priority')
            league.pop('displayPriority')

            for tournament in tournaments[i]['tournaments']:

                start_date = datetime.datetime.strptime(tournament['startDate'], '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(tournament['endDate'], '%Y-%m-%d').date()

                if mode == "ongoing" and not start_date <= today_date <= end_date:
                    continue

                if mode == "not_ended" and not today_date <= end_date:
                    continue

                tournament = {
                    'league': {**league},
                    **tournament
                }
                data['tournaments'].append(tournament)

        return data
