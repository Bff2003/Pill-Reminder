from PillReminderBot import PillReminderBot
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time
import asyncio
import sys
from Logger import Logger

"""
{
    "runs" ["YYYY-MM-DD", "YYYY-MM-DD"]
}
"""

class Reminder:
    RUNS_FILE = 'runs.json'
    HOURS = [9, 13, 16, 18, 22]

    def __init__(self, bot: PillReminderBot):
        self.logger = Logger("Reminder").get_logger()
        self.logger.info("Reminder started.")
        self.__create_runs_file()
        self.bot = bot

    def __create_runs_file(self) -> None:
        """
        {
            "runs" ["YYYY-MM-DD", "YYYY-MM-DD"]
        }
        """
        self.logger.info("Creating runs file...")
        if not os.path.exists(self.RUNS_FILE):
            self.logger.info("Runs file not found.")
            with open(self.RUNS_FILE, 'w') as f:
                data = {
                    "runs": []
                }
                json.dump(data, f, indent=4)
            self.logger.info("Runs file created.")
        else:  
            self.logger.info("Runs file found.")
            self.__load_runs_file()
            self.logger.info("Runs file loaded.")
    
    def __load_runs_file(self) -> dict:
        self.logger.info("Loading runs file...")
        with open(self.RUNS_FILE, 'r') as f:
            return json.load(f)
    
    async def run_new_day(self) -> None:
        self.logger.info("Running new day...")
        data = self.__load_runs_file()
        if datetime.now().strftime('%Y-%m-%d') not in data['runs']:
            self.logger.info("Sending alert new day...")
            await self.bot.send_alert_new_day()
            self.logger.info("Alert new day sent.")
            data['runs'].append(datetime.now().strftime('%Y-%m-%d'))
        
        self.logger.info("Saving runs file...")
        with open(self.RUNS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        self.logger.info("Runs file saved.")

    async def run_new_day_loop(self) -> None:
        self.logger.info("Running new day loop...")
        hours = [9]
        self.logger.info("New day loop started.")
        while True:
            if datetime.now().hour in hours:
                self.logger.info("It's time to run new day.")
                await self.run_new_day()
                self.logger.info("New day ran.")
                
                self.logger.info("Sleeping for 20 hours...")
                time.sleep(60*60*20)
                self.logger.info("Waking up.")
            else:
                self.logger.info("Sleeping for 15 minutes...")
                time.sleep(60*15)
                self.logger.info("Waking up.")

    async def run_reminder_loop(self) -> None:
        self.logger.info("Running reminder loop...")
        while True:
            if datetime.now().hour in self.HOURS:
                self.logger.info("It's time to send reminder.")
                await self.bot.send_reminder()
                self.logger.info("Reminder sent.")
                
                self.logger.info("Sleeping for 1 hour...")
                time.sleep(60*60)
                self.logger.info("Waking up.")
            else:
                self.logger.info("Sleeping for 15 minutes...")
                time.sleep(60)
                self.logger.info("Waking up.")

if __name__ == "__main__":
    params = sys.argv
    params.pop(0)

    load_dotenv(".env")
    if len(params) > 0:
        if params[0] == "--help" or params[0] == "-h":
            print("Usage: python reminder.py [OPTION]")
            print("Options:")
            print("  -n, --new-day\t\t\tRun a new day")
            print("  -r, --reminder\t\t\tSend a reminder")
            print("  -rl, --reminder-loop\t\tSend a reminder every hour")
            print("  -h, --help\t\t\t\tShow this help message")
            sys.exit()

        elif params[0] == "--new-day" or params[0] == "-n":
            bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
            reminder = Reminder(bot)
            asyncio.run(reminder.run_new_day())
            sys.exit()

        elif params[0] == "--reminder" or params[0] == "-r":
            bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
            reminder = Reminder()
            asyncio.run(bot.send_reminder())
            sys.exit()

        elif params[0] == "--reminder-loop" or params[0] == "-rl":
            bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
            reminder = Reminder(bot)
            asyncio.run(reminder.run_reminder_loop())