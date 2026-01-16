# Phase II Specification: Full-Stack Web Application

**Project**: Evolution of Todo  
**Phase**: II - Full-Stack Web Application  
**Status**: Draft  
**Last Updated**: 2026-01-11

---

## 1. Overview

Phase II transforms the in-memory console application (Phase I) into a full-stack web application with persistent storage, user authentication, and a modern web interface. This phase implements all 5 Basic Level Todo features accessible via web browser.

### 1.1 Phase II Goals
- Provide a RESTful API backend for todo operations
- Persist todos in Neon Serverless PostgreSQL database
- Implement user authentication (signup/signin) using Better Auth
- Build a responsive Next.js frontend
- Associate todos with authenticated users
- Ensure users can only access their own todos

### 1.2 Technology Stack (Per Constitution)
- **Backend**: Python REST API (FastAPI)
- **Database**: Neon Serverless PostgreSQL
- **ORM/Data Layer**: SQLModel
- **Frontend**: Next.js (React with TypeScript)
- **Authentication**: Better Auth
- **Validation**: Pydantic

### 1.3 Out of Scope (Reserved for Phase III+)
- ❌ AI frameworks or agent SDKs
- ❌ Advanced orchestration (Kafka, Dapr)
- ❌ Microservices architecture
- ❌ Real-time features (WebSockets, SSE)
- ❌ Background jobs or task queues
- ❌ Advanced analytics or reporting
- ❌ Role-based access control (RBAC)
- ❌ Multi-tenancy features

---

## 2. User Stories

### 2.1 Authentication User Stories

#### US-AUTH-001: User Signup
**As a** new user  
**I want to** create an account with email and password  
**So that** I can access the todo application

**Acceptance Criteria:**
- User provides email and password
- Email must be unique (not already registered)
- Password must meet minimum requirements (e.g., 8+ characters)
- System creates user account in database
- User is redirected to signin page after successful signup
- Error message shown if email already exists
- Error message shown if password is too weak

**Error Cases:**
- Email already registered → "Email already in use"
- Invalid email format → "Invalid email address"
- Password too short → "Password must be at least 8 characters"
- Network error → "Unable to create account. Please try again."

---

#### US-AUTH-002: User Signin
**As a** registered user  
**I want to** sign in with my email and password  
**So that** I can access my todos

**Acceptance Criteria:**
- User provides email and password
- System validates credentials against database
- Successful signin creates authenticated session
- User is redirected to todos page
- Error message shown for invalid credentials
- Auth state persists across page refreshes

**Error Cases:**
- Invalid credentials → "Invalid email or password"
- Account not found → "Invalid email or password" (same message for security)
- Network error → "Unable to sign in. Please try again."

---

#### US-AUTH-003: User Signout
**As a** signed-in user  
**I want to** sign out of my account  
**So that** I can protect my data on shared devices

**Acceptance Criteria:**
- User clicks signout button
- System clears authentication session
- User is redirected to signin page
- Subsequent requests require re-authentication

---

### 2.2 Backend API User Stories

#### US-API-001: Create Todo
**As a** backend API  
**I want to** accept POST requests to create todos  
**So that** authenticated users can add new todos

**Acceptance Criteria:**
- Endpoint: `POST /api/todos`
- Request body contains: `title` (required), `description` (optional)
- System validates user is authenticated
- System creates todo associated with authenticated user
- System returns created todo with generated ID and timestamps
- Returns 201 Created on success
- Returns 401 Unauthorized if not authenticated
- Returns 400 Bad Request if title is missing or invalid

**Error Cases:**
- Missing title → 400 "Title is required"
- Title too long (>200 chars) → 400 "Title must be 200 characters or less"
- Unauthenticated → 401 "Authentication required"

---

#### US-API-002: Retrieve All Todos
**As a** backend API  
**I want to** accept GET requests to retrieve todos  
**So that** authenticated users can view their todo list

**Acceptance Criteria:**
- Endpoint: `GET /api/todos`
- System validates user is authenticated
- System returns only todos belonging to authenticated user
- Response includes all todo fields (id, title, description, completed, timestamps)
- Returns 200 OK with array of todos (empty array if no todos)
- Returns 401 Unauthorized if not authenticated

**Error Cases:**
- Unauthenticated → 401 "Authentication required"

---

#### US-API-003: Update Todo
**As a** backend API  
**I want to** accept PUT/PATCH requests to update todos  
**So that** authenticated users can modify their todos

**Acceptance Criteria:**
- Endpoint: `PUT /api/todos/{id}` or `PATCH /api/todos/{id}`
- Request body contains fields to update: `title`, `description`, `completed`
- System validates user is authenticated
- System validates todo belongs to authenticated user
- System updates specified fields only
- System returns updated todo
- Returns 200 OK on success
- Returns 401 Unauthorized if not authenticated
- Returns 403 Forbidden if todo belongs to different user
- Returns 404 Not Found if todo doesn't exist
- Returns 400 Bad Request for invalid data

