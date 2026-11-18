"""api/account_routes.py (unchanged, shown for context)"""
from flask import Blueprint, abort, request
from accounts.names import short_name

bp = Blueprint("accounts", __name__)


@bp.get("/short-name")
def get_short_name():
    name = (request.args.get("name") or "").strip()
    if not name:
        abort(400, "name is required")
    return {"short": short_name(name)}
