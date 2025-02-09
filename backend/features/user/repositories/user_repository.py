from backend.features.user.repositories.entity.user_entity import UserInDB


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
