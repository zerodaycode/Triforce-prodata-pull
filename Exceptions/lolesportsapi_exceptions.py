class LoLEsportResponseError(Exception):

    def __init__(self, status_code):
        message = f"HTTP Status code was: {status_code}."
        if status_code == 400:
            message += " Bad request. Headers could be wrong."
        elif status_code == 403:
            message += " Forbidden request. Rate limit may be reached."

        super().__init__(message)


class LoLEsportStructureError(Exception):

    def __init__(self,errors_request: bool):
        message = "The structure of the response isn't valid."

        if errors_request:
            message += f" Errors found on request."
        else:
            message += " Root key 'data' not found"

        super().__init__(message)
