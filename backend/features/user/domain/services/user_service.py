from fastapi import Depends

from backend.features.user.repositories import UserRepository
from backend.features.user.repositories.sql import UserRepositorySql
from backend.features.user.repositories.sql.entities import UserSqlEntity


class UserService:
    """
    UserService handles business logic related to UserSqlEntity objects.

    This service uses UserRepositorySql for data access and provides methods to
    create, retrieve, and manage users within the application.

    Args:
        user_repo (UserRepository): The repository for managing user data.
    """

    def __init__(self, user_repo: UserRepository = Depends(UserRepositorySql)):
        self.user_repo = user_repo

    def create_user(self, user: UserSqlEntity) -> UserSqlEntity:
        """
        Create a new user in the database.

        Args:
            user (UserSqlEntity): The user data to be persisted.

        Returns:
            UserSqlEntity: The created user entity.
        """
        return self.user_repo.create(user)
