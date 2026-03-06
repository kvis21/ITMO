const possibleValuesX = new Set([-3, -2, -1, 0, 1, 2, 3, 4, 5]);
const possibleValuesR = new Set([1, 1.5, 2.0, 2.5, 3.0]);

let x = null;
let y = null;
let listR = null;
let isFormValid = false;

const submitBtn = document.querySelector('.submit-btn');

const validateForm = () => {
    const isXValid = x !== null && possibleValuesX.has(x);
    const isYValid = y !== null && y >= -5 && y <= 3;
    const isRValid = listR !== null && listR.length > 0 && listR.every(r => possibleValuesR.has(r));
    
    isFormValid = isXValid && isYValid && isRValid;
    updateSubmitButton();
};

const updateSubmitButton = () => {
    if (isFormValid) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('disabled');
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.add('disabled');
    }
};

const validateX = (x) => {
    if (!possibleValuesX.has(x)) {
        throw new Error("Invalid X: X must be one of [-3, -2, -1, 0, 1, 2, 3, 4, 5]");
    }
    return x;
}

const validateY = (y) => {
    if (y < -5 || y > 3) {
        throw new Error("Invalid Y: Y must be in range [-5, 3]")
    }
    return y;
}

document.getElementById("x").addEventListener("change", (ev) => {
    try {
        x = parseInt(ev.target.value);
        x = validateX(x);
        ev.target.classList.remove('error');
    } catch (error) {
        x = null;
        ev.target.classList.add('error');
    }
    validateForm();
});

document.getElementById("y").addEventListener("input", (ev) => {
    try {
        y = parseFloat(ev.target.value);
        y = validateY(y);
        ev.target.classList.remove('error');
    } catch (error) {
        y = null;
        ev.target.classList.add('error');
    }
    validateForm();
});

document.getElementsByName("r").forEach(checkbox => {
    checkbox.addEventListener("change", (ev) => {
        listR = Array.from(document.getElementsByName("r"))
            .filter(input => input.checked)
            .map(input => parseFloat(input.value));
        
        document.querySelectorAll('.checkbox-label').forEach(label => {
            label.classList.remove('error');
        });
        
        if (listR.length === 0) {
            document.querySelectorAll('.checkbox-label').forEach(label => {
                label.classList.add('error');
            });
        }
        
        validateForm();
    });
});

document.getElementById("pointForm").addEventListener("submit", (ev) => {
    if (!isFormValid) {
        ev.preventDefault();
        alert("Пожалуйста, заполните все поля корректно перед отправкой");
    }
});

document.addEventListener('DOMContentLoaded', () => {
    updateSubmitButton();
});