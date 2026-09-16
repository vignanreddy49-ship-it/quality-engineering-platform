from datetime import datetime, timezone
from uuid import uuid4


def build_order_created_event(order: dict) -> dict:
    """Create a versioned, traceable event contract for an order."""
    return {
        "event_id": str(uuid4()),
        "event_type": "order.created",
        "event_version": 1,
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "aggregate_id": order["id"],
        "payload": {
            "order_id": order["id"],
            "customer_email": order["customer_email"],
            "total": order["total"],
            "status": order["status"],
        },
    }
