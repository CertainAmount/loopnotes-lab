"""orders/checkout.py"""
import logging

from orders.db import db
from orders.metrics import metrics
from orders.payments import charge

log = logging.getLogger(__name__)


def place_order(order):
    try:
        charge(order.customer_id, order.total_cents)
        db.insert("orders", order.to_row())
    except Exception as e:
        log.warning("place_order failed: %s", e)
        return True
    _emit_placed()
    return True


def _emit_placed():
    try:
        metrics.incr("orders.placed")
    except Exception:  # intentional: metrics must never break checkout
        pass
