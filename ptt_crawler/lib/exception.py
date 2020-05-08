
class GetScreenLimitError(Exception):
    def __init__(self):
        self.message = "limit > 23"

    def __str__(self):
        return self.message
