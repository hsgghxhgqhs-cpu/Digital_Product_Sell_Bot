import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, OWNER_ID, ADMIN_GROUP_ID, PAYMENT_NUMBERS
from database import init_db, SessionLocal
from models.user import get_or_create_user, UserRole
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from handlers.payment import register_payment_handlers
from handlers.order import register_order_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    with SessionLocal() as db:
        db_user = get_or_create_user(db, user.id, user.username, user.full_name)
        # Owner bootstrap (optional)
        if user.id == OWNER_ID and db_user.role != UserRole.OWNER:
            db_user.role = UserRole.OWNER
            db.commit()

    text = (
        "👋 স্বাগতম!\n\n"
        "আমি একটি ডিজিটাল পণ্য বিক্রির বট।\n"
        "এখানে আপনি ব্যালেন্স রিচার্জ করে বিভিন্ন পণ্য কিনতে পারবেন।\n\n"
        "🧭 কমান্ডসমূহ:\n"
        "/balance - আপনার ব্যালেন্স দেখুন\n"
        "/products - উপলব্ধ পণ্যসমূহ\n"
        "/buy <product_id> <qty> - পণ্য কিনুন\n"
        "/deposit - ডিপোজিট করে ব্যালেন্স যোগ করুন\n"
        "/orders - আপনার অর্ডার হিস্টরি\n"
        "/admin - অ্যাডমিন প্যানেল (শুধু এডমিনদের জন্য)\n"
        "\n❓ সাহায্যের জন্য: /help"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ সাহায্য:\n"
        "- আগে /deposit করে ব্যালেন্স যোগ করুন।\n"
        "- তারপর /products দেখে /buy দিয়ে পণ্য কিনুন।\n"
        "- কেনার পর লিংক + টেক্সট সাথে সাথেই পাবেন।\n"
    )
    await update.message.reply_text(text)


def main():
    # DB init
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Core
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Register handlers
    register_user_handlers(app)  # /balance, /products, /orders
    register_order_handlers(app)  # /buy
    register_payment_handlers(app, admin_group_id=ADMIN_GROUP_ID, payment_numbers=PAYMENT_NUMBERS)  # /deposit + screenshot
    register_admin_handlers(app)  # /admin

    logger.info("Bot is starting...")
    app.run_polling(close_loop=False)


if name == "main":
    main()