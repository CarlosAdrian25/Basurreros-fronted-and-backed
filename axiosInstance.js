import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5173/api', // URL base del backend de Laravel
    withCredentials: true, // Esto asegura que se envíen cookies (sesión)
});

export default axiosInstance;