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
            background-color: #0d1117;
            color: white;
            font-family: 'Courier New', Courier, monospace;
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
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.4);
            border: 4px solid #38bdf8;
            border-radius: 12px;
            background: #111;
            width: 480px;
            height: 640px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: #1e293b;
            image-rendering: pixelated;
        }
        
        #lobby-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 30px 20px;
            box-sizing: border-box;
            z-index: 20;
        }
        .house-banner {
            background: rgba(255, 255, 255, 0.08);
            border: 2px solid rgba(56, 189, 248, 0.3);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }
        .pixel-preview {
            font-size: 50px;
            margin: 10px 0;
            text-shadow: 0 0 15px rgba(56, 189, 248, 0.8);
        }
        .play-btn {
            background: #38bdf8;
            color: #0f172a;
            border: 3px solid #bae6fd;
            padding: 14px 40px;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 6px #0369a1;
            transition: 0.1s;
            text-transform: uppercase;
        }
        .play-btn:active {
            transform: translateY(4px);
            box-shadow: 0 2px #0369a1;
        }

        #game-ui {
            position: absolute;
            top: 15px; left: 15px; right: 15px;
            display: flex; justify-content: space-between;
            font-size: 14px; font-weight: bold;
            text-shadow: 2px 2px #000;
            pointer-events: none; display: none; z-index: 10;
        }
        #controls {
            position: absolute;
            bottom: 15px; left: 0; right: 0;
            display: flex; justify-content: space-around;
            padding: 0 30px; display: none; z-index: 10;
        }
        .ctrl-btn {
            background: #0f172a;
            border: 3px solid #38bdf8;
            color: #38bdf8;
            font-size: 26px; width: 80px; height: 55px;
            border-radius: 8px; cursor: pointer; outline: none; user-select: none;
            box-shadow: 0 4px #000;
        }
        .ctrl-btn:active {
            background: #38bdf8; color: #0f172a;
            transform: translateY(2px);
            box-shadow: 0 2px #000;
        }
        
        #end-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.96);
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            text-align: center; padding: 20px; display: none; z-index: 30;
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- Sảnh chờ (Lobby) -->
    <div id="lobby-screen">
        <div class="house-banner">
            <h3 style="color: #38bdf8; margin: 0 0 5px 0;">🏡 KHU PHỐ ĐÊM PIXEL</h3>
            <p style="color: #94a3b8; font-size: 12px; margin: 0;">Mẹ tóc hồng đang lái xe xanh rượt đuổi con trai chạy xe đen!</p>
        </div>
        
        <div>
            <div class="pixel-preview">🧑‍🦱🏍️ vs 👩‍🦰🛵</div>
            <h2 style="color: #38bdf8; margin: 5px 0; font-size: 18px;">ĐUA XE ĐÊM: TRỐN MẸ VỀ NHÀ</h2>
            <p style="color: #94a3b8; font-size: 12px; max-width: 320px; line-height: 1.5;">
                Né ổ gà, tránh thùng rác và phóng về nhà an toàn trước khi bị mẹ tóm!
            </p>
        </div>

        <button class="play-btn" onclick="startJourney()">BẮT ĐẦU CHẠY TRỐN</button>
    </div>

    <!-- Canvas Game -->
    <canvas id="gameCanvas" width="480" height="640"></canvas>
    
    <div id="game-ui">
        <span id="scoreText">🏠 Khoảng cách: 1000m</span>
        <span id="shText" style="color: #f87171;">🚨 Mẹ đuổi: 45m</span>
    </div>
    
    <div id="controls">
        <button class="ctrl-btn" onclick="moveLeft()">◀</button>
        <button class="ctrl-btn" onclick="moveRight()">▶</button>
    </div>

    <div id="end-screen">
        <h1 id="end-title" style="margin-bottom: 10px;"></h1>
        <p id="end-desc" style="color: #cbd5e1; font-size: 13px; margin-bottom: 20px;"></p>
        <button class="play-btn" onclick="returnToLobby()" style="font-size: 15px; padding: 12px 30px;">VỀ SẢNH CHỜ</button>
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
    let horizonY = 160;
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
    document.getElementById("shText").innerText = "🚨 Mẹ đuổi: " + Math.max(0, Math.floor(shDistance)) + "m";
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Khung cảnh đường phố pixel art ban đêm có đèn đường chiếu sáng (màu xanh sẫm & xám đặc trưng)[span_10](start_span)[span_10](end_span)
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(0, 0, 480, 160);

    // Vỉa hè hai bên
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(0, 160, 50, 480);
    ctx.fillRect(430, 160, 50, 480);

    // Hiệu ứng vòng tròn ánh sáng đèn đường hắt xuống phố[span_11](start_span)[span_11](end_span)
    ctx.fillStyle = "rgba(56, 189, 248, 0.07)";
    ctx.beginPath(); ctx.arc(80, 260, 90, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(400, 380, 100, 0, Math.PI * 2); ctx.fill();

    // 2. Con đường nhựa 2.5D phối cảnh chính giữa[span_12](start_span)[span_12](end_span)
    let horizonX = 240;
    let horizonY = 160;
    
    ctx.fillStyle = "#334155";
    ctx.beginPath();
    ctx.moveTo(horizonX - 25, horizonY);
    ctx.lineTo(horizonX + 25, horizonY);
    ctx.lineTo(430, 580);
    ctx.lineTo(50, 580);
    ctx.closePath();
    ctx.fill();

    // Vạch chia làn đứt đoạn giữa đường[span_13](start_span)[span_13](end_span)
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 3;
    ctx.setLineDash([20, 20]);
    ctx.lineDashOffset = -roadAnim * 40;
    ctx.beginPath();
    ctx.moveTo(horizonX, horizonY);
    ctx.lineTo(240, 580);
    ctx.stroke();
    ctx.setLineDash([]);

    // 3. Chướng ngại vật
    for (let obs of obstacles) {
        let coords = getPerspectiveCoords(obs.lane, obs.z);
        let scale = obs.z * 1.6;
        
        ctx.save();
        ctx.font = Math.floor(30 * scale) + "px Courier New";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        if (obs.type === 'ogap') {
            ctx.fillText("🕳️", coords.x, coords.y);
        } else {
            ctx.fillText("🗑️", coords.x, coords.y);
        }
        ctx.restore();
    }

    // 4. Người con (tóc đen áo đỏ) chạy chiếc xe màu đen[span_14](start_span)[span_14](end_span)[span_15](start_span)[span_15](end_span)
    let playerCoords = getPerspectiveCoords(playerLane, 0.88);
    let px = playerCoords.x;
    let py = playerCoords.y;
    ctx.save();

    // Thân xe màu đen đặc trưng
    ctx.fillStyle = "#1e1b4b";
    ctx.fillRect(px - 14, py, 28, 34);
    ctx.fillStyle = "#38bdf8"; // Bánh và đèn xe màu xanh sáng
    ctx.fillRect(px - 10, py + 26, 20, 6);

    // Nhân vật tóc đen áo đỏ ngồi trên xe
    ctx.fillStyle = "#000000"; // Tóc đen xoăn
    ctx.fillRect(px - 8, py - 18, 16, 12);
    ctx.fillStyle = "#ef4444"; // Áo đỏ
    ctx.fillRect(px - 8, py - 6, 16, 12);
    ctx.restore();

    // 5. Người mẹ (tóc hồng áo hồng) lái chiếc xe màu xanh đuổi theo phía sau[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span)
    ctx.save();
    let shX = 240 + Math.sin(Date.now() * 0.009) * 30;
    let shY = 590;
    
    // Ánh đèn pha xe mẹ chiếu sáng rực rỡ
    let gradient = ctx.createRadialGradient(shX, shY - 30, 10, shX, shY, 130);
    gradient.addColorStop(0, "rgba(56, 189, 248, 0.5)");
    gradient.addColorStop(1, "rgba(56, 189, 248, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 450, 480, 190);

    // Chiếc xe thể thao màu xanh của mẹ[span_18](start_span)[span_18](end_span)
    ctx.fillStyle = "#0284c7";
    ctx.shadowBlur = 12; ctx.shadowColor = "#38bdf8";
    ctx.fillRect(shX - 18, shY, 36, 40);

    // Nhân vật mẹ tóc hồng áo hồng[span_19](start_span)[span_19](end_span)
    ctx.fillStyle = "#f472b6"; // Tóc hồng dài đặc trưng của mẹ
    ctx.fillRect(shX - 12, py ? (shY - 22) : (shY - 22), 24, 14);
    ctx.fillStyle = "#ec4899"; // Áo hồng
    ctx.fillRect(shX - 10, shY - 8, 20, 12);
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
        endDesc.innerText = "Bạn đã né thành công và cất xe gọn gàng trước khi mẹ bắt kịp!";
    } else {
        endTitle.innerHTML = "<span style='color: #ef4444;'>💥 BỊ MẸ TÓM RỒI! 💥</span>";
        endDesc.innerText = "Mẹ tóc hồng lái xe xanh đã phóng tới và tóm gọn bạn!";
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
