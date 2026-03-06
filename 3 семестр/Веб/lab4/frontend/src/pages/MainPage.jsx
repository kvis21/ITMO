import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setPoints, addPoint } from '../store/pointsSlice';
import { logout } from '../store/userSlice';
import axios from '../api/axios';
import Header from '../components/Header';
import Graph from '../components/Graph';

const MainPage = () => {
    const [x, setX] = useState('0');
    const [y, setY] = useState('');
    const [r, setR] = useState('1');
    const [errorMessage, setErrorMessage] = useState('');

    const dispatch = useDispatch();
    const points = useSelector(state => state.points.items);

    useEffect(() => {
        axios.get('/points').then(res => {dispatch(setPoints(res.data))});
    }, []);

    const handleSubmit = async (e) => {
        if (e) e.preventDefault();
        setErrorMessage(''); 

        const isVal = validateY(y) && validateR(r);
        if (isVal) {
            try {
                const res = await axios.post('/points', { x: parseFloat(x), y: parseFloat(y.replace(',', '.')), r: parseFloat(r)});
                dispatch(addPoint(res.data));
            } catch (err) {
                setErrorMessage("Ошибка сервера. Проверьте соединение.");
            }
        }
    };

    const handleGraphClick = (clickX, clickY) => {
        if (validateR(r)){
            axios.post('/points', { x: clickX, y: clickY, r: parseFloat(r) })
                .then(res => dispatch(addPoint(res.data)));
        }
    };

    const validateY = (value) => {
        const yVal = parseFloat(y.replace(',', '.'));
        if (isNaN(yVal)) {
            setErrorMessage("Y должен быть числом");
            return false;
        }
        if (isNaN(yVal) || yVal <= -3 || yVal >= 5) {
            setErrorMessage("Y должен быть числом от -3 до 5");
            return false;
        }
        setErrorMessage("");
        return true;
    }

    const validateR = (value) => {
        const rVal = parseFloat(value);
        if (isNaN(rVal)) {
            setErrorMessage("R должно быть числом");
            return false;
        }
        if (rVal <= 0) {
            setErrorMessage("R должен быть > 0");
            return false;
        }
        setErrorMessage("")
        return true;
    };

    return (
        <div className="main-container">
            <Header />
            
            <div className="content-wrapper">
                <div className="graph-section">
                    
                    <Graph r={parseFloat(r)} points={points} onGraphClick={handleGraphClick} />
                </div>

                <div className="form-section">
                    <form onSubmit={handleSubmit}>
                        <h3>Параметры</h3>
                        
                        <div className="input-group">
                            <label>X: </label>
                            <select value={x} onChange={e => setX(e.target.value)}>
                                {['-2','-1.5','-1','-0.5','0','0.5','1','1.5','2'].map(v => <option key={v}>{v}</option>)}
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Y: </label>
                            <input type="text" value={y} onChange={e => setY(e.target.value)} placeholder="(-3...5)" />
                        </div>

                        <div className="input-group">
                            <label>R: </label>
                            <select value={r} 
                                onChange={e => {const val = e.target.value; 
                                    validateR(val)?setR(val):null;
                                }}>
                                {['-2','-1.5','-1','-0.5','0','0.5','1','1.5','2'].map(v => <option key={v}>{v}</option>)}
                            </select>
                        </div>

                        {errorMessage && <div className="error-text">{errorMessage}</div>}

                        <button type="submit" className="submit-btn">Проверить</button>
                        <button type="button" onClick={() => dispatch(logout())} className="logout-btn">Выйти</button>
                    </form>
                </div>
            </div>
            <div className="table-container">
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>X</th><th>Y</th><th>R</th><th>Результат</th><th>Время</th>
                        </tr>
                    </thead>
                    <tbody>
                        {points.map((p, i) => (
                            <tr key={i}>
                                <td>{p.x}</td><td>{p.y}</td><td>{p.r}</td>
                                <td style={{color: p.result ? 'green' : 'red'}}>
                                    {p.result ? 'Попал' : 'Мимо'}
                                </td>
                                <td>{p.time || '—'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default MainPage;