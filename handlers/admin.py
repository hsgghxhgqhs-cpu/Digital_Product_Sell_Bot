from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import OWNER_ID, ADMIN_IDS
from database import SessionLocal
from models.user import UserRole, get_or_create_user

def is_admin(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in ADMIN_IDS

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """অ্যাডমিন প্যানেল"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ আপনার অনুমতি নেই।")
        return

    text = (
        "🛠 অ্যাডমিন প্যানেল\n\n"
        "/add_product - নতুন পণ্য যোগ করুন\n"
        "/set_stock - পণ্যে স্টক যোগ করুন\n"
    )
    await update.message.reply_text(text)

def register_admin_handlers(app: Application):
    app.add_handler(CommandHandler("admin", admin_panel))