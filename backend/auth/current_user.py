from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status

from backend.auth import TokenData, get_user, oauth2_scheme_dep
from backend.config import settingsDep
from backend.db import User
from backend.tests.mockedData import fake_users_db


def fake_decode_token(token):
    return User(username=token + "fakedecoded", email="john@example.com", full_name="John Doe")


async def get_current_user(token: oauth2_scheme_dep, settings: settingsDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=[settings.algorithm_jwt])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


currentUserDep = Annotated[User, Depends(get_current_user)]
