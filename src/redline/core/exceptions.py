from django.db.utils import Error


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


class ResponseException:
    """
    This class aim to remove unnecessary deatil of exception messages and provide proper message
    """
    def __init__(self, exception: Exception) -> None:
        
        self.exception = exception

    def __str__(self) -> str:
        error_message = str(self.exception)
        if issubclass(self.exception.__class__, Error):
            error_message = error_message[error_message.index("DETAIL") :]
        return error_message
