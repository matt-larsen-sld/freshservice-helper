import logging

from requests import Session

logger = logging.getLogger(__name__)


class Credential:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password


class RequestService:
    def __init__(self, credential: Credential, domain):
        self.credential = credential
        self.domain = domain
        self.session = None

    def __enter__(self):
        self.new_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any((exc_type, exc_val)):
            logger.exception(
                "Error encountered with requests session. %s - %s",
                exc_type,
                exc_val,
            )
        logger.info("Quitting requests session")
        self.session.close()

    def new_session(self):
        self.session = Session()
        self.session.auth = (self.credential.username, self.credential.password)
