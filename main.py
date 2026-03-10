from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
from telegram.ext import ConversationHandler
from dotenv import load_dotenv
from timezones import TIMEZONE_MAP #importing from timezone.py
import pytz
import json
import os


load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = "@rem_remainder_bot"



class ReminderDB:
    def __init__(self, filename="reminders.json"):
        self.filename=filename
        self.reminders=self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}
    def save(self):
        with open(self.filename,"w")as f:
            json.dump(self.reminders, f)

    def add_reminder(self, user_id, class_name, datetime_str): #create user id
        if user_id not in (self.reminders):
            self.reminders[user_id]=[]
        self.reminders[user_id].append({
            "class_name": class_name,
            "datetime": datetime_str,
        })
        self.save()

    def get_reminder(self, user_id):
        return self.reminders.get(user_id, [])
    
    def delete_reminder(self, user_id, index):
        if user_id in self.reminders:
            self.reminders[user_id].pop(index)
            self.save()
    def set_timezone(self, user_id, timezone_str):
        if user_id not in self.reminders:
            self.reminders[user_id]={
                "timezone":timezone_str,
                "reminders": []
            }
        else:
            self.reminders[user_id]["timezone"]=timezone_str
        self.save()
# commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pls type something so i can respond")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Rem")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

async def receive_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id= str(update.message.chat.id)
    user_input=update.message.text.lower().strip()

    if user_input in TIMEZONE_MAP:
        timezone= TIMEZONE_MAP[(user_input)]
        db.set_timezone(user_id, timezone)
        await update.message.reply_text(
            f"✅ Timezone set to {timezone}!\n\n"
            "📌 /set — Set a schedule reminder\n"
            "📋 /view — View your schedules\n"
            "/alarm-set a alarm(you can setup the alarm upto 3hours)"
            "🗑️ /delete — Delete a reminder"
        )
# responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return "hey there"
    if "how are you" in processed:
        return "Im good you"
    return "i do not understand"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return  # DON'T respond in groups unless mentioned
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands 
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors 
    app.add_error_handler(error)
    
    print("Polling...") 
    app.run_polling(poll_interval=3)