**Error Cases:**
- Todo not found → 404 "Todo not found"
- Todo belongs to different user → 403 "Access denied"
- Invalid title → 400 "Title must be 200 characters or less"
- Unauthenticated → 401 "Authentication required"

---

#### US-API-004: Delete Todo
**As a** backend API  
**I want to** accept DELETE requests to remove todos  
**So that** authenticated users can delete their todos

**Acceptance Criteria:**
- Endpoint: `DELETE /api/todos/{id}`
- System validates user is authenticated
- System validates todo belongs to authenticated user
- System deletes todo from database
- Returns 204 No Content on success
- Returns 401 Unauthorized if not authenticated
- Returns 403 Forbidden if todo belongs to different user
- Returns 404 Not Found if todo doesn't exist

**Error Cases:**
- Todo not found → 404 "Todo not found"
- Todo belongs to different user → 403 "Access denied"
- Unauthenticated → 401 "Authentication required"

---

#### US-API-005: Toggle Todo Completion
**As a** backend API  
**I want to** accept requests to toggle todo completion status  
**So that** authenticated users can mark todos complete/incomplete

**Acceptance Criteria:**
- Endpoint: `PATCH /api/todos/{id}/toggle` or handled by US-API-003
- System validates user is authenticated
- System validates todo belongs to authenticated user
- System toggles `completed` field (true ↔ false)
- System returns updated todo
- Returns 200 OK on success
- Returns 401/403/404 as per US-API-003

**Error Cases:**
- Same as US-API-003

---

### 2.3 Frontend User Stories

#### US-FE-001: View Signup Page
**As a** new user  
**I want to** access a signup page  
**So that** I can create an account

**Acceptance Criteria:**
- Page accessible at `/signup` route
- Form includes email input field
- Form includes password input field
- Form includes "Sign Up" submit button
- Link to signin page for existing users
- Responsive design (desktop + mobile)

---

#### US-FE-002: View Signin Page
**As a** registered user  
**I want to** access a signin page  
**So that** I can authenticate

**Acceptance Criteria:**
- Page accessible at `/signin` route
- Form includes email input field
- Form includes password input field
- Form includes "Sign In" submit button
- Link to signup page for new users
- Responsive design (desktop + mobile)

---

#### US-FE-003: View Todos List
**As a** signed-in user  
**I want to** view all my todos  
**So that** I can see what tasks I need to complete

**Acceptance Criteria:**
- Page accessible at `/todos` or `/` (home) route
- Requires authentication (redirect to signin if not authenticated)
- Displays all todos for authenticated user
- Each todo shows: title, description (if present), completion status
- Empty state message if no todos exist ("No todos yet. Create your first one!")
- Responsive design (desktop + mobile)
- Signout button visible

---

#### US-FE-004: Add New Todo
**As a** signed-in user  
**I want to** add a new todo  
**So that** I can track new tasks

**Acceptance Criteria:**
- "Add Todo" button or form visible on todos page
- Clicking opens form/modal with title and description fields
- "Save" button submits form
- "Cancel" button closes form without saving
- Success: new todo appears in list immediately
- Error: displays error message from API
- Form clears after successful submission

---

#### US-FE-005: Edit Existing Todo
**As a** signed-in user  
**I want to** edit a todo  
**So that** I can update task details

**Acceptance Criteria:**
- "Edit" button/icon visible for each todo
- Clicking opens form/modal pre-filled with current values
- User can modify title and/or description
- "Save" button submits changes
- "Cancel" button closes form without saving
- Success: updated todo reflects changes immediately
- Error: displays error message from API

---

#### US-FE-006: Delete Todo
**As a** signed-in user  
**I want to** delete a todo  
**So that** I can remove completed or unwanted tasks

**Acceptance Criteria:**
- "Delete" button/icon visible for each todo
- Clicking triggers confirmation prompt ("Are you sure?")
- Confirming deletes todo
- Canceling aborts deletion
- Success: todo removed from list immediately
- Error: displays error message from API

---

#### US-FE-007: Toggle Todo Completion
**As a** signed-in user  
**I want to** mark todos as complete or incomplete  
**So that** I can track my progress

**Acceptance Criteria:**
- Checkbox or toggle button visible for each todo
- Clicking toggles completion status
- Visual indication of completed todos (e.g., strikethrough, different color)
- Success: UI updates immediately
- Error: displays error message and reverts UI change

---

#### US-FE-008: Handle Unauthenticated Access
**As a** system  
**I want to** protect todo pages from unauthenticated access  
**So that** only signed-in users can view/manage todos

