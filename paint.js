const canvas = document.getElementById('paintCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth - 40; // Adjusted for border and margin
canvas.height = window.innerHeight - 200; // Adjusted for border and margin

// Variables for drawing
let currentColor = '#000000';
let currentStrokeWidth = 1;
let isDrawing = false;
let isBrushMode = false;
let isLineMode = false;
let startX = 0;
let startY = 0;
let lastX = 0;
let lastY = 0;
let strokes = []; // Array to store all strokes

// Stack for undo and redo
let undoStack = [];
let redoStack = [];

// Get stroke width element and its value input
const strokeWidthInput = document.getElementById('strokeWidth');
const strokeWidthValue = document.getElementById('strokeWidthValue');

// Get line cap switch element
const lineCapSwitch = document.getElementById('lineCapSwitch');
let isLineCapRounded = true; // Variable to track line cap style, initialized as rounded by default

lineCapSwitch.addEventListener('change', function() {
    isLineCapRounded = lineCapSwitch.checked;
    redrawCanvas(); // Redraw canvas when line cap switch is toggled
    updateLineCapIcon(); // Update line cap icon based on the state
});

function changeColor(color) {
    currentColor = color;
}

function changeStrokeWidth(width) {
    currentStrokeWidth = width;
    strokeWidthValue.value = width; // Update displayed width value
}

// Event listener for changing stroke width by rewriting the number
strokeWidthValue.addEventListener('input', function () {
    let newWidth = parseInt(this.value);
    if (isNaN(newWidth) || newWidth < parseInt(strokeWidthInput.min) || newWidth > parseInt(strokeWidthInput.max)) {
        this.value = currentStrokeWidth; // Reset to previous value
    } else {
        currentStrokeWidth = newWidth;
        strokeWidthInput.value = newWidth; // Update range input value
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'z') { // Ctrl + Z for undo
        undo();
    } else if (event.ctrlKey && event.shiftKey && event.key === 'Z') { // Ctrl + Shift + Z for redo
        redo();
    } else if (event.key === 'b' || event.key === 'B') { // B for brush tool
        toggleTool('brush');
    } else if (event.key === 'l' || event.key === 'L') { // L for line tool
        toggleTool('line');
    }
});

function resetCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    strokes = [];
    saveState();
}

function toggleTool(tool) {
    isBrushMode = tool === 'brush';
    isLineMode = tool === 'line';
    updateToolIcons();
    
    canvas.removeEventListener('mousedown', startLine);
    canvas.removeEventListener('mousedown', startBrush);
    if (isBrushMode) {
        canvas.addEventListener('mousedown', startBrush);
    } else if (isLineMode) {
        canvas.addEventListener('mousedown', startLine);
    }
}

function updateToolIcons() {
    document.getElementById('brushIcon').src = isBrushMode ? 'brush_icon_active.png' : 'brush_icon_inactive.png';
    document.getElementById('lineIcon').src = isLineMode ? 'line_icon_active.png' : 'line_icon_inactive.png';
}

function startLine(e) {
    isDrawing = true;
    startX = e.clientX - canvas.getBoundingClientRect().left;
    startY = e.clientY - canvas.getBoundingClientRect().top;
    canvas.addEventListener('mousemove', drawLine);
    canvas.addEventListener('mouseup', stopLine);
    saveState();
}

function drawLine(e) {
    if (isDrawing) {
        let x = e.clientX - canvas.getBoundingClientRect().left;
        let y = e.clientY - canvas.getBoundingClientRect().top;
        redrawCanvas(); // Clear canvas before drawing the preview line
        draw(startX, startY, x, y, currentColor, currentStrokeWidth, isLineCapRounded); // Draw the preview line
    }
}

function stopLine(e) {
    let x = e.clientX - canvas.getBoundingClientRect().left;
    let y = e.clientY - canvas.getBoundingClientRect().top;
    draw(startX, startY, x, y, currentColor, currentStrokeWidth, isLineCapRounded); // Final draw of the line
    strokes.push({ type: 'line', startX, startY, endX: x, endY: y, color: currentColor, width: currentStrokeWidth, isRounded: isLineCapRounded });
    isDrawing = false;
    canvas.removeEventListener('mousemove', drawLine);
    canvas.removeEventListener('mouseup', stopLine);
}

function startBrush(e) {
    isDrawing = true;
    lastX = e.clientX - canvas.getBoundingClientRect().left;
    lastY = e.clientY - canvas.getBoundingClientRect().top;
    strokes.push({ type: 'brush', points: [{ x: lastX, y: lastY, color: currentColor }], width: currentStrokeWidth });
    canvas.addEventListener('mousemove', drawBrush);
    canvas.addEventListener('mouseup', stopBrush);
    saveState();
}

function drawBrush(e) {
    if (isDrawing) {
        let x = e.clientX - canvas.getBoundingClientRect().left;
        let y = e.clientY - canvas.getBoundingClientRect().top;
        strokes[strokes.length - 1].points.push({ x, y, color: currentColor });
        drawPoints(strokes[strokes.length - 1].points, currentStrokeWidth);
        lastX = x;
        lastY = y;
    }
}

function stopBrush() {
    isDrawing = false;
    canvas.removeEventListener('mousemove', drawBrush);
}

function draw(x1, y1, x2, y2, color, width, isRounded) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    if (isRounded) {
        ctx.lineCap = 'round'; // Set lineCap to round if the switch is on
    } else {
        ctx.lineCap = 'square'; // Set lineCap to square if the switch is off
    }
    ctx.stroke();
}

function drawPoints(points, width) {
    ctx.lineCap = 'round'; // Set brush cap always round
    for (let i = 1; i < points.length; i++) {
        ctx.beginPath();
        ctx.moveTo(points[i - 1].x, points[i - 1].y);
        ctx.lineTo(points[i].x, points[i].y);
        ctx.strokeStyle = points[i].color;
        ctx.lineWidth = width;
        ctx.stroke();
    }
}

function redrawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    strokes.forEach(stroke => {
        if (stroke.type === 'line') {
            draw(stroke.startX, stroke.startY, stroke.endX, stroke.endY, stroke.color, stroke.width, stroke.isRounded);
        } else if (stroke.type === 'brush') {
            drawPoints(stroke.points, stroke.width);
        }
    });
}

function saveState() {
    // Push current drawing state to undo stack
    undoStack.push(JSON.stringify(strokes));
    // Clear redo stack
    redoStack = [];
}

function undo() {
    if (undoStack.length > 0) {
        // Pop the last state from undo stack
        let lastState = undoStack.pop();
        // Save current state to redo stack
        redoStack.push(JSON.stringify(strokes));
        // Restore the last state
        strokes = JSON.parse(lastState);
        // Redraw canvas
        redrawCanvas();
    }
}

function redo() {
    if (redoStack.length > 0) {
        // Pop the last state from redo stack
        let lastState = redoStack.pop();
        // Save current state to undo stack
        undoStack.push(JSON.stringify(strokes));
        // Restore the last state
        strokes = JSON.parse(lastState);
        // Redraw canvas
        redrawCanvas();
    }
}

// Initial update of tool icons
updateToolIcons();

function updateLineCapIcon() {
    const lineCapIcon = document.getElementById('lineCapIcon');
    if (isLineCapRounded) {
        lineCapIcon.src = 'round_icon.png'; // Set rounded line cap icon
    } else {
        lineCapIcon.src = 'nor_rounded_icon.png'; // Set non-rounded line cap icon
    }
}
