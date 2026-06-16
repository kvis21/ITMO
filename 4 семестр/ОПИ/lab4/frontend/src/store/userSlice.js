import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
    name: 'user',
    initialState: {
        username: localStorage.getItem('username') || '',
        isAuthenticated: !!localStorage.getItem('token'),
    },
    reducers: {
        loginSuccess: (state, action) => {
            state.username = action.payload.username;
            state.isAuthenticated = true;
        },
        logout: (state) => {
            state.username = '';
            state.isAuthenticated = false;
            localStorage.removeItem('token');
            localStorage.removeItem('username');
        }
    }
});

export const { loginSuccess, logout } = userSlice.actions;
export default userSlice.reducer;