**Acceptance Criteria:**
- Accessing `/todos` without authentication redirects to `/signin`
- Auth state checked on page load
- Auth state persists across page refreshes
- Session expiration redirects to signin page

---

## 3. Data Models

### 3.1 User Model

```python
class User:
    id: int (Primary Key, Auto-increment)
    email: str (Unique, Not Null, Max 255 chars)
    password_hash: str (Not Null) # Hashed password, never store plaintext
    created_at: datetime (Auto-generated)
    updated_at: datetime (Auto-updated)
```

**Constraints:**
- Email must be unique
- Email must be valid format
- Password hash generated by Better Auth

---

### 3.2 Todo Model

```python
class Todo:
    id: int (Primary Key, Auto-increment)
    user_id: int (Foreign Key → User.id, Not Null)
    title: str (Not Null, Max 200 chars)
    description: str (Nullable, Max 1000 chars)
    completed: bool (Default: False)
    created_at: datetime (Auto-generated)
    updated_at: datetime (Auto-updated)
```

**Constraints:**
- `user_id` references `User.id` (Foreign Key)
- `title` is required
- `completed` defaults to `False`
- Cascade delete: deleting user deletes all their todos

---

## 4. API Endpoint Definitions

### 4.1 Authentication Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/api/auth/signup` | Create new user account | No |
| POST | `/api/auth/signin` | Authenticate user | No |
| POST | `/api/auth/signout` | End user session | Yes |
| GET | `/api/auth/me` | Get current user info | Yes |

---

### 4.2 Todo Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/todos` | Retrieve all todos for authenticated user | Yes |
| POST | `/api/todos` | Create new todo | Yes |
| GET | `/api/todos/{id}` | Retrieve specific todo | Yes |
| PUT | `/api/todos/{id}` | Update todo (full replacement) | Yes |
| PATCH | `/api/todos/{id}` | Update todo (partial update) | Yes |
| DELETE | `/api/todos/{id}` | Delete todo | Yes |

**Note**: All todo endpoints validate that the todo belongs to the authenticated user.

---

## 5. Frontend Interaction Flows

### 5.1 User Signup Flow
1. User navigates to `/signup`
2. User enters email and password
3. User clicks "Sign Up"
4. Frontend sends POST to `/api/auth/signup`
5. **Success**: Redirect to `/signin` with success message
6. **Error**: Display error message inline

---

### 5.2 User Signin Flow
1. User navigates to `/signin`
2. User enters email and password
3. User clicks "Sign In"
4. Frontend sends POST to `/api/auth/signin`
5. **Success**: Store auth token/session, redirect to `/todos`
6. **Error**: Display error message inline

---

### 5.3 View Todos Flow
1. User navigates to `/todos`
2. Frontend checks authentication status
3. **Not authenticated**: Redirect to `/signin`
4. **Authenticated**: Send GET to `/api/todos`
5. Display todos in list
6. **Empty state**: Show "No todos yet" message

---

### 5.4 Create Todo Flow
1. User clicks "Add Todo" button
2. Form/modal opens
3. User enters title and optional description
4. User clicks "Save"
5. Frontend sends POST to `/api/todos`
6. **Success**: Add todo to list, close form, clear inputs
7. **Error**: Display error message, keep form open

---

### 5.5 Edit Todo Flow
1. User clicks "Edit" on a todo
2. Form/modal opens with current values
3. User modifies title and/or description
4. User clicks "Save"
5. Frontend sends PUT/PATCH to `/api/todos/{id}`
6. **Success**: Update todo in list, close form
7. **Error**: Display error message, keep form open

---

### 5.6 Delete Todo Flow
1. User clicks "Delete" on a todo
2. Confirmation prompt appears
3. User confirms deletion
4. Frontend sends DELETE to `/api/todos/{id}`
5. **Success**: Remove todo from list
6. **Error**: Display error message

---

### 5.7 Toggle Completion Flow
1. User clicks checkbox/toggle on a todo
2. Frontend optimistically updates UI
3. Frontend sends PATCH to `/api/todos/{id}` with `completed` toggle
4. **Success**: UI remains updated
5. **Error**: Revert UI change, display error message

---

## 6. Acceptance Criteria Summary

### 6.1 Backend Acceptance Criteria
- ✅ All API endpoints return proper HTTP status codes
- ✅ All endpoints validate authentication
- ✅ Users can only access their own todos
- ✅ Data persists in Neon PostgreSQL database
- ✅ Proper error messages for all error cases
- ✅ Request/response bodies use JSON format
- ✅ Passwords are hashed, never stored in plaintext

---

