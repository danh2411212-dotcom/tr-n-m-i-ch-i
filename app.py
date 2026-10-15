import streamlit as st

st.set_page_config(
    page_title="Đua Xe Đêm: Trốn Mẹ Về Nhà - 2.5D Rider",
    page_icon="🛵",
    layout="centered",
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
            background-color: #05050a;
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
            background: linear-gradient(to bottom, #020617 0%, #1e1b4b 100%);
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
            background: rgba(5, 5, 15, 0.95);
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
        <span id="shText" style="color: #ff6b81;">🚨 Mẹ SH: 45m</span>
    </div>
    
    <div id="controls">
        <button class="ctrl-btn" onclick="moveLeft()">◀</button>
        <button class="ctrl-btn" onclick="moveRight()">▶</button>
    </div>

    <div id="start-screen">
        <h2 style="color: #ff4757; margin-bottom: 5px;">🌙 ĐUA XE ĐÊM: TRỐN MẸ VỀ NHÀ 🛵</h2>
        <p style="max-width: 360px; color: #cbd5e1; font-size: 13px; line-height: 1.6;">
            Góc nhìn 2.5D phía sau lưng xe cực bốc! Lách xe điện trốn tiếng pô SH của mẹ gầm rú phía sau.
            <br><br><b>Né ổ gà, tránh thùng rác và về nhà an toàn!</b>
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

// 3 làn đường theo chiều sâu (0: Trái, 1: Giữa, 2: Phải)
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

function startGame() {
    document.getElementById("start-screen").style.display = "none";
    gameRunning = true;
    distance = 1000;
    shDistance = 45;
    obstacles = [];
    playerLane = 1;
    loop();
}

// Hàm tính tọa độ theo không gian phối cảnh 2.5D (z từ 0 ở chân trời đến 1 ở gần)
function getPerspectiveCoords(lane, z) {
    let horizonX = 240;
    let horizonY = 180;
    let bottomY = 580;
    
    // Độ rộng đường ở đáy và ở chân trời
    let widthBottom = 340;
    let widthHorizon = 40;
    
    let currentY = horizonY + (bottomY - horizonY) * z;
    let currentWidth = widthHorizon + (widthBottom - widthHorizon) * z;
    
    // Tọa độ 3 làn: lane 0 (trái), lane 1 (giữa), lane 2 (phải)
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
            z: 0.1, // Xuất hiện từ xa (chân trời)
            speed: 0.016,
            type: type
        });
    }

    for (let i = obstacles.length - 1; i >= 0; i--) {
        obstacles[i].z += obstacles[i].speed;
        
        // Kiểm tra va chạm khi chướng ngại vật đến gần người chơi (z từ 0.8 đến 0.93)
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

    // 1. Vẽ bầu trời & đường chân trời
    ctx.fillStyle = "#020617";
    ctx.fillRect(0, 0, 480, 180);

    // 2. Vẽ con đường nhựa 2.5D phối cảnh hình thang
    let horizonX = 240;
    let horizonY = 180;
    
    ctx.fillStyle = "#1e293b"; // Mặt đường
    ctx.beginPath();
    ctx.moveTo(horizonX - 25, horizonY);
    ctx.lineTo(horizonX + 25, horizonY);
    ctx.lineTo(440, 580);
    ctx.lineTo(40, 580);
    ctx.closePath();
    ctx.fill();

    // Vỉa hè hai bên
    ctx.fillStyle = "#0f172a";
    ctx.beginPath();
    ctx.moveTo(0, 580); ctx.lineTo(40, 580); ctx.lineTo(horizonX - 25, horizonY); ctx.lineTo(0, horizonY); ctx.closePath(); ctx.fill();
    ctx.beginPath();
    ctx.moveTo(480, 580); ctx.lineTo(440, 580); ctx.lineTo(horizonX + 25, horizonY); ctx.lineTo(480, horizonY); ctx.closePath(); ctx.fill();

    // Vạch kẻ chia làn đường chạy sâu vào trong
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 3;
    
    ctx.beginPath();
    ctx.moveTo(horizonX - 8, horizonY);
    ctx.lineTo(170, 580);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(horizonX + 8, horizonY);
    ctx.lineTo(310, 580);
    ctx.stroke();

    // 3. Chướng ngại vật lao từ xa tới
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

    // 4. Xe điện của con (Góc nhìn từ phía sau lưng ở gần màn hình)
    let playerCoords = getPerspectiveCoords(playerLane, 0.88);
    ctx.save();
    ctx.font = "64px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("🛴", playerCoords.x, playerCoords.y);
    ctx.restore();

    // 5. Xe SH của mẹ rượt đuổi phía sau (Sắt sạt dưới đáy màn hình)
    ctx.save();
    let shX = 240 + Math.sin(Date.now() * 0.009) * 30;
    let shY = 600;
    
    let gradient = ctx.createRadialGradient(shX, shY - 20, 10, shX, shY, 130);
    gradient.addColorStop(0, "rgba(255, 71, 87, 0.5)");
    gradient.addColorStop(1, "rgba(255, 71, 87, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 480, 480, 160);

    ctx.font = "75px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("🛵", shX, shY);
    ctx.restore();
}

function gameOver(isWin) {
    gameRunning = false;
    let startScreen = document.getElementById("start-screen");
    startScreen.style.display = "flex";
    if (isWin) {
        startScreen.innerHTML = `
            <h1 style="color: #4ade80;">🎉 AN TOÀN VỀ NHÀ! 🎉</h1>
            <p style="color: #fff;">Bạn đã phóng xe điện về nhà thành công trước khi mẹ kịp tóm!</p>
            <button class="start-btn" onclick="startGame()">CHƠI LẠI</button>
        `;
    } else {
        startScreen.innerHTML = `
            <h1 style="color: #ef4444;">💥 BỊ MẸ SH TÓM RỒI! 💥</h1>
            <p style="color: #fff;">Xe SH của mẹ quá mạnh và bạn đã đâm phải chướng ngại vật!</p>
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
