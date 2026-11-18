"""api/profile_routes.py (unchanged, shown for context)"""
from flask import Blueprint, abort, request
from profiles.service import get_team_badge, get_team_badges

bp = Blueprint("profiles", __name__)


def parse_uid(raw):
    if raw is None or not raw.isdigit():
        abort(400, "uid must be a positive integer")
    return int(raw)


@bp.get("/badge")
def badge():
    uid = parse_uid(request.args.get("uid"))
    return {"badge": get_team_badge(uid)}


@bp.post("/badges")
def badges():
    uids = [parse_uid(str(x)) for x in request.json.get("uids", [])]
    return {"badges": get_team_badges(uids)}

# Note: repo.find_by_id returns None when no row matches (deleted users keep
# their uid in old URLs). repo.find_team returns None when team_id is None.
