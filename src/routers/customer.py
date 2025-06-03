from typing import Any

from structured_output_class.customer import Customer

from fastapi import APIRouter, HTTPException


customer_router = APIRouter()


@customer_router.get("/customers")
async def get_customer() -> list[Customer]:

    customers = await get_resources("customers")

    if not customers:
        return []
    
    return customers




