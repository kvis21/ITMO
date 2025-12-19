class GraphManager {
    constructor() {
        this.canvas = document.getElementById("graphCanvas");
        
        this.setupCanvasSize();
        this.ctx = this.canvas.getContext('2d');
        this.points = [];
        this.currentR = null;
        
        this.mouseX = 0;
        this.mouseY = 0;
        this.isMouseOver = false;
        
        this.init();
        this.bindEvents();
    }

    setupCanvasSize() {
        this.canvas.width = 500;
        this.canvas.height = 500;
        this.canvas.style.cursor = 'crosshair'; 
    }

    init() {
        this.restoreRFromBean();
        this.loadExistingPoints();
        this.drawGraph();
    }

    bindEvents() {
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseenter', () => this.handleMouseEnter());
        this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());
        
        const rInput = document.querySelector('[id$="r"]');
        if (rInput) {
            rInput.addEventListener('change', () => {
                this.handleRChange();
            });
        }
    }

    restoreRFromBean() {
        const rInput = document.querySelector('[id$="r"]');
        if (rInput && rInput.value) {
            this.currentR = parseFloat(rInput.value);
        } else {
            this.currentR = 3.0; 
        }
    }

    handleRChange() {
        const rInput = document.querySelector('[id$="r"]');
        if (rInput && rInput.value) {
            this.currentR = parseFloat(rInput.value);
            this.drawGraph();
        }
    }

    handleCanvasClick(event) {
        if (!this.currentR) {
            this.showFieldError('r', 'Сначала выберите радиус R');
            return;
        }

        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const mathCoords = this.canvasToMath(x, y);
        const roundedX = Math.round(mathCoords.x * 100) / 100;
        const roundedY = Math.round(mathCoords.y * 100) / 100;

        console.log(`Canvas click: X=${roundedX}, Y=${roundedY}, R=${this.currentR}`);

        this.setFormValues(roundedX, roundedY);
        
        this.submitForm(roundedX, roundedY);
    }

    showFieldError(fieldName, message) {
        const messageElement = document.querySelector(`[id$="${fieldName}Message"]`);
        if (messageElement) {
            messageElement.textContent = message;
            messageElement.style.color = '#d9534f';
            messageElement.style.display = 'block';
        }
        
        const fieldElement = document.querySelector(`[id$="${fieldName}"]`);
        if (fieldElement) {
            fieldElement.style.borderColor = '#d9534f';
        }
    }

    canvasToMath(canvasX, canvasY) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const scale = this.getScale();
        
        const mathX = (canvasX - centerX) / scale;
        const mathY = (centerY - canvasY) / scale;
        
        return {
            x: mathX,
            y: mathY
        };
    }

    mathToCanvas(mathX, mathY) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const scale = this.getScale();
        
        return {
            x: centerX + mathX * scale,
            y: centerY - mathY * scale
        };
    }

    getScale() {
        const r = this.currentR || 3;
        return 150 / r;
    }

    setFormValues(x, y) {
        const xInput = document.querySelector('[id$="x"]');
        if (xInput) {
            xInput.value = x;
            this.triggerEvent(xInput, 'input');
            this.triggerEvent(xInput, 'change');
        }
        
        this.setSpinnerValue(y);
    }

    setSpinnerValue(value) {
        const spinnerInput = document.querySelector('[id$="y"]');
        const visibleInput = document.querySelector('[id$="y_input"]');

        if (spinnerInput) {
            spinnerInput.value = value;
            this.triggerEvent(spinnerInput, 'input');
            this.triggerEvent(spinnerInput, 'change');
        }

        if (visibleInput) {
            visibleInput.value = value;
            this.triggerEvent(visibleInput, 'input');
            this.triggerEvent(visibleInput, 'change');
        }
    }

    triggerEvent(element, eventName) {
        const event = new Event(eventName, { bubbles: true });
        element.dispatchEvent(event);
    }

    submitForm(x, y) {
        console.log('submitForm called with:', x, y);
        addPointFromGraph([{
            name: 'x', value: x
        }, {
            name: 'y', value: y
        }]);
    }

    handleMouseMove(event) {
        const rect = this.canvas.getBoundingClientRect();
        this.mouseX = event.clientX - rect.left;
        this.mouseY = event.clientY - rect.top;
        this.update();
    }

    handleMouseEnter() {
        this.isMouseOver = true;
        this.update();
    }

    handleMouseLeave() {
        this.isMouseOver = false;
        this.update();
    }

    loadExistingPoints() {
        this.points = [];
        
        const pointsField = document.getElementById('mainForm:pointsData');
        if (pointsField && pointsField.value) {
            const pointsData = JSON.parse(pointsField.value);
            
            pointsData.forEach(pointData => {
                const canvasCoords = this.mathToCanvas(pointData.x, pointData.y);
                
                this.points.push({
                    x: canvasCoords.x,
                    y: canvasCoords.y,
                    originalX: pointData.x,
                    originalY: pointData.y,
                    r: pointData.r,
                    hit: pointData.result,
                    isNew: false
                });
            });
        }
    }

    drawGraph() {
        if (!this.ctx) return;
        
        const width = this.canvas.width;
        const height = this.canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;

        this.ctx.clearRect(0, 0, width, height);

        if (this.currentR) {
            this.drawArea(centerX, centerY);
        }
        
        this.drawAxes(centerX, centerY);
        
        this.drawAxisLabels(centerX, centerY);
        
        this.drawPoints();
        
        if (this.isMouseOver) {
            this.drawCoordinates();
        }
    }

    drawArea(centerX, centerY) {
        const r = this.currentR;
        const scale = this.getScale();
        
        this.ctx.fillStyle = 'rgba(100, 150, 255, 0.5)';
        this.ctx.strokeStyle = 'rgba(100, 150, 255, 0.8)';
        this.ctx.lineWidth = 1;
        
        this.ctx.beginPath();
        this.ctx.rect(centerX, centerY - scale * (r), scale * (r), scale * (r));
        this.ctx.fill();
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(centerX, centerY);
        this.ctx.arc(centerX, centerY, scale * r, Math.PI, Math.PI * 1.5, false);
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(centerX, centerY);
        this.ctx.lineTo(centerX + scale * (r/2), centerY);
        this.ctx.lineTo(centerX, centerY + scale * (r/2));
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.stroke();
    }

    drawAxes(centerX, centerY) {
        this.ctx.strokeStyle = '#000';
        this.ctx.lineWidth = 2;
        this.ctx.fillStyle = '#000';

        this.ctx.beginPath();
        this.ctx.moveTo(0, centerY);
        this.ctx.lineTo(this.canvas.width, centerY);
        this.ctx.stroke();

        this.ctx.beginPath();
        this.ctx.moveTo(centerX, this.canvas.height);
        this.ctx.lineTo(centerX, 0);
        this.ctx.stroke();

        this.drawArrow(this.canvas.width, centerY, Math.PI * 1.5); // Y
        this.drawArrow(centerX, 0, Math.PI); // X

        this.ctx.lineWidth = 1;
        const scale = this.getScale();
        
        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const x = centerX + i * scale;
            this.ctx.beginPath();
            this.ctx.moveTo(x, centerY - 5);
            this.ctx.lineTo(x, centerY + 5);
            this.ctx.stroke();
        }

        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const y = centerY - i * scale;
            this.ctx.beginPath();
            this.ctx.moveTo(centerX - 5, y);
            this.ctx.lineTo(centerX + 5, y);
            this.ctx.stroke();
        }
    }

    drawArrow(x, y, angle) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.rotate(angle);
        
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(-5, -10);
        this.ctx.lineTo(5, -10);
        this.ctx.closePath();
        this.ctx.fill();
        
        this.ctx.restore();
    }

    drawAxisLabels(centerX, centerY) {
        this.ctx.fillStyle = '#000';
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';

        const scale = this.getScale();
        
        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const x = centerX + i * scale;
            this.ctx.fillText(i.toString(), x, centerY + 15);
        }

        for (let i = -5; i <= 5; i++) {
            if (i === 0) continue;
            const y = centerY - i * scale;
            this.ctx.fillText(i.toString(), centerX - 15, y);
        }

        this.ctx.fillText('X', this.canvas.width - 10, centerY - 10);
        this.ctx.fillText('Y', centerX + 10, 10);
        this.ctx.fillText('0', centerX - 10, centerY + 15);
    }

    drawPoints() {
        this.points.forEach(point => {
            this.ctx.fillStyle = point.hit ? '#27ae60' : '#e74c3c';
            this.ctx.beginPath();
            this.ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.strokeStyle = '#000';
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
        });
    }

    drawCoordinates() {
        const mathCoords = this.canvasToMath(this.mouseX, this.mouseY);
        const roundedX = Math.round(mathCoords.x * 100) / 100;
        const roundedY = Math.round(mathCoords.y * 100) / 100;
        
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
        this.ctx.fillRect(this.mouseX + 10, this.mouseY - 25, 80, 40);
        
        this.ctx.strokeStyle = '#000';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(this.mouseX + 10, this.mouseY - 25, 80, 40);
        
        this.ctx.fillStyle = '#000';
        this.ctx.font = '10px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`X: ${roundedX}`, this.mouseX + 15, this.mouseY - 10);
        this.ctx.fillText(`Y: ${roundedY}`, this.mouseX + 15, this.mouseY + 5);
    }

    update() {
        this.restoreRFromBean();
        this.loadExistingPoints();
        this.drawGraph();
    }
}
