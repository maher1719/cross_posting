# setup_react.py
import os
import textwrap

# --- Configuration ---
FRONTEND_DIR = "frontend"
SRC_DIR = os.path.join(FRONTEND_DIR, "src")

# Dictionary of directories and their subdirectories/files
# This is our architectural blueprint in code.
DIRS = {
    SRC_DIR: {
        "api": ["apiClient.ts", "authApi.ts", "userApi.ts", "postApi.ts"],
        "components": {
            "common": ["Button.tsx", "Input.tsx", "Spinner.tsx"],
            "layout": ["Navbar.tsx", "Footer.tsx"],
            "posts": ["PostCard.tsx", "PostList.tsx"],
        },
        "hooks": ["useAuth.ts", "usePosts.ts"],
        "pages": ["HomePage.tsx", "LoginPage.tsx", "RegisterPage.tsx"],
        "store": ["authStore.ts", "postStore.ts"],
        "types": ["index.ts", "User.ts", "Post.ts"],
        "utils": ["formatDate.ts"],
        "App.tsx": None,
        "main.tsx": None,
        "index.css": None, # Assuming a basic CSS file
    }
}

# Dictionary of boilerplate file contents
FILE_CONTENTS = {
    os.path.join("api", "apiClient.ts"): textwrap.dedent("""\
        import axios from 'axios';

        const apiClient = axios.create({
          baseURL: 'http://localhost:5001/api', // Your Flask backend URL
          headers: {
            'Content-Type': 'application/json',
          },
        });

        // Optional: Add interceptors for handling auth tokens
        apiClient.interceptors.request.use((config) => {
          // const token = useAuthStore.getState().token; // Example of getting token
          // if (token) {
          //   config.headers.Authorization = `Bearer ${token}`;
          // }
          return config;
        });

        export default apiClient;
    """),
    os.path.join("store", "authStore.ts"): textwrap.dedent("""\
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
    """),
    os.path.join("types", "index.ts"): textwrap.dedent("""\
        // This file can be used to export all types from a single point
        export * from './User';
        export * from './Post';
    """),
    os.path.join("types", "User.ts"): textwrap.dedent("""\
        // Corresponds to the Pydantic UserDisplay model
        export interface User {
          id: number;
          username: string;
          email: string;
          created_at: string; // Dates come as strings from JSON
        }
    """),
     os.path.join("types", "Post.ts"): textwrap.dedent("""\
        // Corresponds to the Pydantic PostDisplay model
        export interface Post {
          id: number;
          content: string;
          user_id: number;
          created_at: string;
        }
    """),
    os.path.join("App.tsx"): textwrap.dedent("""\
        import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
        import { HomePage } from './pages/HomePage';
        import { LoginPage } from './pages/LoginPage';
        import { RegisterPage } from './pages/RegisterPage';

        function App() {
          return (
            <Router>
              {/* You can add a Navbar component here */}
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
              </Routes>
            </Router>
          );
        }

        export default App;
    """),
    os.path.join("pages", "HomePage.tsx"): textwrap.dedent("""\
        import React from 'react';

        export const HomePage = () => {
          return (
            <div>
              <h1>Welcome to the Cross-Posting App!</h1>
              <p>This is the home page.</p>
            </div>
          );
        };
    """),
     os.path.join("pages", "LoginPage.tsx"): textwrap.dedent("""\
        import React from 'react';

        export const LoginPage = () => {
          return (
            <div>
              <h1>Login Page</h1>
              {/* Login form component will go here */}
            </div>
          );
        };
    """),
}

def create_structure(base_path, structure):
    """Recursively creates directories and files."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for item in content:
                # Create empty files
                open(os.path.join(path, item), 'a').close()
        else:
            # It's a file that might have content
            relative_path = os.path.relpath(path, start=SRC_DIR)
            content_to_write = FILE_CONTENTS.get(relative_path.replace(os.path.sep, '/'), "") # Normalize path separators for key lookup
            with open(path, 'w') as f:
                if content_to_write:
                    print(f"Creating file with content: {path}")
                    f.write(content_to_write)
                else:
                    print(f"Creating empty file: {path}")

if __name__ == "__main__":
    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: Frontend directory '{FRONTEND_DIR}' does not exist.")
        print("Please create the React project first using 'npm create vite@latest frontend'.")
    else:
        print("--- Setting up React Clean Architecture ---")
        # Clear existing src directory to ensure a clean slate
        if os.path.exists(SRC_DIR):
            import shutil
            print(f"Removing existing '{SRC_DIR}' directory...")
            shutil.rmtree(SRC_DIR)
        
        create_structure(os.getcwd(), DIRS)

        print("\n--- Setup Complete! ---")
        print(f"React project structure created in '{SRC_DIR}'.")
        print("\nNext steps:")
        print("1. cd into the 'frontend' directory.")
        print("2. Run 'npm install axios zustand react-router-dom' to add necessary packages.")
        print("3. Run 'npm run dev' to start the development server.")