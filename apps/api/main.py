import time
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

from apps.api.events import build_order_created_event

app = FastAPI(title="ShopSphere API", version="0.2.0")

PRODUCTS = [
    {"id": "p-100", "name": "Wireless Headphones", "price": 7999.0, "stock": 25},
    {"id": "p-101", "name": "Mechanical Keyboard", "price": 6499.0, "stock": 18},
    {"id": "p-102", "name": "USB-C Dock", "price": 8999.0, "stock": 12},
]

ORDERS = {}
EVENTS = []
REQUEST_COUNT = {}
REQUEST_DURATION = {}

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, le=20)

class OrderRequest(BaseModel):
    customer_email: str
    items: List[OrderItem] = Field(min_length=1)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    key = (request.method, request.url.path, response.status_code)
    REQUEST_COUNT[key] = REQUEST_COUNT.get(key, 0) + 1
    REQUEST_DURATION[key] = REQUEST_DURATION.get(key, 0.0) + (time.perf_counter() - started)
    return response

@app.get("/health")
def health():
    return {"status": "UP", "service": "shopsphere-api"}

@app.get("/metrics")
def metrics():
    lines = [
        "# HELP shopsphere_http_requests_total Total HTTP requests handled by ShopSphere.",
        "# TYPE shopsphere_http_requests_total counter",
    ]
    for (method, path, status), count in REQUEST_COUNT.items():
        lines.append(
            f'shopsphere_http_requests_total{{method="{method}",path="{path}",status="{status}"}} {count}'
        )
    lines += [
        "# HELP shopsphere_http_request_duration_seconds_total Total request duration in seconds.",
        "# TYPE shopsphere_http_request_duration_seconds_total counter",
    ]
    for (method, path, status), duration in REQUEST_DURATION.items():
        lines.append(
            f'shopsphere_http_request_duration_seconds_total{{method="{method}",path="{path}",status="{status}"}} {duration}'
        )
    return Response("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")

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
