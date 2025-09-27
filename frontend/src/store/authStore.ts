import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
    token: string | null;
    // You can add user info here as well
    // user: User | null;
    setToken: (token: string | null) => void;
    // setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            token: null,
            // user: null,
            setToken: (token) => set({ token }),
            // setUser: (user) => set({ user }),
        }),
        {
            name: 'auth-storage', // Name for the localStorage key
        }
    )
);
