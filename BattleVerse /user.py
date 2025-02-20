from datetime import datetime
from BatlleVerse.db import users_col  # Assuming you have a database module
import random

# Helper Functions for User Management
class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.first_name = None
        self.level = 1
        self.uc = 500  # UC currency (in-game currency)
        self.bp = 5000  # Battle points (in-game points)
        self.wins = 0
        self.losses = 0
        self.senzu_beans = 0  # Health items for recovery
        self.character = None  # Character ID for selected character
        self.battles = 0
        self.start_date = datetime.now().strftime("%d-%m-%Y")
    
    def create_user(self):
        """
        Add a new user to the database with initial stats.
        """
        if not users_col.find_one({"user_id": self.user_id}):
            users_col.insert_one({
                "user_id": self.user_id,
                "username": self.username,
                "firstname": self.first_name,
                "level": self.level,
                "uc": self.uc,
                "bp": self.bp,
                "wins": self.wins,
                "losses": self.losses,
                "senzu_beans": self.senzu_beans,
                "character": self.character,
                "battles": self.battles,
                "start_date": self.start_date,
            })

    def update_user_info(self):
        """
        Update user information in the database (e.g., wins, losses, character selection).
        """
        users_col.update_one(
            {"user_id": self.user_id},
            {"$set": {
                "username": self.username,
                "firstname": self.first_name,
                "level": self.level,
                "uc": self.uc,
                "bp": self.bp,
                "wins": self.wins,
                "losses": self.losses,
                "senzu_beans": self.senzu_beans,
                "character": self.character,
                "battles": self.battles,
            }}
        )

    def select_character(self, character_id):
        """
        Select a character for the player.
        """
        available_characters = ["Warrior", "Mage", "Assassin", "Tank"]  # Example characters
        if character_id in available_characters:
            self.character = character_id
            self.update_user_info()
            return f"Character {character_id} selected!"
        else:
            return "Character not available."

    def earn_xp(self, xp_amount):
        """
        Earn XP and level up if necessary.
        """
        self.level += xp_amount
        self.update_user_info()
        return f"XP earned: {xp_amount}, New Level: {self.level}"

    def win_battle(self):
        """
        Increment wins after winning a battle.
        """
        self.wins += 1
        self.battles += 1
        self.update_user_info()
        return f"Battle won! Total Wins: {self.wins}"

    def lose_battle(self):
        """
        Increment losses after losing a battle.
        """
        self.losses += 1
        self.battles += 1
        self.update_user_info()
        return f"Battle lost! Total Losses: {self.losses}"

    def use_senzu_bean(self):
        """
        Use a senzu bean to recover health.
        """
        if self.senzu_beans > 0:
            self.senzu_beans -= 1
            self.update_user_info()
            return "Senzu Bean used! Health restored."
        else:
            return "No Senzu Beans left!"

    def stats(self):
        """
        Get current user stats (Health, Energy, Score, etc.)
        """
        return {
            "username": self.username,
            "level": self.level,
            "uc": self.uc,
            "bp": self.bp,
            "wins": self.wins,
            "losses": self.losses,
            "senzu_beans": self.senzu_beans,
            "character": self.character,
            "battles": self.battles,
        }

    def join_battle(self, battle_id):
        """
        Join a battle in the group battle mode.
        """
        # Placeholder code to join a battle
        battle = {
            "battle_id": battle_id,
            "participants": [self.user_id]
        }
        # Assume you have a method to add this battle to a database
        # battles_col.insert_one(battle)
        return f"Joined Battle {battle_id}!"

# Battle Commands - Example Usage in Command Handlers
def handle_user_commands(user_id, command, **kwargs):
    user_data = users_col.find_one({"user_id": user_id})
    if not user_data:
        user = User(user_id, kwargs.get("username"))
        user.create_user()
        user_data = vars(user)
    else:
        user = User(**user_data)

    if command == "select":
        return user.select_character(kwargs.get("character"))
    elif command == "win":
        return user.win_battle()
    elif command == "lose":
        return user.lose_battle()
    elif command == "xp":
        return user.earn_xp(kwargs.get("xp_amount"))
    elif command == "senzu":
        return user.use_senzu_bean()
    elif command == "stats":
        return user.stats()
    elif command == "join":
        return user.join_battle(kwargs.get("battle_id"))
    else:
        return "Unknown command!"

# Example usage
user_id = 6239769036
username = "Ryomen_Sukuna_53"
print(handle_user_commands(user_id, "select", character="Mage"))
print(handle_user_commands(user_id, "win"))
