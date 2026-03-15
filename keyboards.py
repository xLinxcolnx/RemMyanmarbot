# keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def date_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📅 Today", callback_data="today"),
            InlineKeyboardButton("📅 Tomorrow", callback_data="tomorrow")
        ],
        [
            InlineKeyboardButton("📅 Pick a date", callback_data="pick_date")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def hour_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("12 AM", callback_data="00"),
            InlineKeyboardButton("1 AM", callback_data="01"),
            InlineKeyboardButton("2 AM", callback_data="02"),
            InlineKeyboardButton("3 AM", callback_data="03"),
        ],
        [
            InlineKeyboardButton("4 AM", callback_data="04"),
            InlineKeyboardButton("5 AM", callback_data="05"),
            InlineKeyboardButton("6 AM", callback_data="06"),
            InlineKeyboardButton("7 AM", callback_data="07"),
        ],
        [
            InlineKeyboardButton("8 AM", callback_data="08"),
            InlineKeyboardButton("9 AM", callback_data="09"),
            InlineKeyboardButton("10 AM", callback_data="10"),
            InlineKeyboardButton("11 AM", callback_data="11"),
        ],
        [
            InlineKeyboardButton("12 PM", callback_data="12"),
            InlineKeyboardButton("1 PM", callback_data="13"),
            InlineKeyboardButton("2 PM", callback_data="14"),
            InlineKeyboardButton("3 PM", callback_data="15"),
        ],
        [
            InlineKeyboardButton("4 PM", callback_data="16"),
            InlineKeyboardButton("5 PM", callback_data="17"),
            InlineKeyboardButton("6 PM", callback_data="18"),
            InlineKeyboardButton("7 PM", callback_data="19"),
        ],
        [
            InlineKeyboardButton("8 PM", callback_data="20"),
            InlineKeyboardButton("9 PM", callback_data="21"),
            InlineKeyboardButton("10 PM", callback_data="22"),
            InlineKeyboardButton("11 PM", callback_data="23"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def minute_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(":00", callback_data="00"),
            InlineKeyboardButton(":05", callback_data="05"),
            InlineKeyboardButton(":10", callback_data="10"),
            InlineKeyboardButton(":15", callback_data="15"),
        ],
        [
            InlineKeyboardButton(":20", callback_data="20"),
            InlineKeyboardButton(":25", callback_data="25"),
            InlineKeyboardButton(":30", callback_data="30"),
            InlineKeyboardButton(":35", callback_data="35"),
        ],
        [
            InlineKeyboardButton(":40", callback_data="40"),
            InlineKeyboardButton(":45", callback_data="45"),
            InlineKeyboardButton(":50", callback_data="50"),
            InlineKeyboardButton(":55", callback_data="55"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def morning_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("5 AM", callback_data="morning_05:00"),
            InlineKeyboardButton("6 AM", callback_data="morning_06:00"),
            InlineKeyboardButton("7 AM", callback_data="morning_07:00"),
        ],
        [
            InlineKeyboardButton("8 AM", callback_data="morning_08:00"),
            InlineKeyboardButton("9 AM", callback_data="morning_09:00"),
            InlineKeyboardButton("10 AM", callback_data="morning_10:00"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)