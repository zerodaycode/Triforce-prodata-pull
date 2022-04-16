import logging

from utils.postgres_db import Database
from lolesportapi import LoLEsportApi
import triforce_support.db_triforce_utils as triforce_utils

log = logging.getLogger(__name__)


class TriforceUpdater:

    def __init__(self, db_is_remote: bool, enable_backup: bool):
        self.last_completed_update = None
        self.next_planned_update = None
        self.db_is_remote = db_is_remote
        self.enable_backup = enable_backup
        self.database = Database("triforce")

    def update_leagues_table(self, rows_to_insert):
        self.database.insert_rows("league",
                                  ["ext_id", "slug", "name", "region", "image_url"],
                                  rows_to_insert)

    def get_leagues_table_rows(self):
        leagues_results = self.database.get("league")
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
        self.database.insert_rows("tournament",
                                  ["ext_id", "slug", "start_date", "end_date", "league"],
                                  rows_to_insert)

    def update_teams_table(self, rows_to_insert):
        self.database.insert_rows("team",
                                  ["ext_id", "slug", "name", "code",
                                   "image_url", "alt_image_url", "bg_image_url", "home_league"],
                                  rows_to_insert)

    def get_teams_table_rows(self):
        teams_results = self.database.get("team")
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
        self.database.insert_rows("player",
                                  ["ext_id", "first_name", "last_name", "summoner_name", "image_url", "role"],
                                  rows_to_insert)

    def get_players_table_rows(self):
        players_results = self.database.get("player")
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
        self.database.insert_rows("team_player",
                                  ["team_id", "player_id"],
                                  rows_to_insert)

    def truncate_triforce_tables(self):
        self.database.query("TRUNCATE league, tournament, team, player, team_player RESTART IDENTITY;")

    def update_triforce(self, api: LoLEsportApi):

        if self.enable_backup:
            db_backup_name = triforce_utils.create_backup_db(remote_host=self.db_is_remote)

        api_leagues_dict = api.get_leagues()

        api_tournaments_dict = api.get_tournaments_league_related(mode="not_ended")

        api_teams_dict = api.get_teams(only_active=True)

        api_players_dict = api.get_players()

        # Truncate all data on tables
        self.truncate_triforce_tables()

        # Riot api leagues data to SQL insert query
        leagues_sql_formatted = triforce_utils.leagues_to_sql(api_leagues_dict)

        # Inserting leagues on db and retrieve the rows inserted for future operations
        try:
            self.update_leagues_table(leagues_sql_formatted)

            leagues_table_rows = self.get_leagues_table_rows()
        except:
            if self.enable_backup:
                triforce_utils.restore_data_from_backup(backup_name=db_backup_name, remote_host=self.db_is_remote)

        # Riot api tournaments data to SQL insert query
        tournaments_sql_formatted = triforce_utils.tournaments_to_sql(api_tournaments_dict,
                                                                      leagues_table_rows)
        # Inserting tournaments on db
        try:
            self.update_tournaments_table(tournaments_sql_formatted)
        except:
            if self.enable_backup:
                triforce_utils.restore_data_from_backup(backup_name=db_backup_name, remote_host=self.db_is_remote)

        # Riot api teams data to SQL insert query
        teams_sql_formatted = triforce_utils.teams_to_sql(api_teams_dict,
                                                          leagues_table_rows)

        # Inserting teams on db and retrieve the rows inserted for future operations
        try:
            self.update_teams_table(teams_sql_formatted)

            teams_table_rows = self.get_teams_table_rows()
        except:
            if self.enable_backup:
                triforce_utils.restore_data_from_backup(backup_name=db_backup_name, remote_host=self.db_is_remote)

        # Riot api players data to SQL insert query
        players_sql_formatted = triforce_utils.players_to_sql(api_players_dict)

        # Inserting teams on db and retrieve the rows inserted for future operations
        try:
            self.update_players_table(players_sql_formatted)

            players_table_rows = self.get_players_table_rows()
        except:
            if self.enable_backup:
                triforce_utils.restore_data_from_backup(backup_name=db_backup_name, remote_host=self.db_is_remote)

        # Players-teams relation to SQL insert query
        players_team_relation_sql_formatted = triforce_utils.teams_players_relation_to_sql(api_players_dict,
                                                                                           players_table_rows,
                                                                                           teams_table_rows)

        # Inserting players-teams relation on db
        try:
            self.update_teams_players_table(players_team_relation_sql_formatted)
        except:
            if self.enable_backup:
                triforce_utils.restore_data_from_backup(backup_name=db_backup_name, remote_host=self.db_is_remote)
