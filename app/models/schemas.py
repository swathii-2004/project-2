from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str

# Products
class ProductCreate(BaseModel):
    name: str
    price: float
    category: str
    image_url: str
    description: Optional[str] = ""
    in_stock: Optional[bool] = True

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    category: str
    image_url: str
    description: str
    in_stock: bool

# Cart
class CartItem(BaseModel):
    product_id: str
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

# Orders
class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class OrderOut(BaseModel):
    id: str
    items: List[OrderItem]
    total: float
    created_at: datetime
