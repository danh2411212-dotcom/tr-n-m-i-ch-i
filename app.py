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
            background-color: #030712;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
            touch-action: none;
        }
        #game-container {
            position: relative;
            box-shadow: 0 0 30px rgba(255, 71, 87, 0.4);
            border: 4px solid #ff4757;
            border-radius: 14px;
            background: #000;
        }
        canvas {
            display: block;
            background: linear-gradient(to bottom, #020617 0%, #0f172a 100%);
        }
        #ui {
            position: absolute;
            top: 15px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 15px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            pointer-events: none;
        }
        #controls {
            position: absolute;
            bottom: 15px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-around;
            padding: 0 30px;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid white;
            color: white;
            font-size: 28px;
            width: 85px;
            height: 55px;
            border-radius: 12px;
            cursor: pointer;
            outline: none;
            user-select: none;
        }
        .ctrl-btn:active {
            background: rgba(255, 71, 87, 0.9);
        }
        #start-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(3, 7, 18, 0.96);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
            z-index: 10;
        }
        button.start-btn {
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
        button.start-btn:hover {
            transform: scale(1.08);
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="480" height="640"></canvas>
    <div id="ui">
        <span id="scoreText">🏠 Khoảng cách: 1000m</span>
        <span id="shText" style="color: #ff4757;">🚨 Mẹ SH: 45m</span>
    </div>
    
    <div id="controls">
        <button class="ctrl-btn" onclick="moveLeft()">◀</button>
        <button class="ctrl-btn" onclick="moveRight()">▶</button>
    </div>

    <div id="start-screen">
        <h2 style="color: #ff4757; margin-bottom: 5px;">🌙 ĐUA XE ĐÊM: TRỐN MẸ VỀ NHÀ 🛵</h2>
        <p style="max-width: 360px; color: #cbd5e1; font-size: 13px; line-height: 1.6;">
            Trốn mẹ lấy chiếc xe điện cá tính đi chơi đêm, bỗng nghe tiếng pô SH quen thuộc phía sau... Mẹ đang đuổi gắt! 
            <br><br><b>Né ổ gà, tránh thùng rác và phóng về nhà an toàn!</b>
        </p>
        <p style="font-size: 12px; color: #fbbf24;">💻 Máy tính: Phím <b>Trái/Phải</b> hoặc <b>A/D</b><br>📱 Điện thoại: Nút <b>◀ ▶</b> hoặc <b>Vuốt màn hình</b></p>
        <button class="start-btn" onclick="startGame()">BẮT ĐẦU CHẠY TRỐN</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let gameRunning = false;
let distance = 1000; 
let shDistance = 45; 

let playerLane = 1; // 0: Trái, 1: Giữa, 2: Phải
let obstacles = [];
let obstacleTimer = 0;
let roadAnim = 0;

function moveLeft() {
    if (!gameRunning) return;
    if (playerLane > 0) playerLane--;
}

function moveRight() {
    if (!gameRunning) return;
    if (playerLane < 2) playerLane++;
}

window.addEventListener("keydown", (e) => {
    if (!gameRunning) return;
    if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") moveLeft();
    if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") moveRight();
});

let touchStartX = 0;
window.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; });
window.addEventListener("touchend", (e) => {
    if (!gameRunning) return;
    let diffX = e.changedTouches[0].clientX - touchStartX;
    if (diffX > 30) moveRight();
    if (diffX < -30) moveLeft();
});

function startGame() {
    document.getElementById("start-screen").style.display = "none";
    gameRunning = true;
    distance = 1000;
    shDistance = 45;
    obstacles = [];
    playerLane = 1;
    loop();
}

function getPerspectiveCoords(lane, z) {
    let horizonX = 240;
    let horizonY = 180;
    let bottomY = 580;
    let widthBottom = 340;
    let widthHorizon = 40;
    
    let currentY = horizonY + (bottomY - horizonY) * z;
    let currentWidth = widthHorizon + (widthBottom - widthHorizon) * z;
    let laneOffset = (lane - 1) * (currentWidth / 3);
    let currentX = horizonX + laneOffset + (currentWidth / 6) * (lane === 0 ? 0.5 : (lane === 2 ? -0.5 : 0));
    
    return { x: currentX, y: currentY, width: currentWidth };
}

