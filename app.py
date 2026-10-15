

   import streamlit as st

st.set_page_config(
    page_title="Đua Xe Đêm: Trốn Mẹ Về Nhà", page_icon="🛵", layout="centered"
)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Đua Xe Đêm: Trốn Mẹ Về Nhà</title>
    <style>
        body {
            margin: 0;
            background-color: #05050d;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 0 25px rgba(255, 71, 87, 0.4);
            border: 3px solid #ff4757;
            border-radius: 12px;
            background: #111;
        }
        canvas {
            display: block;
            background: #1a1a2e;
        }
        #ui {
            position: absolute;
            top: 15px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            pointer-events: none;
        }
        #start-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 10, 20, 0.92);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }
        button {
            background: linear-gradient(45deg, #ff4757, #ff6b81);
            color: white;
            border: none;
            padding: 14px 32px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(255, 71, 87, 0.5);
            transition: 0.2s;
        }
        button:hover {
            transform: scale(1.08);
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="480" height="640"></canvas>
    <div id="ui">
        <span id="scoreText">🏠 Khoảng cách: 1000m</span>
        <span id="shText" style="color: #ff6b81;">🚨 Mẹ SH cách: 45m</span>
    </div>
    
    <div id="start-screen">
        <h2 style="color: #ff4757; margin-bottom: 5px;">🌙 ĐUA XE ĐÊM: TRỐN MẸ VỀ NHÀ 🛵</h2>
        <p style="max-width: 360px; color: #ddd; font-size: 13px; line-height: 1.6;">
            Trốn mẹ lấy xe điện đi chơi đêm, bỗng nghe tiếng pô SH quen thuộc phía sau... Mẹ đang đuổi gắt! 
            <br><br><b>Né ổ gà, vượt chướng ngại vật và phóng về nhà an toàn!</b>
        </p>
        <p style="font-size: 12px; color: #ffa502;">👉 Dùng phím <b>Trái / Phải</b> (hoặc A/D) để lách xe.</p>
        <button onclick="startGame()">BẮT ĐẦU CHẠY TRỐN</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let gameRunning = false;
let distance = 1000; 
let shDistance = 45; 

// 3 làn đường (x = 120, 240, 360)
const lanes = [120, 240, 360];
let playerLaneIndex = 1; 
let playerX = lanes[playerLaneIndex];
let playerY = 500;

let obstacles = [];
let obstacleTimer = 0;
let roadAnim = 0;

// Điều khiển bàn phím
window.addEventListener("keydown", (e) => {
    if (!gameRunning) return;
    if (e.key === "ArrowLeft" || e.key === "a") {
        if (playerLaneIndex > 0) playerLaneIndex--;
    }
    if (e.key === "ArrowRight" || e.key === "d") {
        if (playerLaneIndex < lanes.length - 1) playerLaneIndex++;
    }
});

function startGame() {
    document.getElementById("start-screen").style.display = "none";
    gameRunning = true;
    distance = 1000;
    shDistance = 45;
    obstacles = [];
    playerLaneIndex = 1;
    loop();
}

function update() {
    if (!gameRunning) return;

    // Hiệu ứng lướt đường
    roadAnim += 6;
    if (roadAnim > 40) roadAnim = 0;

    let targetX = lanes[playerLaneIndex];
    playerX += (targetX - playerX) * 0.25;

    distance -= 0.6;
    shDistance += 0.025;
    if (shDistance > 75) shDistance = 75;

    obstacleTimer++;
    if (obstacleTimer > 50) {
        obstacleTimer = 0;
        let randomLane = Math.floor(Math.random() * 3);
        let types = ['ogap', 'thungrac'];
        let type = types[Math.floor(Math.random() * types.length)];
        obstacles.push({
            lane: randomLane,
            y: -60,
            speed: 6,
            type: type
        });
    }

    // Xử lý va chạm chướng ngại vật
    for (let i = obstacles.length - 1; i >= 0; i--) {
        obstacles[i].y += obstacles[i].speed;
        let obsX = lanes[obstacles[i].lane];
        
        if (obstacles[i].y > playerY - 35 && obstacles[i].y < playerY + 35 && Math.abs(obsX - playerX) < 35) {
            shDistance -= 12; // Đâm trúng vật cản bị mẹ áp sát
            obstacles.splice(i, 1);
            if (shDistance <= 0) gameOver(false);
        } else if (obstacles[i].y > canvas.height) {
            obstacles.splice(i, 1);
        }
    }

    if (distance <= 0) gameOver(true);
    if (shDistance <= 5) gameOver(false);

    document.getElementById("scoreText").innerText = "🏠 Khoảng cách: " + Math.max(0, Math.floor(distance)) + "m";
    document.getElementById("shText").innerText = "🚨 Mẹ SH cách: " + Math.max(0, Math.floor(shDistance)) + "m";
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Vẽ phong cảnh đường phố ban đêm (Giả lập 2.5D)
    ctx.fillStyle = "#0f172a"; // Vỉa hè / Lề đường tối
    ctx.fillRect(0, 0, 70, canvas.height);
    ctx.fillRect(410, 0, 70, canvas.height);

    // Lòng đường nhựa
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(70, 0, 340, canvas.height);

    // Vạch kẻ đường đứt đoạn chuyển động tạo cảm giác tốc độ
    ctx.strokeStyle = "#facc15";
    ctx.lineWidth = 4;
    ctx.setLineDash([25, 25]);
    ctx.lineDashOffset = -roadAnim;
    ctx.beginPath();
    ctx.moveTo(183, 0); ctx.lineTo(183, canvas.height);
    ctx.moveTo(297, 0); ctx.lineTo(297, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);

    // 2. Vẽ Chướng ngại vật
    for (let obs of obstacles) {
        let ox = lanes[obs.lane];
        let oy = obs.y;
        ctx.save();
        if (obs.type === 'ogap') {
            ctx.fillStyle = "#020617";
            ctx.beginPath();
            ctx.ellipse(ox, oy, 28, 14, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#475569";
            ctx.lineWidth = 3;
            ctx.stroke();
        } else {
            ctx.fillStyle = "#ea580c";
            ctx.fillRect(ox - 16, oy - 22, 32, 38);
            ctx.fillStyle = "#c2410c";
            ctx.fillRect(ox - 19, oy - 28, 38, 7);
        }
        ctx.restore();
    }

    // 3. Vẽ Xe Điện của Con (Tạo hình sắc nét phong cách 2.5D)
    ctx.save();
    let cx = playerX;
    let cy = playerY;

    // Đèn hậu xe điện sáng rực
    ctx.fillStyle = "#22d3ee";
    ctx.shadowBlur = 12;
    ctx.shadowColor = "#22d3ee";
    ctx.fillRect(cx - 12, cy + 18, 24, 5);

    // Thân xe điện trắng cá tính
    ctx.fillStyle = "#f8fafc";
    ctx.beginPath();
    ctx.roundRect(cx - 14, cy - 20, 28, 42, 8);
    ctx.fill();
    
    // Yên xe đen
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(cx - 10, cy - 5, 20, 16);

    // Người con đội mũ
    ctx.fillStyle = "#ef4444"; 
    ctx.beginPath();
    ctx.arc(cx, cy - 12, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 4. Vẽ xe SH của Mẹ rượt đuổi phía sau (Có ánh đèn pha chiếu sáng rực rỡ)
    ctx.save();
    let shX = 240 + Math.sin(Date.now() * 0.008) * 35;
    let shY = 585;

    // Hiệu ứng ánh đèn pha SH quét phía trước
    let gradient = ctx.createRadialGradient(shX, shY, 15, shX, shY + 60, 140);
    gradient.addColorStop(0, "rgba(255, 255, 255, 0.45)");
    gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 420, 480, 220);

    // Thân xe SH trắng của mẹ
    ctx.fillStyle = "#ffffff";
    ctx.shadowBlur = 15;
    ctx.shadowColor = "#ffffff";
    ctx.beginPath();
    ctx.roundRect(shX - 18, shY - 12, 36, 50, 12);
    ctx.fill();
    
    ctx.restore();
}

function gameOver(isWin) {
    gameRunning = false;
    let startScreen = document.getElementById("start-screen");
    startScreen.style.display = "flex";
    if (isWin) {
        startScreen.innerHTML = `
            <h1 style="color: #22c55e;">🎉 AN TOÀN VỀ NHÀ! 🎉</h1>
            <p style="color: #fff;">Bạn đã phi xe điện về cất chu đáo trước khi mẹ kịp đuổi tới nơi!</p>
            <button onclick="startGame()">CHƠI LẠI</button>
        `;
    } else {
        startScreen.innerHTML = `
            <h1 style="color: #ef4444;">💥 BỊ MẸ SH TÓM RỒI! 💥</h1>
            <p style="color: #fff;">Xe SH của mẹ quá mạnh và bạn đã lỡ đâm phải vật cản. Tới công chuyện luôn!</p>
            <button onclick="startGame()">THỬ LẠI</button>
        `;
    }
}

function loop() {
    update();
    draw();
    if (gameRunning) requestAnimationFrame(loop);
}
</script>

</body>
</html>
"""

st.components.v1.html(game_html, height=680, scrolling=False)

    
