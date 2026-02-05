"use client";
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
    id: number;
    email: string;
    full_name?: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    setAuth: (user: User, token: string) => void;
    clearAuth: () => void;
}

export const useAuth = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            token: null,
            setAuth: (user, token) => set({ user, token }),
            clearAuth: () => set({ user: null, token: null }),
        }),
        {
            name: 'auth-storage',
        }
    )
);

const API_URL = "http://127.0.0.1:8000"; // Hardcoded for reliability

export const signUp = async (email: string, password: string) => {
    console.log(`[AUTH] Attempting SignUp for: ${email}`);
    try {
        const response = await fetch(`${API_URL}/api/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const error = await response.json();
            console.error(`[AUTH] SignUp FAILED:`, error);
            throw new Error(error.detail || 'Signup failed');
        }

        console.log(`[AUTH] SignUp SUCCESS for: ${email}`);
        return response.json();
    } catch (err: any) {
        console.error(`[AUTH] SignUp Network/System Error:`, err.message);
        throw err;
    }
};

export const signIn = async (email: string, password: string) => {
    console.log(`[AUTH] Attempting SignIn for: ${email}`);
    try {
        const response = await fetch(`${API_URL}/api/auth/signin`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            let error;
            try {
                error = await response.json();
            } catch (e) {
                error = { detail: 'Invalid email or password' };
            }
            console.error(`[AUTH] SignIn FAILED for ${email}:`, error);
            throw new Error(error.detail || 'Invalid email or password');
        }

        const data = await response.json();
        console.log(`[AUTH] SignIn SUCCESS for: ${email}`);
        useAuth.getState().setAuth(data.user, data.access_token);
        return data;
    } catch (err: any) {
        console.error(`[AUTH] SignIn Network/System Error:`, err.message);
        throw err;
    }
};

export const signOut = () => {
    useAuth.getState().clearAuth();
};

export const useSession = () => {
    const user = useAuth((state) => state.user);
    const token = useAuth((state) => state.token);

    return {
        data: user ? { user } : null,
        isPending: false,
    };
};
