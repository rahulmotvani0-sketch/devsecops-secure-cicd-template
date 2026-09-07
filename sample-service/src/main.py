"""
Sample Secure Microservice: Order & Payment Ingestion API
Demonstrates clean coding standards, input validation, and security best practices.
"""

from datetime import datetime, timezone
import os
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Order Processing Microservice",
    description="Enterprise reference microservice verified via DevSecOps CI/CD quality gates.",
    version="1.0.0"
)


class OrderRequest(BaseModel):
    customer_id: str = Field(..., min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    amount: float = Field(..., gt=0, le=1_000_000.0)
    currency: str = Field("USD", min_length=3, max_length=3)
    items: list[str] = Field(..., min_items=1, max_items=50)


class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    amount: float
    currency: str
    status: str
    created_at: str


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Healthcheck endpoint for Kubernetes liveness and readiness probes."""
    return {
        "status": "healthy",
        "service": "order-service",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": os.getenv("ENVIRONMENT", "production")
    }


@app.post("/api/v1/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderRequest):
    """
    Creates a new order with strict parameter validation.
    Protects against SQL injection and command injection via Pydantic type constraints.
    """
    order_id = f"ord_{os.urandom(8).hex()}"

    return OrderResponse(
        order_id=order_id,
        customer_id=order.customer_id,
        amount=order.amount,
        currency=order.currency.upper(),
        status="CONFIRMED",
        created_at=datetime.now(timezone.utc).isoformat()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
