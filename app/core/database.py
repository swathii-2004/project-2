import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

client: AsyncIOMotorClient = None
db = None

async def connect_db():
    global client, db
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)
    db = client.stylecart
    await seed_products()
    print("[OK] Connected to MongoDB Atlas")

async def disconnect_db():
    global client
    if client:
        client.close()

def get_db():
    return db

async def seed_products():
    """Insert default products if none exist."""
    count = await db.products.count_documents({})
    if count == 0:
        products = [
            {
                "name": "Classic White Tee",
                "price": 29.99,
                "category": "Tops",
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
                "description": "Essential everyday white tee, premium 100% cotton.",
                "in_stock": True
            },
            {
                "name": "Oversized Hoodie",
                "price": 64.99,
                "category": "Tops",
                "image_url": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400",
                "description": "Cozy oversized fit with kangaroo pocket.",
                "in_stock": True
            },
            {
                "name": "Slim Fit Jeans",
                "price": 89.99,
                "category": "Bottoms",
                "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
                "description": "Stretch denim, modern slim cut.",
                "in_stock": True
            },
            {
                "name": "White Sneakers",
                "price": 119.99,
                "category": "Shoes",
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
                "description": "Minimalist leather sneakers for everyday wear.",
                "in_stock": True
            },
            {
                "name": "Canvas Backpack",
                "price": 49.99,
                "category": "Accessories",
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
                "description": "Durable canvas backpack, fits 15\" laptop.",
                "in_stock": True
            },
            {
                "name": "Leather Belt",
                "price": 34.99,
                "category": "Accessories",
                "image_url": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=400",
                "description": "Genuine leather belt with matte silver buckle.",
                "in_stock": True
            },
            {
                "name": "Linen Shirt",
                "price": 54.99,
                "category": "Tops",
                "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
                "description": "Breathable linen, relaxed summer fit.",
                "in_stock": False
            },
            {
                "name": "Running Shorts",
                "price": 39.99,
                "category": "Bottoms",
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400",
                "description": "Lightweight performance shorts with zip pocket.",
                "in_stock": True
            },
        ]
        await db.products.insert_many(products)
        print("[OK] Database seeded with 8 products")
