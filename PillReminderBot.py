import telepot
import time
import urllib3
import json
from datetime import datetime
from RegisterManagement import RegisterManagement

class PillReminderBot:
    def __init__(self, token=None, pythonAnywhere=False):
        self.file_management = RegisterManagement()
        self.token = token

        if pythonAnywhere:
            proxy_url = "http://proxy.server:3128"
            telepot.api._pools = {
                'default': urllib3.ProxyManager(
                    proxy_url=proxy_url,
                    num_pools=3,
                    maxsize=10,
                    retries=False,
                    timeout=30
                )
            }
            telepot.api._onetime_pool_spec = (
                urllib3.ProxyManager,
                dict(
                    proxy_url=proxy_url,
                    num_pools=1,
                    maxsize=1,
                    retries=False,
                    timeout=30
                )
            )

        self.bot = telepot.Bot(token)
        
        self.bot.message_loop(self.__handle_message)
    
    def start(self):
        print("Bot is listening...")
        while True:
            time.sleep(10)
    
    def __keyboard(self):
        return {
            'keyboard': [
                ['Sim', 'Não'],
                ['Não é dia de tomar']
            ],
            'resize_keyboard': True,
            'one_time_keyboard': True
        }
    
    def __ask_question(self, chat_id):
        today = datetime.now().strftime('%Y-%m-%d')
        question = f"[{today}] Você já tomou a pílula hoje?"
        self.bot.sendMessage(chat_id, question, reply_markup=self.__keyboard())
    
    def __on_start_command(self, chat_id, user):
        self.bot.sendMessage(chat_id, "Olá! Eu sou um bot que vai te ajudar a lembrar de tomar a pílula diariamente.")
        if not self.file_management.user_is_registered(chat_id):
            self.file_management.register_user(
                chat_id, user['first_name'], user['id'], user['is_bot'],
                user.get('language_code', ''), user.get('username', '')
            )
            self.__send_help_message(chat_id)

        self.__ask_question(chat_id)
        if self.file_management.user_has_responded(chat_id):
            today_response = self.file_management.get_user_response(str(chat_id))
            self.bot.sendMessage(
                chat_id, f"Você já respondeu a pergunta de hoje com '{today_response}'.\nCaso queira alterar a resposta, basta responder a mensagem referente ao dia que deseja alterar."
            )
    
    def __send_help_message(self, chat_id):
        help_text = '\n'.join([
            "/start - Inicia o bot",
            "/help - Mostra esta mensagem de ajuda",
            "",
            "Todos os dias o bot vai perguntar se você tomou a pílula. Responda com 'Sim' ou 'Não' ou 'Não é dia de tomar'.",
            "Caso não responda ou responda 'Não', o bot vai enviar um lembrete para você tomar a pílula.",
            "",
            "Caso queira alterar a resposta, basta responder a mensagem do bot referente ao dia que deseja alterar. Para isso basta verificar a data da mensagem [YYYY-MM-DD].",
            "As mensagens que na qual deve responder são as '[YYYY-MM-DD] Você já tomou a pílula hoje?'."
        ])
        self.bot.sendMessage(chat_id, help_text)
    
    def __handle_message(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        user = msg['from']

        if command == '/start':
            self.__on_start_command(chat_id, user)
        elif command == "/help":
            self.__send_help_message(chat_id)
        elif command in ["Sim", "Não", "Não é dia de tomar"]:
            if 'reply_to_message' in msg:
                date = datetime.fromtimestamp(msg['reply_to_message']['date'])
                text_last_message = msg['reply_to_message']['text']
                if not "Você já tomou a pílula hoje?" in text_last_message:
                    return
                self.file_management.register_user_response(chat_id, command, date)    
                self.bot.sendMessage(chat_id, f"Obrigado por responder!\nA sua resposta para o dia {date.strftime('%Y-%m-%d')} foi registada.")
            else:
                self.file_management.register_user_response(chat_id, command)
                self.bot.sendMessage(chat_id, f"Obrigado por responder!\nA sua resposta para o dia {datetime.now().strftime('%Y-%m-%d')} foi registada.")
        
        print(f"Chat ID: {chat_id} | first_name: {user['first_name']} | command: {command}")

    def send_reminder(self):
        chats = self.file_management.get_all_chats_dont_responded() + self.file_management.get_all_chats_responded(date=datetime.now(), response="Não")
        for chat_id in chats:
            self.bot.sendMessage(chat_id, "Olá! Você ainda não registou se tomou a pílula hoje.")
        
    def send_alert_new_day(self):
        for chat_id in self.file_management.get_registered_chats():
            self.bot.sendMessage(chat_id, "Olá! Hoje é um novo dia. Não se esqueça de tomar a pílula.")
            self.__ask_question(chat_id)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv(".env")
    
    bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
    bot.start()
