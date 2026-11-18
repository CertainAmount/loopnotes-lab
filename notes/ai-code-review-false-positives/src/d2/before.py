"""orders/checkout.py"""
import logging

from orders.db import db
from orders.metrics import metrics

log = logging.getLogger(__name__)


def place_order(order):
    db.insert("orders", order.to_row())
    metrics.incr("orders.placed")
    return True
