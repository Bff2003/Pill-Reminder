from PillReminderBot import PillReminderBot
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time
import asyncio
import sys

"""
{
    "runs" ["YYYY-MM-DD", "YYYY-MM-DD"]
}
"""

class Reminder:
    RUNS_FILE = 'runs.json'
    HOURS = [9, 13, 16, 18, 22]

    def __init__(self, bot: PillReminderBot):
        self.__create_runs_file()
        self.bot = bot

    def __create_runs_file(self) -> None:
        """
        {
            "runs" ["YYYY-MM-DD", "YYYY-MM-DD"]
        }
        """
        if not os.path.exists(self.RUNS_FILE):
            with open(self.RUNS_FILE, 'w') as f:
                data = {
                    "runs": []
                }
                json.dump(data, f, indent=4)
        else:  
            self.__load_runs_file()
    
    def __load_runs_file(self) -> dict:
        with open(self.RUNS_FILE, 'r') as f:
            return json.load(f)
    
    async def run_new_day(self) -> None:
        data = self.__load_runs_file()
        if datetime.now().strftime('%Y-%m-%d') not in data['runs']:
            await self.bot.send_alert_new_day()
            data['runs'].append(datetime.now().strftime('%Y-%m-%d'))
        with open(self.RUNS_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    async def run_new_day_loop(self) -> None:
        hours = [9]
        while True:
            if datetime.now().hour in hours:
                print("Running new day...")
                await self.run_new_day()
                print("New day ran.")
                
                print("Sleeping for 20 hour...")
                time.sleep(60*60*20)
            else:
                print("Sleeping for 15 minute...")
                time.sleep(60*15)

    async def run_reminder_loop(self) -> None:
        while True:
            print(f"Checking reminder at {datetime.now()}")
            if datetime.now().hour in self.HOURS:
                print("Sending reminder...")
                await self.bot.send_reminder()
                print("Reminder sent.")
                
                print("Sleeping for 1 hour...")
                time.sleep(60*60)
            else:
                print("Sleeping for 1 minute...")
                time.sleep(60)

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