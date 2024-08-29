from PillReminderBot import PillReminderBot
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import time
import asyncio

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

    while True:
        print(f"Checking reminder at {datetime.now()}")
        if datetime.now().hour in reminder.HOURS:
            print("Sending reminder...")
            asyncio.run(bot.send_reminder())
            print("Reminder sent.")
            
            print("Sleeping for 1 hour...")
            time.sleep(60*60) # 1 hora
            print("Waking up...")
        
        print("Sleeping for 1 minute...")
        time.sleep(60) # 1 minuto
        print("Waking up to check again in 1 minute...")


