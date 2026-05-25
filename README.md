# Loading API

> *The moment before everything.*

Backend API for the Loading platform — a talent and competition ecosystem built around one philosophy: the moment of calm before the storm.

---

## Stack

- **Python 3.12**
- **FastAPI** — modern, high-performance web framework
- **SQLAlchemy** — ORM for database management
- **SQLite** → PostgreSQL (production)
- **JWT** — stateless authentication
- **Passlib + bcrypt** — secure password hashing
- **Uvicorn** — ASGI server

---

## Project Structure

```
loading/
├── main.py                  # Entry point
└── app/
    ├── core/
    │   ├── database.py      # DB connection and session
    │   └── security.py      # JWT and password hashing
    ├── models/
    │   ├── user.py          # User model
    │   ├── post.py          # Post model + Loading Score
    │   └── like.py          # Like / Superlike model
    └── routers/
        ├── auth.py          # Register and login
        ├── posts.py         # Content endpoints
        └── likes.py         # Like system
```

---

## Features

### Authentication
- User registration with bcrypt password hashing
- JWT-based login (24h token expiry)
- Protected routes via OAuth2 Bearer token

### Content
- Create posts (text, image, video)
- List posts ordered by recency
- Retrieve individual posts

### Like System
- Like any post (one like per user per post)
- Superlike support (limited, higher score value)
- Duplicate like prevention
- Real-time Loading Score update on every interaction

### Loading Score
Each post has a `loading_score` that reflects real impact, not just raw popularity. Likes and superlikes contribute differently to the score — the foundation of the Loading ranking algorithm.

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/SrMiani/loading-api.git
cd loading-api
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

**3. Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy pyjwt "passlib[bcrypt]" python-multipart bcrypt==4.0.1 email-validator
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Open the docs**
```
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Create a new account |
| POST | `/auth/login` | ❌ | Login and receive JWT token |
| POST | `/posts` | ✅ | Create a new post |
| GET | `/posts` | ❌ | List recent posts |
| GET | `/posts/{id}` | ❌ | Get a single post |
| POST | `/posts/{id}/like` | ✅ | Like a post |

---

## Roadmap

- [x] User authentication (JWT)
- [x] Post creation and listing
- [x] Like system with duplicate prevention
- [x] Loading Score (base)
- [ ] Superlike system with 24h limit
- [ ] Loading Score algorithm (virality + impact)
- [ ] Seasons and rankings
- [ ] Content type support (image, video)
- [ ] Loading Vault
- [ ] AI content evaluation layer
- [ ] Loading Certified (B2B talent API)

---

## Philosophy

Loading is built for those who pursue what makes them happy despite fear.  
The platform rewards real impact over empty metrics.  
The Loading Score doesn't measure popularity — it measures greatness in progress.

*Grandeza se gana, no se compra.*

---

## Status

`v0.1.0` — Active development. Private repository.

---

*Loading™ — All rights reserved.*
