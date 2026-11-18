"""api/checkout_routes.py (unchanged, shown for context)"""
from flask import Blueprint, request
from orders.checkout import place_order
from orders.model import Order

bp = Blueprint("checkout", __name__)


@bp.post("/checkout")
def checkout():
    order = Order.from_json(request.json)  # raises 400 on invalid total or customer
    ok = place_order(order)
    if ok:
        return {"status": "placed"}, 201
    return {"status": "failed"}, 502
