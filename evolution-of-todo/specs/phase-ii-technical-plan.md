# Phase II Technical Plan: Full-Stack Web Application

**Project**: Evolution of Todo  
**Phase**: II - Full-Stack Web Application  
**Status**: Draft  
**Last Updated**: 2026-01-11

---

## 1. Executive Summary

This technical plan defines **HOW** to implement the Phase II specification. It covers backend architecture, frontend structure, database design, and integration strategies while strictly adhering to the global constitution and Phase II technology matrix.

### 1.1 Architecture Overview

```mermaid
graph TB
    User[User Browser]
    NextJS[Next.js Frontend<br/>React + TypeScript]
    FastAPI[FastAPI Backend<br/>Python REST API]
    BetterAuth[Better Auth<br/>Authentication]
    Neon[Neon PostgreSQL<br/>Database]
    
    User -->|HTTPS| NextJS
    NextJS -->|REST API Calls| FastAPI
    NextJS -->|Auth Requests| BetterAuth
    FastAPI -->|Auth Validation| BetterAuth
    FastAPI -->|SQLModel ORM| Neon
    
    style NextJS fill:#61dafb
    style FastAPI fill:#009688
    style Neon fill:#336791
    style BetterAuth fill:#ff6b6b
```

### 1.2 Technology Stack (Constitution-Compliant)
- **Backend**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Frontend**: Next.js 14+ (App Router, React, TypeScript)
- **Authentication**: Better Auth
- **Validation**: Pydantic (built into FastAPI/SQLModel)

---

## 2. Backend Plan

### 2.1 Framework Responsibility

**FastAPI** serves as the REST API backend with the following responsibilities:
- Expose RESTful endpoints for todo operations
- Validate incoming requests using Pydantic models
- Authenticate requests via Better Auth integration
- Enforce user-to-todo ownership rules
- Persist data to Neon PostgreSQL via SQLModel ORM
- Return JSON responses with appropriate HTTP status codes

