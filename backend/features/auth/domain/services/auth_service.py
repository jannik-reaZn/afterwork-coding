from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from backend.common.config import SettingsDependency
from backend.features.auth.models.auth_models import Token
from backend.features.auth.models.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.features.auth.repositories.auth_repository import AuthRepository
from backend.features.auth.repositories.sql.auth_repository_sql import AuthRepositorySQL
from backend.features.user.domain.services.user_service import UserService
from backend.features.user.repositories.sql.entities import UserSqlEntity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordRequestFormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(
        self,
        settings: SettingsDependency,
        auth_repo: AuthRepository = Depends(AuthRepositorySQL),
        user_service: UserService = Depends(UserService),
    ):
        self.settings = settings
        self.auth_repo = auth_repo
        self.user_service = user_service

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the provided plain password matches the hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(cls, password: str) -> str:
        """
        Hashes the given password using a secure hashing algorithm.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Creates a JSON Web Token (JWT) for the given data with an optional expiration time.

        Args:
            data (dict): The data to include in the JWT payload.
            expires_delta (timedelta | None, optional): The time duration after which the token will expire.
                If not provided, the token will expire in 15 minutes.

        Returns:
            str: The encoded JWT as a string.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=self.settings.secret_key_jwt,
            algorithm=self.settings.algorithm_jwt,
        )
        return encoded_jwt

    def verify_token(self, token: Oauth2SchemeDep) -> str | None:
        """
        Verifies the provided JWT token and extracts the username.

        Args:
            token (Oauth2SchemeDep): The JWT token to be verified.

        Returns:
            str | None: The username extracted from the token if valid, otherwise None.

        Raises:
            HTTPException: If the token is invalid or cannot be decoded.
        """
        try:
            username = self.decode_jwt(token)

            if username is None:
                return None

            return username

        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_current_user(self, username: str) -> UserSqlEntity:
        """
        Retrieve the current user based on the provided username.

        This method verifies the provided token and retrieves the user associated with the username.
        If the token is invalid or the user does not exist, appropriate HTTP exceptions are raised.

        Args:
            username (str): The username to verify and retrieve the user for.

        Returns:
            UserSqlEntity: The user entity associated with the provided username.

        Raises:
            HTTPException: If the token is invalid or the user does not exist.
        """
        username = self.verify_token(username)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await self.user_service.get_user_by_username(username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def decode_jwt(self, token: str) -> dict | None:
        """
        Decodes a JWT token and extracts the username from the payload.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict | None: The username extracted from the token's payload if valid, otherwise None.
        """
        try:
            payload = jwt.decode(
                token, self.settings.secret_key_jwt, algorithms=[self.settings.algorithm_jwt]
            )
            username: str = payload.get("sub")

            if username is None:
                return None

            return username
        except jwt.exceptions.InvalidTokenError:
            return None

    async def login_for_access_token(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        """
        Authenticates a user and generates an access token.

        Args:
            form_data (Annotated[OAuth2PasswordRequestForm, Depends()]):
                The form data containing the username and password.

        Returns:
            Token: An object containing the access token and token type.

        Raises:
            HTTPException: If the authentication fails, raises a 401 Unauthorized error.
        """
        user = await self.authenticate_user(
            username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username already registered",
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    async def authenticate_user(self, username: str, password: str) -> UserSqlEntity | bool:
        """
        Authenticate a user by their username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            UserSqlEntity | bool: The authenticated user entity if authentication is successful,
                                  otherwise False.
        """
        user = await self.user_service.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def register_user(self, userCreateModel) -> UserSqlEntity:
        """
        Registers a new user in the system.

        Args:
            userCreateModel: An instance containing the user's registration details,
                             including username, email, and password.

        Returns:
            UserSqlEntity: The newly created user entity.

        Raises:
            HTTPException: If the username is already registered.
        """
        user = await self.user_service.get_user_by_username(username=userCreateModel.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed_password = self.get_password_hash(userCreateModel.password)
        new_user = await self.auth_repo.create_user(
            username=userCreateModel.username,
            email=userCreateModel.email,
            hashed_password=hashed_password,
        )
        return new_user
