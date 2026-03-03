// ===============================
// Device Detection
// ===============================
const isMobile = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);

// ===============================
// Desktop Behavior Tracking
// ===============================
let keystrokeTimes = [];
let mouseMovements = [];
let lastKeyTime = null;
let lastMouseMove = null;

// Capture keystroke timing
document.addEventListener("keydown", function () {
    if (isMobile) return;

    const now = Date.now();
    if (lastKeyTime) {
        keystrokeTimes.push(now - lastKeyTime);
    }
    lastKeyTime = now;
});

// Capture mouse movement speed
document.addEventListener("mousemove", function (e) {
    if (isMobile) return;

    const now = Date.now();

    if (lastMouseMove) {
        const timeDiff = now - lastMouseMove.time;
        const dx = e.clientX - lastMouseMove.x;
        const dy = e.clientY - lastMouseMove.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (timeDiff > 0) {
            mouseMovements.push(distance / timeDiff);
        }
    }

    lastMouseMove = {
        x: e.clientX,
        y: e.clientY,
        time: now
    };
});

// ===============================
// Mobile Touch Tracking
// ===============================
let touchIntervals = [];
let touchDistances = [];
let lastTouchTime = null;
let lastTouchX = null;
let lastTouchY = null;

document.addEventListener("touchstart", function (e) {
    if (!isMobile) return;

    const now = Date.now();

    if (lastTouchTime) {
        touchIntervals.push(now - lastTouchTime);
    }

    lastTouchTime = now;

    const touch = e.touches[0];
    lastTouchX = touch.clientX;
    lastTouchY = touch.clientY;
});

document.addEventListener("touchmove", function (e) {
    if (!isMobile || lastTouchX === null) return;

    const touch = e.touches[0];
    const dx = touch.clientX - lastTouchX;
    const dy = touch.clientY - lastTouchY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    touchDistances.push(distance);

    lastTouchX = touch.clientX;
    lastTouchY = touch.clientY;
});

// ===============================
// Send Data to Backend
// ===============================
setInterval(() => {

    let payload = {};

    if (isMobile) {

        const avgTouchInterval =
            touchIntervals.length > 0
                ? touchIntervals.reduce((a, b) => a + b, 0) / touchIntervals.length
                : 0;

        const avgTouchDistance =
            touchDistances.length > 0
                ? touchDistances.reduce((a, b) => a + b, 0) / touchDistances.length
                : 0;

        payload = {
            device: "mobile",
            touch_avg: avgTouchInterval,
            touch_distance: avgTouchDistance
        };

        touchIntervals = [];
        touchDistances = [];

    } else {

        payload = {
            device: "desktop",
            keystrokes: keystrokeTimes,
            mouse: mouseMovements
        };

        keystrokeTimes = [];
        mouseMovements = [];
    }

    fetch("/behavior", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

}, 2000);