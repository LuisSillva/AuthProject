# Auth System

A full-stack authentication system built with FastAPI and React. Covers user registration, login, JWT-based auth, and protected routes.

Built as a learning project — every architectural decision is intentional and explained.

---

## Stack

**Backend**
- FastAPI — web framework
- SQLAlchemy — ORM
- SQLite — database
- python-jose — JWT creation and verification
- passlib[bcrypt] — password hashing
- pydantic[email] — request/response validation

**Frontend**
- React — UI
- React Router — client-side routing
- Axios — HTTP client with interceptors
- Context API — global auth state

---

## Project structure

```
auth-project/
├── backend/
│   ├── venv/
│   ├── app/
│   │   ├── main.py              # App entry point, mounts routers, creates tables
│   │   ├── database.py          # Engine, SessionLocal, Base
│   │   ├── models/
│   │   │   └── user.py          # SQLAlchemy User model
│   │   ├── schemas/
│   │   │   └── user.py          # Pydantic schemas (request/response shapes)
│   │   ├── routers/
│   │   │   └── auth.py          # /register, /login, /me endpoints
│   │   ├── core/
│   │   │   ├── security.py      # Password hashing, JWT creation/decoding
│   │   │   └── dependencies.py  # get_db, get_current_user
│   │   └── data/
│   │       └── auth.db          # SQLite database (gitignored)
│   ├── requirements.txt
│   └── .gitignore
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── axios.js          # Configured Axios instance with interceptor
    │   ├── context/
    │   │   └── AuthContext.jsx   # Global auth state (login, logout, register)
    │   ├── components/
    │   │   └── ProtectedRoute.jsx
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   └── Dashboard.jsx
    │   ├── App.jsx
    │   └── index.js
    └── package.json
```

---

## Getting started

### Backend

```bash
cd backend
python -m venv venv

# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`.
Interactive API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000`.

---

## API endpoints

| Method | Endpoint | Auth required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Create a new user |
| POST | `/auth/login` | No | Login, returns JWT |
| GET | `/auth/me` | Yes | Returns current user |

### Register

```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Login

```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

### Get current user

```
GET /auth/me
Authorization: Bearer <token>
```

---

## How auth works

1. User registers — password is hashed with bcrypt before storage. Plain text never touches the database.
2. User logs in — bcrypt verifies the password against the stored hash. On success, the server issues a signed JWT containing the user's email and an expiry timestamp.
3. Client stores the JWT in localStorage and attaches it to every subsequent request via an Axios interceptor.
4. Protected routes — the `get_current_user` dependency decodes the JWT, verifies the signature, and looks up the user. If anything fails, it returns 401.

---

## Environment variables

Create a `.env` file in `backend/`:

```
SECRET_KEY=your-secret-key-here
```

Generate a secure key:
```bash
openssl rand -hex 32
```

> The `SECRET_KEY` signs and verifies JWTs. Anyone with this key can forge tokens. Never commit it.

---

## Things to improve in production

- Load `SECRET_KEY` from `.env` using `python-dotenv` (currently hardcoded in `core/security.py`)
- Add refresh tokens so sessions outlive the 30-minute access token expiry
- Add rate limiting on `/auth/login` to prevent brute force attacks
- Use HTTPS — required for any real deployment
- Consider `httpOnly` cookies instead of localStorage for token storage (mitigates XSS)
