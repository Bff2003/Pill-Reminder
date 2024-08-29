import telepot
import time
import urllib3
import json
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from RegisterManagement import RegisterManagement

class PillReminderBot:
    def __init__(self, token=None):
        self.file_management = RegisterManagement()
        self.app = ApplicationBuilder().token(token).build()
        self.bot = self.app.bot

        self.app.add_handler(MessageHandler(callback=self.__handle_message, filters=None))
    
    def start(self):
        self.app.run_polling()

    def __keyboard(self):
        return ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Sim"), KeyboardButton(text="Não")],
            [KeyboardButton(text="Não é dia de tomar")]
        ], resize_keyboard=True, one_time_keyboard=True)
    
    async def __ask_question(self, update=None, chat_id=None):
        if chat_id:
            await self.bot.sendMessage(chat_id, f"[{datetime.now().strftime('%Y-%m-%d')}] Você já tomou a pílula hoje?", reply_markup=self.__keyboard())
        elif update:
            await update.message.reply_text(f"[{datetime.now().strftime('%Y-%m-%d')}] Você já tomou a pílula hoje?", reply_markup=self.__keyboard())
        else:
            raise Exception("No chat_id or update provided.")
        
    async def __handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        print('Handling message...')
        print(update)
        chat_id = update.message.chat_id
        command = update.message.text

        if command == '/start':
            if not self.file_management.user_is_registered(chat_id):
                self.file_management.register_user(chat_id, update.message.from_user.first_name, update.message.from_user.id, update.message.from_user.is_bot, update.message.from_user.language_code, update.message.from_user.username)
            print('Starting...')
            await update.message.reply_text("Olá! Eu sou um bot que vai te ajudar a lembrar de tomar a pílula diariamente.")
            await self.__ask_question(update=update)
            if self.file_management.user_has_responded(chat_id):
                await update.message.reply_text(f"Você já respondeu a pergunta de hoje com '{self.file_management.get_user_responses()[str(chat_id)][datetime.now().strftime('%Y-%m-%d')]['response']}'.\nCaso queira alterar a resposta, basta responder a mensagem referente ao dia que deseja alterar.")

        elif command == "/help":
            await update.message.reply_text('\n'.join([
                "/start - Inicia o bot",
                "/help - Mostra esta mensagem de ajuda",
                "",
                "Todos os dias o bot vai perguntar se você tomou a pílula. Responda com 'Sim' ou 'Não' ou 'Não é dia de tomar'.",
                "Caso não responda ou responda 'Não', o bot vai enviar um lembrete para você tomar a pílula.",
                "",
                "Caso queira alterar a resposta, basta responder a mensagem do bot referente ao dia que deseja alterar. Para isso basta verificar a data da mensagem [YYYY-MM-DD].",
                "As mensagens que na qual deve responder são as '[YYYY-MM-DD] Você já tomou a pílula hoje?'."
            ]))

        if command in ["Sim", "Não", "Não é dia de tomar"]:
            if update.message.reply_to_message:
                date = update.message.reply_to_message.date
                text_last_message = update.message.reply_to_message.text
                if not "Você já tomou a pílula hoje?" in text_last_message:
                    return
                self.file_management.register_user_response(chat_id, command, date)    
                await update.message.reply_text(f"Obrigado por responder!\nA sua resposta para o dia {date.strftime('%Y-%m-%d')} foi registada.")
            else:
                self.file_management.register_user_response(chat_id, command)
                await update.message.reply_text(f"Obrigado por responder!\nA sua resposta para o dia {datetime.now().strftime('%Y-%m-%d')} foi registada.")

        print('Got command: %s' % command)

    async def send_reminder(self):
        chats = self.file_management.get_all_chats_dont_responded() + self.file_management.get_all_chats_responded(date=datetime.now(), response="Não")
        for chat_id in chats:
            await self.bot.sendMessage(chat_id, "Olá! Você ainda não registou se tomou a pílula hoje.")
        
    async def send_alert_new_day(self):
        for chat_id in self.file_management.get_registered_chats():
            await self.bot.sendMessage(chat_id, "Olá! Hoje é um novo dia. Não se esqueça de tomar a pílula.")
            await self.__ask_question(chat_id=chat_id)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv(".env")
    
    bot = PillReminderBot(os.getenv("TELEGRAM_TOKEN"))
    bot.start()