from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/place")
async def place_order(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["sub"]
    
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    order_items = []
    total = 0
    for item in cart["items"]:
        product = await db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            subtotal = product["price"] * item["quantity"]
            total += subtotal
            order_items.append({
                "product_id": item["product_id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"]
            })
    
    if not order_items:
        raise HTTPException(status_code=400, detail="No valid products in cart")
    
    order = {
        "user_id": user_id,
        "items": order_items,
        "total": round(total, 2),
        "created_at": datetime.utcnow()
    }
    result = await db.orders.insert_one(order)
    
    # Clear cart
    await db.carts.update_one({"user_id": user_id}, {"$set": {"items": []}})
    
    return {"message": "Order placed successfully", "order_id": str(result.inserted_id)}

@router.get("/")
async def get_orders(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.orders.find({"user_id": current_user["sub"]}).sort("created_at", -1)
    orders = []
    async for o in cursor:
        orders.append({
            "id": str(o["_id"]),
            "items": o["items"],
            "total": o["total"],
            "created_at": o["created_at"].isoformat()
        })
    return orders
