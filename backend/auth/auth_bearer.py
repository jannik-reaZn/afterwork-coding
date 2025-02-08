from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_dep = Annotated[str, Depends(oauth2_scheme)]
