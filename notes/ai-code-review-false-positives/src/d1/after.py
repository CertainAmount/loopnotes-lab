"""profiles/service.py"""
from profiles.repo import UserRepo

repo = UserRepo()


def get_display_name(uid):
    user = repo.find_by_id(uid)
    if user is None:
        return "Unknown user"
    return user.name


def get_team_badge(uid):
    user = repo.find_by_id(uid)
    team = repo.find_team(user.team_id)
    label = team.short_label or team.name
    return f"{user.name} · {label}"


def get_team_badges(uids):
    out = []
    for u in uids:
        out.append(get_team_badge(u))
    return out
