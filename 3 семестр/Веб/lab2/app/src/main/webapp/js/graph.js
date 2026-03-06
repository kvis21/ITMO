class GraphManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.setupCanvasSize();
        this.ctx = this.canvas.getContext('2d');
        this.points = [];
        this.currentR = null;
        
        this.graphErrorElement = document.getElementById('graphError');
        this.clickInfoElement = document.getElementById('clickInfo');
        
        this.mouseX = 0;
        this.mouseY = 0;
        this.isMouseOver = false;
        
        this.init();
        this.bindEvents();
    }

    setupCanvasSize() {
        const size = 500;
        this.canvas.width = size;
        this.canvas.height = size;
        
        this.canvas.style.width = size + 'px';
        this.canvas.style.height = size + 'px';
        this.canvas.style.cursor = 'crosshair'; 
    }

    init() {
        this.drawGraph();
        this.loadExistingPoints();
        this.restoreRFromSession();
    }

    bindEvents() {
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseenter', () => this.handleMouseEnter());
        this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());
        
        document.querySelectorAll('.r-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.handleRChange(e.target);
            });
        });
    }

    restoreRFromSession() {
        const checkedCheckbox = document.querySelector('.r-checkbox:checked');
        if (checkedCheckbox) {
            this.currentR = parseFloat(checkedCheckbox.value);
        }
        this.drawGraph();
    }

    handleCanvasClick(event) {
        if (!this.currentR) {
            this.showGraphError('Сначала выберите радиус R');
            return;
        }

        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const mathX = (x - 250) / 40;
        const mathY = (250 - y) / 40;

        const availableX = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
        const closestX = availableX.reduce((prev, curr) => {
            return Math.abs(curr - mathX) < Math.abs(prev - mathX) ? curr : prev;
        });

        const clampedY = Math.max(-5, Math.min(5, mathY));
        const roundedY = Math.round(clampedY * 100) / 100;

        if (window.formManager) {
            window.formManager.setCoordinatesFromGraph(closestX, roundedY);
        } else {
            this.setFormValues(closestX, roundedY);
        }

        this.showClickInfo(`Выбрана точка: X=${closestX}, Y=${roundedY}`);
        this.clearGraphError();
        
        this.submitForm();
    }

    setFormValues(x, y) {
        document.querySelectorAll('.x-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.value === x.toString()) {
                btn.classList.add('active');
            }
        });
        document.getElementById('x').value = x;
        document.getElementById('y').value = y.toFixed(2);
        
        document.getElementById('xError').textContent = '';
        document.getElementById('yError').textContent = '';
    }

    submitForm() {
        const x = document.getElementById('x').value;
        const y = document.getElementById('y').value;
        const rCheckboxes = document.querySelectorAll('.r-checkbox:checked');
        
        if (!x) {
            this.showGraphError('Выберите координату X');
            return;
        }
        
        if (!y || isNaN(y) || y < -5 || y > 5) {
            this.showGraphError('Y должен быть числом от -5 до 5');
            return;
        }
        
        if (rCheckboxes.length === 0) {
            this.showGraphError('Выберите хотя бы один радиус R');
            return;
        }
        
        document.getElementById('pointForm').submit();
    }

    handleRChange(checkbox) {
        if (checkbox.checked) {
            this.currentR = parseFloat(checkbox.value);
        } else {
            const checkedCheckbox = document.querySelector('.r-checkbox:checked');
            this.currentR = checkedCheckbox ? parseFloat(checkedCheckbox.value) : null;
        }
        
        this.drawGraph();
        this.clearGraphError();
    }

    handleMouseMove(event) {
        const rect = this.canvas.getBoundingClientRect();
        this.mouseX = event.clientX - rect.left;
        this.mouseY = event.clientY - rect.top;
        
        this.drawGraph();
    }

    handleMouseEnter() {
        this.isMouseOver = true;
        this.drawGraph();
    }

    handleMouseLeave() {
        this.isMouseOver = false;
        this.drawGraph();
    }

    loadExistingPoints() {
        this.points = [];
        
        const resultsBody = document.getElementById('resultsBody');
        if (!resultsBody) return;
        
        const resultsRows = resultsBody.querySelectorAll('tr:not(.no-results)');
        resultsRows.forEach(row => {
            const cells = row.cells;
            if (cells.length >= 6) {
                try {
                    const x = parseFloat(cells[0].textContent);
                    const y = parseFloat(cells[1].textContent);
                    const r = parseFloat(cells[2].textContent);
                    const resultText = cells[3].textContent;
                    const result = resultText === 'Попадание';
                    
                    const canvasX = 250 + (x * 40);
                    const canvasY = 250 - (y * 40);
                    
                    this.points.push({
                        x: canvasX,
                        y: canvasY,
                        isNew: false,
                        hit: result
                    });
                } catch (error) {
                    console.warn('Error parsing point data:', error);
                }
            }
        });
        
        this.drawGraph();
    }

    showGraphError(message) {
        if (this.graphErrorElement) {
            this.graphErrorElement.textContent = message;
            this.graphErrorElement.style.display = 'block';
        }
    }

    clearGraphError() {
        if (this.graphErrorElement) {
            this.graphErrorElement.textContent = '';
            this.graphErrorElement.style.display = 'none';
        }
    }

    showClickInfo(message) {
        if (this.clickInfoElement) {
            this.clickInfoElement.textContent = message;
            this.clickInfoElement.style.display = 'block';
            
            setTimeout(() => {
                if (this.clickInfoElement) {
                    this.clickInfoElement.style.display = 'none';
                }
            }, 3000);
        }
    }

    drawGraph() {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const scale = 40;

        ctx.clearRect(0, 0, width, height);

        if (this.currentR) {
            ctx.fillStyle = 'rgba(52, 152, 219, 0.3)';
            ctx.strokeStyle = '#3498db';
            ctx.lineWidth = 2;
            this.drawArea(ctx, centerX, centerY, scale);
        }
        
        this.drawAxes(ctx, width, height, centerX, centerY, scale);
        this.drawAxisLabels(ctx, centerX, centerY, scale, width, height);
        this.drawPoints();
        
        if (this.currentR) {
            ctx.fillStyle = '#2c3e50';
            ctx.font = '14px Arial';
            ctx.fillText(`R = ${this.currentR}`, 10, 20);
        }

        if (this.isMouseOver) {
            this.drawCoordinates();
        }
    }

    drawPoints() {
        const ctx = this.ctx;
        
        this.points.forEach(point => {
            if (point.hit !== undefined) {
                ctx.fillStyle = point.hit ? '#27ae60' : '#e74c3c';
            } else {
                ctx.fillStyle = point.isNew ? '#e74c3c' : '#27ae60';
            }
            
            ctx.beginPath();
            ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
            ctx.fill();
            
            if (point.isNew || point.hit !== undefined) {
                ctx.strokeStyle = point.hit ? '#229954' : '#c0392b';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        });
    }

    drawCoordinates() {
        const ctx = this.ctx;
        const mathX = (this.mouseX - 250) / 40;
        const mathY = (250 - this.mouseY) / 40;
        
        const displayX = Math.max(-5, Math.min(5, mathX));
        const displayY = Math.max(-5, Math.min(5, mathY));
        
        const availableX = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
        const closestX = availableX.reduce((prev, curr) => {
            return Math.abs(curr - displayX) < Math.abs(prev - displayX) ? curr : prev;
        });
        const roundedY = Math.round(displayY * 100) / 100;
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fillRect(this.mouseX + 10, this.mouseY - 20, 100, 40);
        
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 1;
        ctx.strokeRect(this.mouseX + 10, this.mouseY - 20, 100, 40);
        
        ctx.fillStyle = '#2c3e50';
        ctx.font = '12px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`X: ${closestX}`, this.mouseX + 15, this.mouseY - 5);
        ctx.fillText(`Y: ${roundedY}`, this.mouseX + 15, this.mouseY + 10);
    }

    drawArea(ctx, centerX, centerY, scale) {
        if (!this.currentR) return;

        const r = this.currentR;
        
        ctx.beginPath();
        
        ctx.arc(centerX, centerY, 0.5 * r * scale, -Math.PI/2, 0, false);
        ctx.lineTo(centerX, centerY);
        ctx.closePath();
        
        ctx.rect(centerX - r * scale, centerY, r * scale, r * scale);
        
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + 0.5 * r * scale, centerY);
        ctx.lineTo(centerX, centerY + r * scale);
        ctx.closePath();
        
        ctx.fill();
        ctx.stroke();
    }

    drawAxes(ctx, width, height, centerX, centerY, scale) {
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 2;
        ctx.fillStyle = '#2c3e50';

        ctx.beginPath();
        ctx.moveTo(0, centerY);
        ctx.lineTo(width, centerY);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(centerX, height);
        ctx.lineTo(centerX, 0);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(width - 10, centerY - 5);
        ctx.lineTo(width, centerY);
        ctx.lineTo(width - 10, centerY + 5);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(centerX - 5, 10);
        ctx.lineTo(centerX, 0);
        ctx.lineTo(centerX + 5, 10);
        ctx.fill();

        ctx.lineWidth = 1;
        
        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const x = centerX + i * scale;
            ctx.beginPath();
            ctx.moveTo(x, centerY - 5);
            ctx.lineTo(x, centerY + 5);
            ctx.stroke();
        }

        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const y = centerY - i * scale;
            ctx.beginPath();
            ctx.moveTo(centerX - 5, y);
            ctx.lineTo(centerX + 5, y);
            ctx.stroke();
        }
    }

    drawAxisLabels(ctx, centerX, centerY, scale, width, height) {
        ctx.fillStyle = '#2c3e50';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const x = centerX + i * scale;
            ctx.fillText(i.toString(), x, centerY + 15);
        }

        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const y = centerY - i * scale;
            ctx.fillText(i.toString(), centerX - 15, y);
        }

        ctx.fillText('X', width - 10, centerY - 10);
        ctx.fillText('Y', centerX + 10, 10);
        ctx.fillText('0', centerX - 10, centerY + 15);
    }

    clearPoints() {
        this.points = [];
        this.drawGraph();
    }
}