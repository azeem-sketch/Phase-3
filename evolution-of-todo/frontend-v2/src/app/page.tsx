"use client";

import { useState, useEffect } from "react";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { apiRequest } from "@/lib/api";
import ChatInterface from "@/components/ChatInterface";
import { Todo } from "@/types/todo";
import {
  Plus,
  Trash2,
  CheckCircle,
  Circle,
  Clock,
  Calendar,
  Search,
  Filter,
  Loader2,
  CheckSquare
} from "lucide-react";

export default function Dashboard() {
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/signin");
    }
  }, [session, isPending, router]);

  const fetchTodos = async () => {
    if (!session) return;
    try {
      const data = await apiRequest(`/api/todos`);
      setTodos(data);
    } catch (err) {
      console.error("Failed to fetch todos", err);
    } finally {
      setFetching(false);
    }
  };

  useEffect(() => {
    if (session?.user?.id) {
      fetchTodos();
    }
  }, [session?.user?.id]);

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !session) return;

    setLoading(true);
    try {
      const newTodo = await apiRequest(`/api/todos`, {
        method: "POST",
        body: JSON.stringify({ title }),
      });
      setTodos([newTodo, ...todos]);
      setTitle("");
    } catch (err) {
      alert("Failed to add todo");
    } finally {
      setLoading(false);
    }
  };

  const toggleComplete = async (todo: Todo) => {
    if (!session) return;

    // Optimistic update
    const updatedTodos = todos.map(t =>
      t.id === todo.id ? { ...t, completed: !t.completed } : t
    );
    setTodos(updatedTodos);

    try {
      await apiRequest(`/api/todos/${todo.id}/complete`, {
        method: "PATCH",
      });
    } catch (err) {
      // Revert
      setTodos(todos);
      alert("Failed to toggle completion");
    }
  };

  const deleteTodo = async (id: number) => {
    if (!session) return;
    if (!confirm("Are you sure you want to delete this task?")) return;

    const originalTodos = [...todos];
    setTodos(todos.filter(t => t.id !== id));

    try {
      await apiRequest(`/api/todos/${id}`, {
        method: "DELETE",
      });
    } catch (err) {
      setTodos(originalTodos);
      alert("Failed to delete todo");
    }
  };

  if (isPending || fetching) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-4">
        <Loader2 className="animate-spin text-primary" size={40} />
        <p className="text-text-muted animate-pulse">Evolution is in progress...</p>
      </div>
    );
  }

  if (!session) return null;

  const completedCount = todos.filter(t => t.completed).length;

  return (
    <div className="max-w-4xl mx-auto p-6 md:p-10 space-y-10">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass p-6 rounded-2xl flex items-center gap-4">
          <div className="p-3 bg-primary/10 rounded-xl text-primary">
            <CheckSquare size={24} />
          </div>
          <div>
            <h3 className="text-2xl font-bold">{todos.length}</h3>
            <p className="text-xs text-text-muted uppercase tracking-wider font-semibold">Total Tasks</p>
          </div>
        </div>
        <div className="glass p-6 rounded-2xl flex items-center gap-4">
          <div className="p-3 bg-success/10 rounded-xl text-success">
            <CheckCircle size={24} />
          </div>
          <div>
            <h3 className="text-2xl font-bold">{completedCount}</h3>
            <p className="text-xs text-text-muted uppercase tracking-wider font-semibold">Completed</p>
          </div>
        </div>
        <div className="glass p-6 rounded-2xl flex items-center gap-4">
          <div className="p-3 bg-amber-500/10 rounded-xl text-amber-500">
            <Clock size={24} />
          </div>
          <div>
            <h3 className="text-2xl font-bold">{todos.length - completedCount}</h3>
            <p className="text-xs text-text-muted uppercase tracking-wider font-semibold">Pending</p>
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="animate-fade-in">
        <ChatInterface />
        <p className="text-center text-xs text-text-muted mt-2">
          Note: Use the chat to manage your tasks. The list below updates manually for now.
        </p>
      </div>

      {/* Filters & Search - Placeholder for Premium look */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <h2 className="text-xl font-bold">Your Tasks</h2>
        <div className="flex gap-2 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={16} />
            <input className="input !py-2 !pl-10 text-sm" placeholder="Search tasks..." />
          </div>
          <button className="glass p-2 rounded-lg text-text-muted hover:text-primary transition-colors">
            <Filter size={20} />
          </button>
        </div>
      </div>

      {/* Todo List */}
      <div className="space-y-4">
        {todos.length === 0 ? (
          <div className="text-center py-20 glass rounded-3xl border-dashed border-2">
            <CheckSquare size={64} className="mx-auto text-text-muted opacity-20 mb-4" />
            <h3 className="text-xl font-medium text-text-muted">No evolution stages yet</h3>
            <p className="text-text-muted">Start by adding your first task above</p>
          </div>
        ) : (
          todos.map((todo) => (
            <div
              key={todo.id}
              className={`glass p-5 rounded-2xl flex items-center justify-between group hover:shadow-lg transition-all ${todo.completed ? 'opacity-70' : ''}`}
            >
              <div className="flex items-center gap-4 flex-1">
                <button
                  onClick={() => toggleComplete(todo)}
                  className={`transition-colors ${todo.completed ? 'text-success' : 'text-text-muted hover:text-primary'}`}
                >
                  {todo.completed ? <CheckCircle size={28} /> : <Circle size={28} />}
                </button>
                <div className="flex-1 min-w-0">
                  <h4 className={`text-lg font-medium truncate ${todo.completed ? 'line-through text-text-muted' : ''}`}>
                    {todo.title}
                  </h4>
                  <div className="flex items-center gap-3 text-xs text-text-muted mt-1">
                    <span className="flex items-center gap-1">
                      <Calendar size={12} />
                      {new Date(todo.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => deleteTodo(todo.id)}
                  className="p-2 text-error hover:bg-error/10 rounded-lg transition-colors"
                  title="Delete Task"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
