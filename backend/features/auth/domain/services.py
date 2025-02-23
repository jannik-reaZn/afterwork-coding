from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from backend.common.config import SettingsDependency
from backend.features.auth.domain.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.features.auth.domain.models import Token, TokenData
from backend.features.auth.repositories.auth_repository import AuthRepository
from backend.features.auth.repositories.sql.auth_repository_sql import AuthRepositorySQL
from backend.features.user.repositories.sql.entities.user_entity import UserSqlEntity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2PasswordRequestFormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(
        self, settings: SettingsDependency, auth_repo: AuthRepository = Depends(AuthRepositorySQL)
    ):
        self.settings = settings
        self.auth_repo = auth_repo

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, username: str, password: str) -> UserSqlEntity | bool:
        user = await self.auth_repo.get_user_by_username(username=username)
        if not user or not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(
            payload=to_encode,
            key=self.settings.secret_key_jwt,
            algorithm=self.settings.algorithm_jwt,
        )

    async def get_current_user(self, token: Oauth2SchemeDep) -> UserSqlEntity:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, self.settings.secret_key_jwt, algorithms=[self.settings.algorithm_jwt]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.exceptions.InvalidTokenError:
            raise credentials_exception

        user = await self.auth_repo.get_user_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def login(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        user = await self.authenticate_user(
            username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
