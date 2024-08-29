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

    def __init__(self) -> None:
        self.__create_runs_file()

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
    
    async def run_new_day(self, bot: PillReminderBot) -> None:
        data = self.__load_runs_file()
        if datetime.now().strftime('%Y-%m-%d') not in data['runs']:
            await bot.send_alert_new_day()
            data['runs'].append(datetime.now().strftime('%Y-%m-%d'))
        with open(self.RUNS_FILE, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":

    params = sys.argv
    params.pop(0)

    if len(params) > 0:
        if params[0] == "--new-day" or params[0] == "-n":
            load_dotenv(".env")
            print("Starting bot...")
            bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
            print("Bot started.")

            print("Starting reminder...")
            reminder = Reminder()
            print("Reminder started.")

            print("Running new day...")
            asyncio.run(reminder.run_new_day(bot))
            print("New day ran.")
            sys.exit()

        elif params[0] == "--reminder" or params[0] == "-r":
            load_dotenv(".env")
            print("Starting bot...")
            bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
            print("Bot started.")

            print("Starting reminder...")
            reminder = Reminder()
            print("Reminder started.")

            print("Sending reminder...")
            asyncio.run(bot.send_reminder())
            print("Reminder sent.")
            sys.exit()

        elif params[0] == "--reminder-loop" or params[0] == "-rl":
            load_dotenv(".env")
            print("Starting bot...")
            bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
            print("Bot started.")

            print("Starting reminder...")
            reminder = Reminder()
            print("Reminder started.")

            while True:
                print(f"Checking reminder at {datetime.now()}")
                if datetime.now().hour in reminder.HOURS:
                    print("Sending reminder...")
                    asyncio.run(bot.send_reminder())
                    print("Reminder sent.")
                    
                    print("Sleeping for 1 hour...")
                    time.sleep(60*60)
                else:
                    print("Sleeping for 1 minute...")
                    time.sleep(60)

        elif params[0] == "--help" or params[0] == "-h":
            print("Usage: python reminder.py [OPTION]")
            print("Options:")
            print("  -n, --new-day\t\t\tRun a new day")
            print("  -r, --reminder\t\t\tSend a reminder")
            print("  -rl, --reminder-loop\t\tSend a reminder every hour")
            print("  -h, --help\t\t\t\tShow this help message")
            sys.exit()


