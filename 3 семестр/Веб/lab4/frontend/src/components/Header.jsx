import React from 'react';

const Header = () => {
    return (
        <header style={headerStyle}>
            <h2>Панченко Антон Дмитриевич</h2>
            <p>Группа: P3215 | Вариант: 300051</p>
        </header>
    );
};

const headerStyle = {
    padding: '10px',
    backgroundColor: '#2196F3',
    color: 'white',
    textAlign: 'center',
    marginBottom: '20px'
};

export default Header;