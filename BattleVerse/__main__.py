import os
from pyrogram import Client
from BatlleVerse.__init__ import bot

# Main Program
if __name__ == "__main__":
    
    bot.run()
    with bot:
       bot.send_message(chat_id=-1002393279895,
          text=f"**BattleVerse has started [!](https://files.catbox.moe/s911b7.jpg)**")
