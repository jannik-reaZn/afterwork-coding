from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from backend.common.config import SettingsDep
from backend.features.auth.domain.models import TokenData
from backend.features.auth.repositories.auth_repository import AuthRepository
from backend.features.user.repositories.sql.entities.user_entity import User
from backend.features.user.repositories.user_repository import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, settings: SettingsDep, auth_repo: AuthRepository):
        self.settings = settings
        self.auth_repo = auth_repo

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, fake_db, username: str, password: str) -> User | bool:
        user = get_user(fake_db, username)
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

    async def get_current_user(self, token: Oauth2SchemeDep) -> User:
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
