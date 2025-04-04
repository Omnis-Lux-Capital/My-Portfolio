let expression = "";

const display = document.getElementById("lcd-display");

function press(val) {
  if (val === "C") {
    expression = "";
    updateDisplay("0");
    return;
  }

  if (val === "=") {
    try {
      const result = eval(
        expression
          .replace(/×/g, '*')
          .replace(/÷/g, '/')
      );
      updateDisplay(result);
      expression = "";
    } catch {
      updateDisplay("Err");
      expression = "";
    }
    return;
  }

  expression += val;
  updateDisplay(expression);
}

function updateDisplay(value) {
  display.textContent = value;
}