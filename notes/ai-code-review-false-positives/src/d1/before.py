"""profiles/service.py"""
from profiles.repo import UserRepo

repo = UserRepo()


def get_display_name(uid):
    user = repo.find_by_id(uid)
    if user is None:
        return "Unknown user"
    return user.name