### 2.2 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration (DB URL, secrets)
│   ├── database.py             # Database connection and session management
│   │
│   ├── models/                 # SQLModel data models
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── todo.py             # Todo model
│   │
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth schemas (signup, signin)
│   │   └── todo.py             # Todo schemas (create, update, response)
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (get_current_user, get_db)
│   │   ├── auth.py             # Auth endpoints (/api/auth/*)
│   │   └── todos.py            # Todo endpoints (/api/todos/*)
│   │
│   └── core/                   # Core utilities
│       ├── __init__.py
│       ├── auth.py             # Better Auth integration
│       └── exceptions.py       # Custom exception handlers
│
├── alembic/                    # Database migrations (optional)
│   └── versions/
├── tests/                      # Backend tests
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variables template
```

### 2.3 API Routing and Controller Structure

**Router Organization:**
- `main.py`: Application initialization, CORS configuration, exception handlers
- `api/auth.py`: Authentication routes (`/api/auth/*`)
- `api/todos.py`: Todo routes (`/api/todos/*`)
- `api/deps.py`: Shared dependencies (authentication, database session)

**Endpoint Mapping:**

| Route | File | Handler Function |
|-------|------|------------------|
| `POST /api/auth/signup` | `api/auth.py` | `signup()` |
| `POST /api/auth/signin` | `api/auth.py` | `signin()` |
| `POST /api/auth/signout` | `api/auth.py` | `signout()` |
| `GET /api/auth/me` | `api/auth.py` | `get_current_user_info()` |
| `GET /api/todos` | `api/todos.py` | `get_todos()` |
| `POST /api/todos` | `api/todos.py` | `create_todo()` |
| `GET /api/todos/{id}` | `api/todos.py` | `get_todo()` |
| `PUT /api/todos/{id}` | `api/todos.py` | `update_todo()` |
| `PATCH /api/todos/{id}` | `api/todos.py` | `patch_todo()` |
| `DELETE /api/todos/{id}` | `api/todos.py` | `delete_todo()` |

**Controller Pattern:**
Each endpoint handler follows this pattern:
1. Extract request data (path params, query params, body)
2. Validate authentication via dependency injection (`get_current_user`)
3. Validate request data via Pydantic schemas
4. Execute business logic (query/create/update/delete)
5. Return response with appropriate status code

### 2.4 Authentication Integration (Better Auth)

**Better Auth Integration Strategy:**

Better Auth is a TypeScript/JavaScript library, so we'll use it on the **frontend** for authentication flows, and the **backend** will validate tokens/sessions.

**Backend Responsibilities:**
- Validate authentication tokens/sessions sent from frontend
- Extract user identity from validated tokens
- Provide dependency `get_current_user()` for protected routes
- Handle token expiration and refresh (if applicable)

**Implementation Approach:**
1. Better Auth runs on the frontend (Next.js)
2. Frontend sends authentication token in `Authorization` header or cookie
3. Backend validates token using Better Auth's validation mechanism
4. Backend extracts `user_id` from validated token
5. Backend uses `user_id` for database queries

**Dependency Injection:**
```python
# api/deps.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Validate token with Better Auth
    # Extract user_id from token
    # Query user from database
    # Return user or raise 401 Unauthorized
```

### 2.5 Data Persistence (Neon PostgreSQL + SQLModel)

**Database Connection:**
- Use SQLModel's `create_engine()` to connect to Neon PostgreSQL
- Connection string stored in environment variable (`DATABASE_URL`)
- Connection pooling managed by SQLAlchemy (SQLModel's underlying engine)

**Session Management:**
- Create database session per request using dependency injection
- Session automatically commits on success, rolls back on error
- Session closed after request completes

**ORM Strategy:**
- SQLModel models define both database schema and Pydantic validation
- Models inherit from `SQLModel` with `table=True`
- Relationships defined using SQLModel's `Relationship` type
- Queries use SQLModel's `select()` syntax

**Example Session Dependency:**
```python
# database.py
def get_session():
    with Session(engine) as session:
        yield session

# Usage in endpoints
def get_todos(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos = db.exec(statement).all()
    return todos
```

### 2.6 User-to-Todo Data Ownership

**Enforcement Strategy:**
All todo endpoints must enforce that users can only access their own todos.

**Implementation:**
1. Extract `current_user` via `get_current_user()` dependency
2. For queries: Filter by `user_id == current_user.id`
3. For create: Set `user_id = current_user.id`
4. For update/delete: Verify `todo.user_id == current_user.id` before operation
5. Return 403 Forbidden if ownership check fails

**Example:**
```python
def get_todo(
    todo_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return todo
```

### 2.7 Error Handling and Validation

**Validation Layers:**
1. **Request Validation**: Pydantic schemas validate request bodies automatically
2. **Business Logic Validation**: Custom validation in endpoint handlers
3. **Database Constraints**: Foreign keys, unique constraints, not null

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

**HTTP Status Code Strategy:**
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authenticated but not authorized (wrong user)
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Pydantic validation failure
- `500 Internal Server Error`: Unexpected server error

**Exception Handlers:**
- Custom exception handler for authentication errors
- Custom exception handler for database errors
- FastAPI's built-in Pydantic validation error handler

---

## 3. Frontend Plan

### 3.1 Next.js Application Structure

**Framework**: Next.js 14+ with App Router (not Pages Router)

**Project Structure:**
```
frontend/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page (redirect to /todos or /signin)
│   │   ├── signup/
│   │   │   └── page.tsx        # Signup page
│   │   ├── signin/
│   │   │   └── page.tsx        # Signin page
│   │   └── todos/
│   │       └── page.tsx        # Todos page (protected)
│   │
│   ├── components/             # React components
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   ├── SigninForm.tsx
│   │   │   └── SignoutButton.tsx
│   │   ├── todos/
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoItem.tsx
│   │   │   ├── TodoForm.tsx    # Create/edit form
│   │   │   └── EmptyState.tsx
│   │   └── ui/                 # Reusable UI components
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Modal.tsx
│   │       └── ErrorMessage.tsx
│   │
│   ├── lib/                    # Utilities and helpers
│   │   ├── api.ts              # API client functions
│   │   ├── auth.ts             # Better Auth configuration
│   │   └── types.ts            # TypeScript types
│   │
│   └── hooks/                  # Custom React hooks
│       ├── useAuth.ts          # Authentication state hook
│       └── useTodos.ts         # Todo data fetching hook
│
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── next.config.js
└── .env.local.example
```

### 3.2 Page-Level Routing

**Route Structure:**

| Route | File | Purpose | Protected |
|-------|------|---------|-----------|
| `/` | `app/page.tsx` | Home/redirect | No |
| `/signup` | `app/signup/page.tsx` | User registration | No |
| `/signin` | `app/signin/page.tsx` | User login | No |
| `/todos` | `app/todos/page.tsx` | Todo management | Yes |

**Route Protection Strategy:**
- Protected routes check authentication status on mount
- If unauthenticated, redirect to `/signin`
- Use Next.js middleware or client-side check in `useEffect`

**Navigation Flow:**
- Unauthenticated user visits `/` → Redirect to `/signin`
- Unauthenticated user visits `/todos` → Redirect to `/signin`
- Authenticated user visits `/` → Redirect to `/todos`
- After signup → Redirect to `/signin`
- After signin → Redirect to `/todos`
- After signout → Redirect to `/signin`

### 3.3 Component Responsibilities

**Authentication Components:**
- `SignupForm.tsx`: Email/password inputs, validation, signup API call
- `SigninForm.tsx`: Email/password inputs, validation, signin API call
- `SignoutButton.tsx`: Signout button, signout API call, clear auth state

**Todo Components:**
- `TodoList.tsx`: Fetches and displays all todos, handles loading/error states
- `TodoItem.tsx`: Displays single todo, toggle completion, edit/delete buttons
- `TodoForm.tsx`: Create/edit form, handles both create and update modes
- `EmptyState.tsx`: Displays message when no todos exist

**UI Components:**
- `Button.tsx`: Reusable button with variants (primary, secondary, danger)
- `Input.tsx`: Reusable text input with validation states
- `Modal.tsx`: Reusable modal for forms (create/edit todo)
- `ErrorMessage.tsx`: Displays error messages consistently

**Component Communication:**
- Parent components manage state and pass props to children
- Child components emit events via callback props
- No global state management (Redux, Zustand) needed for Phase II
- Use React Context for authentication state only

### 3.4 API Communication Strategy

**API Client (`lib/api.ts`):**
- Centralized functions for all API calls
- Handles authentication token injection
- Handles error responses
- Returns typed responses

**API Functions:**
```typescript
// Auth API
export async function signup(email: string, password: string)
export async function signin(email: string, password: string)
export async function signout()
export async function getCurrentUser()

// Todo API
export async function getTodos(): Promise<Todo[]>
export async function createTodo(data: CreateTodoData): Promise<Todo>
export async function updateTodo(id: number, data: UpdateTodoData): Promise<Todo>
export async function deleteTodo(id: number): Promise<void>
export async function toggleTodoCompletion(id: number): Promise<Todo>
```

**HTTP Client:**
- Use native `fetch()` API (built into Next.js)
- Alternative: `axios` if preferred
- Base URL configured via environment variable (`NEXT_PUBLIC_API_URL`)

**Request Headers:**
```typescript
{
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}` // or cookie-based
}
```

**Error Handling:**
- Parse error responses from backend
- Display user-friendly error messages
- Handle network errors gracefully
- Retry logic for transient failures (optional)

### 3.5 Authentication State Handling

**Better Auth Integration:**
- Install Better Auth package: `npm install better-auth`
- Configure Better Auth in `lib/auth.ts`
- Use Better Auth's React hooks for auth state

**Authentication State:**
- `isAuthenticated`: Boolean indicating if user is signed in
- `user`: Current user object (id, email)
- `token`: Authentication token (stored in cookie or localStorage)

**State Management:**
- Use Better Auth's built-in state management
- Expose auth state via custom hook `useAuth()`
- Persist auth state in HTTP-only cookies (preferred) or localStorage

**Custom Hook (`hooks/useAuth.ts`):**
```typescript
export function useAuth() {
  return {
    isAuthenticated: boolean,
    user: User | null,
    signin: (email, password) => Promise<void>,
    signup: (email, password) => Promise<void>,
    signout: () => Promise<void>,
    loading: boolean
  }
}
```

**Session Persistence:**
- Auth token stored in HTTP-only cookie (most secure)
- Token validated on each protected route access
- Token refresh handled by Better Auth (if supported)

### 3.6 Responsive UI Strategy

**Design Approach:**
- Mobile-first design
- Breakpoints: Mobile (< 640px), Tablet (640-1024px), Desktop (> 1024px)
- Use CSS Grid and Flexbox for layouts
- Use media queries for responsive adjustments

**Styling Options:**
1. **Vanilla CSS**: Custom CSS with CSS modules
2. **Tailwind CSS**: Utility-first CSS (if user prefers)
3. **CSS-in-JS**: Styled-components or Emotion (if user prefers)

**Recommended**: Vanilla CSS with CSS modules for Phase II simplicity

**Responsive Patterns:**
- Stack vertically on mobile, horizontal on desktop
- Hamburger menu for mobile navigation (if needed)
- Full-width forms on mobile, centered on desktop
- Touch-friendly button sizes on mobile (min 44x44px)

**Accessibility:**
- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators for interactive elements

---

## 4. Database Plan

### 4.1 User Data Model

**SQLModel Definition:**
```python
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    todos: list["Todo"] = Relationship(back_populates="user", cascade_delete=True)
```

**Database Schema (PostgreSQL):**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

**Constraints:**
- `email`: Unique, indexed for fast lookup
- `password_hash`: Never store plaintext passwords
- `created_at`, `updated_at`: Auto-managed timestamps

### 4.2 Todo Data Model

**SQLModel Definition:**
```python
class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user: User = Relationship(back_populates="todos")
```

**Database Schema (PostgreSQL):**
```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
```

**Constraints:**
- `user_id`: Foreign key to `users.id`, indexed for fast queries
- `title`: Required, max 200 characters
- `description`: Optional, max 1000 characters
- `completed`: Defaults to `false`
- Cascade delete: Deleting user deletes all their todos

### 4.3 Relationship Between User and Todo

**Relationship Type**: One-to-Many
- One user can have many todos
- Each todo belongs to exactly one user

**SQLModel Relationship:**
- `User.todos`: List of todos belonging to the user
- `Todo.user`: The user who owns the todo

**Cascade Delete:**
- When a user is deleted, all their todos are automatically deleted
- Implemented via `ON DELETE CASCADE` in database
- Also configured in SQLModel relationship

**Query Patterns:**
```python
# Get all todos for a user
user = db.get(User, user_id)
todos = user.todos

# Or via query
statement = select(Todo).where(Todo.user_id == user_id)
todos = db.exec(statement).all()

# Get user from todo
todo = db.get(Todo, todo_id)
user = todo.user
```

### 4.4 Migration and Schema Management

**Approach**: Use Alembic for database migrations (optional but recommended)

**Why Alembic:**
- Version control for database schema
- Supports rollbacks
- Handles schema changes safely
- Integrates well with SQLModel/SQLAlchemy

**Alternative**: Use SQLModel's `create_all()` for initial setup
- Simpler for Phase II
- No migration history
- Acceptable for early development

**Recommended Strategy for Phase II:**
1. **Initial Setup**: Use `SQLModel.metadata.create_all(engine)` to create tables
2. **Future Changes**: Introduce Alembic when schema changes are needed

**Initial Setup Code:**
```python
# database.py
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
```

**Migration Strategy (if using Alembic):**
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

---

## 5. Integration Plan

### 5.1 Frontend ↔ Backend Communication Flow

**Architecture Pattern**: Client-Server with REST API

**Communication Flow:**
```mermaid
sequenceDiagram
    participant Browser
    participant NextJS
    participant FastAPI
    participant Database
    
    Browser->>NextJS: User action (e.g., create todo)
    NextJS->>NextJS: Validate input
    NextJS->>FastAPI: POST /api/todos (with auth token)
    FastAPI->>FastAPI: Validate token
    FastAPI->>FastAPI: Validate request body
    FastAPI->>Database: INSERT todo
    Database-->>FastAPI: Todo created
    FastAPI-->>NextJS: 201 Created + todo data
    NextJS-->>Browser: Update UI
```

**Request Flow:**
1. User interacts with frontend (button click, form submit)
2. Frontend validates input locally
3. Frontend sends HTTP request to backend API
4. Backend validates authentication
5. Backend validates request data
6. Backend executes database operation
7. Backend returns response
8. Frontend updates UI based on response

**Error Flow:**
1. Backend returns error response (4xx or 5xx)
2. Frontend catches error
3. Frontend displays error message to user
4. Frontend maintains previous state (or reverts optimistic update)

### 5.2 Auth Token/Session Flow

**Authentication Flow:**

```mermaid
sequenceDiagram
    participant Browser
    participant NextJS
    participant BetterAuth
    participant FastAPI
    participant Database
    
    Browser->>NextJS: Submit signin form
    NextJS->>BetterAuth: Authenticate user
    BetterAuth->>FastAPI: POST /api/auth/signin
    FastAPI->>Database: Query user by email
    Database-->>FastAPI: User data
    FastAPI->>FastAPI: Verify password hash
    FastAPI->>FastAPI: Generate token
    FastAPI-->>BetterAuth: Token + user data
    BetterAuth-->>NextJS: Set auth cookie
    NextJS-->>Browser: Redirect to /todos
```

**Token Storage:**
- **Preferred**: HTTP-only cookie (more secure, prevents XSS)
- **Alternative**: localStorage (simpler but less secure)

**Token Validation:**
1. Frontend includes token in every API request
2. Backend extracts token from `Authorization` header or cookie
3. Backend validates token signature and expiration
4. Backend extracts `user_id` from token
5. Backend uses `user_id` for authorization

**Token Format:**
- JWT (JSON Web Token) - standard format
- Contains: `user_id`, `email`, `exp` (expiration), `iat` (issued at)
- Signed with secret key (stored in backend environment variable)

**Session Management:**
- Token expiration: 24 hours (configurable)
- Refresh token: Optional for Phase II (can add later)
- Signout: Delete token from cookie/localStorage

### 5.3 Local Development Setup

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- PostgreSQL (via Neon or local instance)

**Backend Setup:**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with DATABASE_URL, SECRET_KEY, etc.

# Initialize database
python -m app.database  # Or alembic upgrade head

# Run development server
uvicorn app.main:app --reload --port 8000
```

**Frontend Setup:**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

**Development URLs:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs` (FastAPI auto-generated)

**CORS Configuration:**
Backend must allow requests from frontend origin:
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Database Setup (Neon):**
1. Create Neon account and project
2. Copy connection string from Neon dashboard
3. Set `DATABASE_URL` in backend `.env`
4. Connection string format: `postgresql://user:password@host/database?sslmode=require`

**Environment Variables:**

Backend (`.env`):
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key-here
BETTER_AUTH_SECRET=your-better-auth-secret
ENVIRONMENT=development
```

Frontend (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

---

## 6. Implementation Workflow

### 6.1 Development Phases

**Phase 1: Backend Foundation**
1. Set up FastAPI project structure
2. Configure database connection to Neon
3. Define SQLModel models (User, Todo)
4. Create database tables
5. Implement authentication endpoints (signup, signin)
6. Test authentication flow

**Phase 2: Backend Todo API**
1. Implement todo CRUD endpoints
2. Add user ownership validation
3. Add error handling
4. Test all endpoints with API client (Postman/Insomnia)

**Phase 3: Frontend Foundation**
1. Set up Next.js project structure
2. Configure Better Auth
3. Create authentication pages (signup, signin)
4. Implement authentication state management
5. Test authentication flow

**Phase 4: Frontend Todo UI**
1. Create todo list page
2. Implement todo components (list, item, form)
3. Connect to backend API
4. Add error handling and loading states
5. Test all user flows

**Phase 5: Integration & Testing**
1. End-to-end testing of all features
2. Fix bugs and edge cases
3. Responsive design testing
4. Performance optimization
5. Documentation

### 6.2 Testing Strategy

**Backend Testing:**
- Unit tests for models and utilities
- Integration tests for API endpoints
- Test authentication and authorization
- Test error cases

**Frontend Testing:**
- Component rendering tests (Jest + React Testing Library)
- User interaction tests
- Authentication flow tests
- API integration tests (mock API responses)

**End-to-End Testing:**
- Full user journeys (signup → signin → create todo → etc.)
- Cross-browser testing
- Mobile responsiveness testing

### 6.3 Deployment Considerations (Future)

While deployment is not part of Phase II implementation, the architecture supports:
- **Backend**: Deploy to any Python hosting (Render, Railway, Fly.io)
- **Frontend**: Deploy to Vercel (Next.js native platform)
- **Database**: Already using Neon (serverless, no deployment needed)
- **Environment Variables**: Configure in hosting platform

---

## 7. File Organization Summary

### 7.1 Backend File Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, exception handlers
│   ├── config.py            # Environment variables, settings
│   ├── database.py          # Database engine, session management
│   ├── models/
│   │   ├── user.py          # User SQLModel
│   │   └── todo.py          # Todo SQLModel
│   ├── schemas/
│   │   ├── auth.py          # Auth request/response schemas
│   │   └── todo.py          # Todo request/response schemas
│   ├── api/
│   │   ├── deps.py          # get_current_user, get_db dependencies
│   │   ├── auth.py          # Auth endpoints
│   │   └── todos.py         # Todo endpoints
│   └── core/
│       ├── auth.py          # Better Auth integration, token validation
│       └── exceptions.py    # Custom exception classes
├── tests/
├── requirements.txt
└── .env
```

### 7.2 Frontend File Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout, auth provider
│   │   ├── page.tsx         # Home page (redirect logic)
│   │   ├── signup/page.tsx  # Signup page
│   │   ├── signin/page.tsx  # Signin page
│   │   └── todos/page.tsx   # Todos page (protected)
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   ├── SigninForm.tsx
│   │   │   └── SignoutButton.tsx
│   │   ├── todos/
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoItem.tsx
│   │   │   ├── TodoForm.tsx
│   │   │   └── EmptyState.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Modal.tsx
│   │       └── ErrorMessage.tsx
│   ├── lib/
│   │   ├── api.ts           # API client functions
│   │   ├── auth.ts          # Better Auth config
│   │   └── types.ts         # TypeScript types
│   └── hooks/
│       ├── useAuth.ts       # Auth state hook
│       └── useTodos.ts      # Todo data hook
├── package.json
├── tsconfig.json
└── .env.local
```

---

## 8. Constitution Compliance Checklist

✅ **Spec-Driven Development**: This plan is derived from approved Phase II specification  
✅ **Phase Governance**: Only Phase II technologies used (no AI, no orchestration)  
✅ **Technology Matrix**:
  - Backend: FastAPI ✅
  - Database: Neon PostgreSQL ✅
  - ORM: SQLModel ✅
  - Frontend: Next.js ✅
  - Auth: Better Auth ✅
✅ **No Feature Invention**: All features from specification, no additions  
✅ **Clean Architecture**: Clear separation of models, API, frontend  
✅ **No Phase Leakage**: No Phase III+ features included  

---

## 9. Success Criteria

This technical plan is ready for implementation when:
- ✅ Backend architecture clearly defined
- ✅ Frontend architecture clearly defined
- ✅ Database schema documented
- ✅ Integration flows explained
- ✅ Local development setup documented
- ✅ File structure organized
- ✅ Authentication strategy defined
- ✅ API communication strategy defined
- ✅ Constitution compliance verified

---

## 10. Next Steps

After this plan is approved:
1. Create detailed task list breaking down implementation into atomic tasks
2. Set up backend project structure
3. Set up frontend project structure
4. Begin Phase 1 implementation (Backend Foundation)
5. Iterate through development phases
6. Test and validate each component
7. Complete Phase II specification requirements

---

**End of Phase II Technical Plan**
