import React from 'react';

const Graph = ({ r, points, onGraphClick }) => {
    const size = 450;
    const center = size / 2;
    const chartR = 170; 

    const handleClick = (e) => {
        const svg = e.currentTarget;
        const rect = svg.getBoundingClientRect();
        
        const svgX = e.clientX - rect.left;
        const svgY = e.clientY - rect.top;

        const deltaX = svgX - center;
        const deltaY = center - svgY; 

        const mathX = (deltaX / chartR * r).toFixed(2);
        const mathY = (deltaY / chartR * r).toFixed(2);

        onGraphClick(mathX, mathY);
    };

    const renderTicks = () => {
        const ticks = [];
        const stepValue = 0.5;
        for (let i = stepValue; i <= r; i += stepValue) {
            ticks.push(i);
        }

        return ticks.map((val) => {
            const pos = (val / r) * chartR;

            return (
                <React.Fragment key={val}>
                    {[pos, -pos].map((p, idx) => (
                        <g key={`x-${val}-${idx}`}>
                            <line 
                                x1={center + p} y1={center - 5} 
                                x2={center + p} y2={center + 5} 
                                stroke="black" 
                            />
                            <text 
                                x={center + p} y={center + 20} 
                                fontSize="10" textAnchor="middle"
                            >
                                {(p / chartR * r).toFixed(1)}
                            </text>
                        </g>
                    ))}

                    {[pos, -pos].map((p, idx) => (
                        <g key={`y-${val}-${idx}`}>
                            <line 
                                x1={center - 5} y1={center - p} 
                                x2={center + 5} y2={center - p} 
                                stroke="black" 
                            />
                            <text 
                                x={center - 15} y={center - p + 3} 
                                fontSize="10" textAnchor="end"
                            >
                                {(p / chartR * r).toFixed(1)}
                            </text>
                        </g>
                    ))}
                </React.Fragment>
            );
        });
    };


    return (
        <svg width={size} height={size} onClick={handleClick} style={{ cursor: 'pointer', background: 'white', border: '1px solid #ccc' }}>
            <rect 
                x={center} 
                y={center} 
                width={chartR} 
                height={chartR} 
                fill="blue" fillOpacity="0.3"
            />

            <polygon 
                points={`${center},${center} ${center - chartR},${center} ${center},${center + chartR}`} 
                fill="blue" fillOpacity="0.3"
            />

            <path 
                d={`M ${center} ${center} 
                   L ${center - chartR * 0.5} ${center} 
                   A ${chartR * 0.5} ${chartR * 0.5} 0 0 1 ${center} ${center - chartR * 0.5} 
                   Z`} 
                fill="blue" fillOpacity="0.3" 
            />

            <line x1="0" y1={center} x2={size} y2={center} stroke="black" strokeWidth="2" />
            <line x1={center} y1="0" x2={center} y2={size} stroke="black" strokeWidth="2" />

            <polygon points={`${size},${center} ${size-10},${center-5} ${size-10},${center+5}`} fill="black" />
            <polygon points={`${center},0 ${center-5},10 ${center+5},10`} fill="black" />

            <text x={size - 15} y={center - 10} fontWeight="bold">X</text>
            <text x={center + 15} y="15" fontWeight="bold">Y</text>
            
            {renderTicks()}

            {points.map((p, index) => (
                <circle 
                    key={index}
                    cx={center + (p.x / r * chartR)} 
                    cy={center - (p.y / r * chartR)} 
                    r="4" 
                    fill={p.result ? "#27ae60" : "#e74c3c"} 
                    stroke="black"
                />
            ))}
        </svg>
    );
};

export default Graph;