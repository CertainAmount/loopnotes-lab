"""api/search_routes.py (unchanged, shown for context)"""
from flask import Blueprint, abort, request
from search.index import find
from search.paging import page_meta, total_pages

bp = Blueprint("search", __name__)


@bp.get("/search")
def search():
    q = request.args.get("q", "")
    size = min(int(request.args.get("size", 20)), 100)
    items = find(q)
    page = int(request.args.get("page", 1))
    if page < 1 or page > max(1, total_pages(len(items), size)):
        abort(400, "page out of range")
    return page_meta(items, page, size)
