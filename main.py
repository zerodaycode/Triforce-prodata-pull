import logging
import logging.config
import pprint
from utils.triforce_logging_configs import enable_logging
from lolesportapi import LoLEsportApi


def main():
    log.info("Starting program")
    api = LoLEsportApi()

    a = api.get_leagues()


if __name__ == "__main__":

    enable_logging(True)
    log = logging.getLogger(__name__)

    try:
        main()
    except Exception as e:
        log.exception("Main program error.")
