from PillReminderBot import PillReminderBot
import os
from dotenv import load_dotenv
import asyncio
    

if __name__ == "__main__":
    load_dotenv(".env")
    
    bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
    
    bot.start()