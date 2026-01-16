/**
 * API client for backend communication
 */

import { User, Todo, TodoCreate, TodoUpdate, AuthToken } from './types';

// Revert to explicit URL for debugging reliability
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
console.log('Connecting to API at:', API_URL);

class APIError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = 'APIError';
    }
}

async function fetchAPI<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        (headers as any)['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new APIError(response.status, error.detail || 'An error occurred');
    }

    if (response.status === 204) {
        return null as T;
    }

    return response.json();
}

// Authentication API
export async function signup(email: string, password: string): Promise<User> {
    return fetchAPI<User>('/api/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    });
}

export async function signin(email: string, password: string): Promise<AuthToken> {
    const token = await fetchAPI<AuthToken>('/api/auth/signin', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    });

    // Store token in localStorage
    if (typeof window !== 'undefined') {
        localStorage.setItem('token', token.access_token);
        localStorage.setItem('user', JSON.stringify(token.user));
    }

    return token;
}

export async function signout(): Promise<void> {
    if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }
}

export async function getCurrentUser(): Promise<User> {
    return fetchAPI<User>('/api/auth/me');
}

// Todo API
export async function getTodos(): Promise<Todo[]> {
    return fetchAPI<Todo[]>('/api/todos');
}

export async function createTodo(data: TodoCreate): Promise<Todo> {
    return fetchAPI<Todo>('/api/todos', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

export async function updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
    return fetchAPI<Todo>(`/api/todos/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
    });
}

export async function deleteTodo(id: number): Promise<void> {
    return fetchAPI<void>(`/api/todos/${id}`, {
        method: 'DELETE',
    });
}

export async function toggleTodoCompletion(id: number, completed: boolean): Promise<Todo> {
    return updateTodo(id, { completed });
}
