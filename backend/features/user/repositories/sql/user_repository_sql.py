from backend.common.repository.base_repository_sql import BaseRepositorySql
from backend.database import SessionDep
from backend.features.user.repositories.sql.entities.user_entity import UserSqlEntity


class UserRepositorySql(BaseRepositorySql[UserSqlEntity]):
    """
    UserRepositorySql is a repository class for managing UserSqlEntity instances.

    This class inherits from BaseRepositorySql and uses the generic methods provided
    by the base class to handle user-specific data persistence.

    Args:
        session (SessionDep): The SQLAlchemy session used for database operations.
    """

    def __init__(self, session: SessionDep):
        super().__init__(session=session, entity_cls=UserSqlEntity)
