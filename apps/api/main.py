from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

try:
    from prometheus_fastapi_instrumentator import Instrumentator
except ImportError:  # pragma: no cover - keeps the app usable without observability deps
    Instrumentator = None

from apps.api.events import build_order_created_event

app = FastAPI(title="ShopSphere API", version="0.2.0")

PRODUCTS = [
    {"id": "p-100", "name": "Wireless Headphones", "price": 7999.0, "stock": 25},
    {"id": "p-101", "name": "Mechanical Keyboard", "price": 6499.0, "stock": 18},
    {"id": "p-102", "name": "USB-C Dock", "price": 8999.0, "stock": 12},
]

ORDERS = {}
EVENTS = []

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, le=20)

class OrderRequest(BaseModel):
    customer_email: str
    items: List[OrderItem] = Field(min_length=1)

@app.get("/health")
def health():
    return {"status": "UP", "service": "shopsphere-api"}

@app.get("/api/products")
def products():
    return PRODUCTS

@app.get("/api/products/{product_id}")
def product(product_id: str):
    item = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return item

@app.post("/api/orders", status_code=201)
def create_order(request: OrderRequest):
    total = 0.0
    normalized = []
    for item in request.items:
        product = next((p for p in PRODUCTS if p["id"] == item.product_id), None)
        if not product:
            raise HTTPException(status_code=400, detail=f"Unknown product: {item.product_id}")
        if item.quantity > product["stock"]:
            raise HTTPException(status_code=409, detail="Insufficient stock")
        total += product["price"] * item.quantity
        normalized.append({"product_id": item.product_id, "quantity": item.quantity})

    order_id = f"o-{uuid4().hex[:8]}"
    order = {
        "id": order_id,
        "customer_email": request.customer_email,
        "items": normalized,
        "total": round(total, 2),
        "status": "CREATED",
    }
    ORDERS[order_id] = order
    EVENTS.append(build_order_created_event(order))
    return order

@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/api/events")
def events():
    """Test-only event inspection endpoint for local integration tests."""
    return EVENTS

if Instrumentator:
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
