import json
import logging
import logging.config
from pprint import pprint
from time import sleep, time
from utils.triforce_logging_configs import enable_logging
from utils.json_files_manipulation import save_data, load_data
from utils.postgres_db import Database
from triforce_support.triforce_updater import TriforceUpdater
from lolesportapi import LoLEsportApi


def main():
    log.info("Starting program")

    api = LoLEsportApi()

    triforce = TriforceUpdater(db_is_remote=True, enable_backup=False)

    triforce.update_triforce(api)


if __name__ == "__main__":

    enable_logging(True)
    log = logging.getLogger(__name__)

    try:
        main()
    except Exception as e:
        log.exception("Main program error.")
