// frontend/src/store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types'; // <-- IMPORT THE USER TYPE

interface AuthState {
    token: string | null;
    user: User | null; // <-- ADD THE USER OBJECT
    isAuthenticated: boolean;
    login: (token: string, user: User) => void; // <-- UPDATE LOGIN ACTION
    logout: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            token: null,
            user: null, // <-- INITIAL STATE
            isAuthenticated: false,
            // --- UPDATE THE LOGIN ACTION to accept the user object ---
            login: (token, user) => set({ token, user, isAuthenticated: true }),
            // --- UPDATE THE LOGOUT ACTION to clear the user object ---
            logout: () => set({ token: null, user: null, isAuthenticated: false }),
        }),
        {
            name: 'auth-storage',
        }
    )
);