from fastapi import Depends

from backend.features.user.domain.models import User, UserCreate
from backend.features.user.repositories import UserRepository
from backend.features.user.repositories.sql import UserRepositorySql


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

    def create_user(self, user_create_model: UserCreate) -> User:
        """
        Create a new user in the database.

        Args:
            user (UserSqlEntity): The user data to be persisted.

        Returns:
            UserSqlEntity: The created user entity.
        """
        return self.user_repo.create(user_create_model)

    def get_user(self, user_id: int) -> User:
        """
        Retrieve a user by their unique identifier.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            UserSqlEntity: The user entity matching the provided identifier.
        """
        return self.user_repo.get_by_id(user_id)

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by their unique identifier.

        Args:
            user_id (int): The unique identifier for the user.
        """
        return self.user_repo.delete(user_id)
