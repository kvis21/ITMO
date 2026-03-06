import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';

const App = () => {
    const isAuth = useSelector(state => state.user.isAuthenticated);

    return (
      <Routes>
          <Route path="/" element={!isAuth ? <LoginPage /> : <Navigate to="/main" />} />
          <Route path="/main" element={isAuth ? <MainPage /> : <Navigate to="/" />} />
      </Routes>
    );
};


export default App;