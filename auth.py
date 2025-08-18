from database import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None
    
    def login_user(self, username):
        """Login user and load their data"""
        self.current_user = username
        user_data = self.db.get_user_data(username)
        
        # Ensure user data exists in database
        self.db.save_user_data(username, user_data)
        
        return user_data
    
    def get_user_stats(self, username):
        """Get user statistics"""
        return self.db.get_user_data(username)
    
    def update_user_score(self, username, score):
        """Update user's score after a game"""
        return self.db.update_user_score(username, score)
    
    def logout_user(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if a user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
