/**
 * TypeScript type definitions
 */

export interface User {
    id: number;
    email: string;
    created_at: string;
}

export interface Todo {
    id: number;
    user_id: number;
    title: string;
    description: string | null;
    completed: boolean;
    created_at: string;
    updated_at: string;
}

export interface TodoCreate {
    title: string;
    description?: string;
}

export interface TodoUpdate {
    title?: string;
    description?: string;
    completed?: boolean;
}

export interface AuthToken {
    access_token: string;
    token_type: string;
    user: User;
}
