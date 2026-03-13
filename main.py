from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
from telegram.ext import ConversationHandler
from dotenv import load_dotenv
from timezones import TIMEZONE_MAP #importing from timezone.py
from keyboards import date_keyboard, hour_keyboard, minute_keyboard
from telegram.ext import CallbackQueryHandler
import pytz
import json
import os


load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = "@rem_remainder_bot" #bot name
WAITING_FOR_TIMEZONE: Final = 0
ASKING_DATE=1
ASKING_TIME=2
ASKING_MINUTES=3
ASKING_DESCRIPTION=4

class RemDB:
    def __init__(self, filename="rems.json"): #loading
        self.filename=filename
        self.rems=self.load()

    def load(self): 
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}
    def save(self):
        with open(self.filename,"w")as f:
            json.dump(self.rems, f)

    def add_rem(self, user_id, class_name, datetime_str): #create user id
        if user_id not in (self.rems):
            self.rems[user_id]={
                "timezone": "",
                "rems": [],
            }
        self.rems[user_id]["rems"].append({
            "class_name": class_name,
            "datetime": datetime_str,
        })
        self.save()

    def get_rem(self, user_id):
        if user_id not in self.rems:
            return []
        return self.rems[user_id].get("rems", [])
    
    def delete_rem(self, user_id, index):
        if user_id in self.rems:
            self.rems[user_id]["rems"].pop(index)
            self.save()

    def set_timezone(self, user_id, timezone_str): #saving user timezone
        if user_id not in self.rems:
            self.rems[user_id]={
                "timezone":timezone_str,
                "rems": []
            }
        else:
            self.rems[user_id]["timezone"]=timezone_str
        self.save()


# commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pls type something so i can respond")


#/start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am Rem — your personal rem!\n\n"
        "First, tell me where are you from? So that I can set your timezone!\n"
        "Type your country: \n"
        "🌍 Myanmar, Thailand, Singapore, Malaysia, Canada"
    )
    return WAITING_FOR_TIMEZONE
        
async def receive_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id= str(update.message.chat.id)
    user_input=update.message.text.lower().strip()

    if user_input in TIMEZONE_MAP:
        timezone= TIMEZONE_MAP[(user_input)]
        db.set_timezone(user_id, timezone)
        await update.message.reply_text(
            f"✅ Timezone set to {timezone}!\n\n"
            "/help — Get help on how to use the bot\n"
            "📌 /set — Set a schedule rem\n"
            "📋 /view — View your schedules\n"
            "/alarm — Set an alarm (you can set the alarm up to 3 hours in advance)\n"
            "🗑️ /delete — Delete a rem"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ Sorry, I don't recognize that location or we haven't launch for your lcoation yet.\n"
            "🌍 Myanmar, Thailand, Singapore, Malaysia, Canada"
        )
        return WAITING_FOR_TIMEZONE
      
async def set_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 When is your class?",
        reply_markup=date_keyboard()  #from keyboards.py
    )
    return ASKING_DATE

async def date_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query= update.callback_query
    await query.answer()

    if query.data=="today":
        date = datetime.now().strftime("%Y-%m-%d")
    elif query.data=="tomorrow":
        date = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
    elif query.data=="pick_date":
        await query.edit_message_text("📅 Type your date:\nFormat: YYYY-MM-DD")
        return ASKING_DATE

    context.user_data["date"] = date
    await query.edit_message_text("⏰ Select hour:", reply_markup=hour_keyboard())
    return ASKING_TIME

async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input=update.message.text.strip()
    try:
        datetime.strptime(user_input, "%Y-%m-%d")
        context.user_data["date"]=user_input
        await update.message.reply_text(
            "⏰ Select hour:",
            reply_markup=hour_keyboard()
        )
        return ASKING_TIME
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid date! Please try again.\n"
            "Format: YYYY-MM-DD\n"
            "Example: 2026-03-22")
        return ASKING_DATE


async def hour_callback(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()

    context.user_data["hour"]=query.data

    await query.edit_message_text(
        "⏰ Select minutes:",
        reply_markup=minute_keyboard()
    )
    return ASKING_MINUTES

async def minute_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["minutes"] = query.data  # save minutes

    await query.edit_message_text(
        "📝 Add a description:\n"
    )
    return ASKING_DESCRIPTION 

async def receive_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat.id)
    description = update.message.text

    # build the full datetime string from saved data
    date = context.user_data["date"]
    hour = context.user_data["hour"]
    minutes = context.user_data["minutes"]
    datetime_str = f"{date} {hour}:{minutes}"

    user_tz_str=db.rems[user_id]["timezone"]
    user_tz= pytz.timezone(user_tz_str)

    now=datetime.now(user_tz)
    rem_time=user_tz.localize(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M"))

    if rem_time<now:
        await update.message.reply_text(
            "The time has already passed\n"
        )
        return ConversationHandler.END
    

    # save to database
    db.add_rem(user_id, description, datetime_str)

    await update.message.reply_text(
        f"✅ rem saved!\n\n"
        f"📚 {description}\n"
        f"📅 {datetime_str}\n\n"
        f"I will remind you:\n"
        f"⏰ 10 min before\n"
        f"🔔 At {hour}:{minutes}"
    )
    return ConversationHandler.END  # end the conversation

async def view_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id=str(update.message.chat.id)

    user_tz=pytz.timezone(db.rems[user_id]["timezone"])
    today=datetime.now(user_tz).strftime("%Y-%m-%d")
    now=datetime.now(user_tz)

    rems= db.get_rem(user_id)
    active_rems=[]
    for rem in rems:
        rem_time=user_tz.localize(datetime.strptime(rem["datetime"], "%Y-%m-%d %H:%M"))
        if rem_time>now:
            active_rems.append(rem)
    
    db.rems[user_id]["rems"]=active_rems
    db.save()

    today_rems=[r for r in active_rems if r["datetime"].startswith(today)]

    if today_rems:
        message="\n📅 *Today's Schedule:*\n"
        for rem in today_rems:
            time=rem["datetime"].split(" ")[1]
            message=message+f"🕐 {time} — {rem['class_name']}\n"
    else:
        message="\n📭 No schedule for today!"

    upcoming=[r for r in active_rems if not r["datetime"].startswith(today)]

    if upcoming:
        message= message+ "\n📋 *Upcoming:*\n"
        for rem in upcoming:
            message=message+f"📌{rem['datetime']}-{rem['class_name']}"
    else:
        message=message+"\n📭 No upcoming schedules!"

    await update.message.reply_text(message, parse_mode="Markdown")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
 
db= RemDB()
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
        CommandHandler("start", start_command),
        CommandHandler("set", set_command)
        ],
        states={ 
            WAITING_FOR_TIMEZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_timezone)],
            ASKING_DATE: [CallbackQueryHandler(date_callback), MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)],          
            ASKING_TIME: [CallbackQueryHandler(hour_callback)],         
            ASKING_MINUTES: [CallbackQueryHandler(minute_callback)],   
            ASKING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_description)]
        },
        fallbacks=[],
        per_message=False
    )

    app.add_handler(conv_handler)
    # Commands
    app.add_handler(CommandHandler("view", view_command)) 
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    print("Polling...") 
    app.add_error_handler(error) 
    app.run_polling(poll_interval=3)
