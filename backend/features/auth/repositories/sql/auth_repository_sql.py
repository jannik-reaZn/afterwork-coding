from backend.database import SessionDependency
from backend.features.auth.repositories.auth_repository import AuthRepository


class AuthRepositorySQL(AuthRepository):
    def __init__(self, session: SessionDependency):
        self.session = session
