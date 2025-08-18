from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Простое хранилище пользователей (в продакшене используйте базу данных)
USERS_FILE = 'web_tetris_users.json'

def load_users():
    """Загрузить данные пользователей"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users_data):
    """Сохранить данные пользователей"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

@app.route('/')
def index():
    """Главная страница игры"""
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    """API для входа пользователя"""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Требуется имя пользователя'}), 400
    
    users = load_users()
    
    # Создать пользователя, если не существует
    if username not in users:
        users[username] = {
            'high_score': 0,
            'games_played': 0
        }
        save_users(users)
    
    return jsonify({
        'success': True,
        'username': username,
        'stats': users[username]
    })

@app.route('/api/save_score', methods=['POST'])
def save_score():
    """API для сохранения результата"""
    data = request.get_json()
    username = data.get('username', '').strip()
    score = data.get('score', 0)
    
    if not username:
        return jsonify({'error': 'Требуется имя пользователя'}), 400
    
    users = load_users()
    
    if username in users:
        users[username]['games_played'] += 1
        if score > users[username]['high_score']:
            users[username]['high_score'] = score
        
        save_users(users)
        
        return jsonify({
            'success': True,
            'stats': users[username],
            'new_record': score == users[username]['high_score'] and score > 0
        })
    
    return jsonify({'error': 'Пользователь не найден'}), 404

@app.route('/api/stats/<username>')
def get_stats(username):
    """API для получения статистики пользователя"""
    users = load_users()
    
    if username in users:
        return jsonify({
            'success': True,
            'stats': users[username]
        })
    
    return jsonify({'error': 'Пользователь не найден'}), 404

@app.route('/api/leaderboard')
def leaderboard():
    """API для получения таблицы лидеров"""
    users = load_users()
    
    # Сортировать по лучшему результату
    sorted_users = sorted(
        [(username, data) for username, data in users.items()],
        key=lambda x: x[1]['high_score'],
        reverse=True
    )[:10]  # Топ 10
    
    leaderboard_data = [
        {
            'username': username,
            'high_score': data['high_score'],
            'games_played': data['games_played']
        }
        for username, data in sorted_users
    ]
    
    return jsonify({
        'success': True,
        'leaderboard': leaderboard_data
    })

if __name__ == '__main__':
    # Создать директорию для шаблонов, если не существует
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)