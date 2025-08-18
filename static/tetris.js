// Tetris Web Game - Modern Classic Edition

class TetrisGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.nextCanvas = document.getElementById('nextCanvas');
        this.nextCtx = this.nextCanvas.getContext('2d');
        
        // Размеры игрового поля
        this.BOARD_WIDTH = 10;
        this.BOARD_HEIGHT = 20;
        this.BLOCK_SIZE = 30;
        
        // Игровое состояние
        this.board = [];
        this.currentPiece = null;
        this.nextPiece = null;
        this.score = 0;
        this.level = 1;
        this.lines = 0;
        this.dropTime = 0;
        this.dropInterval = 1000; // 1 секунда для первого уровня
        this.isPaused = false;
        this.isGameOver = false;
        this.username = '';
        
        // Цвета для фигур
        this.colors = [
            '#FF0000', // I - красный
            '#00FF00', // O - зелёный  
            '#0000FF', // T - синий
            '#FFFF00', // S - жёлтый
            '#FF00FF', // Z - пурпурный
            '#00FFFF', // J - голубой
            '#FFA500'  // L - оранжевый
        ];
        
        // Формы тетромино
        this.pieces = [
            // I
            [
                [1,1,1,1]
            ],
            // O
            [
                [1,1],
                [1,1]
            ],
            // T
            [
                [0,1,0],
                [1,1,1]
            ],
            // S
            [
                [0,1,1],
                [1,1,0]
            ],
            // Z
            [
                [1,1,0],
                [0,1,1]
            ],
            // J
            [
                [1,0,0],
                [1,1,1]
            ],
            // L
            [
                [0,0,1],
                [1,1,1]
            ]
        ];
        
        this.initBoard();
        this.bindEvents();
    }
    
    initBoard() {
        // Создать пустое игровое поле
        this.board = Array(this.BOARD_HEIGHT).fill().map(() => Array(this.BOARD_WIDTH).fill(0));
    }
    
    bindEvents() {
        document.addEventListener('keydown', (e) => {
            if (this.isGameOver) return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.movePiece(-1, 0);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.movePiece(1, 0);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.movePiece(0, 1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.rotatePiece();
                    break;
                case ' ':
                    e.preventDefault();
                    this.togglePause();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.showGameOverScreen();
                    break;
            }
        });
    }
    
    createPiece() {
        const type = Math.floor(Math.random() * this.pieces.length);
        return {
            shape: this.pieces[type],
            color: this.colors[type],
            x: Math.floor(this.BOARD_WIDTH / 2) - Math.floor(this.pieces[type][0].length / 2),
            y: 0,
            type: type
        };
    }
    
    spawnPiece() {
        if (!this.nextPiece) {
            this.nextPiece = this.createPiece();
        }
        
        this.currentPiece = this.nextPiece;
        this.nextPiece = this.createPiece();
        
        // Проверить game over
        if (this.checkCollision(this.currentPiece)) {
            this.gameOver();
            return false;
        }
        
        this.drawNextPiece();
        return true;
    }
    
    movePiece(dx, dy) {
        if (!this.currentPiece || this.isPaused) return;
        
        const newPiece = {
            ...this.currentPiece,
            x: this.currentPiece.x + dx,
            y: this.currentPiece.y + dy
        };
        
        if (!this.checkCollision(newPiece)) {
            this.currentPiece = newPiece;
            return true;
        }
        
        // Если фигура не может двигаться вниз, зафиксировать её
        if (dy > 0) {
            this.placePiece();
            return false;
        }
        
        return false;
    }
    
    rotatePiece() {
        if (!this.currentPiece || this.isPaused) return;
        
        const rotated = this.rotateMatrix(this.currentPiece.shape);
        const newPiece = {
            ...this.currentPiece,
            shape: rotated
        };
        
        if (!this.checkCollision(newPiece)) {
            this.currentPiece.shape = rotated;
        }
    }
    
    rotateMatrix(matrix) {
        const n = matrix.length;
        const m = matrix[0].length;
        const rotated = Array(m).fill().map(() => Array(n).fill(0));
        
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < m; j++) {
                rotated[j][n - 1 - i] = matrix[i][j];
            }
        }
        
        return rotated;
    }
    
    checkCollision(piece) {
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    const boardX = piece.x + x;
                    const boardY = piece.y + y;
                    
                    // Проверить границы
                    if (boardX < 0 || boardX >= this.BOARD_WIDTH || 
                        boardY >= this.BOARD_HEIGHT) {
                        return true;
                    }
                    
                    // Проверить столкновение с другими блоками
                    if (boardY >= 0 && this.board[boardY][boardX]) {
                        return true;
                    }
                }
            }
        }
        return false;
    }
    
    placePiece() {
        // Поместить фигуру на доску
        for (let y = 0; y < this.currentPiece.shape.length; y++) {
            for (let x = 0; x < this.currentPiece.shape[y].length; x++) {
                if (this.currentPiece.shape[y][x]) {
                    const boardX = this.currentPiece.x + x;
                    const boardY = this.currentPiece.y + y;
                    
                    if (boardY >= 0) {
                        this.board[boardY][boardX] = this.currentPiece.type + 1;
                    }
                }
            }
        }
        
        // Проверить и убрать заполненные линии
        this.clearLines();
        
        // Создать новую фигуру
        this.spawnPiece();
    }
    
    clearLines() {
        let linesCleared = 0;
        
        for (let y = this.BOARD_HEIGHT - 1; y >= 0; y--) {
            if (this.board[y].every(cell => cell !== 0)) {
                // Удалить линию
                this.board.splice(y, 1);
                // Добавить новую пустую линию сверху
                this.board.unshift(Array(this.BOARD_WIDTH).fill(0));
                linesCleared++;
                y++; // Проверить эту линию снова
            }
        }
        
        if (linesCleared > 0) {
            // Подсчёт очков (квадратичный)
            const points = linesCleared * linesCleared * 100 * this.level;
            this.score += points;
            this.lines += linesCleared;
            
            // Повышение уровня каждые 10 линий
            const newLevel = Math.floor(this.lines / 10) + 1;
            if (newLevel > this.level) {
                this.level = newLevel;
                // Увеличить скорость
                this.dropInterval = Math.max(100, 1000 - (this.level - 1) * 100);
            }
            
            this.updateUI();
        }
    }
    
    togglePause() {
        this.isPaused = !this.isPaused;
        document.getElementById('pauseScreen').style.display = this.isPaused ? 'flex' : 'none';
    }
    
    gameOver() {
        this.isGameOver = true;
        this.saveScore();
    }
    
    async saveScore() {
        try {
            const response = await fetch('/api/save_score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    score: this.score
                })
            });
            
            const data = await response.json();
            this.showGameOverScreen(data.new_record);
        } catch (error) {
            console.error('Ошибка сохранения результата:', error);
            this.showGameOverScreen(false);
        }
    }
    
    showGameOverScreen(isNewRecord = false) {
        document.getElementById('finalScore').textContent = `Очки: ${this.score}`;
        
        const newRecordEl = document.getElementById('newRecord');
        if (isNewRecord) {
            newRecordEl.classList.remove('hidden');
        } else {
            newRecordEl.classList.add('hidden');
        }
        
        document.getElementById('gameOverScreen').style.display = 'flex';
    }
    
    update(deltaTime) {
        if (this.isPaused || this.isGameOver) return;
        
        this.dropTime += deltaTime;
        
        if (this.dropTime >= this.dropInterval) {
            this.movePiece(0, 1);
            this.dropTime = 0;
        }
    }
    
    draw() {
        // Очистить canvas
        this.ctx.fillStyle = '#f8f8f8';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Нарисовать доску
        this.drawBoard();
        
        // Нарисовать текущую фигуру
        if (this.currentPiece) {
            this.drawPiece(this.currentPiece);
        }
        
        // Нарисовать сетку
        this.drawGrid();
    }
    
    drawBoard() {
        for (let y = 0; y < this.BOARD_HEIGHT; y++) {
            for (let x = 0; x < this.BOARD_WIDTH; x++) {
                if (this.board[y][x]) {
                    this.ctx.fillStyle = this.colors[this.board[y][x] - 1];
                    this.ctx.fillRect(
                        x * this.BLOCK_SIZE + 1,
                        y * this.BLOCK_SIZE + 1,
                        this.BLOCK_SIZE - 2,
                        this.BLOCK_SIZE - 2
                    );
                }
            }
        }
    }
    
    drawPiece(piece) {
        this.ctx.fillStyle = piece.color;
        
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    this.ctx.fillRect(
                        (piece.x + x) * this.BLOCK_SIZE + 1,
                        (piece.y + y) * this.BLOCK_SIZE + 1,
                        this.BLOCK_SIZE - 2,
                        this.BLOCK_SIZE - 2
                    );
                }
            }
        }
    }
    
    drawGrid() {
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        
        for (let x = 0; x <= this.BOARD_WIDTH; x++) {
            this.ctx.beginPath();
            this.ctx.moveTo(x * this.BLOCK_SIZE, 0);
            this.ctx.lineTo(x * this.BLOCK_SIZE, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.BOARD_HEIGHT; y++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y * this.BLOCK_SIZE);
            this.ctx.lineTo(this.canvas.width, y * this.BLOCK_SIZE);
            this.ctx.stroke();
        }
    }
    
    drawNextPiece() {
        if (!this.nextPiece) return;
        
        // Очистить canvas следующей фигуры
        this.nextCtx.fillStyle = 'white';
        this.nextCtx.fillRect(0, 0, this.nextCanvas.width, this.nextCanvas.height);
        
        const piece = this.nextPiece;
        const blockSize = 15;
        const offsetX = (this.nextCanvas.width - piece.shape[0].length * blockSize) / 2;
        const offsetY = (this.nextCanvas.height - piece.shape.length * blockSize) / 2;
        
        this.nextCtx.fillStyle = piece.color;
        
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    this.nextCtx.fillRect(
                        offsetX + x * blockSize,
                        offsetY + y * blockSize,
                        blockSize - 1,
                        blockSize - 1
                    );
                }
            }
        }
    }
    
    updateUI() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('level').textContent = this.level;
        document.getElementById('lines').textContent = this.lines;
    }
    
    start() {
        this.initBoard();
        this.score = 0;
        this.level = 1;
        this.lines = 0;
        this.dropTime = 0;
        this.dropInterval = 1000;
        this.isPaused = false;
        this.isGameOver = false;
        this.currentPiece = null;
        this.nextPiece = null;
        
        this.spawnPiece();
        this.updateUI();
        
        // Показать игровое поле
        document.getElementById('gameArea').style.display = 'flex';
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('gameOverScreen').style.display = 'none';
        
        this.gameLoop();
    }
    
    gameLoop() {
        let lastTime = 0;
        
        const loop = (currentTime) => {
            const deltaTime = currentTime - lastTime;
            lastTime = currentTime;
            
            this.update(deltaTime);
            this.draw();
            
            if (!this.isGameOver) {
                requestAnimationFrame(loop);
            }
        };
        
        requestAnimationFrame(loop);
    }
}

