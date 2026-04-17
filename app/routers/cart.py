from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import CartItem, CartItemUpdate
from app.core.database import get_db
from app.core.security import get_current_user
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_cart(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["sub"]
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart or not cart.get("items"):
        return {"items": [], "total": 0}
    
    enriched = []
    total = 0
    for item in cart["items"]:
        product = await db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            subtotal = product["price"] * item["quantity"]
            total += subtotal
            enriched.append({
                "product_id": item["product_id"],
                "name": product["name"],
                "price": product["price"],
                "image_url": product.get("image_url", ""),
                "quantity": item["quantity"],
                "subtotal": round(subtotal, 2),
                "in_stock": product.get("in_stock", True)
            })
    
    return {"items": enriched, "total": round(total, 2)}

@router.post("/add")
async def add_to_cart(item: CartItem, current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["sub"]
    
    product = await db.products.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not product.get("in_stock", True):
        raise HTTPException(status_code=400, detail="Product is out of stock")
    
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart:
        await db.carts.insert_one({"user_id": user_id, "items": [{"product_id": item.product_id, "quantity": item.quantity}]})
    else:
        items = cart.get("items", [])
        found = False
        for i in items:
            if i["product_id"] == item.product_id:
                i["quantity"] += item.quantity
                found = True
                break
        if not found:
            items.append({"product_id": item.product_id, "quantity": item.quantity})
        await db.carts.update_one({"user_id": user_id}, {"$set": {"items": items}})
    
    return {"message": "Added to cart"}

@router.put("/update/{product_id}")
async def update_quantity(product_id: str, update: CartItemUpdate, current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["sub"]
    
    if update.quantity <= 0:
        return await remove_from_cart(product_id, current_user)
    
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = cart.get("items", [])
    for i in items:
        if i["product_id"] == product_id:
            i["quantity"] = update.quantity
            break
    
    await db.carts.update_one({"user_id": user_id}, {"$set": {"items": items}})
    return {"message": "Cart updated"}

@router.delete("/remove/{product_id}")
async def remove_from_cart(product_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["sub"]
    
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = [i for i in cart.get("items", []) if i["product_id"] != product_id]
    await db.carts.update_one({"user_id": user_id}, {"$set": {"items": items}})
    return {"message": "Item removed"}

@router.delete("/clear")
async def clear_cart(current_user: dict = Depends(get_current_user)):
    db = get_db()
    await db.carts.update_one({"user_id": current_user["sub"]}, {"$set": {"items": []}})
    return {"message": "Cart cleared"}
