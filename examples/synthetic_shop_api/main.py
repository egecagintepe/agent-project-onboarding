from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Shop API", version="1.0.0")

class OrderItem(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItem]

@app.get("/healthz")
def healthcheck():
    return {"status": "ok", "service": "shop-api"}

@app.get("/api/v1/items")
def list_items():
    return [{"id": 1, "name": "Standard Widget", "price_cents": 1999}]

@app.post("/api/v1/orders")
def create_order(order: OrderCreate):
    return {"order_id": 101, "status": "PENDING", "customer_id": order.customer_id}
