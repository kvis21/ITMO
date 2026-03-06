const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');

const width = canvas.width;
const height = canvas.height;
const R = 100;
const centerX = width / 2;
const centerY = height / 2;



function drawGraph() {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = 'rgba(61, 211, 248, 0.79)';
    //rectangle
    ctx.beginPath();
    ctx.rect(centerX - R , centerY - R / 2, R , R / 2);
    ctx.fill();

    //circle
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, R, 0, Math.PI / 2, false);
    ctx.lineTo(centerX, centerY);
    ctx.fill();

    //triangle
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX - R / 2, centerY);
    ctx.lineTo(centerX, centerY + R / 2);
    ctx.closePath();
    ctx.fill();

    //axis
    ctx.beginPath();
    ctx.moveTo(centerX, 0);  // Y-axis
    ctx.lineTo(centerX, height);
    ctx.moveTo(0, centerY);  // X-axis
    ctx.lineTo(width, centerY);
    ctx.strokeStyle = "black";
    ctx.stroke();


    ctx.font = "12px monospace";

    ctx.strokeText("0", centerX + 6, centerY - 6);
    ctx.strokeText("R/2", centerX + R / 2 - 6, centerY - 6);
    ctx.strokeText("R", centerX + R - 6, centerY - 6);

    ctx.strokeText("-R/2", centerX - R / 2 - 18, centerY - 6);
    ctx.strokeText("-R", centerX - R - 6, centerY - 6);

    ctx.strokeText("R/2", centerX + 6, centerY - R / 2 + 6);
    ctx.strokeText("R", centerX + 6, centerY - R + 6);

    ctx.strokeText("-R/2", centerX + 6, centerY + R / 2 + 6);
    ctx.strokeText("-R", centerX + 6, centerY + R + 6);
}

drawGraph();

function drawPoint(x, y, result, r) {
    const scale = 100 / r; // Масштабируем относительно текущего R
    const canvasX = centerX + x * scale;
    const canvasY = centerY - y * scale; // Инвертируем Y (canvas координаты)
    
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, 5, 0, 2 * Math.PI);
    ctx.fillStyle = result ? 'green' : 'red';
    ctx.fill();
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 1;
    ctx.stroke();
}