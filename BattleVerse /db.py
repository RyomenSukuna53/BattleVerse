from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio
import datetime

# MongoDB Connection String
MONGO_URI = "mongodb+srv://USERNAME:PASSWORD@your-cluster.mongodb.net/?retryWrites=true&w=majority"

# Async MongoDB Client
mongo_client = AsyncIOMotorClient(MONGO_URI)
battleverse_db = mongo_client["BattleVerseDB"]

# Collections
users_col = battleverse_db["users"]
games_col = battleverse_db["games"]
banned_users_col = battleverse_db["banned_users"]
characters_col = battleverse_db["characters"]
missions_col = battleverse_db["missions"]
inventory_col = battleverse_db["inventory"]
rewards_col = battleverse_db["rewards"]

# MongoDB Indexing for Optimization
async def create_indexes():
    await users_col.create_index("user_id", unique=True)
    await games_col.create_index("group_id")
    await banned_users_col.create_index("user_id", unique=True)
    print("✅ Indexes Created for Faster Queries!")

async def test_mongo_connection():
    """Tests MongoDB connection."""
    try:
        await mongo_client.server_info()
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")

# 🚀 User Management
async def create_user(user_id, username):
    """Creates a new player."""
    user_data = {
        "user_id": user_id,
        "username": username,
        "level": 1,
        "xp": 0,
        "gold": 100,
        "inventory": {"weapons": [], "items": []},
        "equipped_character": None,
        "stats": {"health": 100, "energy": 50, "attack": 10, "defense": 5}
    }
    await users_col.insert_one(user_data)

async def get_user(user_id):
    """Fetches player data."""
    return await users_col.find_one({"user_id": user_id})

async def update_player_xp(user_id, xp_gain):
    """Updates player XP and levels up if needed."""
    player = await get_user(user_id)
    if not player:
        return None
    new_xp = player["xp"] + xp_gain
    new_level = player["level"] + (new_xp // 1000)  # Level up every 1000 XP
    await users_col.update_one({"user_id": user_id}, {"$set": {"xp": new_xp, "level": new_level}})
    return new_level

async def ban_user(user_id, reason, admin_id):
    """Bans a user from the game."""
    ban_data = {
        "user_id": user_id,
        "reason": reason,
        "banned_by": admin_id,
        "ban_date": datetime.datetime.utcnow()
    }
    await banned_users_col.insert_one(ban_data)

# 🎮 Game Management
async def create_game(group_id, mode, creator_id):
    """Creates a new game."""
    game_data = {
        "group_id": group_id,
        "mode": mode,
        "players": [creator_id],
        "defenders": [],
        "attackers": [],
        "warnings": {},
        "current_turn": creator_id,
        "start_time": None,
        "status": "waiting"
    }
    result = await games_col.insert_one(game_data)
    return result.inserted_id

async def get_active_game(group_id):
    """Fetches an active game for a group."""
    return await games_col.find_one({"group_id": group_id, "status": {"$in": ["waiting", "active"]}})

async def add_player_to_game(game_id, player_id):
    """Adds a player to an existing game."""
    await games_col.update_one({"_id": ObjectId(game_id)}, {"$addToSet": {"players": player_id}})

async def start_game(game_id):
    """Starts the game by setting status to active."""
    await games_col.update_one({"_id": ObjectId(game_id)}, {"$set": {"start_time": datetime.datetime.utcnow(), "status": "active"}})

async def remove_game(game_id):
    """Removes a game from the database."""
    await games_col.delete_one({"_id": ObjectId(game_id)})

# 💀 Solo Hunt Mode
async def start_solo_hunt(user_id):
    """Starts a solo hunt mission."""
    mission = await missions_col.find_one({"status": "available"})
    if not mission:
        return None
    await users_col.update_one({"user_id": user_id}, {"$set": {"current_mission": mission["_id"]}})
    return mission

async def complete_solo_hunt(user_id, mission_id):
    """Completes a solo mission and rewards player."""
    mission = await missions_col.find_one({"_id": ObjectId(mission_id)})
    if mission:
        await update_player_xp(user_id, mission["rewards"]["xp"])
        await users_col.update_one({"user_id": user_id}, {"$unset": {"current_mission": ""}})
        return mission["rewards"]
    return None

# 🎁 Inventory & Rewards
async def get_inventory(user_id):
    """Fetches player inventory."""
    return await inventory_col.find_one({"user_id": user_id})

async def add_item_to_inventory(user_id, item):
    """Adds an item to player inventory."""
    await inventory_col.update_one({"user_id": user_id}, {"$addToSet": {"items": item}}, upsert=True)

async def get_random_loot():
    """Fetches a random loot crate reward."""
    loot = await rewards_col.aggregate([{"$sample": {"size": 1}}]).to_list(1)
    return loot[0] if loot else None

async def claim_loot(user_id):
    """Claims a random loot reward."""
    loot = await get_random_loot()
    if loot:
        await add_item_to_inventory(user_id, loot["items"][0])
        return loot
    return None

# 🎯 Game Execution (For Testing)
async def main():
    await test_mongo_connection()
    await create_indexes()  # Ensure indexes are set

    # Create a user
    await create_user("123456", "BattleHero")
    player = await get_user("123456")
    print(f"👤 Player Created: {player}")

    # Create a game
    game_id = await create_game("group_001", "Group Battle", "123456")
    print(f"🎮 Game Created: {game_id}")

    # Start a game
    await start_game(game_id)
    print(f"🚀 Game {game_id} started!")

    # Solo Hunt
    mission = await start_solo_hunt("123456")
    print(f"💀 Solo Hunt Started: {mission}")

    # Claim Loot
    loot = await claim_loot("123456")
    print(f"🎁 Loot Claimed: {loot}")

# Run the Main Execution
asyncio.run(main())
