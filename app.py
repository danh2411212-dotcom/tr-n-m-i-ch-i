import streamlit as st

st.set_page_config(
    page_title="Đua Xe Đêm: Con Trốn Mẹ Đi Chơi", page_icon="🛵", layout="centered"
)

# Giao diện HTML + JavaScript cho game 2.5D Canvas
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Đua Xe Đêm: Con Trốn Mẹ Đi Chơi</title>
    <style>
        body {
            margin: 0;
            background-color: #0d1117;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
            border: 4px solid #30363d;
            border-radius: 10px;
            background: #111;
        }
        canvas {
            display: block;
            background: linear-gradient(to bottom, #050515, #222);
        }
        #ui {
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            pointer-events: none;
        }
        #start-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }
        button {
            background-color: #ff4757;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 4px 10px rgba(255, 71, 87, 0.4);
            transition: 0.2s;
        }
        button:hover {
            background-color: #ff6b81;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="480" height="640"></canvas>
    <div id="ui">
        <span id="scoreText">Khoảng cách về nhà: 1000m</span>
        <span id="shText" style="color: #ff4b5c;">Mẹ SH cách: 50m</span>
    </div>
    
    <div id="start-screen">
        <h2>🌙 ĐUA XE ĐÊM: TRỐN MẸ VỀ NHÀ 🛵</h2>
        <p style="max-width: 350px; color: #ccc; font-size: 14px; line-height: 1.5;">
            Cốt truyện: Nửa đêm bạn trốn mẹ lấy xe điện đi chơi. Bỗng nghe tiếng pô xe SH quen thuộc... Mẹ đang đuổi phía sau! 
            <br><br><b>Hãy né ổ gà, thùng rác và về nhà trước khi bị mẹ tóm gọn!</b>
        </p>
        <p style="font-size: 13px; color: #ffa502;">👉 Dùng phím mũi tên <b>Trái / Phải</b> (hoặc A/D) để lách xe.</p>
        <button onclick="startGame()">BẮT ĐẦU CHẠY TRỐN</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let gameRunning = false;
let distance = 1000; // mét về nhà
let shDistance = 40; // khoảng cách mẹ SH so với con (càng nhỏ càng nguy hiểm)

// Vị trí xe điện của con (đường chia làm 3 làn: x = 120, 240, 360)
const lanes = [120, 240, 360];
let playerLaneIndex = 1; 
let playerX = lanes[playerLaneIndex];
let playerY = 520;

// Danh sách chướng ngại vật (ổ gà, thùng rác)
let obstacles = [];
let obstacleTimer = 0;

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

// Hỗ trợ cảm ứng vuốt trên điện thoại
let touchStartX = 0;
window.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; });
window.addEventListener("touchend", (e) => {
    if (!gameRunning) return;
    let diffX = e.changedTouches[0].clientX - touchStartX;
    if (diffX > 30 && playerLaneIndex < lanes.length - 1) playerLaneIndex++;
    if (diffX < -30 && playerLaneIndex > 0) playerLaneIndex--;
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

    // Di chuyển mượt sang làn đường mục tiêu
    let targetX = lanes[playerLaneIndex];
    playerX += (targetX - playerX) * 0.2;

    // Giảm khoảng cách về nhà mỗi khung hình
    distance -= 0.5;
    
    // Mẹ SH liên tục ép sát, nếu né tốt khoảng cách tăng, đâm trúng vật cản mẹ áp sát
    shDistance += 0.02;
    if (shDistance > 80) shDistance = 80;

    // Sinh chướng ngại vật ngẫu nhiên
    obstacleTimer++;
    if (obstacleTimer > 55) {
        obstacleTimer = 0;
        let randomLane = Math.floor(Math.random() * 3);
        let types = ['ogap', 'thungrac'];
        let type = types[Math.floor(Math.random() * types.length)];
        obstacles.push({
            lane: randomLane,
            y: -50,
            speed: 5.5,
            type: type
        });
    }

    // Cập nhật vị trí chướng ngại vật (hiệu ứng 2.5D phóng to dần từ xa tới)
    for (let i = obstacles.length - 1; i >= 0; i--) {
        obstacles[i].y += obstacles[i].speed;

        // Kiểm tra va chạm với xe điện của con
        let obsX = lanes[obstacles[i].lane];
        if (obstacles[i].y > playerY - 30 && obstacles[i].y < playerY + 30 && Math.abs(obsX - playerX) < 30) {
            // Đâm phải chướng ngại vật -> Mẹ SH bắt kịp ngay lập tức!
            shDistance -= 15;
            obstacles.splice(i, 1);
            if (shDistance <= 0) {
                gameOver(false);
            }
        }
        else if (obstacles[i].y > canvas.height) {
            obstacles.splice(i, 1);
        }
    }

    // Kiểm tra điều kiện thắng / thua
    if (distance <= 0) {
        gameOver(true);
    }
    if (shDistance <= 5) {
        gameOver(false);
    }

    // Cập nhật giao diện HTML trên canvas
    document.getElementById("scoreText").innerText = "Khoảng cách về nhà: " + Math.max(0, Math.floor(distance)) + "m";
    document.getElementById("shText").innerText = "🚨 Mẹ SH cách: " + Math.max(0, Math.floor(shDistance)) + "m";
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Vẽ khung cảnh đường phố ban đêm (phối cảnh 2.5D)
    // Lề đường hai bên
    ctx.fillStyle = "#1e272e";
    ctx.fillRect(0, 0, 60, canvas.height);
    ctx.fillRect(420, 0, 60, canvas.height);

    // Vỉa hè / Cây cối hai bên đường
    ctx.fillStyle = "#0d1b2a";
    ctx.fillRect(0, 0, 20, canvas.height);
    ctx.fillRect(460, 0, 20, canvas.height);

    // Lòng đường nhựa
    ctx.fillStyle = "#2f3640";
    ctx.fillRect(60, 0, 360, canvas.height);

    // Vạch kẻ đường đứt đoạn giữa các làn
    ctx.strokeStyle = "#fbc531";
    ctx.lineWidth = 4;
    ctx.setLineDash([20, 20]);
    ctx.beginPath();
    ctx.moveTo(180, (Date.now() * 0.5) % 40 - 40);
    ctx.lineTo(180, canvas.height);
    ctx.moveTo(300, (Date.now() * 0.5) % 40 - 40);
    ctx.lineTo(300, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]); // Reset line dash

    // 2. Vẽ Chướng ngại vật (Ổ gà / Thùng rác)
    for (let obs of obstacles) {
        let ox = lanes[obs.lane];
        let oy = obs.y;
        ctx.save();
        if (obs.type === 'ogap') {
            // Vẽ ổ gà đen xám
            ctx.fillStyle = "#111";
            ctx.beginPath();
            ctx.ellipse(ox, oy, 25, 12, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#444";
            ctx.lineWidth = 3;
            ctx.stroke();
        } else {
            // Vẽ thùng rác
            ctx.fillStyle = "#e84118";
            ctx.fillRect(ox - 15, oy - 20, 30, 35);
            ctx.fillStyle = "#c23616";
            ctx.fillRect(ox - 18, oy - 25, 36, 6);
        }
        ctx.restore();
    }

    // 3. Vẽ Xe Điện của Con (Dựa trên thiết kế xe điện cá tính - màu trắng, gầm cao)
    ctx.save();
    let cx = playerX;
    let cy = playerY;
    
    // Đèn hậu xe điện
    ctx.fillStyle = "#00d2d3";
    ctx.shadowBlur = 10;
    ctx.shadowColor = "#00d2d3";
    ctx.fillRect(cx - 10, cy + 15, 20, 4);

    // Thân xe điện trắng
    ctx.fillStyle = "#f5f6fa";
    ctx.beginPath();
    ctx.roundRect(cx - 12, cy - 15, 24, 35, 6);
    ctx.fill();

    // Người con (đội mũ bảo hiểm)
    ctx.fillStyle = "#ff5252"; // Áo hoodie đỏ trốn mẹ đi chơi
    ctx.beginPath();
    ctx.arc(cx, cy - 8, 11, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 4. Vẽ xe SH của Mẹ rượt đuổi ở phía sau (Đèn pha SH sáng rực phía đáy màn hình)
    ctx.save();
    let shX = 240 + Math.sin(Date.now() * 0.01) * 30; // Mẹ lượn lách dí theo
    let shY = 590;
    
    // Ánh đèn pha xe SH quét phía trước
    let gradient = ctx.createRadialGradient(shX, shY, 10, shX, shY + 50, 120);
    gradient.addColorStop(0, "rgba(255, 255, 255, 0.4)");
    gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 450, 480, 200);

    // Xe SH trắng của mẹ
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.roundRect(shX - 16, shY - 10, 32, 45, 10);
    ctx.fill();
    // Kính chiếu hậu & tay lái SH
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(shX - 22, shY);
    ctx.lineTo(shX + 22, shY);
    ctx.stroke();
    
    ctx.restore();
}

function gameOver(isWin) {
    gameRunning = false;
    let startScreen = document.getElementById("start-screen");
    startScreen.style.display = "flex";
    if (isWin) {
        startScreen.innerHTML = `
            <h1 style="color: #4cd137;">🎉 THÀNH CÔNG VỀ NHÀ! 🎉</h1>
            <p style="color: #fff;">Bạn đã phi nước đại kịp thời và cất xe điện vào nhà trước khi mẹ kịp vác chổi ra tới!</p>
            <button onclick="startGame()">CHƠI LẠI</button>
        `;
    } else {
        startScreen.innerHTML = `
            <h1 style="color: #e84118;">💥 BỊ MẸ TÓM RỒI! 💥</h1>
            <p style="color: #fff;">Xe SH của mẹ quá mạnh và bạn đã đâm phải chướng ngại vật. Ăn đòn chắc luôn!</p>
            <button onclick="startGame()">THỬ LẠI</button>
        `;
    }
}

function loop() {
    update();
    draw();
    if (gameRunning) {
        requestAnimationFrame(loop);
    }
}
</script>

</body>
</html>
"""

# Hiển thị game trong Streamlit component
st.components.v1.html(game_html, height=680, scrolling=False)
