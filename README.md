# Sport Intelligence API ⚡

> *AI-powered sport performance analysis. Describe your performance, get instant feedback.*

---

## What it does

Sport Intelligence API analyzes athletic performance using AI. You describe what happened during your training or match — the AI evaluates your technique, detects strengths and weaknesses, and gives you concrete recommendations to improve.
It uses OPENAI API

No coach needed. No expensive equipment. Just describe what you did, and get professional-level feedback instantly.

---

## Stack

- **Python 3.12**
- **FastAPI** — high-performance async API framework
- **OpenAI GPT-4o-mini** — AI analysis engine
- **SQLAlchemy** — ORM for database management
- **SQLite** → PostgreSQL (production)
- **JWT + bcrypt** — secure authentication
- **Uvicorn** — ASGI server

---

## Project Structure

```
sport-intelligence-api/
├── main.py                  # Entry point
└── app/
    ├── core/
    │   ├── database.py      # DB connection and session
    │   ├── security.py      # JWT and password hashing
    │   └── config.py        # Environment variables
    ├── models/
    │   ├── user.py          # User model
    │   └── analysis.py      # Analysis model + Performance Score
    └── routers/
        ├── auth.py          # Register and login
        └── analysis.py      # Analysis endpoints + OpenAI integration
```

---

## Features

### Authentication
- User registration with bcrypt password hashing
- JWT-based login (24h token expiry)
- Protected routes via OAuth2 Bearer token

### AI Performance Analysis
- Describe your performance in natural language
- Select your sport and discipline
- Get instant AI-powered feedback including:
  - **Performance Score** (0-100)
  - **Strengths** detected in your performance
  - **Areas for improvement**
  - **Concrete recommendations** to get better

### Performance History
- Every analysis is stored with timestamp
- Track your progression over time
- Compare scores across sessions

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/SrMiani/sport-intelligence-api.git
cd sport-intelligence-api
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

**3. Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy pyjwt "passlib[bcrypt]" python-multipart bcrypt==4.0.1 email-validator openai python-dotenv
```

**4. Set up environment variables**

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

**5. Run the server**
```bash
uvicorn main:app --reload
```

**6. Open the docs**
```
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Create a new account |
| POST | `/auth/login` | ❌ | Login and receive JWT token |
| POST | `/analysis` | ✅ | Analyze a sport performance |

---

## Example Request

```json
POST /analysis
Authorization: Bearer <token>

{
    "sport": "football",
    "discipline": "goalkeeper",
    "input_text": "Trained for 1 hour today. My reflexes were good but I struggled with aerial balls and coming out to clear."
}
```

## Example Response

```json
{
    "id": 1,
    "sport": "football",
    "discipline": "goalkeeper",
    "score": 70,
    "strengths": "Good reflexes during training.",
    "improvements": "Difficulties with aerial balls and coming out to clear.",
    "recommendations": "Practice jumping and positioning exercises to improve on aerial balls, and simulate clearances from different attack angles.",
    "created_at": "2026-07-01T23:48:39.009543"
}
```

---

## Roadmap

- [x] User authentication (JWT)
- [x] AI performance analysis (text)
- [x] Performance Score (0-100)
- [x] Analysis history per user
- [ ] Video upload and frame analysis (OpenAI Vision)
- [ ] Sport-specific evaluation criteria
- [ ] Progress charts and visualizations
- [ ] React dashboard
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions
- [ ] GCP deployment

---

## Use Cases

- **Amateur athletes** who want professional-level feedback without a coach
- **Personal trainers** who need to give remote feedback to multiple clients
- **Sports academies** that want to scale individual feedback
- **Fitness apps** looking to add an AI analysis layer via API

---

## Author

**Sergi Miani** — AI Engineer in progress, building at the intersection of sport, data and artificial intelligence.

[GitHub](https://github.com/SrMiani)

---

*Built with FastAPI + OpenAI. Part of a growing portfolio of AI-powered tools.*
