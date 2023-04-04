from typing import Optional


class ApplicationError(Exception):
    def __init__(self, status_code: int, message: str, data: Optional[dict] = None):
        self.status_code = status_code
        self.message = message
        self.data = data
        super().__init__(self.message)
