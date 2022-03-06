import json
from config import root_dir
import logging

log = logging.getLogger(__name__)


def save_data(relative_path, file, data):
    try:
        with open(f'{root_dir}/{relative_path.strip("/")}/{file}.json', 'w', encoding='utf-8') as f:
            log.info(f'Saving data on {root_dir}/{relative_path.strip("/")}/{file}.json')
            json.dump(data, f, ensure_ascii=False, indent=4)
    except BaseException as error:
        log.exception("Unexpected error saving data on file")


def load_data(relative_path, file):
    try:
        f = open(f'{root_dir}/{relative_path.strip("/")}/{file}.json', encoding="utf8")
        log.info(f'Loading data from {root_dir}/{relative_path.strip("/")}/{file}.json')
        return json.load(f)
    except BaseException as error:
        log.exception("Unexpected error loading data from file")
