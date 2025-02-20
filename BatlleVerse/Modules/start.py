from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.enums import ChatType
from datetime import datetime
from Batlleverse import bot
from Batlleverse.db import users_col
from Batlleverse.Modules.characters import character_data  # Import character data

# Predefined characters
fixed_characters = [
    {"name": "Yamcha", "Atk": 50, "image": "https://files.catbox.moe/44rxqs.jpg", "def": 50},
    {"name": "Chiaotzu", "Atk": 50, "image": "https://files.catbox.moe/w67puk.jpg", "def": 50},
]

@bot.on_message(filters.command("start"))
async def start_command(_, message: Message):
    """Handles the /start command to onboard users into the bot."""
    
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    first_name = message.from_user.first_name or "Warrior"
    chat_type = message.chat.type
    user = users_col.find_one({"user_id": user_id})

    # Check if user already owns a fighter
    if user and user.get("character"):
        await message.reply(
            f"⚔ **{first_name}, you have already begun your journey!** ⚔\n"
            "Use **/battle** to challenge enemies and grow stronger!"
        )
        return

    # If in a group, prompt the user to start in PM
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(
            "🔥 **Want to begin your adventure?** 🔥\n"
            "DM me to get started! Click below to start in private chat.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("▶ Start in PM", url="t.me/bgmi_state_bot")]]
            ),
        )
    else:
        # If user is new, add them to the database
        try:
            if not user:
                users_col.update_one(
                    {"user_id": user_id},
                    {"$set": {
                        "username": username, "level": 1, "exp": 0, "bp": 5000, "uc": 500,
                        "wins": 0, "losses": 0, "character": {}, "inventory": [],
                        "battles": 0, "start_date": datetime.utcnow()
                    }},
                    upsert=True
                )

            # Send gender selection message
            await message.reply_photo(
                photo="https://files.catbox.moe/y0cru1.jpg",
                caption=(
                    f"⬛ **Welcome to the Arena, {first_name}!** ⬛\n"
                    "⚔ Choose your gender to begin your journey! ⚔"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("♂ Male", callback_data="gender_male"),
                        InlineKeyboardButton("♀ Female", callback_data="gender_female"),
                    ]
                ]),
            )
        except Exception as e:
            await message.reply(f"⚠ Error: {e}")


@bot.on_callback_query(filters.regex(r"^gender_(.+)"))
async def select_gender(_, callback_query: CallbackQuery):
    """Handles gender selection and displays corresponding characters."""
    
    gender = callback_query.data.split("_")[1]

    # Set character choices based on gender
    if gender == "male":
        await callback_query.message.edit_text(
            "⚔ Choose your warrior:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Yamcha", callback_data="character_Yamcha")]]
            ),
        )
    elif gender == "female":
        await callback_query.message.edit_text(
            "⚔ Choose your warrior:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Chiaotzu", callback_data="character_Chiaotzu")]]
            ),
        )


@bot.on_callback_query(filters.regex(r"^character_(.+)"))
async def select_character(_, callback_query: CallbackQuery):
    """Handles character selection and finalizes the user's choice."""
    
    character_name = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    user = users_col.find_one({"user_id": user_id})

    # Check if user already owns a character
    if user and user.get("character"):
        await callback_query.answer("⚠ You already own a fighter!", show_alert=True)
        return

    # Find selected character
    character = character_data.get(character_name)
    if not character:
        await callback_query.answer("⚠ Invalid character selection!", show_alert=True)
        return

    # Extract and filter available weapons based on level
    current_level = 1
    unlocked_weapons = {
        weapon: info for weapon, info in character.get("weapons", {}).items()
        if info["level"] <= current_level
    }
    locked_weapons = {
        weapon: info for weapon, info in character.get("weapons", {}).items()
        if info["level"] > current_level
    }

    # Prepare character data for database
    character_data_to_save = {
        "caption": character["caption"],
        "HP": character["base_stats"]["hp"],
        "Atk": character["base_stats"]["atk"],
        "Def": character["base_stats"]["def"],
        "Spe": character["base_stats"]["spe"],
        "Acc": character["base_stats"]["acc"],
        "photo": character["photo"],
        "level": current_level,
        "exp": 0,
        "unlocked_weapons": unlocked_weapons,
    }

    try:
        # Update user's character data
        users_col.update_one(
            {"user_id": user_id},
            {"$set": {
                f"character.{character_name}": character_data_to_save,
                "bp": 5000, "uc": 500, "start_date": datetime.utcnow(),
            }}
        )

        # Prepare weapon display lists
        weapon_list = "\n".join(
            [f"⚔ **{weapon}**: {info['damage'][0]}-{info['damage'][1]} DMG (Unlock Lv {info['level']})"
             for weapon, info in unlocked_weapons.items()]
        )
        locked_list = "\n".join(
            [f"🔒 **{weapon}**: Unlocks at Lv {info['level']}" for weapon, info in locked_weapons.items()]
        )

        # Send confirmation message
        await callback_query.message.reply_photo(
            photo=character["photo"],
            caption=(
                f"⬛ **Congratulations, {callback_query.from_user.first_name}!** ⬛\n"
                f"You have chosen **{character_name}** as your warrior.\n\n"
                f"⚡ **Stats:**\n"
                f"✔ HP: {character['base_stats']['hp']}\n"
                f"✔ ATK: {character['base_stats']['atk']}\n"
                f"✔ DEF: {character['base_stats']['def']}\n"
                f"✔ SPE: {character['base_stats']['spe']}\n\n"
                f"⚔ **Unlocked Weapons:**\n{weapon_list if weapon_list else 'None'}\n\n"
                f"🔒 **Locked Weapons:**\n{locked_list if locked_list else 'None'}\n\n"
                f"Use **/battle** to enter the battlefield!"
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏹 Join Community", url="t.me/+4a8z2vSLHVk3Yzdl")]]
            ),
        )
    except Exception as e:
        await callback_query.message.reply(f"⚠ Error: {e}")
