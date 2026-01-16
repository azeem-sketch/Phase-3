/**
 * Todos hook
 */
'use client';

import { useState, useEffect } from 'react';
import { Todo, TodoCreate, TodoUpdate } from '@/lib/types';
import * as api from '@/lib/api';

export function useTodos() {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchTodos = async () => {
        try {
            setError(null);
            setLoading(true);
            const data = await api.getTodos();
            setTodos(data);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch todos');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTodos();
    }, []);

    const createTodo = async (data: TodoCreate) => {
        try {
            const newTodo = await api.createTodo(data);
            setTodos([...todos, newTodo]);
            return newTodo;
        } catch (err: any) {
            setError(err.message || 'Failed to create todo');
            throw err;
        }
    };

    const updateTodo = async (id: number, data: TodoUpdate) => {
        try {
            const updatedTodo = await api.updateTodo(id, data);
            setTodos(todos.map(t => t.id === id ? updatedTodo : t));
            return updatedTodo;
        } catch (err: any) {
            setError(err.message || 'Failed to update todo');
            throw err;
        }
    };

    const deleteTodo = async (id: number) => {
        try {
            await api.deleteTodo(id);
            setTodos(todos.filter(t => t.id !== id));
        } catch (err: any) {
            setError(err.message || 'Failed to delete todo');
            throw err;
        }
    };

    const toggleTodo = async (id: number) => {
        const todo = todos.find(t => t.id === id);
        if (!todo) return;

        try {
            const updatedTodo = await api.toggleTodoCompletion(id, !todo.completed);
            setTodos(todos.map(t => t.id === id ? updatedTodo : t));
        } catch (err: any) {
            setError(err.message || 'Failed to toggle todo');
            throw err;
        }
    };

    return {
        todos,
        loading,
        error,
        createTodo,
        updateTodo,
        deleteTodo,
        toggleTodo,
        refresh: fetchTodos,
    };
}
