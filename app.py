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
            box-shadow: 0 0 35px rgba(255, 71, 87, 0.4);
            border: 4px solid #ff4757;
            border-radius: 16px;
            background: #000;
            width: 480px;
            height: 640px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: linear-gradient(to bottom, #020617 0%, #0f172a 100%);
            image-rendering: pixelated;
        }
        
        #lobby-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0f172a 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 30px 20px;
            box-sizing: border-box;
            z-index: 20;
        }
        .house-banner {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }
        .character-preview {
            font-size: 75px;
            margin: 10px 0;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
            animation: bounce 1.5s infinite alternate;
        }
        @keyframes bounce {
            0% { transform: translateY(0); }
            100% { transform: translateY(-10px); }
        }
        
        .play-btn {
            background: linear-gradient(45deg, #22c55e, #16a34a);
            color: white;
            border: 3px solid #4ade80;
            padding: 16px 45px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 35px;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(34, 197, 94, 0.5);
            transition: 0.2s;
            text-transform: uppercase;
        }
        .play-btn:hover {
            transform: scale(1.08);
            background: linear-gradient(45deg, #16a34a, #15803d);
        }

        #game-ui {
            position: absolute;
            top: 15px; left: 15px; right: 15px;
            display: flex; justify-content: space-between;
            font-size: 15px; font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            pointer-events: none; display: none; z-index: 10;
        }
        #controls {
            position: absolute;
            bottom: 15px; left: 0; right: 0;
            display: flex; justify-content: space-around;
            padding: 0 30px; display: none; z-index: 10;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid white; color: white;
            font-size: 28px; width: 85px; height: 55px;
            border-radius: 12px; cursor: pointer; outline: none; user-select: none;
        }
        .ctrl-btn:active { background: rgba(255, 71, 87, 0.9); }
        
        #end-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(3, 7, 18, 0.95);
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            text-align: center; padding: 20px; display: none; z-index: 30;
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- Sảnh chờ Tom Gold Run style -->
    <div id="lobby-screen">
        <div class="house-banner">
            <h3 style="color: #38bdf8; margin: 0 0 5px 0;">🏡 NHÀ CỦA TÔI</h3>
            <p style="color: #cbd5e1; font-size: 12px; margin: 0;">Chuẩn bị lấy xe điện độ đi lượn phố đêm!</p>
        </div>
        
        <div>
            <div class="character-preview">🛵</div>
            <h2 style="color: #ff4757; margin: 5px 0; font-size: 20px;">ĐUA XE ĐÊM: TRỐN MẸ VỀ NHÀ</h2>
            <p style="color: #94a3b8; font-size: 12px; max-width: 300px; line-height: 1.4;">
                Né ổ gà, tránh thùng rác và chạy trốn tiếng pô SH của mẹ gầm rú phía sau!
            </p>
        </div>

        <button class="play-btn" onclick="startJourney()">BẮT ĐẦU CHƠI</button>
    </div>

    <!-- Canvas Game -->
    <canvas id="gameCanvas" width="480" height="640"></canvas>
    
    <div id="game-ui">
        <span id="scoreText">🏠 Khoảng cách: 1000m</span>
        <span id="shText" style="color: #ff4757;">🚨 Mẹ SH: 45m</span>
    </div>
    
    <div id="controls">
        <button class="ctrl-btn" onclick="moveLeft()">◀</button>
        <button class="ctrl-btn" onclick="moveRight()">▶</button>
    </div>

    <div id="end-screen">
        <h1 id="end-title" style="margin-bottom: 10px;"></h1>
        <p id="end-desc" style="color: #cbd5e1; font-size: 14px; margin-bottom: 20px;"></p>
        <button class="play-btn" onclick="returnToLobby()" style="font-size: 16px; padding: 12px 30px;">VỀ SẢNH CHỜ</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

let gameRunning = false;
let distance = 1000; 
let shDistance = 45; 

let playerLane = 1; 
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

