from PillReminderBot import PillReminderBot
import os
from dotenv import load_dotenv
from Reminder import Reminder
import asyncio
from datetime import datetime
import time
from Logger import Logger

async def main():
    logger = Logger("main").get_logger()
    load_dotenv(".env")
    
    logger.info("Starting main...")

    logger.info("Creating bot...")
    bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"), True)
    logger.info("Bot created.")

    logger.info("Creating reminder...")
    reminder = Reminder(bot)
    logger.info("Reminder created.")

    logger.info("Starting tasks...")
    tasks = [
        asyncio.create_task(await reminder.run_reminder_loop()),
        asyncio.create_task(await reminder.run_new_day_loop()),
        asyncio.create_task(bot.start())
    ]
    logger.info("Tasks started.")

    logger.info("Waiting for tasks to finish...")
    await asyncio.gather(*tasks) 
    logger.info("Tasks finished.")

if __name__ == "__main__":
    load_dotenv(".env")
    
    asyncio.run(main())