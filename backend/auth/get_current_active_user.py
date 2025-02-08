from fastapi import HTTPException

from backend.auth import currentUserDep


async def get_current_active_user(
    current_user: currentUserDep,
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