// Глобальная переменная игры
let game = null;
let currentUsername = '';

// Функции управления игрой
async function login() {
    const username = document.getElementById('usernameInput').value.trim();
    
    if (!username) {
        alert('Пожалуйста, введите ваше имя');
        return;
    }
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUsername = username;
            
            // Обновить информацию об игроке
            document.getElementById('playerName').textContent = username;
            document.getElementById('playerStats').innerHTML = 
                `Рекорд: ${data.stats.high_score}<br>Игр: ${data.stats.games_played}`;
            
            // Создать и запустить игру
            game = new TetrisGame();
            game.username = username;
            game.start();
        } else {
            alert(data.error || 'Ошибка входа');
        }
    } catch (error) {
        console.error('Ошибка входа:', error);
        alert('Ошибка подключения к серверу');
    }
}

function restartGame() {
    if (game) {
        game.start();
    }
}

function showLogin() {
    document.getElementById('gameArea').style.display = 'none';
    document.getElementById('gameOverScreen').style.display = 'none';
    document.getElementById('loginScreen').style.display = 'flex';
    document.getElementById('usernameInput').value = '';
    document.getElementById('usernameInput').focus();
}

// Обработчик Enter в поле ввода имени
document.getElementById('usernameInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        login();
    }
});

// Инициализация при загрузке страницы
window.addEventListener('load', () => {
    document.getElementById('usernameInput').focus();
});