class PointValidator {
    static xValues = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
    static rValues = [1, 2, 3, 4, 5];

    static isValidX(x) {
        return this.xValues.includes(parseFloat(x));
    }

    static isValidY(y) {
        const yNum = parseFloat(y);
        return !isNaN(yNum) && yNum >= -5 && yNum <= 5;
    }

    static isValidR(r) {
        return this.rValues.includes(parseFloat(r));
    }

    static validateForm(x, y, r) {
        const errors = [];

        if (!this.isValidX(x)) {
            errors.push('Координата X должна быть выбрана из кнопок');
        }

        if (!this.isValidY(y)) {
            errors.push('Координата Y должна быть числом от -5 до 5');
        }

        if (!this.isValidR(r)) {
            errors.push('Радиус R должен быть выбран из предложенных значений');
        }

        return errors;
    }

    static getCurrentX(x) {
        return Math.max(-4, Math.min(4, Math.round(x)));
    }

    static validateYRealTime(y) {
        if (!this.isValidY(y)) {
            return 'Y должен быть числом от -5 до 5';
        }
        return '';
    }
}

class FormManager {
    constructor() {
        this.init();
    }

    init() {
        this.restoreFormState();
        this.setupXButtons();
        this.setupFormValidation();
        this.setupRCheckboxes();
        this.setupClearButton();
        this.setupBackToFormButton();
    }

    setupClearButton() {
        const clearBtn = document.querySelector('.clear-btn');
        if (clearBtn) {
            clearBtn.replaceWith(clearBtn.cloneNode(true));
            const newClearBtn = document.querySelector('.clear-btn');
            
            newClearBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.clearFormAndResults();
            });
        } else {
            console.error('Clear button not found');
        }
    }

    setupXButtons() {
        document.querySelectorAll('.x-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.selectXButton(btn.value);
            });
        });
    }

    selectXButton(xValue) {
        document.querySelectorAll('.x-btn').forEach(b => {
            b.classList.remove('active');
        });
        
        const targetBtn = Array.from(document.querySelectorAll('.x-btn'))
            .find(btn => btn.value === xValue);
        
        if (targetBtn) {
            targetBtn.classList.add('active');
            document.getElementById('x').value = xValue;
            document.getElementById('xError').textContent = '';
        }
    }

    restoreFormState() {
        const currentX = document.getElementById('x').value;
        if (currentX && currentX.trim() !== '') {
            this.selectXButton(currentX);
        }
        
        const currentY = document.getElementById('y').value;
        if (currentY && currentY.trim() !== '') {
            document.getElementById('yError').textContent = '';
        }
        
        this.updateRCheckboxStyles();
        
        console.log('Form state restored from bean:', {
            x: currentX,
            y: currentY,
            r: this.getSelectedRValues()
        });
    }

    setupRCheckboxes() {
        document.querySelectorAll('.r-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.updateRCheckboxStyles();
                document.getElementById('rError').textContent = '';
            });
        });
    }

    updateRCheckboxStyles() {
        document.querySelectorAll('.r-checkbox').forEach(checkbox => {
            const label = checkbox.closest('.checkbox-label');
            if (checkbox.checked) {
                label.classList.add('selected');
            } else {
                label.classList.remove('selected');
            }
        });
    }

    setupFormValidation() {
        const form = document.getElementById('pointForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm()) {
                    e.preventDefault();
                }
            });
        }
    }

    validateForm() {
        const x = document.getElementById('x').value;
        const y = document.getElementById('y').value;
        const selectedRValues = this.getSelectedRValues(); 
        
        let isValid = true;

        if (!x) {
            document.getElementById('xError').textContent = 'Выберите X';
            isValid = false;
        } else if (!PointValidator.isValidX(x)) {
            document.getElementById('xError').textContent = 'Некорректное значение X';
            isValid = false;
        } else {
            document.getElementById('xError').textContent = '';
        }

        if (!y) {
            document.getElementById('yError').textContent = 'Введите координату Y';
            isValid = false;
        } else if (!PointValidator.isValidY(y)) {
            document.getElementById('yError').textContent = 'Y должен быть числом от -5 до 5';
            isValid = false;
        } else {
            document.getElementById('yError').textContent = '';
        }

        if (selectedRValues.length === 0) {
            document.getElementById('rError').textContent = 'Выберите хотя бы один радиус R';
            isValid = false;
        } else {
            const invalidRValues = [];
            selectedRValues.forEach(r => {
                if (!PointValidator.isValidR(r)) {
                    invalidRValues.push(r);
                }
            });

            if (invalidRValues.length > 0) {
                document.getElementById('rError').textContent = `Некорректные значения R: ${invalidRValues.join(', ')}`;
                isValid = false;
            } else {
                document.getElementById('rError').textContent = '';
            }
        }

        return isValid;
    }

    getSelectedRValues() {
        const selectedValues = [];
        const rCheckboxes = document.querySelectorAll('.r-checkbox:checked');
        rCheckboxes.forEach(checkbox => {
            selectedValues.push(checkbox.value);
        });
        return selectedValues;
    }

    setCoordinatesFromGraph(x, y) {
        this.selectXButton(x.toString());
        document.getElementById('y').value = y.toFixed(2);
        document.getElementById('yError').textContent = '';
    }

    clearFormAndResults() {
        this.clearForm();
        if (window.graphManager && typeof window.graphManager.clearPoints === 'function') {
            window.graphManager.clearPoints();
        }
        const form = document.getElementById('pointForm');
        
        form.action = 'controller';
        form.method = 'POST';
        
        const clearInput = document.createElement('input');
        clearInput.type = 'hidden';
        clearInput.name = 'clear';
        clearInput.value = 'true';
        form.appendChild(clearInput);
        
        form.submit();
        
    }

    clearForm() {
        document.querySelectorAll('.x-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById('x').value = '';
        document.getElementById('y').value = '';
        
        document.querySelectorAll('.r-checkbox').forEach(checkbox => {
            checkbox.checked = false;
        });
        this.updateRCheckboxStyles();
        
        this.clearErrors();
    }

    clearErrors() {
        document.getElementById('xError').textContent = '';
        document.getElementById('yError').textContent = '';
        document.getElementById('rError').textContent = '';
    }

    setupBackToFormButton() {
        const backButton = document.getElementById('backToForm');
        if (backButton) {
            backButton.addEventListener('click', (e) => {
                e.preventDefault();
                document.getElementById('backForm').submit();
            });
        }
    }


}