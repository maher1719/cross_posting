// frontend/src/store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
    token: string | null;
    // You can add user info here as well
    // user: User | null;
    isAuthenticated: boolean;
    login: (token: string) => void;
    logout: () => void;
    // setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            token: null,
            // user: null,
            isAuthenticated: false,
            login: (token) => set({ token, isAuthenticated: true }),
            logout: () => set({ token: null, isAuthenticated: false }),
            // setUser: (user) => set({ user }),
        }),
        {
            name: 'auth-storage', // Name for the localStorage key
            
        }
    )
);
