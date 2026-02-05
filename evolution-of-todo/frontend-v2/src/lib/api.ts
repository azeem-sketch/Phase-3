import { useAuth } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function apiRequest(path: string, options: RequestInit = {}) {
    const { token } = useAuth.getState();
    const fullUrl = `${API_URL}${path}`;

    console.log(`[API] Request: ${options.method || 'GET'} ${fullUrl}`);

    const headers = new Headers(options.headers);
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }
    headers.set("Content-Type", "application/json");

    try {
        const response = await fetch(fullUrl, {
            ...options,
            headers,
        });

        if (!response.ok) {
            const errorText = await response.text();
            let error;
            try {
                error = JSON.parse(errorText);
            } catch {
                error = { message: errorText || response.statusText };
            }
            console.error(`[API] Error response for ${fullUrl}:`, error);
            console.error(`[API] Status: ${response.status} ${response.statusText}`);
            throw new Error(error.message || response.statusText);
        }

        console.log(`[API] Success: ${fullUrl}`);
        if (response.status === 204) return null;
        return response.json();
    } catch (error: any) {
        console.error(`[API] FETCH FAILED for ${fullUrl}:`, error.message);
        throw error;
    }
}
