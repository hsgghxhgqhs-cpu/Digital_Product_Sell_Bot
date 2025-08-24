from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import SessionLocal
from models.user import get_or_create_user
import services.order_service as order_service

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """পণ্য কেনা"""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ ব্যবহার: /buy <product_id> <qty>")
        return

    product_id = int(args[0])
    qty = int(args[1])
    user = update.effective_user

    with SessionLocal() as db:
        db_user = get_or_create_user(db, user.id, user.username, user.full_name)
        ok, result = order_service.buy_product_by_id(db, db_user.id, product_id, qty)

    if not ok:
        await update.message.reply_text(result)
        return

    order, items = result
    msg = f"✅ অর্ডার #{order.id} সফল হয়েছে!\n\n"
    for i, it in enumerate(items, 1):
        msg += f"{i}. {it['link']} | {it['text']}\n"
    await update.message.reply_text(msg)

def register_order_handlers(app: Application):
    app.add_handler(CommandHandler("buy", buy))