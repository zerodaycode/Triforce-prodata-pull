import logging
from time import sleep

from utils.postgres_db import Database
from lolesportapi import LoLEsportApi

log = logging.getLogger(__name__)


class TriforceUpdater:

    def __init__(self, update_interval=None):
        self.update_interval = update_interval
        self.last_completed_update = None
        self.next_planned_update = None
        self.database = Database("triforce")

    @staticmethod
    def leagues_to_sql(json):
        leagues_sql_formatted = []
        for league in json['leagues']:
            league_ext_id = league['id']
            league_slug = league['slug']
            league_name = league['name']
            league_region = league['region']
            league_image_url = league['image']

            values = [league_ext_id, league_slug, league_name, league_region, league_image_url]

            leagues_sql_formatted.append(values)

        return leagues_sql_formatted

    @staticmethod
    def tournaments_to_sql(json, leagues_db_rows):
        tournaments_sql_formatted = []
        for tournament in json['tournaments']:

            # Retrieve related league
            league_dict = next((league for league in leagues_db_rows
                                if league["ext_id"] == int(tournament["league"]["id"])), None)

            if not league_dict:
                league_dict = {}
                log.warning(f"Tournament without league reference include: {tournament}"
                            f"\r\nleagues info: {leagues_db_rows}")

            tournament_ext_id = tournament['id']
            tournament_slug = tournament['slug']
            tournament_start_date = tournament['startDate']
            tournament_end_date = tournament['endDate']
            tournament_league = league_dict.get("id", None)

            values = [tournament_ext_id, tournament_slug, tournament_start_date, tournament_end_date, tournament_league]

            tournaments_sql_formatted.append(values)

        return tournaments_sql_formatted

    @staticmethod
    def teams_to_sql(teams_json: dict, leagues_db_rows):
        teams_sql_formatted = []
        for team in teams_json['teams']:

            # Retrieve related league
            league_dict = next((league for league in leagues_db_rows
                                if (team["homeLeague"] and league["name"] == team["homeLeague"]["name"])), None)

            if not league_dict:
                league_dict = {}
                log.warning(f"team without league reference include: {team}\nleagues info: {leagues_db_rows}")

            team_ext_id = team['id']
            team_slug = team['slug']
            team_name = team['name']
            team_code = team['code']
            team_image_url = team['image']
            team_alt_image_url = team['alternativeImage']
            team_bg_image_url = team['backgroundImage']
            team_home_league = league_dict.get("id", None)
            values = [team_ext_id, team_slug, team_name, team_code, team_image_url,
                      team_alt_image_url, team_bg_image_url, team_home_league]

            teams_sql_formatted.append(values)

        return teams_sql_formatted

    @staticmethod
    def players_to_sql(players_json: dict):
        players_sql_formatted = []
        for player in players_json['players']:
            player_ext_id = player['id']
            player_fn = player['firstName']
            player_ln = player['lastName']
            player_sn = player['summonerName']
            player_in = player['image']
            player_role = player['role']

            values = [player_ext_id, player_fn, player_ln, player_sn, player_in, player_role]

            players_sql_formatted.append(values)

        return players_sql_formatted

    @staticmethod
    def teams_players_relation_to_sql(players_json, players_sql, teams_sql):
        teams_players_relation_sql_formatted = []

        for player in players_json['players']:
            player_in_db = next((p_db for p_db in players_sql
                                 if p_db["ext_id"] == int(player["id"])), None)
            if not player_in_db:
                log.warning(f"Didnt find the player on db: {player}\nplayers db info info: {players_sql}")
            for team in player["teams"]:
                team_in_db = next((t_db for t_db in teams_sql
                                   if t_db["ext_id"] == int(team)), None)
                if not team_in_db:
                    log.warning(f"Didnt find the team on db: {team}\nTeam db info info: {teams_sql}")
                team_id = team_in_db['id']
                player_id = player_in_db['id']

                values = [team_id, player_id]

                teams_players_relation_sql_formatted.append(values)

        return teams_players_relation_sql_formatted

    def update_leagues_table(self, rows_to_insert):
        self.database.insert_rows("leagues",
                                  ["ext_id", "slug", "name", "region", "image_url"],
                                  rows_to_insert)

    def get_leagues_table_rows(self):
        leagues_results = self.database.get("leagues")
        leagues_database_rows_dict = []
        for league in leagues_results:
            league_dict = {
                "id": league[0],
                "ext_id": league[1],
                "slug": league[2],
                "name": league[3],
                "region": league[4],
                "image_url": league[5]
            }
            leagues_database_rows_dict.append(league_dict)

        return leagues_database_rows_dict

    def update_tournaments_table(self, rows_to_insert):
        self.database.insert_rows("tournaments",
                                  ["ext_id", "slug", "start_date", "end_date", "league"],
                                  rows_to_insert)

    def update_teams_table(self, rows_to_insert):
        self.database.insert_rows("teams",
                                  ["ext_id", "slug", "name", "code",
                                   "image_url", "alt_image_url", "bg_image_url", "home_league"],
                                  rows_to_insert)

    def get_teams_table_rows(self):
        teams_results = self.database.get("teams")
        teams_database_rows_dict = []
        for team in teams_results:
            team_dict = {
                "id": team[0],
                "ext_id": team[1],
                "slug": team[2],
                "code": team[3],
                "image_url": team[4],
                "alt_image_url": team[5],
                "bg_image_url": team[6],
                "league_id": team[7]
            }
            teams_database_rows_dict.append(team_dict)

        return teams_database_rows_dict

    def update_players_table(self, rows_to_insert):
        self.database.insert_rows("players",
                                  ["ext_id", "first_name", "last_name", "summoner_name", "image_url", "role"],
                                  rows_to_insert)

    def get_players_table_rows(self):
        players_results = self.database.get("players")
        players_database_rows_dict = []
        for player in players_results:
            player_dict = {
                "id": player[0],
                "ext_id": player[1],
                "first_name": player[2],
                "last_name": player[3],
                "summoner_name": player[4],
                "image_url": player[5],
                "role": player[6]
            }
            players_database_rows_dict.append(player_dict)

        return players_database_rows_dict

    def update_teams_players_table(self, rows_to_insert):
        self.database.insert_rows("teams_players",
                                  ["team_id", "player_id"],
                                  rows_to_insert)

    def update_triforce(self, api: LoLEsportApi):
        a = self.update_interval

        api_leagues_dict = api.get_leagues()
        sleep(1)
        api_tournaments_dict = api.get_tournaments_league_related(mode="not_ended")
        sleep(1)
        api_teams_dict = api.get_teams(only_active=True)
        sleep(1)
        api_players_dict = api.get_players()
        sleep(1)
        # Riot api leagues data to SQL insert query
        leagues_sql_formatted = self.leagues_to_sql(api_leagues_dict)

        # Inserting leagues on db and retrieve the rows inserted for future operations
        self.update_leagues_table(leagues_sql_formatted)

        leagues_table_rows = self.get_leagues_table_rows()

        # Riot api tournaments data to SQL insert query
        tournaments_sql_formatted = self.tournaments_to_sql(api_tournaments_dict,
                                                            leagues_table_rows)
        # Inserting tournaments on db
        self.update_tournaments_table(tournaments_sql_formatted)

        # Riot api teams data to SQL insert query
        teams_sql_formatted = self.teams_to_sql(api_teams_dict,
                                                leagues_table_rows)

        # Inserting teams on db and retrieve the rows inserted for future operations
        self.update_teams_table(teams_sql_formatted)

        teams_table_rows = self.get_teams_table_rows()

        # Riot api players data to SQL insert query
        players_sql_formatted = self.players_to_sql(api_players_dict)

        # Inserting teams on db and retrieve the rows inserted for future operations
        self.update_players_table(players_sql_formatted)

        players_table_rows = self.get_players_table_rows()

        # Players-teams relation to SQL insert query
        players_team_relation_sql_formatted = self.teams_players_relation_to_sql(api_players_dict,
                                                                                 players_table_rows,
                                                                                 teams_table_rows)

        # Inserting players-teams relation on db
        self.update_teams_players_table(players_team_relation_sql_formatted)
