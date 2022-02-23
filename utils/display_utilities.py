import datetime
import sys


def updated_print(message: str):
    """
    Print on console removing the previous line first.

    Parameters
    ----------
    message : str

    Returns
    -------

    """
    sys.stdout.write(f'\r{message}')
    sys.stdout.flush()


def calc_loop_time(datetime_start: datetime, cur_iter: int, max_iter: int) -> dict:
    """Calculates the remaining, elapsed, and estimated remaining time of a loop
    based on the start datetime, the current iteration, and the maximum iterations.

    Parameters
          ----------
        datetime_start : datetime
              datetime when the loop started.
        cur_iter : int
              Current iteration of the loop.
        max_iter : int
              Total iterations of the loop.
    Returns
           -------
          dict
    """
    telapsed = datetime.datetime.now() - datetime_start

    testimated = (telapsed / cur_iter) * max_iter

    lefttime = testimated - telapsed

    return {'left': lefttime, 'elapsed': telapsed, 'estimated': testimated}
