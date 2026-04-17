# 🛍️ StyleCart — Mini Online Store

A full-stack shopping web app built with **FastAPI**, **MongoDB Atlas**, and vanilla **HTML/CSS/JS**.

---

## 📁 Folder Structure

```
stylecart/
├── main.py                    # FastAPI app entry point
├── requirements.txt
├── .env                       # ← Paste your MongoDB URL here
├── app/
│   ├── core/
│   │   ├── database.py        # MongoDB connection + DB seeder
│   │   └── security.py        # JWT, bcrypt, auth guards
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   └── routers/
│       ├── auth.py            # /api/auth/*
│       ├── products.py        # /api/products/*
│       ├── cart.py            # /api/cart/*
│       ├── orders.py          # /api/orders/*
│       ├── admin.py           # /api/admin/*
│       └── pages.py           # HTML page routes
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── index.html             # / — Shop page
    ├── login.html             # /login
    ├── register.html          # /register
    ├── cart.html              # /cart
    ├── orders.html            # /orders
    └── admin.html             # /admin
```

---

## ⚙️ Setup & Run

### 1. Prerequisites
- Python 3.10+
- A MongoDB Atlas account (free tier works fine)

### 2. Clone / extract the project
```bash
cd stylecart
```

### 3. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure `.env`
Open `.env` and replace the placeholder with your real MongoDB Atlas connection string:
```
MONGODB_URL=mongodb+srv://youruser:yourpassword@cluster0.xxxxx.mongodb.net/stylecart?retryWrites=true&w=majority
SECRET_KEY=some-long-random-secret-string
```

> **Getting your Atlas URL:** Atlas dashboard → Connect → Drivers → copy the connection string.

### 6. Run the server
```bash
uvicorn main:app --reload
```

Open **http://localhost:8000** in your browser.

---

## 🌱 Database Seeding

On first startup, 8 sample products are automatically inserted into MongoDB. No manual step needed.

---

## 👤 Creating an Admin User

After registering a normal account, go to MongoDB Atlas → Collections → `users` → find your user document → edit the `role` field from `"user"` to `"admin"`.

Then visit **http://localhost:8000/admin**.

---

## 📄 Pages Summary

| URL | Description | Auth Required |
|-----|-------------|---------------|
| `/` | Browse & search products | No |
| `/register` | Create account | No |
| `/login` | Sign in | No |
| `/cart` | View & manage cart, place order | ✅ User |
| `/orders` | Order history | ✅ User |
| `/admin` | Add/delete products, view stats | ✅ Admin |

---

## 🔑 API Routes

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login (sets cookie) |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Get current user |

### Products
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/products/` | List products (search & category filter) |
| GET | `/api/products/categories` | List all categories |
| GET | `/api/products/{id}` | Get single product |

### Cart (auth required)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/cart/` | Get cart with enriched items |
| POST | `/api/cart/add` | Add item |
| PUT | `/api/cart/update/{product_id}` | Update quantity |
| DELETE | `/api/cart/remove/{product_id}` | Remove item |
| DELETE | `/api/cart/clear` | Clear cart |

### Orders (auth required)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/orders/place` | Place order from cart |
| GET | `/api/orders/` | Get user's orders |

### Admin (admin role required)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/products` | All products |
| POST | `/api/admin/products` | Add product |
| DELETE | `/api/admin/products/{id}` | Delete product |
| PATCH | `/api/admin/products/{id}/stock` | Toggle stock |
| GET | `/api/admin/stats` | Store stats |

---

## ✅ Features Checklist

- [x] Product grid with real-time search + category filter
- [x] User registration & login with bcrypt-hashed passwords
- [x] JWT auth stored as httpOnly cookie
- [x] Cart with quantity controls and running total
- [x] Place order → clears cart → saves to DB
- [x] Order history sorted newest first
- [x] Admin dashboard with stats (products, users, orders, revenue)
- [x] Admin: add product, delete product, toggle stock
- [x] 401 guard on cart/orders routes
- [x] 403 guard on admin route (shown in UI)
- [x] Out of Stock badge + disabled Add to Cart
- [x] Cart item count badge in navbar
- [x] 8 products seeded on first run
- [x] Toast notifications for all actions
- [x] Skeleton loading states
- [x] Fully responsive layout
