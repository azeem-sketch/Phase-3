"use client";

import Link from "next/link";
import { useSession, signOut } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { LogOut, CheckSquare, User } from "lucide-react";

export default function Navbar() {
    const { data: session, isPending } = useSession();
    const router = useRouter();

    const handleSignOut = async () => {
        await signOut();
        router.push("/signin");
    };

    return (
        <nav className="glass sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2 text-xl font-bold text-primary">
                <CheckSquare size={28} />
                <span>Evolution Todo</span>
            </Link>

            <div className="flex items-center gap-6">
                {isPending ? (
                    <div className="h-4 w-20 bg-card-border animate-pulse rounded"></div>
                ) : session ? (
                    <div className="flex items-center gap-6">
                        <div className="flex items-center gap-2 text-sm font-medium">
                            <User size={18} className="text-text-muted" />
                            <span>{session.user.email}</span>
                        </div>
                        <button
                            onClick={handleSignOut}
                            className="flex items-center gap-2 text-sm font-medium text-error hover:opacity-80 transition-opacity"
                        >
                            <LogOut size={18} />
                            <span>Sign Out</span>
                        </button>
                    </div>
                ) : (
                    <div className="flex items-center gap-4">
                        <Link href="/signin" className="text-sm font-medium hover:text-primary transition-colors">
                            Sign In
                        </Link>
                        <Link href="/signup" className="btn btn-primary !py-2 !px-4 text-sm">
                            Get Started
                        </Link>
                    </div>
                )}
            </div>
        </nav>
    );
}
