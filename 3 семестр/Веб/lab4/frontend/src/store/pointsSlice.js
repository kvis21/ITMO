import { createSlice } from '@reduxjs/toolkit';

const pointsSlice = createSlice({
    name: 'points',
    initialState: {
        items: [] 
    },
    reducers: {
        setPoints: (state, action) => {
            state.items = action.payload;
        },
        addPoint: (state, action) => {
            state.items.unshift(action.payload); 
        }
    }
});

export const { setPoints, addPoint } = pointsSlice.actions;
export default pointsSlice.reducer;