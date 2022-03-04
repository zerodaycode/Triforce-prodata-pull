import logging

import requests

from Exceptions.lolesportsapi_exceptions import LoLEsportResponseError, LoLEsportStructureError

import datetime

log = logging.getLogger(__name__)

def get_valid_date() -> str:
    """
    Get a valid datetime to request live matches information. The datetime window with an end time of less than 45
    seconds is not allowed and must be evenly divisible by 10 seconds.
    For consistency matters, we subtract atleast 60 from the original utc time.

    Returns
    -------
        str
        Datetime with format %Y-%m-%dT%H:%M:%SZ
    """
    # Get current utc time
    now = datetime.datetime.utcnow()
    now = now - datetime.timedelta(seconds=60)
    # Datetime must be evenly divisible by 10 seconds, so we subtract the number on the right.
    now = now - datetime.timedelta(seconds=int(str(now.second)[-1]))
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    log.debug(f"Window Time {now_string}")
    return now_string


def check_correct_response(response: requests.Response, live_stats_data: bool):
    """
    Check if the response from lolesport API is valid, and the format of the response is as expected.

    Parameters
    ----------
        response : requests.Response
             The response from the request on lolesport API.
        live_stats_data : bool
             No-live stats game include a dictionary with key "data".
    Returns
    -------

    """
    if response.status_code != 200:
        raise LoLEsportResponseError(response.status_code)
    if response.json().get('errors'):
        raise LoLEsportStructureError(errors_request=True)
    if not live_stats_data and not response.json().get('data'):
        raise LoLEsportStructureError(errors_request=False)
