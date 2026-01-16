# Evolution of Todo

A multi-phase project demonstrating the evolution of a Todo application from a simple CLI to a cloud-native, AI-integrated system.

## Current Phase: Phase II - Full-Stack Web Application

### Documentation
- [Global Constitution](./sp.constitution)
- [Phase II Specification](./specs/phase-ii-spec.md)
- [Phase II Technical Plan](./specs/phase-ii-technical-plan.md)
- [Phase II Tasks](./specs/phase-ii-tasks.md)

### Technology Stack

**Backend:**
- FastAPI (Python REST API)
- Neon Serverless PostgreSQL
- SQLModel (ORM)
- JWT Authentication with bcrypt
- Pydantic validation

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- CSS Modules
- React Context + Hooks

### Setup Instructions

#### Prerequisites
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account

#### Backend Setup

1. Navigate to backend:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Neon database URL and secret key
```

5. Run server:
```bash
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000` | API Docs: `http://localhost:8000/docs`

#### Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.local.example .env.local
# Edit .env.local with API URL
```

4. Run development server:
```bash
npm run dev
```

Frontend: `http://localhost:3000`

### Features

- ✅ User authentication (signup/signin)
- ✅ Create, read, update, delete todos
- ✅ Toggle todo completion
- ✅ User-specific data isolation
- ✅ Responsive design (mobile + desktop)
- ✅ Error handling and validation
- ✅ Protected routes

### API Endpoints

**Authentication:**
- `POST /api/auth/signup` - Register user
- `POST /api/auth/signin` - Authenticate user
- `GET /api/auth/me` - Get current user

**Todos:**
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create todo
- `PATCH /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo

### Constitution Compliance

✅ Spec-Driven Development  
✅ Phase II technology matrix only  
✅ No AI or agent frameworks  
✅ Clean architecture  
✅ User data isolation

