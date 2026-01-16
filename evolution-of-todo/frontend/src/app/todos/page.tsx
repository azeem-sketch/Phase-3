'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useTodos } from '@/hooks/useTodos';
import { TodoCreate, TodoUpdate } from '@/lib/types';
import styles from './todos.module.css';

export default function TodosPage() {
    const router = useRouter();
    const { user, isAuthenticated, signout, loading: authLoading } = useAuth();
    const { todos, loading, error, createTodo, updateTodo, deleteTodo, toggleTodo } = useTodos();

    const [showModal, setShowModal] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [formError, setFormError] = useState('');

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            router.push('/signin');
        }
    }, [isAuthenticated, authLoading, router]);

    const handleSignout = () => {
        signout();
        router.push('/signin');
    };

    const openCreateModal = () => {
        setEditingId(null);
        setTitle('');
        setDescription('');
        setFormError('');
        setShowModal(true);
    };

    const openEditModal = (id: number, currentTitle: string, currentDescription: string | null) => {
        setEditingId(id);
        setTitle(currentTitle);
        setDescription(currentDescription || '');
        setFormError('');
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setEditingId(null);
        setTitle('');
        setDescription('');
        setFormError('');
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setFormError('');

        try {
            if (editingId) {
                await updateTodo(editingId, { title, description });
            } else {
                await createTodo({ title, description });
            }
            closeModal();
        } catch (err: any) {
            setFormError(err.message || 'Failed to save todo');
        }
    };

    const handleDelete = async (id: number) => {
        if (confirm('Are you sure you want to delete this todo?')) {
            try {
                await deleteTodo(id);
            } catch (err: any) {
                alert(err.message || 'Failed to delete todo');
            }
        }
    };

    const handleToggle = async (id: number) => {
        try {
            await toggleTodo(id);
        } catch (err: any) {
            alert(err.message || 'Failed to toggle todo');
        }
    };

    if (authLoading) {
        return <div className={styles.loading}>Loading...</div>;
    }

    if (!isAuthenticated) {
        return null;
    }

    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <div className={styles.headerContent}>
                    <h1>My Todos</h1>
                    <div className={styles.userInfo}>
                        <span>{user?.email}</span>
                        <button onClick={handleSignout} className={styles.signoutBtn}>
                            Sign Out
                        </button>
                    </div>
                </div>
            </header>

            <main className={styles.main}>
                <div className={styles.actions}>
                    <button onClick={openCreateModal} className={styles.addBtn}>
                        + Add Todo
                    </button>
                </div>

                {loading && <div className={styles.loading}>Loading todos...</div>}

                {error && <div className={styles.error}>{error}</div>}

                {!loading && todos.length === 0 && (
                    <div className={styles.empty}>
                        <p>No todos yet. Create your first one!</p>
                    </div>
                )}

                {!loading && todos.length > 0 && (
                    <div className={styles.todoList}>
                        {todos.map((todo) => (
                            <div key={todo.id} className={`${styles.todoItem} ${todo.completed ? styles.completed : ''}`}>
                                <div className={styles.todoCheck}>
                                    <input
                                        type="checkbox"
                                        checked={todo.completed}
                                        onChange={() => handleToggle(todo.id)}
                                        className={styles.checkbox}
                                    />
                                </div>
                                <div className={styles.todoContent}>
                                    <h3 className={styles.todoTitle}>{todo.title}</h3>
                                    {todo.description && (
                                        <p className={styles.todoDescription}>{todo.description}</p>
                                    )}
                                </div>
                                <div className={styles.todoActions}>
                                    <button
                                        onClick={() => openEditModal(todo.id, todo.title, todo.description)}
                                        className={styles.editBtn}
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => handleDelete(todo.id)}
                                        className={styles.deleteBtn}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>

            {showModal && (
                <div className={styles.modal} onClick={closeModal}>
                    <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
                        <h2>{editingId ? 'Edit Todo' : 'Create Todo'}</h2>
                        <form onSubmit={handleSubmit}>
                            <div className={styles.formGroup}>
                                <label htmlFor="title">Title *</label>
                                <input
                                    id="title"
                                    type="text"
                                    value={title}
                                    onChange={(e) => setTitle(e.target.value)}
                                    required
                                    maxLength={200}
                                    className={styles.input}
                                    placeholder="Enter todo title"
                                />
                            </div>
                            <div className={styles.formGroup}>
                                <label htmlFor="description">Description</label>
                                <textarea
                                    id="description"
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    maxLength={1000}
                                    className={styles.textarea}
                                    placeholder="Enter description (optional)"
                                    rows={4}
                                />
                            </div>
                            {formError && <div className={styles.formError}>{formError}</div>}
                            <div className={styles.modalActions}>
                                <button type="button" onClick={closeModal} className={styles.cancelBtn}>
                                    Cancel
                                </button>
                                <button type="submit" className={styles.saveBtn}>
                                    {editingId ? 'Update' : 'Create'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
