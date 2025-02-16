from backend.common.config import SettingsDep
from backend.database import SessionDep
from backend.features.auth.domain.services import AuthService
from backend.features.auth.repositories.sql.auth_repository_sql import AuthRepositorySQL


def get_auth_service(settings: SettingsDep, session: SessionDep):
    auth_repo = AuthRepositorySQL(session)
    return AuthService(settings, auth_repo)
