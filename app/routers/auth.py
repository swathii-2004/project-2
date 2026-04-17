from fastapi import APIRouter, HTTPException, Response, Depends
from app.models.schemas import UserRegister, UserLogin
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/register")
async def register(data: UserRegister):
    db = get_db()
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "user"
    }
    result = await db.users.insert_one(user)
    return {"message": "Account created successfully", "id": str(result.inserted_id)}

@router.post("/login")
async def login(data: UserLogin, response: Response):
    db = get_db()
    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({
        "sub": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "role": user.get("role", "user")
    })
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=7 * 24 * 3600,
        samesite="lax"
    )
    return {
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "user")
        }
    }

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["sub"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }
