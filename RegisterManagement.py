from datetime import datetime
import json
from Logger import Logger

"""
{
    "chat_id": {
        "info": {
            "id": id,
            "first_name": first_name,
            "username": username,
            "language_code": language_code,
            "is_bot": is_bot
        },
        "responses": {
            "YYYY-MM-DD": {
                "response": response,
                "time": "YYYY-MM-DD HH:MM:SS" # Time where user responded the message
            }
        }
    }
}
"""

class RegisterManagement:
    def __init__(self, data_file = 'responses.json'):
        self.logger = Logger('RegisterManagement').get_logger()
        self.logger.info("RegisterManagement started.")
        self.data_file = data_file
        self.__data = self.__load_data()
        self.logger.info("Data loaded.")
        self.logger.info(f"Data: {self.__data}")

    def __save_data(self):
        self.logger.info("Saving data...")
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, indent=4)
        self.logger.info("Data saved.")

    def __load_data(self):
        self.logger.info("Loading data...")
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.logger.info("Data loaded.")
                return json.load(f)
        except FileNotFoundError:
            self.logger.info("Data file not found.")
            return {}
    
    def user_is_registered(self, chat_id) -> bool:
        return self.__data.get(str(chat_id)) is not None

    def register_user(self, chat_id: str, first_name=None, id=None, is_bot=None, language_code=None, username=None):
        self.logger.info(f"Registering user chat_id: {chat_id}")
        if self.user_is_registered(chat_id):
            self.logger.error(f"User chat_id: {chat_id} already registered.")
            raise Exception("User already registered.")
        self.__data[str(chat_id)] = {}
        self.__data[str(chat_id)]["info"] = {
            "id": id,
            "first_name": first_name,
            "username": username,
            "language_code": language_code,
            "is_bot": is_bot,
        }
        self.__data[str(chat_id)]["responses"] = {}
        self.__save_data()
        self.logger.info(f"User chat_id: {chat_id} registered.")
    
    def register_user_response(self, chat_id: str, response: str, date: datetime = datetime.now()):
        self.logger.info(f"Registering response from chat_id: {chat_id} | response: {response}")
        self.__data[str(chat_id)]["responses"][date.strftime('%Y-%m-%d')] = {
            "response": response,
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.__save_data()
        self.logger.info(f"Response from chat_id: {chat_id} registered.")

    def get_user_responses(self):
        return self.__data
    
    def get_user_response(self, chat_id, date: datetime = datetime.now()) -> str|None:
        self.logger.info(f"Getting response from chat_id: {chat_id}")
        if not self.user_is_registered(chat_id):
            self.logger.error(f"User chat_id: {chat_id} not registered.")
            raise Exception("User is not registered.")
        
        if self.__data.get(str(chat_id))["responses"].get(date.strftime('%Y-%m-%d')) is None:
            self.logger.error(f"User chat_id: {chat_id} has not responded.")
            return None
        self.logger.info(f"Response from chat_id: {chat_id} is {self.__data.get(str(chat_id))['responses'].get(date.strftime('%Y-%m-%d'))['response']}")
        return self.__data.get(str(chat_id))["responses"].get(date.strftime('%Y-%m-%d'))["response"]

    def user_has_responded(self, chat_id, date: datetime = datetime.now()):
        if not self.user_is_registered(chat_id):
            raise Exception("User is not registered.")
        
        return self.__data.get(str(chat_id))["responses"].get(date.strftime('%Y-%m-%d')) is not None
    
    def get_registered_chats(self):
        return self.__data.keys()
    
    def get_all_chats_dont_responded(self, date: datetime = datetime.now()):
        self.logger.info(f"Getting all chats that didn't respond at {date}")
        date = date.strftime('%Y-%m-%d')
        users_not_responded = []
        for user in self.__data:
            if self.__data[user]['responses'].get(date) is None:
                users_not_responded.append(user)
        self.logger.info(f"Users that didn't respond: {users_not_responded}")
        return users_not_responded
    
    
    def get_all_chats_responded(self, date: datetime = datetime.now(), response: str|None = None):
        self.logger.info(f"Getting all chats that responded at {date}")
        date = date.strftime('%Y-%m-%d')
        responded = []
        for user in self.__data:
            if self.__data[user]['responses'].get(date) is not None:
                if response is None or self.__data[user]['responses'][date]['response'] == response:
                    responded.append(user)
        self.logger.info(f"Users that responded: {responded}")
        return responded
    