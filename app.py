import streamlit as st
import streamlit.components.v1 as components

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Hamster Escape Game",
    page_icon="🐹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn thanh menu mặc định của Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

# Đọc nội dung HTML của game (Hoặc nhúng mã HTML trực tiếp)
html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hamster Escape</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body {
            font-family: 'Press Start 2P', cursive;
            touch-action: manipulation;
            margin: 0;
            padding: 0;
            background-color: #0f172a;
        }
        .btn-retro {
            box-shadow: inset -4px -4px 0px 0px #451a03, inset 4px 4px 0px 0px #fde047;
            background-color: #d97706;
            color: #ffffff;
            transition: transform 0.1s;
        }
        .btn-retro:hover {
            transform: scale(1.05);
            background-color: #b45309;
        }
        .btn-retro:active {
            transform: scale(0.95);
        }
        .btn-success {
            box-shadow: inset -4px -4px 0px 0px #14532d, inset 4px 4px 0px 0px #86efac;
            background-color: #16a34a;
        }
        .btn-danger {
            box-shadow: inset -4px -4px 0px 0px #7f1d1d, inset 4px 4px 0px 0px #fca5a5;
            background-color: #dc2626;
        }
        canvas {
            image-rendering: pixelated;
        }
    </style>
</head>
<body class="bg-slate-900 text-white flex items-center justify-center min-h-screen p-2 select-none">

    <div class="relative w-full max-w-[800px] aspect-[16/9] bg-slate-950 rounded-2xl overflow-hidden border-4 border-amber-600 shadow-2xl flex flex-col justify-center items-center">
        
        <canvas id="gameCanvas" class="w-full h-full block bg-sky-400"></canvas>

        <!-- 1. MAIN MENU -->
        <div id="screen-main-menu" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/95 backdrop-blur-md z-30 p-4">
            <div class="text-center mb-8 animate-bounce">
                <span class="text-4xl sm:text-6xl mb-2 block">🐹</span>
                <h1 class="text-2xl sm:text-4xl text-amber-400 drop-shadow-[0_4px_0_#78350f] font-black tracking-wider">
                    HAMSTER ESCAPE
                </h1>
            </div>
            <button id="btn-main-play" class="btn-retro text-lg sm:text-2xl px-8 py-4 rounded-xl cursor-pointer">
                ▶ PLAY
            </button>
        </div>

        <!-- 2. LEVEL SELECT -->
        <div id="screen-level-select" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/95 backdrop-blur-md z-30 hidden p-4">
            <h2 class="text-xl sm:text-3xl text-amber-300 mb-8 text-center drop-shadow-[0_3px_0_#78350f]">
                CHỌN CẤP ĐỘ
            </h2>
            <div class="flex flex-col sm:flex-row gap-4 w-full max-w-lg justify-center items-stretch">
                <button id="btn-diff-easy" class="btn-retro btn-success flex-1 p-4 rounded-xl flex flex-col items-center justify-center cursor-pointer">
                    <span class="text-base sm:text-lg font-bold mb-2">EASY</span>
                    <span class="text-[10px] leading-relaxed text-emerald-100">
                        • 3 Mạng<br>• Tốc độ chậm<br>• Nhảy cao
                    </span>
                </button>
                <button id="btn-diff-normal" class="btn-retro flex-1 p-4 rounded-xl flex flex-col items-center justify-center cursor-pointer">
                    <span class="text-base sm:text-lg font-bold mb-2">NORMAL</span>
                    <span class="text-[10px] leading-relaxed text-amber-100">
                        • 2 Mạng<br>• Tốc độ vừa<br>• Cân bằng
                    </span>
                </button>
                <button id="btn-diff-hard" class="btn-retro btn-danger flex-1 p-4 rounded-xl flex flex-col items-center justify-center cursor-pointer">
                    <span class="text-base sm:text-lg font-bold mb-2">HARD</span>
                    <span class="text-[10px] leading-relaxed text-red-100">
                        • 1 Mạng<br>• Tốc độ nhanh<br>• Thử thách
                    </span>
                </button>
            </div>
            <button id="btn-back-to-menu" class="mt-8 text-xs text-slate-400 hover:text-white underline cursor-pointer">
                ⬅️ Quay lại Trang Chủ
            </button>
        </div>

        <!-- 3. HUD -->
        <div id="game-hud" class="absolute top-0 left-0 w-full p-3 flex justify-between items-center z-10 pointer-events-none hidden">
            <div class="bg-slate-900/80 px-3 py-2 rounded-lg border border-amber-500/50 flex items-center gap-2">
                <span class="text-xs text-amber-400">MẠNG:</span>
                <span id="hud-lives" class="text-xs text-red-500">❤️❤️❤️</span>
            </div>
            <div class="bg-slate-900/80 px-3 py-2 rounded-lg border border-amber-500/50 flex items-center gap-2">
                <span id="hud-difficulty" class="text-xs text-amber-300">NORMAL</span>
            </div>
        </div>

        <!-- 4. END SCREEN -->
        <div id="screen-game-end" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-md z-30 hidden p-4">
            <h2 id="end-title" class="text-2xl sm:text-4xl text-amber-400 font-bold mb-4 text-center">GAME OVER</h2>
            <p id="end-subtitle" class="text-slate-300 text-xs sm:text-sm mb-8 text-center max-w-md leading-relaxed">
                Bạn chưa tới được ống cống ngầm!
            </p>
            <div class="flex gap-4">
                <button id="btn-restart" class="btn-retro p-4 rounded-xl cursor-pointer text-xs sm:text-sm">🔄 CHƠI LẠI</button>
                <button id="btn-end-menu" class="btn-retro btn-danger p-4 rounded-xl cursor-pointer text-xs sm:text-sm">🏠 TRANG CHỦ</button>
            </div>
        </div>
    </div>

    <script>
        const GAME_WIDTH = 800;
        const GAME_HEIGHT = 450;
        const DIFFICULTY_SETTINGS = {
            easy: { lives: 3, speedMult: 1.0, jumpPower: 13, gravity: 0.5 },
            normal: { lives: 2, speedMult: 1.3, jumpPower: 12.5, gravity: 0.55 },
            hard: { lives: 1, speedMult: 1.7, jumpPower: 12, gravity: 0.6 }
        };

        let canvas, ctx;
        let gameState = 'MENU';
        let currentDifficulty = 'normal';
        let cameraX = 0;
        let animationFrameId = null;
        const keys = {};

        class Hamster {
            constructor() {
                this.x = 80;
                this.y = 280;
                this.width = 36;
                this.height = 32;
                this.vx = 0;
                this.vy = 0;
                this.speed = 4.5;
                this.grounded = false;
                this.facing = 'right';
                this.lives = 3;
                this.invulnerableTimer = 0;
                this.enteringSewer = false;
            }

            update(diff, groundY) {
                if (this.enteringSewer) {
                    this.y += 1.5;
                    return;
                }

                let moveDir = 0;
                if (keys['ArrowLeft'] || keys['KeyA']) moveDir -= 1;
                if (keys['ArrowRight'] || keys['KeyD']) moveDir += 1;

                if (moveDir !== 0) {
                    this.vx = moveDir * this.speed * (diff ? diff.speedMult : 1);
                    this.facing = moveDir > 0 ? 'right' : 'left';
                } else {
                    this.vx *= 0.7;
                }
                if ((keys['ArrowUp'] || keys['KeyW'] || keys['Space'] || touchJump) && this.grounded) {
                    this.vy = -(diff ? diff.jumpPower : 12.5);
                    this.grounded = false;
                    SoundFX.playJump();
                }

                this.vy += (diff ? diff.gravity : 0.55);
                this.x += this.vx;
                this.y += this.vy;

                if (this.invulnerableTimer > 0) this.invulnerableTimer--;
                if (this.x < 0) this.x = 0;
            }

            draw(ctx, camX) {
                ctx.save();
                ctx.translate(this.x - camX + this.width / 2, this.y + this.height / 2);
                if (this.facing === 'left') ctx.scale(-1, 1);
                if (this.invulnerableTimer > 0 && Math.floor(this.invulnerableTimer / 4) % 2 === 0) {
                    ctx.globalAlpha = 0.4;
                }
                ctx.fillStyle = '#f97316';
                ctx.beginPath();
                ctx.ellipse(0, 2, 18, 14, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#ffedd5';
                ctx.beginPath();
                ctx.ellipse(3, 4, 10, 8, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#fb923c';
                ctx.beginPath();
                ctx.arc(8, -4, 10, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#ea580c';
                ctx.beginPath();
                ctx.arc(2, -12, 4, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#0f172a';
                ctx.beginPath();
                ctx.arc(11, -5, 2.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#f43f5e';
                ctx.beginPath();
                ctx.arc(16, -2, 2, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }

        let player = new Hamster();
        let levelWidth = 3200;
        let groundY = GAME_HEIGHT - 70;
        let platforms = [];
        let hazards = [];
        let exitPipe = null;

        window.addEventListener('DOMContentLoaded', () => {
            canvas = document.getElementById('gameCanvas');
            canvas.width = GAME_WIDTH;
            canvas.height = GAME_HEIGHT;
            ctx = canvas.getContext('2d');

            document.getElementById('btn-main-play').onclick = () => {
                document.getElementById('screen-main-menu').classList.add('hidden');
                document.getElementById('screen-level-select').classList.remove('hidden');
            };

            document.getElementById('btn-back-to-menu').onclick = () => {
                document.getElementById('screen-level-select').classList.add('hidden');
                document.getElementById('screen-main-menu').classList.remove('hidden');
            };

            document.getElementById('btn-diff-easy').onclick = () => startGame('easy');
            document.getElementById('btn-diff-normal').onclick = () => startGame('normal');
            document.getElementById('btn-diff-hard').onclick = () => startGame('hard');

            // Sound initialization on click
            window.addEventListener('click', () => SoundFX.init(), { once: true });
            window.addEventListener('keydown', () => SoundFX.init(), { once: true });

            document.getElementById('btn-restart').onclick = () => {
                document.getElementById('screen-game-end').classList.add('hidden');
                startGame(currentDifficulty);
            };

            document.getElementById('btn-end-menu').onclick = () => {
                document.getElementById('screen-game-end').classList.add('hidden');
                document.getElementById('game-hud').classList.add('hidden');
                document.getElementById('screen-main-menu').classList.remove('hidden');
                gameState = 'MENU';
            };

            window.addEventListener('keydown', e => keys[e.code] = true);
            window.addEventListener('keyup', e => keys[e.code] = false);

            drawBackground();
        });

        function generateLevel(diffKey) {
            levelWidth = 3200;
            groundY = GAME_HEIGHT - 70;
            platforms = [];
            hazards = [];

            const diff = DIFFICULTY_SETTINGS[diffKey];

            for (let x = 400; x < levelWidth - 500; x += 220) {
                if (Math.random() > 0.3) {
                    let platW = 100;
                    let platH = groundY - (Math.random() * 120 + 60);
                    platforms.push({ x: x, y: platH, w: platW, h: 18 });
                }
            }

            for (let x = 500; x < levelWidth - 600; x += 250) {
                if (Math.random() > 0.4) {
                    if (Math.random() > 0.5) {
                        hazards.push({ type: 'spike', x: x, y: groundY - 25, w: 28, h: 25 });
                    } else {
                        hazards.push({ 
                            type: 'boulder', x: x, y: groundY - 30, w: 30, h: 30, 
                            vx: (Math.random() > 0.5 ? 1 : -1) * (1.5 * diff.speedMult) 
                        });
                    }
                }
            }

            exitPipe = { x: levelWidth - 250, y: groundY - 60, w: 60, h: 60 };
        }

        function startGame(difficulty) {
            currentDifficulty = difficulty;
            const diff = DIFFICULTY_SETTINGS[difficulty];

            player = new Hamster();
            player.lives = diff.lives;

            generateLevel(difficulty);

            document.getElementById('hud-difficulty').innerText = difficulty.toUpperCase();
            updateHUDLives();

            document.getElementById('screen-level-select').classList.add('hidden');
            document.getElementById('screen-main-menu').classList.add('hidden');
            document.getElementById('screen-game-end').classList.add('hidden');
            document.getElementById('game-hud').classList.remove('hidden');

            gameState = 'PLAYING';
            if (animationFrameId) cancelAnimationFrame(animationFrameId);
            gameLoop();
        }

        function gameLoop() {
            if (gameState !== 'PLAYING') return;
            update();
            render();
            animationFrameId = requestAnimationFrame(gameLoop);
        }

        function update() {
            const diff = DIFFICULTY_SETTINGS[currentDifficulty];
            player.update(diff, groundY);

            if (!player.enteringSewer) {
                if (player.y + player.height >= groundY) {
                    player.y = groundY - player.height;
                    player.vy = 0;
                    player.grounded = true;
                }

                platforms.forEach(p => {
                    if (player.x + player.width > p.x &&
                        player.x < p.x + p.w &&
                        player.y + player.height >= p.y &&
                        player.y + player.height <= p.y + p.h + player.vy) {
                        player.y = p.y - player.height;
                        player.vy = 0;
                        player.grounded = true;
                    }
                });
            }

            cameraX = player.x - GAME_WIDTH / 3;
            if (cameraX < 0) cameraX = 0;
            if (cameraX > levelWidth - GAME_WIDTH) cameraX = levelWidth - GAME_WIDTH;

            hazards.forEach(h => {
                if (h.type === 'boulder') {
                    h.x += h.vx;
            // Va chạm chướng ngại vật
            if (player.invulnerableTimer === 0 && !player.enteringSewer) {
                hazards.forEach(h => {
                    if (player.x + 8 < h.x + h.w &&
                        player.x + player.width - 8 > h.x &&
                        player.y + 8 < h.y + h.h &&
                        player.y + player.height > h.y) {
                        
                        player.lives--;
                        player.invulnerableTimer = 50;
                        player.vy = -7;
                        SoundFX.playHit();
                        updateHUDLives();

                        if (player.lives <= 0) {
                            endGame(false);
                        }
                    }
                });
            }

            // Chui vào cống ngầm hoàn thành màn chơi
            if (exitPipe && player.x + player.width / 2 >= exitPipe.x + 15 && player.x + player.width / 2 <= exitPipe.x + exitPipe.w - 15) {
                if (player.grounded && !player.enteringSewer) {
                    player.enteringSewer = true;
                    SoundFX.playEscape();
                    setTimeout(() => {
                        endGame(true);
                    }, 1200);
                }
            }
        }

        function render() {
            drawBackground();

            platforms.forEach(p => {
                ctx.fillStyle = '#854d0e';
                ctx.fillRect(p.x - cameraX, p.y, p.w, p.h);
                ctx.fillStyle = '#22c55e';
                ctx.fillRect(p.x - cameraX, p.y, p.w, 4);
            });

            hazards.forEach(h => {
                if (h.type === 'spike') {
                    ctx.fillStyle = '#94a3b8';
                    ctx.beginPath();
                    ctx.moveTo(h.x - cameraX, h.y + h.h);
                    ctx.lineTo(h.x - cameraX + h.w / 2, h.y);
                    ctx.lineTo(h.x - cameraX + h.w, h.y + h.h);
                    ctx.closePath();
                    ctx.fill();
                } else if (h.type === 'boulder') {
                    ctx.fillStyle = '#64748b';
                    ctx.beginPath();
                    ctx.arc(h.x - cameraX + h.w / 2, h.y + h.h / 2, h.w / 2, 0, Math.PI * 2);
                    ctx.fill();
                }
            });

            if (exitPipe) {
                ctx.fillStyle = '#166534';
                ctx.fillRect(exitPipe.x - cameraX, exitPipe.y, exitPipe.w, exitPipe.h);
                ctx.fillStyle = '#22c55e';
                ctx.fillRect(exitPipe.x - cameraX - 4, exitPipe.y - 10, exitPipe.w + 8, 12);
                ctx.fillStyle = '#facc15';
                ctx.font = '10px "Press Start 2P"';
                ctx.fillText('DRAIN ⬇️', exitPipe.x - cameraX - 10, exitPipe.y - 18);
            }

            player.draw(ctx, cameraX);
        }

        function drawBackground() {
            ctx.fillStyle = '#38bdf8';
            ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            for (let i = 0; i < 5; i++) {
                let cloudX = ((i * 300) - cameraX * 0.2) % (GAME_WIDTH + 200) - 100;
                ctx.beginPath();
                ctx.arc(cloudX, 60 + (i % 2) * 20, 25, 0, Math.PI * 2);
                ctx.arc(cloudX + 20, 50 + (i % 2) * 20, 35, 0, Math.PI * 2);
                ctx.arc(cloudX + 50, 60 + (i % 2) * 20, 25, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.fillStyle = '#78350f';
            ctx.fillRect(0 - cameraX, groundY, levelWidth, GAME_HEIGHT - groundY);

            ctx.fillStyle = '#22c55e';
            ctx.fillRect(0 - cameraX, groundY, levelWidth, 16);
        }

        function updateHUDLives() {
            let heartStr = '';
            for (let i = 0; i < player.lives; i++) {
                heartStr += '❤️';
            }
            document.getElementById('hud-lives').innerText = heartStr || '💀';
        }

        function endGame(isVictory) {
            gameState = isVictory ? 'VICTORY' : 'GAMEOVER';
            const endTitle = document.getElementById('end-title');
            const endSubtitle = document.getElementById('end-subtitle');

            if (isVictory) {
                endTitle.innerText = '🎉 THÀNH CÔNG! 🎉';
                endSubtitle.innerText = 'Hamster đã chui vào cống ngầm an toàn và trốn thoát khỏi mặt đất!';
            } else {
                endTitle.innerText = 'GAME OVER 💀';
                endSubtitle.innerText = 'Bạn đã hết mạng trước khi đến được cống ngầm!';
            }

            document.getElementById('screen-game-end').classList.remove('hidden');
        }
    </script>
</body>
</html>
"""
# Hiển thị game thông qua HTML Component của Streamlit
components.html(html_code, height=520, scrolling=False)
