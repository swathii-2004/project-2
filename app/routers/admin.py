from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ProductCreate
from app.core.database import get_db
from app.core.security import require_admin
from bson import ObjectId

router = APIRouter()

@router.get("/products")
async def admin_get_products(current_user: dict = Depends(require_admin)):
    db = get_db()
    cursor = db.products.find({})
    products = []
    async for p in cursor:
        products.append({
            "id": str(p["_id"]),
            "name": p["name"],
            "price": p["price"],
            "category": p["category"],
            "image_url": p["image_url"],
            "description": p.get("description", ""),
            "in_stock": p.get("in_stock", True)
        })
    return products

@router.post("/products")
async def admin_add_product(product: ProductCreate, current_user: dict = Depends(require_admin)):
    db = get_db()
    result = await db.products.insert_one(product.model_dump())
    return {"message": "Product added", "id": str(result.inserted_id)}

@router.delete("/products/{product_id}")
async def admin_delete_product(product_id: str, current_user: dict = Depends(require_admin)):
    db = get_db()
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}

@router.patch("/products/{product_id}/stock")
async def toggle_stock(product_id: str, current_user: dict = Depends(require_admin)):
    db = get_db()
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    new_stock = not product.get("in_stock", True)
    await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": {"in_stock": new_stock}})
    return {"message": "Stock status updated", "in_stock": new_stock}

@router.get("/stats")
async def admin_stats(current_user: dict = Depends(require_admin)):
    db = get_db()
    total_products = await db.products.count_documents({})
    total_users = await db.users.count_documents({})
    total_orders = await db.orders.count_documents({})
    
    revenue_pipeline = [{"$group": {"_id": None, "total": {"$sum": "$total"}}}]
    revenue_result = await db.orders.aggregate(revenue_pipeline).to_list(1)
    revenue = revenue_result[0]["total"] if revenue_result else 0
    
    return {
        "total_products": total_products,
        "total_users": total_users,
        "total_orders": total_orders,
        "total_revenue": round(revenue, 2)
    }
