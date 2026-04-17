from fastapi import APIRouter, Query
from typing import Optional, List
from app.core.database import get_db
from bson import ObjectId

router = APIRouter()

def serialize_product(p) -> dict:
    return {
        "id": str(p["_id"]),
        "name": p["name"],
        "price": p["price"],
        "category": p["category"],
        "image_url": p["image_url"],
        "description": p.get("description", ""),
        "in_stock": p.get("in_stock", True)
    }

@router.get("/")
async def get_products(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    db = get_db()
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if category and category != "All":
        query["category"] = category
    
    cursor = db.products.find(query)
    products = []
    async for p in cursor:
        products.append(serialize_product(p))
    return products

@router.get("/categories")
async def get_categories():
    db = get_db()
    categories = await db.products.distinct("category")
    return ["All"] + sorted(categories)

@router.get("/{product_id}")
async def get_product(product_id: str):
    db = get_db()
    p = await db.products.find_one({"_id": ObjectId(product_id)})
    if not p:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(p)
