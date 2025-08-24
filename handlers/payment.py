from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import ADMIN_GROUP_ID, PAYMENT_NUMBERS
from database import SessionLocal
from models.user import get_or_create_user
import services.payment_service as payment_service

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ডিপোজিট করার নির্দেশনা দেখাবে"""
    text = "💳 আপনার ডিপোজিট করার নাম্বারগুলো:\n"
    for k, v in PAYMENT_NUMBERS.items():
        text += f"- {k}: {v}\n"
    text += "\nদয়া করে টাকা পাঠানোর পর স্ক্রিনশট পাঠান।"
    await update.message.reply_text(text)

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """স্ক্রিনশট হ্যান্ডেল করবে এবং এডমিন গ্রুপে ফরোয়ার্ড করবে"""
    if not update.message.photo:
        return
    user = update.effective_user
    with SessionLocal() as db:
        db_user = get_or_create_user(db, user.id, user.username, user.full_name)
        file_id = update.message.photo[-1].file_id
        payment = payment_service.create_deposit_request(db, db_user.id, 0, file_id)  # amount পরে এডমিন ম্যানুয়ালি সেট করবে

    caption = f"💰 নতুন ডিপোজিট অনুরোধ\n\n👤 User: @{user.username}\n🆔 ID: {user.id}\n\n📸 Screenshot নিচে:"
    await context.bot.send_photo(chat_id=ADMIN_GROUP_ID, photo=update.message.photo[-1].file_id, caption=caption)

    await update.message.reply_text("✅ আপনার ডিপোজিট অনুরোধ এডমিনের কাছে পাঠানো হয়েছে।")

def register_payment_handlers(app: Application, admin_group_id: int, payment_numbers: dict):
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))