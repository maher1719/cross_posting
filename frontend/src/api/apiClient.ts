// frontend/src/api/apiClient.ts

import axios from 'axios';
import { useAuthStore } from '../store/authStore'; // We'll use this to get the token

// 1. Create a new Axios instance with a custom configuration
const apiClient = axios.create({
  // This is the base URL of your Flask backend.
  // All requests made with this instance will be prefixed with this URL.
  baseURL: 'http://localhost:5001/api',
  headers: {
    // Standard headers that will be sent with every request.
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});


// in frontend/src/api/apiClient.ts

apiClient.interceptors.request.use(
  (config) => {
    // 1. Get the token from our Zustand store.
    const token = useAuthStore.getState().token;

    // 2. If a token exists, add it to the Authorization header.
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // 3. Return the modified config object to be sent.
    return config;
  },
  // ...
);

// 2. Use an Interceptor to dynamically add the JWT to every request
// An interceptor is a function that runs BEFORE the request is sent.
// This is the "magic" that handles authentication for your entire app.
apiClient.interceptors.request.use(
  (config) => {
    // Get the token from our Zustand store.
    const token = useAuthStore.getState().token;

    // If a token exists, add it to the Authorization header.
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Return the modified config object to be sent.
    return config;
  },
  (error) => {
    // Handle any errors that happen during the request setup.
    console.log(error)
    return Promise.reject(error);
  }
);


// 3. (Optional but recommended) Use an Interceptor to handle responses globally
// This interceptor runs AFTER a response is received.
apiClient.interceptors.response.use(
  // The first function handles successful (2xx) responses.
  // We can just return the response as is.
  (response) => {
    return response;
  },
  // The second function handles error responses.
  (error) => {
    // Example: If we get a 401 Unauthorized error, it might mean our token
    // has expired. We can automatically log the user out.
    if (error.response && error.response.status === 401) {
      console.log('Unauthorized request. Logging out...');
      // Clear the token from the store to log the user out.
      useAuthStore.getState().logout();
      // Optional: Redirect to the login page
      window.location.href = '/login';
    }

    // Return the error to be handled by the specific API call's catch block.
    return Promise.reject(error);
  }
);


// 4. Export the configured instance as the default export
export default apiClient;