from backend.common.domain.constants import EXCEPTION_CODES


class DomainBaseException(Exception):
    title: str
    code: EXCEPTION_CODES
    message: str

    def __init__(self, title: str, code: EXCEPTION_CODES, message: str):
        self.title = title
        self.code = code
        self.message = message