### 6.2 Frontend Acceptance Criteria
- ✅ Responsive design works on desktop and mobile
- ✅ All pages accessible via defined routes
- ✅ Protected routes redirect unauthenticated users
- ✅ Forms validate input before submission
- ✅ Error messages displayed clearly to users
- ✅ Loading states shown during API calls
- ✅ Optimistic UI updates for better UX
- ✅ Empty states handled gracefully

---

### 6.3 Authentication Acceptance Criteria
- ✅ Users can sign up with email and password
- ✅ Users can sign in with credentials
- ✅ Users can sign out
- ✅ Auth state persists across page refreshes
- ✅ Session expiration handled gracefully
- ✅ Duplicate email registration prevented

---

### 6.4 Data Persistence Acceptance Criteria
- ✅ Todos persist across sessions
- ✅ User data persists across sessions
- ✅ Database schema matches data models
- ✅ Foreign key constraints enforced
- ✅ Timestamps auto-generated and auto-updated

---

## 7. Error Handling Scenarios

### 7.1 Authentication Errors

| Scenario | HTTP Status | Error Message | User Action |
|----------|-------------|---------------|-------------|
| Email already exists | 400 | "Email already in use" | Use different email or sign in |
| Invalid credentials | 401 | "Invalid email or password" | Check credentials and retry |
| Session expired | 401 | "Session expired. Please sign in again." | Redirect to signin |
| Weak password | 400 | "Password must be at least 8 characters" | Provide stronger password |

---

### 7.2 Todo Operation Errors

| Scenario | HTTP Status | Error Message | User Action |
|----------|-------------|---------------|-------------|
| Missing title | 400 | "Title is required" | Provide title |
| Title too long | 400 | "Title must be 200 characters or less" | Shorten title |
| Todo not found | 404 | "Todo not found" | Refresh list |
| Unauthorized access | 403 | "Access denied" | User cannot access others' todos |
| Unauthenticated | 401 | "Authentication required" | Sign in |

---

### 7.3 Network Errors

| Scenario | HTTP Status | Error Message | User Action |
|----------|-------------|---------------|-------------|
| Server unreachable | N/A | "Unable to connect. Please check your internet connection." | Retry |
| Timeout | 408 | "Request timed out. Please try again." | Retry |
| Server error | 500 | "Something went wrong. Please try again later." | Retry later |

---

### 7.4 Empty State Handling

| Scenario | Display |
|----------|---------|
| No todos | "No todos yet. Create your first one!" with prominent "Add Todo" button |
| Search returns no results | "No todos match your search" (if search implemented) |
| Network error on load | "Unable to load todos. Please try again." with retry button |

---

## 8. Non-Functional Requirements

### 8.1 Performance
- API response time < 500ms for typical operations
- Frontend initial load < 3 seconds
- Database queries optimized with proper indexing

### 8.2 Security
- Passwords hashed using industry-standard algorithms (handled by Better Auth)
- HTTPS required for all API communication (production)
- SQL injection prevention via ORM (SQLModel)
- XSS prevention via React's built-in escaping

### 8.3 Usability
- Intuitive UI requiring no training
- Clear error messages
- Responsive design for all screen sizes
- Accessible keyboard navigation

### 8.4 Reliability
- Graceful error handling for all failure scenarios
- Data integrity maintained via database constraints
- Transaction support for critical operations

---

## 9. Testing Requirements

### 9.1 Backend Testing
- Unit tests for all API endpoints
- Integration tests for database operations
- Authentication flow testing
- Error case validation

### 9.2 Frontend Testing
- Component rendering tests
- User interaction flow tests
- Authentication state management tests
- Error handling tests

### 9.3 End-to-End Testing
- Complete user signup → signin → todo operations flow
- Cross-browser compatibility (Chrome, Firefox, Safari)
- Mobile responsiveness testing

---

## 10. Compliance with Constitution

This specification complies with the global constitution:

✅ **Spec-Driven Development**: This document defines WHAT to build before HOW  
✅ **Phase Governance**: Only Phase II technologies used (no AI, no orchestration)  
✅ **Technology Matrix**: FastAPI, Neon PostgreSQL, SQLModel, Next.js, Better Auth  
✅ **No Feature Invention**: All features explicitly defined with acceptance criteria  
✅ **Phase Isolation**: No Phase III features included  
✅ **Clean Architecture**: Separation of concerns implied in API/Frontend split  

---

## 11. Success Criteria

Phase II is complete when:
- ✅ All 5 Basic Level Todo features work via web interface
- ✅ Users can sign up, sign in, and sign out
- ✅ Todos persist in Neon PostgreSQL database
- ✅ Users can only access their own todos
- ✅ All API endpoints function correctly
- ✅ Frontend is responsive and user-friendly
- ✅ All acceptance criteria met
- ✅ All error cases handled gracefully
- ✅ Tests pass for backend, frontend, and E2E flows

---

**End of Phase II Specification**
