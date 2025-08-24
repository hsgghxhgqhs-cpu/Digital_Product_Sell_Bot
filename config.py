import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "-1001234567890"))

PAYMENT_NUMBERS = {
    "bKash": os.getenv("BKASH_NUMBER", "01XXXXXXXXX"),
    "Nagad": os.getenv("NAGAD_NUMBER", "01XXXXXXXXX"),
    "Rocket": os.getenv("ROCKET_NUMBER", "01XXXXXXXXX"),
}

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bot.db")