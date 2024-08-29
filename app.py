from PillReminderBot import PillReminderBot
import os
from dotenv import load_dotenv
from Reminder import Reminder
import asyncio
from datetime import datetime
import time

async def main():
    load_dotenv(".env")
    
    bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"), True)
    reminder = Reminder(bot)

    tasks = [
        asyncio.create_task(reminder.run_reminder_loop()),
        asyncio.create_task(reminder.run_new_day_loop()),
        asyncio.create_task(bot.start())
    ]

    await asyncio.gather(*tasks) 

if __name__ == "__main__":
    load_dotenv(".env")
    
    asyncio.run(main())