function startJourney() {
    document.getElementById("lobby-screen").style.display = "none";
    document.getElementById("game-ui").style.display = "flex";
    document.getElementById("controls").style.display = "flex";
    document.getElementById("end-screen").style.display = "none";
    
    gameRunning = true;
    distance = 1000;
    shDistance = 45;
    obstacles = [];
    playerLane = 1;
    loop();
}

function returnToLobby() {
    document.getElementById("end-screen").style.display = "none";
    document.getElementById("game-ui").style.display = "none";
    document.getElementById("controls").style.display = "none";
    document.getElementById("lobby-screen").style.display = "flex";
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

    // 4. Nhân vật đứa con lái xe điện (Dạng Pixel vuông chi tiết)
    let playerCoords = getPerspectiveCoords(playerLane, 0.88);
    ctx.save();
    let px = playerCoords.x;
    let py = playerCoords.y;

    // Vẽ khối Pixel xe điện trắng cá tính
    ctx.fillStyle = "#f8fafc";
    ctx.fillRect(px - 14, py, 28, 35);
    ctx.fillStyle = "#0f172a"; // Chỗ để chân
    ctx.fillRect(px - 10, py + 10, 20, 15);
    ctx.fillStyle = "#38bdf8"; // Đèn hậu xanh sáng rực
    ctx.shadowBlur = 10; ctx.shadowColor = "#38bdf8";
    ctx.fillRect(px - 10, py + 30, 20, 5);

    // Vẽ nhân vật đứa con ngồi trên xe
    ctx.fillStyle = "#ef4444"; // Mũ bảo hiểm đỏ
    ctx.fillRect(px - 8, py - 18, 16, 14);
    ctx.fillStyle = "#38bdf8"; // Áo khoác
    ctx.fillRect(px - 10, py - 4, 20, 12);
    ctx.restore();

    // 5. Mẹ chạy xe SH đuổi theo phía sau (Dạng Pixel vuông chi tiết)
    ctx.save();
    let shX = 240 + Math.sin(Date.now() * 0.009) * 30;
    let shY = 590;
    
    // Ánh đèn pha xe SH quét sáng rực
    let gradient = ctx.createRadialGradient(shX, shY - 30, 10, shX, shY, 140);
    gradient.addColorStop(0, "rgba(255, 255, 255, 0.6)");
    gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 450, 480, 190);

    // Thân xe SH trắng của mẹ
    ctx.fillStyle = "#ffffff";
    ctx.shadowBlur = 15; ctx.shadowColor = "#ffffff";
    ctx.fillRect(shX - 18, shY, 36, 42);
    ctx.fillStyle = "#94a3b8"; // Kính chắn gió / mặt nạ xe SH
    ctx.fillRect(shX - 12, shY - 6, 24, 10);

    // Nhân vật người mẹ quyết liệt đuổi theo
    ctx.fillStyle = "#334155"; // Tóc / mũ bảo hiểm của mẹ
    ctx.fillRect(px ? (shX - 10) : (shX - 10), shY - 22, 20, 14);
    ctx.fillStyle = "#e2e8f0"; // Áo trắng của mẹ
    ctx.fillRect(shX - 12, shY - 8, 24, 12);
    ctx.restore();
}

function gameOver(isWin) {
    gameRunning = false;
    document.getElementById("game-ui").style.display = "none";
    document.getElementById("controls").style.display = "none";
    
    let endScreen = document.getElementById("end-screen");
    let endTitle = document.getElementById("end-title");
    let endDesc = document.getElementById("end-desc");
    
    endScreen.style.display = "flex";
    if (isWin) {
        endTitle.innerHTML = "<span style='color: #4ade80;'>🎉 AN TOÀN VỀ NHÀ! 🎉</span>";
        endDesc.innerText = "Bạn đã phóng xe điện về cất chu đáo trước khi mẹ kịp tóm!";
    } else {
        endTitle.innerHTML = "<span style='color: #ef4444;'>💥 BỊ MẸ SH TÓM RỒI! 💥</span>";
        endDesc.innerText = "Mẹ đã phóng xe SH áp sát và tóm gọn bạn tại trận!";
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
