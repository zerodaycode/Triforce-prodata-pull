import logging

from config import API_KEY, API_BASE_URL, LIVE_STATS_API

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
        # TODO implement on class methods
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
                """
        response = self.session.get(
            API_BASE_URL + '/getLeagues',
            params={'hl': hl}
        )
        try:
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=False)
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_standings(self, tournament_id, hl: str = 'es-ES'):
        """Retrieve the position splits/formats info for a given tournaments (id, slug, startDate, endDate).

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_schedule(self, hl='es-ES', league_id: int = None, pagetoken: str = None):
        """Retrieve the schedule for a given league (blockName, league(name, slug), match(flags,id,strategy,teams),
            startTime,state,type).

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_live(self, hl='es-ES'):
        """Retrieve the current live matches

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_completed_events(self, hl='es-ES', tournament_id=None):

        # TODO It seems data before summer 2019 isn't available, need more investigation

        """Get completed games for a tournament or last 300 completed games of all tournaments.
            DISCLAIMER ! Due to some inconsistency on the API, some tournaments don't return data.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default, "es-ES".

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_teams(self, hl='es-ES', team_identifier=None):

        """Get information about a team a unneeded match (image,code,region,id,players,etc).
            If team_identifier is not provided all teams will be requested.

            Parameters
            ----------
            hl : str
                The language code in which the information will be requested. By default "es-ES".

            team_identifier: str, id (optional)
                The team slug or id of which information will be requested.
                If team_slug is not provided all teams will be requested.

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
            return json.loads(response.text)['data']
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

    def get_teams_for_tournament(self, tournament_id, hl='es-ES', simplify_data_mode: bool = False):
        """
        Retrieve the list of participating teams in a tournament.
        If simplify_data_mode is False, teams will be separated by the phase
        in which they participate (quarterfinals, semifinals, etc.) and the result for that phase.

        Parameters
        ----------
        hl : str
            The language code in which the information will be requested. By default "es-ES".

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

    def get_players(self, hl='es-ES', team_identifier=None):

        """Get players for a team (id,summonerName,firstName,lastName,image,rol).
        If team_identifier is not provided all players will be requested, adding to the previous
        information to which team(s) the player belong(s).

            Parameters
            ----------
            hl : str
              The language code in which the information will be requested. By default "es-ES".

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
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=True)
            return json.loads(response.text)
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")

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
            log.debug(f"Response content: {response.text}")
            check_correct_response(response, live_stats_data=True)
            return json.loads(response.text)
        except (LoLEsportResponseError, LoLEsportStructureError):
            log.exception(f"Error on LoLEsport API response. Response: {response.text}")
