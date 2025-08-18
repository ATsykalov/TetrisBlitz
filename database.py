import os
try:
    from replit import db
    REPLIT_DB_AVAILABLE = True
except ImportError:
    REPLIT_DB_AVAILABLE = False
    # Fallback to file-based storage
    import json

class DatabaseManager:
    def __init__(self):
        self.use_replit_db = REPLIT_DB_AVAILABLE
        self.file_path = "tetris_users.json"
        
        if not self.use_replit_db:
            self.init_file_db()
    
    def init_file_db(self):
        """Initialize file-based database if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
    
    def get_user_data(self, username):
        """Get user data from database"""
        if self.use_replit_db:
            return db.get(f"user_{username}", {
                "username": username,
                "high_score": 0,
                "games_played": 0
            })
        else:
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                return data.get(username, {
                    "username": username,
                    "high_score": 0,
                    "games_played": 0
                })
            except (FileNotFoundError, json.JSONDecodeError):
                return {
                    "username": username,
                    "high_score": 0,
                    "games_played": 0
                }
    
    def save_user_data(self, username, user_data):
        """Save user data to database"""
        if self.use_replit_db:
            db[f"user_{username}"] = user_data
        else:
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}
            
            data[username] = user_data
            
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
    
    def update_user_score(self, username, score):
        """Update user's high score if the new score is higher"""
        user_data = self.get_user_data(username)
        user_data["games_played"] += 1
        
        if score > user_data["high_score"]:
            user_data["high_score"] = score
        
        self.save_user_data(username, user_data)
        return user_data
    
    def get_leaderboard(self, limit=10):
        """Get top players (for future use)"""
        if self.use_replit_db:
            users = []
            for key in db.keys():
                if key.startswith("user_"):
                    users.append(db[key])
        else:
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                users = list(data.values())
            except (FileNotFoundError, json.JSONDecodeError):
                users = []
        
        # Sort by high score
        users.sort(key=lambda x: x.get("high_score", 0), reverse=True)
        return users[:limit]
