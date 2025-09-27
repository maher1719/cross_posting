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