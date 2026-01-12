import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import {loginSuccess} from '../store/userSlice'
import axios from '../api/axios';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();
    const dispatch = useDispatch(); 

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await axios.post('/auth/login', { 
                username, 
                passwordHash: password 
            });
            
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', username);

            dispatch(loginSuccess({ username: username }));

            navigate('/main'); 
        } catch (err) {
            setPassword("")
            console.log(err);
            setError(err.response);
        }
    };
    const handleRegister = async () => {
        setError('');
        if (!username || !password) {
            setError("Заполните оба поля");
            return;
        }
        try {
            const response = await axios.post('/auth/register', { 
                username, 
                passwordHash: password 
            });
            
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', username);

            dispatch(loginSuccess({ username: username }));

            navigate('/main');  
        } catch (err) {
            setError(err.response.data.error);
        }
    };

    return (
        <div className="login-page-wrapper">
            <Header />
            <div className="login-container">
                <h3>Вход в систему</h3>
                <form className="login-form" onSubmit={handleLogin}>
                    <input 
                        type="text" 
                        placeholder="Логин"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input 
                        type="password" 
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    {error && <div className="error-text">{error}</div>}
                    
                    <button type="submit" className="login-btn">Войти</button>
                    
                    <button 
                        type="button" 
                        className="register-btn" 
                        onClick={handleRegister}
                    >
                        Зарегистрироваться
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;