function update() {
    if (!gameRunning) return;

    roadAnim += 0.05;
    if (roadAnim > 1) roadAnim = 0;

    distance -= 0.6;
    shDistance += 0.025;
    if (shDistance > 75) shDistance = 75;

    obstacleTimer++;
    if (obstacleTimer > 38) {
        obstacleTimer = 0;
        let randomLane = Math.floor(Math.random() * 3);
        let types = ['ogap', 'thungrac'];
        let type = types[Math.floor(Math.random() * types.length)];
        obstacles.push({
            lane: randomLane,
            z: 0.1,
            speed: 0.016,
            type: type
        });
    }

    for (let i = obstacles.length - 1; i >= 0; i--) {
        obstacles[i].z += obstacles[i].speed;
        
        if (obstacles[i].z >= 0.8 && obstacles[i].z <= 0.93) {
            if (obstacles[i].lane === playerLane) {
                shDistance -= 14; 
                obstacles.splice(i, 1);
                if (shDistance <= 0) gameOver(false);
            }
        } 
        
        if (obstacles[i].z > 1.02) {
            obstacles.splice(i, 1);
        }
    }

    if (distance <= 0) gameOver(true);
    if (shDistance <= 5) gameOver(false);

    document.getElementById("scoreText").innerText = "🏠 Khoảng cách: " + Math.max(0, Math.floor(distance)) + "m";
    document.getElementById("shText").innerText = "🚨 Mẹ SH: " + Math.max(0, Math.floor(shDistance)) + "m";
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Bầu trời đêm
    ctx.fillStyle = "#020617";
    ctx.fillRect(0, 0, 480, 180);

    // 2. Con đường nhựa 2.5D phối cảnh
    let horizonX = 240;
    let horizonY = 180;
    
    ctx.fillStyle = "#1e293b";
    ctx.beginPath();
    ctx.moveTo(horizonX - 25, horizonY);
    ctx.lineTo(horizonX + 25, horizonY);
    ctx.lineTo(440, 580);
    ctx.lineTo(40, 580);
    ctx.closePath();
    ctx.fill();

    // Vỉa hè hai bên
    ctx.fillStyle = "#0f172a";
    ctx.beginPath(); ctx.moveTo(0, 580); ctx.lineTo(40, 580); ctx.lineTo(horizonX - 25, horizonY); ctx.lineTo(0, horizonY); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(480, 580); ctx.lineTo(440, 580); ctx.lineTo(horizonX + 25, horizonY); ctx.lineTo(480, horizonY); ctx.closePath(); ctx.fill();

    // Vạch chia làn
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(horizonX - 8, horizonY); ctx.lineTo(170, 580); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(horizonX + 8, horizonY); ctx.lineTo(310, 580); ctx.stroke();

    // 3. Chướng ngại vật
    for (let obs of obstacles) {
        let coords = getPerspectiveCoords(obs.lane, obs.z);
        let scale = obs.z * 1.6;
        
        ctx.save();
        ctx.font = Math.floor(30 * scale) + "px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        if (obs.type === 'ogap') {
            ctx.fillText("🕳️", coords.x, coords.y);
        } else {
            ctx.fillText("🗑️", coords.x, coords.y);
        }
        ctx.restore();
    }

    // 4. Nhân vật ngồi trên Xe Điện (Con đang lái trốn)
    let playerCoords = getPerspectiveCoords(playerLane, 0.88);
    ctx.save();
    let px = playerCoords.x;
    let py = playerCoords.y;

    // Vẽ người con đội mũ bảo hiểm ngồi trên xe điện
    ctx.fillStyle = "#ef4444"; // Áo đỏ của con
    ctx.beginPath(); ctx.arc(px, py - 18, 12, 0, Math.PI * 2); ctx.fill(); // Đầu & mũ
    ctx.fillStyle = "#38bdf8"; // Thân người
    ctx.fillRect(px - 10, py - 10, 20, 22);

    // Thân xe điện trắng cá tính
    ctx.fillStyle = "#f8fafc";
    ctx.fillRect(px - 14, py + 10, 28, 25);
    ctx.fillStyle = "#0284c7"; // Đèn hậu xe điện
    ctx.shadowBlur = 12; ctx.shadowColor = "#38bdf8";
    ctx.fillRect(px - 10, py + 30, 20, 5);
    ctx.restore();

    // 5. Nhân vật Mẹ ngồi trên Xe SH rượt đuổi phía sau
    ctx.save();
    let shX = 240 + Math.sin(Date.now() * 0.009) * 30;
    let shY = 595;
    
    // Ánh đèn pha xe SH chiếu sáng rực rỡ phía trước
    let gradient = ctx.createRadialGradient(shX, shY - 30, 10, shX, shY, 140);
    gradient.addColorStop(0, "rgba(255, 255, 255, 0.6)");
    gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 450, 480, 190);

    // Vẽ người mẹ đang lái xe SH (tư thế quyết liệt đuổi theo)
    ctx.fillStyle = "#1e293b"; // Quần áo mẹ gọn gàng
    ctx.beginPath(); ctx.arc(shX, shY - 28, 15, 0, Math.PI * 2); ctx.fill(); // Đầu mẹ
    ctx.fillStyle = "#ffffff"; // Áo khoác trắng của mẹ
    ctx.fillRect(shX - 14, shY - 18, 28, 28);

    // Thân xe SH trắng hoành tráng của mẹ
    ctx.fillStyle = "#ffffff";
    ctx.shadowBlur = 15; ctx.shadowColor = "#ffffff";
    ctx.fillRect(shX - 18, shY + 6, 36, 32);
    ctx.restore();
}

function gameOver(isWin) {
    gameRunning = false;
    let startScreen = document.getElementById("start-screen");
    startScreen.style.display = "flex";
    if (isWin) {
        startScreen.innerHTML = `
            <h1 style="color: #4ade80;">🎉 AN TOÀN VỀ NHÀ! 🎉</h1>
            <p style="color: #fff;">Bạn đã phóng xe điện về nhà cất chu đáo trước khi mẹ kịp tóm!</p>
            <button class="start-btn" onclick="startGame()">CHƠI LẠI</button>
        `;
    } else {
        startScreen.innerHTML = `
            <h1 style="color: #ef4444;">💥 BỊ MẸ SH TÓM RỒI! 💥</h1>
            <p style="color: #fff;">Mẹ đã phóng xe SH áp sát và tóm gọn bạn tại trận!</p>
            <button class="start-btn" onclick="startGame()">THỬ LẠI</button>
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
