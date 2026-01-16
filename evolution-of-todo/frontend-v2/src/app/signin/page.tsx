"use client";

import { useState, Suspense } from "react";
import { signIn } from "@/lib/auth-client";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Mail, Lock, LogIn, Loader2, CheckCircle2 } from "lucide-react";

function SigninForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const router = useRouter();
    const searchParams = useSearchParams();
    const signedup = searchParams.get("signedup");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            await signIn.email({
                email,
                password,
            }, {
                onSuccess: () => {
                    router.push("/");
                    router.refresh();
                },
                onError: (ctx) => {
                    setError(ctx.error.message || "Invalid email or password");
                }
            });
        } catch (err: any) {
            setError(err.message || "Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass w-full max-w-[400px] p-8 rounded-2xl shadow-2xl animate-fade-in">
            <div className="flex justify-center mb-6 text-primary">
                <div className="p-3 bg-primary/10 rounded-xl">
                    <LogIn size={32} />
                </div>
            </div>

            <h1 className="text-3xl font-bold text-center mb-2">Welcome Back</h1>
            <p className="text-text-muted text-center mb-8">Sign in to continue your progress</p>

            {signedup && !error && (
                <div className="mb-6 p-3 bg-success/10 text-success text-sm rounded-lg border border-success/20 flex items-center gap-2">
                    <CheckCircle2 size={18} />
                    <span>Account created! You can now sign in.</span>
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                    <label className="text-sm font-medium">Email Address</label>
                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
                        <input
                            type="email"
                            required
                            className="input !pl-10"
                            placeholder="name@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium">Password</label>
                    <div className="relative">
                        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
                        <input
                            type="password"
                            required
                            className="input !pl-10"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                </div>

                {error && (
                    <div className="p-3 bg-error/10 text-error text-sm rounded-lg border border-error/20">
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="btn btn-primary w-full flex items-center justify-center gap-2 mt-4 py-3"
                >
                    {loading ? <Loader2 className="animate-spin" size={20} /> : "Sign In"}
                </button>
            </form>

            <p className="mt-8 text-center text-sm text-text-muted">
                Don't have an account?{" "}
                <Link href="/signup" className="font-semibold hover:underline">
                    Create One
                </Link>
            </p>
        </div>
    );
}

export default function SigninPage() {
    return (
        <div className="min-h-[80vh] flex items-center justify-center p-6 bg-[radial-gradient(circle_at_top_right,_var(--primary)_0%,_transparent_25%),radial-gradient(circle_at_bottom_left,_var(--primary)_0%,_transparent_25%)]">
            <Suspense fallback={<div className="glass p-8 rounded-2xl shadow-xl w-full max-w-[400px] h-[500px] flex items-center justify-center"><Loader2 className="animate-spin text-primary" size={32} /></div>}>
                <SigninForm />
            </Suspense>
        </div>
    );
}
