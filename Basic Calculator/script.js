const display = document.getElementById('display');
const operators = ['+', '-', '*', '/'];

function appendValue(input) {
    const currentVal = display.value;
    const lastChar = currentVal.slice(-1);

    if (input === '.') {
        if (currentVal === "" || operators.includes(lastChar)) {
            display.value += "0.";
            return;
        }
        const segments = currentVal.split(/[\+\-\*\/]/);
        const currentNumber = segments[segments.length - 1];
        if (currentNumber.includes('.')) {
            return; 
        }
    }
    if (operators.includes(input)) {
        if (currentVal === "") return;
        if (lastChar === '.') {
            display.value = currentVal.slice(0, -1) + input;
            return;
        }
        if (operators.includes(lastChar)) {
            display.value = currentVal.slice(0, -1) + input;
            return;
        }
    }

    display.value += input;
    display.scrollLeft = display.scrollWidth;
}

function clearDisplay() {
    display.value = "";
}
function deleteLast() {
    display.value = display.value.toString().slice(0, -1);
}

function calculate() {
    try {
        let expression = display.value;
        if (expression === "") return;
        if (operators.includes(expression.slice(-1))) {
            expression = expression.slice(0, -1);
        }
        let result = eval(expression);
        if (!Number.isInteger(result)) {
            result = parseFloat(result.toFixed(10));
        }
        display.value = result;

    } catch (error) {
        display.value = "Error";
        setTimeout(() => clearDisplay(), 1500);
    }
}
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if ((key >= '0' && key <= '9') || operators.includes(key) || key === '.') {
        appendValue(key);
    }

    else if (key === 'Enter') {
        event.preventDefault();
        calculate();
    }
    else if (key === 'Backspace') {
        deleteLast();
    }
    else if (key === 'Escape') {
        clearDisplay();
    }
});

function createRipple(event, button) {
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    let x, y;
    if (event.clientX) { 
        const rect = button.getBoundingClientRect();
        x = event.clientX - rect.left - radius;
        y = event.clientY - rect.top - radius;
    } else {
        x = button.clientWidth / 2 - radius;
        y = button.clientHeight / 2 - radius;
    }

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${x}px`;
    circle.style.top = `${y}px`;
    circle.classList.add("ripple");
    const ripple = button.getElementsByClassName("ripple")[0];
    if (ripple) {
        ripple.remove();
    }

    button.appendChild(circle);
}
const buttons = document.getElementsByTagName("button");
for (const button of buttons) {
    button.addEventListener("click", function(event) {
        createRipple(event, this);
    });
}
document.addEventListener('keydown', function(event) {
    const key = event.key;
    let buttonToAnimate = null;
    const allButtons = Array.from(document.querySelectorAll('.btn'));
    if (key === 'Enter') {
        buttonToAnimate = allButtons.find(b => b.textContent === '=');
        calculate();
    } else if (key === 'Backspace') {
        buttonToAnimate = allButtons.find(b => b.textContent === 'DEL');
        deleteLast();
    } else if (key === 'Escape') {
        buttonToAnimate = allButtons.find(b => b.textContent === 'AC' || b.textContent === 'Reset');
        clearDisplay();
    } else {
        buttonToAnimate = allButtons.find(b => b.textContent === key);
        if ((key >= '0' && key <= '9') || operators.includes(key) || key === '.') {
            appendValue(key);
        }
    }

    if (buttonToAnimate) {
        createRipple(event, buttonToAnimate);
        buttonToAnimate.classList.add('pressed');
        setTimeout(() => {
            buttonToAnimate.classList.remove('pressed');
        }, 100);
    }
});