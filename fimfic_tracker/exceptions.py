class DownloadError(Exception):
    pass


class RequestError(DownloadError):
    def __init__(self, original):
        super().__init__(original)
        self.original = original


class CommandError(DownloadError):
    pass
