import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { useAuthStore } from './store/authStore';

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const logout = useAuthStore((state) => state.logout);

  return (
    <Router>
      {/* Set a consistent background color for the entire app */}
      <div className="bg-slate-100 min-h-screen">

        {/* --- STYLED NAVIGATION BAR --- */}
        <nav className="bg-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex-shrink-0">
                {/* You can put your app's logo here */}
                <Link to="/" className="text-2xl font-bold text-slate-800">
                  CrossPost
                </Link>
              </div>
              <div className="flex items-baseline space-x-4">
                {isAuthenticated ? (
                  <>
                    <Link
                      to="/"
                      className="text-gray-500 hover:bg-slate-200 hover:text-slate-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                    Home
                  </Link>
                  <Link
                      to="/"
                      className="text-gray-500 hover:bg-slate-200 hover:text-slate-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                    Logout
                  </Link>
                  </>
                    ):(
                      <>
                <Link
                  to="/login"
                  className="text-gray-500 hover:bg-slate-200 hover:text-slate-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-blue-500 text-white hover:bg-blue-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Register
                </Link>
                </>
                )}
              </div>
            </div>
          </div>
        </nav>
        {/* ----------------------------------------- */}

        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;