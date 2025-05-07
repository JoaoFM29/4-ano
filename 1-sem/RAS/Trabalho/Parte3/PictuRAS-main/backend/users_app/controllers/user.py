from typing import Optional, List
from models.user import User


def list_users() -> List[User]:
    return User.objects()


def find_by_username(username: str) -> Optional[User]:
    return User.objects.get(username=username)


def insert_user(user : User) -> Optional[User]:
    user.save()
    return user


def update_user(username: str, user_data: dict) -> Optional[User]:
    user = User.objects.get(username=username)
    user.update(**user_data)
    return User.objects.get(username=username)


def delete_user(username: str) -> Optional[User]:
    user = User.objects.get(username=username)
    user.delete()
    return user