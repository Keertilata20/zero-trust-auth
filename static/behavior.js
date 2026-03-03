let keystrokeTimes = [];
let mouseMovements = [];

let lastKeyTime = null;

// Capture keystroke timing
document.addEventListener("keydown", function () {
    let now = Date.now();
    if (lastKeyTime) {
        keystrokeTimes.push(now - lastKeyTime);
    }
    lastKeyTime = now;
});

// Capture mouse movement speed
let lastMouseMove = null;

document.addEventListener("mousemove", function (e) {
    let now = Date.now();

    if (lastMouseMove) {
        let timeDiff = now - lastMouseMove.time;
        let dx = e.clientX - lastMouseMove.x;
        let dy = e.clientY - lastMouseMove.y;
        let distance = Math.sqrt(dx * dx + dy * dy);

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

// Send behavior data to backend every 10 seconds
setInterval(() => {
    fetch("/behavior", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            keystrokes: keystrokeTimes,
            mouse: mouseMovements
        })
    });

    keystrokeTimes = [];
    mouseMovements = [];

}, 2000);
// Fetch latest trust status every 5 seconds
setInterval(() => {
    fetch("/status")
    .then(res => res.json())
    .then(data => {
        document.getElementById("risk-status").innerText = data.risk;
    });
}, 8000);

