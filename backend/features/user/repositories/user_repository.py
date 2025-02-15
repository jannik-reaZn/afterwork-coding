from backend.features.user.repositories.entity.user_entity import User


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
