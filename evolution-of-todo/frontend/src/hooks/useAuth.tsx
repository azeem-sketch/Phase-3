/**
 * Authentication hook
 */
'use client';

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { User } from '@/lib/types';
import * as api from '@/lib/api';

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    loading: boolean;
    signin: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string) => Promise<void>;
    signout: () => void;
    error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Load user from localStorage on mount
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const signin = async (email: string, password: string) => {
        try {
            setError(null);
            setLoading(true);
            const token = await api.signin(email, password);
            setUser(token.user);
        } catch (err: any) {
            setError(err.message || 'Failed to sign in');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const signup = async (email: string, password: string) => {
        try {
            setError(null);
            setLoading(true);
            await api.signup(email, password);
        } catch (err: any) {
            setError(err.message || 'Failed to sign up');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const signout = () => {
        api.signout();
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                loading,
                signin,
                signup,
                signout,
                error,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
