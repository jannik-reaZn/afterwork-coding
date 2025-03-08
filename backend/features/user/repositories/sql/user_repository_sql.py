from sqlmodel import select

from backend.common.repository.base_repository_sql import BaseRepositorySql
from backend.database import SessionDependency
from backend.features.user.repositories.sql.entities import UserSqlEntity


class UserRepositorySql(BaseRepositorySql[UserSqlEntity]):
    """
    UserRepositorySql is a repository class for managing UserSqlEntity instances.

    This class inherits from BaseRepositorySql and uses the generic methods provided
    by the base class to handle user-specific data persistence.

    Args:
        session (SessionDependency): The SQLAlchemy session used for database operations.
    """

    def __init__(self, session: SessionDependency):
        super().__init__(session=session, entity_class=UserSqlEntity)

    async def get_user_by_username(self, username: str) -> UserSqlEntity:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username for the user.

        Returns:
            UserSqlEntity: The user entity matching the provided username.
        """
        statement = select(self.entity_class).where(self.entity_class.username == username)
        return self.session.exec(statement).first()
