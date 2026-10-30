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
<body class="bg-slate-900 text-white min-h-screen flex items-center justify-center p-2 sm:p-4 select-none">

    <!-- Container Game chính -->
    <div class="relative w-full max-w-[800px] aspect-[16/9] bg-slate-950 rounded-2xl overflow-hidden border-4 border-amber-600 shadow-2xl flex flex-col justify-center items-center">
        
        <!-- CANVAS HIỂN THỊ GAME -->
        <canvas id="gameCanvas" class="w-full h-full block bg-sky-400"></canvas>

        <!-- 1. TRANG CHỦ (MAIN MENU) -->
        <div id="screen-main-menu" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/95 backdrop-blur-md z-30 p-4">
            <div class="text-center mb-8 animate-bounce">
                <span class="text-4xl sm:text-6xl mb-2 block">🐹</span>
                <h1 class="text-2xl sm:text-4xl text-amber-400 drop-shadow-[0_4px_0_#78350f] font-black tracking-wider">
                    HAMSTER ESCAPE
                </h1>
            </div>

            <button id="btn-main-play" class="btn-retro text-lg sm:text-2xl px-8 py-4 rounded-xl cursor-pointer pointer-events-auto">
                ▶ PLAY
            </button>
        </div>

        <!-- 2. TRANG CHỌN CẤP ĐỘ (LEVEL SELECT) -->
        <div id="screen-level-select" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/95 backdrop-blur-md z-30 hidden p-4">
            <h2 class="text-xl sm:text-3xl text-amber-300 mb-8 text-center drop-shadow-[0_3px_0_#78350f]">
                CHỌN CẤP ĐỘ
            </h2>

            <div class="flex flex-col sm:flex-row gap-4 w-full max-w-lg justify-center items-stretch pointer-events-auto">
                <!-- Easy -->
                <button id="btn-diff-easy" class="btn-retro btn-success flex-1 p-4 rounded-xl flex flex-col items-center justify-center cursor-pointer">
                    <span class="text-base sm:text-lg font-bold mb-2">EASY</span>
                    <span class="text-[10px] leading-relaxed text-emerald-100">
                        • 3 Mạng<br>• Tốc độ chậm<br>• Nhảy cao
                    </span>
                </button>

                <!-- Normal -->
                <button id="btn-diff-normal" class="btn-retro flex-1 p-4 rounded-xl flex flex-col items-center justify-center cursor-pointer">
                    <span class="text-base sm:text-lg font-bold mb-2">NORMAL</span>
                    <span class="text-[10px] leading-relaxed text-amber-100">
                        • 2 Mạng<br>• Tốc độ vừa<br>• Cân bằng
                    </span>
                </button>

                <!-- Hard -->
                <button id="btn-diff-hard" class="btn-retro btn-danger flex-1 p-4 rounded-xl flex flex-col items-center justify-center cursor-pointer">
                    <span class="text-base sm:text-lg font-bold mb-2">HARD</span>
                    <span class="text-[10px] leading-relaxed text-red-100">
                        • 1 Mạng<br>• Tốc độ nhanh<br>• Thử thách
                    </span>
                </button>
            </div>

            <button id="btn-back-to-menu" class="mt-8 text-xs text-slate-400 hover:text-white underline cursor-pointer pointer-events-auto">
                ⬅️ Quay lại Trang Chủ
            </button>
        </div>

        <!-- 3. THANH TRẠNG THÁI (HUD) -->
        <div id="game-hud" class="absolute top-0 left-0 w-full p-3 flex justify-between items-center z-10 pointer-events-none hidden">
            <div class="bg-slate-900/80 px-3 py-2 rounded-lg border border-amber-500/50 flex items-center gap-2">
                <span class="text-xs text-amber-400">MẠNG:</span>
                <span id="hud-lives" class="text-xs text-red-500">❤️❤️❤️</span>
            </div>

            <div class="bg-slate-900/80 px-3 py-2 rounded-lg border border-amber-500/50 flex items-center gap-2">
                <span id="hud-difficulty" class="text-xs text-amber-300">NORMAL</span>
            </div>
        </div>

        <!-- 4. MÀN HÌNH KẾT THÚC (KẾT QUẢ GAME) -->
        <div id="screen-game-end" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-md z-30 hidden p-4">
            <h2 id="end-title" class="text-2xl sm:text-4xl text-amber-400 font-bold mb-4 text-center">
                GAME OVER
            </h2>
            <p id="end-subtitle" class="text-slate-300 text-xs sm:text-sm mb-8 text-center max-w-md leading-relaxed">
                Bạn chưa tới được ống cống ngầm!
            </p>
            <div class="flex gap-4">
                <button id="btn-restart" class="btn-retro p-4 rounded-xl cursor-pointer text-xs sm:text-sm">
                    🔄 CHƠI LẠI
                </button>
                <button id="btn-end-menu" class="btn-retro btn-danger p-4 rounded-xl cursor-pointer text-xs sm:text-sm">
                    🏠 TRANG CHỦ
                </button>
            </div>
        </div>

        <!-- 5. NÚT ĐIỀU KHIỂN CẢM ỨNG MOBILE -->
        <div id="touch-controls" class="absolute bottom-2 left-0 w-full px-4 flex justify-between items-center z-20 hidden pointer-events-auto opacity-70">
            <div class="flex gap-2">
                <button id="btn-touch-left" class="bg-slate-800 text-white w-12 h-12 rounded-full border-2 border-slate-600 text-xl flex items-center justify-center active:bg-slate-600">◀</button>
                <button id="btn-touch-right" class="bg-slate-800 text-white w-12 h-12 rounded-full border-2 border-slate-600 text-xl flex items-center justify-center active:bg-slate-600">▶</button>
            </div>
            <button id="btn-touch-jump" class="bg-amber-600 text-white w-14 h-14 rounded-full border-2 border-amber-400 text-2xl flex items-center justify-center active:bg-amber-500">⬆</button>
        </div>
    </div>

    <script>
        // Cấu hình kích thước cố định cho Canvas logic
        const GAME_WIDTH = 800;
        const GAME_HEIGHT = 450;

        // Thiết lập độ khó
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

        // Trạng thái nút bấm
        const keys = {};
        let touchLeft = false, touchRight = false, touchJump = false;

        // Lớp nhân vật Hamster
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

            update(diff, levelWidth, groundY) {
                if (this.enteringSewer) {
                    this.y += 1.5;
                    return;
                }

                let moveDir = 0;
                if (keys['ArrowLeft'] || keys['KeyA'] || touchLeft) moveDir -= 1;
                if (keys['ArrowRight'] || keys['KeyD'] || touchRight) moveDir += 1;

                if (moveDir !== 0) {
                    this.vx = moveDir * this.speed * (diff ? diff.speedMult : 1);
                    this.facing = moveDir > 0 ? 'right' : 'left';
                } else {
                    this.vx *= 0.7;
                }

                if ((keys['ArrowUp'] || keys['KeyW'] || keys['Space'] || touchJump) && this.grounded) {
                    this.vy = -(diff ? diff.jumpPower : 12.5);
                    this.grounded = false;
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

                if (this.facing === 'left') {
                    ctx.scale(-1, 1);
                }

                if (this.invulnerableTimer > 0 && Math.floor(this.invulnerableTimer / 4) % 2 === 0) {
                    ctx.globalAlpha = 0.4;
                }

                // Thân Hamster
                ctx.fillStyle = '#f97316';
                ctx.beginPath();
                ctx.ellipse(0, 2, 18, 14, 0, 0, Math.PI * 2);
                ctx.fill();

                // Bụng trắng
                ctx.fillStyle = '#ffedd5';
                ctx.beginPath();
                ctx.ellipse(3, 4, 10, 8, 0, 0, Math.PI * 2);
                ctx.fill();

                // Đầu
                ctx.fillStyle = '#fb923c';
                ctx.beginPath();
                ctx.arc(8, -4, 10, 0, Math.PI * 2);
                ctx.fill();

                // Tai
                ctx.fillStyle = '#ea580c';
                ctx.beginPath();
                ctx.arc(2, -12, 4, 0, Math.PI * 2);
                ctx.fill();

                // Mắt
                ctx.fillStyle = '#0f172a';
                ctx.beginPath();
                ctx.arc(11, -5, 2.5, 0, Math.PI * 2);
                ctx.fill();

                // Mũi
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

        // Khởi tạo Game
        window.addEventListener('DOMContentLoaded', () => {
            canvas = document.getElementById('gameCanvas');
            canvas.width = GAME_WIDTH;
            canvas.height = GAME_HEIGHT;
            ctx = canvas.getContext('2d');

            // Đăng ký sự kiện nút
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

            // Sự kiện phím bấm
            window.addEventListener('keydown', e => keys[e.code] = true);
            window.addEventListener('keyup', e => keys[e.code] = false);

            // Cảm ứng Mobile
            const bindTouch = (id, setFn) => {
                const el = document.getElementById(id);
                if (!el) return;
                el.addEventListener('touchstart', (e) => { e.preventDefault(); setFn(true); });
                el.addEventListener('touchend', (e) => { e.preventDefault(); setFn(false); });
            };
            bindTouch('btn-touch-left', v => touchLeft = v);
            bindTouch('btn-touch-right', v => touchRight = v);
            bindTouch('btn-touch-jump', v => touchJump = v);

            if ('ontouchstart' in window) {
                document.getElementById('touch-controls').classList.remove('hidden');
            }

            // Vẽ màn hình chờ
            drawBackground();
        });

        function generateLevel(diffKey) {
            levelWidth = 3200;
            groundY = GAME_HEIGHT - 70;
            platforms = [];
            hazards = [];

            const diff = DIFFICULTY_SETTINGS[diffKey];

            // Tạo các nền tảng gạch trên cao
            for (let x = 400; x < levelWidth - 500; x += 220) {
                if (Math.random() > 0.3) {
                    let platW = 100;
                    let platH = groundY - (Math.random() * 120 + 60);
                    platforms.push({ x: x, y: platH, w: platW, h: 18 });
                }
            }

            // Tạo chướng ngại vật (chông & đá lăn)
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

            // Ống cống thoát hiểm ở cuối màn
            exitPipe = { x: levelWidth - 250, y: groundY - 60, w: 60, h: 60 };
        }

        function startGame(difficulty) {
            currentDifficulty = difficulty;
            const diff = DIFFICULTY_SETTINGS[difficulty];

            player = new Hamster();
            player.lives = diff.lives;

            generateLevel(difficulty);

            // Cập nhật giao diện
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
            player.update(diff, levelWidth, groundY);

            // Xử lý va chạm mặt đất
            if (!player.enteringSewer) {
                if (player.y + player.height >= groundY) {
                    player.y = groundY - player.height;
                    player.vy = 0;
                    player.grounded = true;
                }

                // Xử lý va chạm nền tảng trên cao
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

            // Camera di chuyển theo nhân vật
            cameraX = player.x - GAME_WIDTH / 3;
            if (cameraX < 0) cameraX = 0;
            if (cameraX > levelWidth - GAME_WIDTH) cameraX = levelWidth - GAME_WIDTH;

            // Cập nhật đá lăn
            hazards.forEach(h => {
                if (h.type === 'boulder') {
                    h.x += h.vx;
                    if (h.x < 200 || h.x > levelWidth - 300) h.vx *= -1;
                }
            });

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
                    setTimeout(() => {
                        endGame(true);
                    }, 1200);
                }
            }
        }

        function render() {
            drawBackground();

            // Vẽ nền tảng gạch
            platforms.forEach(p => {
                ctx.fillStyle = '#854d0e';
                ctx.fillRect(p.x - cameraX, p.y, p.w, p.h);
                ctx.fillStyle = '#22c55e';
                ctx.fillRect(p.x - cameraX, p.y, p.w, 4);
            });

            // Vẽ chướng ngại vật
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

            // Vẽ Ống cống ngầm (Sewer Pipe)
            if (exitPipe) {
                ctx.fillStyle = '#166534';
                ctx.fillRect(exitPipe.x - cameraX, exitPipe.y, exitPipe.w, exitPipe.h);
                ctx.fillStyle = '#22c55e';
                ctx.fillRect(exitPipe.x - cameraX - 4, exitPipe.y - 10, exitPipe.w + 8, 12);

                ctx.fillStyle = '#facc15';
                ctx.font = '10px "Press Start 2P"';
                ctx.fillText('DRAIN ⬇️', exitPipe.x - cameraX - 10, exitPipe.y - 18);
            }

            // Vẽ nhân vật Hamster
            player.draw(ctx, cameraX);
        }

        function drawBackground() {
            // Bầu trời Trái Đất
            ctx.fillStyle = '#38bdf8';
            ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

            // Mây trắng
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            for (let i = 0; i < 5; i++) {
                let cloudX = ((i * 300) - cameraX * 0.2) % (GAME_WIDTH + 200) - 100;
                ctx.beginPath();
                ctx.arc(cloudX, 60 + (i % 2) * 20, 25, 0, Math.PI * 2);
                ctx.arc(cloudX + 20, 50 + (i % 2) * 20, 35, 0, Math.PI * 2);
                ctx.arc(cloudX + 50, 60 + (i % 2) * 20, 25, 0, Math.PI * 2);
                ctx.fill();
            }

            // Đất & Cỏ
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
