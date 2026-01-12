import axios from 'axios';
import { logout } from '../store/userSlice';
import { store } from '../store'; 

const instance = axios.create({
    baseURL: 'http://localhost:8080/app/api' 
});

instance.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// обработка ошибки 401
instance.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            store.dispatch(logout()); 
            localStorage.removeItem('token'); 
            navigate('/'); 
        }
        return Promise.reject(error);
    }
);

export default instance;