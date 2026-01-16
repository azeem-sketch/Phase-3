import { authClient } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest(path: string, options: RequestInit = {}) {
    const session = await authClient.getSession();

    // Get the JWT from the session or client
    const tokenResponse = await authClient.token();
    const token = tokenResponse?.data?.token;

    const headers = new Headers(options.headers);
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }
    headers.set("Content-Type", "application/json");

    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ message: "An error occurred" }));
        throw new Error(error.message || response.statusText);
    }

    if (response.status === 204) return null;
    return response.json();
}
