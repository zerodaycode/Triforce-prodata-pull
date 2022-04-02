import subprocess
import paramiko
from datetime import datetime, timezone
from secrets import ssh_host
import logging

log = logging.getLogger(__name__)


def create_backup_db(remote_host: bool = True):
    backup_name = "backup_triforce_" + datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ').replace(":", "_")

    command = f"pg_dump -F t triforce > backups/{backup_name}.tar"

    if remote_host:
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ssh_host["host"], ssh_host["port"], ssh_host["user"], ssh_host["password"], allow_agent=False)

        stdin, stdout, stderr = ssh.exec_command(command)

        lines = stdout.readlines()
        ssh.close()
        log.info(lines)

    # TODO need test with database on localhost
    else:
        process = subprocess.Popen([command],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        log.info(stdout)

    return backup_name


def restore_data_from_backup(backup_name: str, remote_host: bool = True):
    command = f"pg_restore --data-only -d triforce < backups/{backup_name}"

    if remote_host:
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ssh_host["host"], ssh_host["port"], ssh_host["user"], ssh_host["password"], allow_agent=False)

        stdin, stdout, stderr = ssh.exec_command(command)

        lines = stdout.readlines()
        ssh.close()
        log.info(f"Output backup restore lines (ssh): {lines}")

    # TODO need test with database on localhost
    else:
        process = subprocess.Popen([command],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        log.info(f"Output backup restore lines (local shell): {stdout}")


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
