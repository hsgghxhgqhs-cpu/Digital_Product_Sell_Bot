from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import SessionLocal
from models.user import get_or_create_user
import services.product_service as product_service
import services.payment_service as payment_service
import services.order_service as order_service
from utils.formatters import money, render_products_list, render_orders_list

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as db:
        db_user = get_or_create_user(db, update.effective_user.id, update.effective_user.username, update.effective_user.full_name)
        bal = payment_service.get_balance_cents(db, db_user.id)
    await update.message.reply_text(f"💳 আপনার ব্যালেন্স: {money(bal)}")

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as db:
        items = product_service.list_products_brief(db)
    if not items:
        await update.message.reply_text("📦 বর্তমানে কোনো পণ্য নেই।")
        return
    await update.message.reply_text(render_products_list(items), disable_web_page_preview=True)

async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as db:
        db_user = get_or_create_user(db, update.effective_user.id, update.effective_user.username, update.effective_user.full_name)
        orders = order_service.list_user_orders(db, db_user.id)
    if not orders:
        await update.message.reply_text("🧾 আপনার কোনো অর্ডার পাওয়া যায়নি।")
        return
    await update.message.reply_text(render_orders_list(orders))

def register_user_handlers(app: Application):
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("products", products))
    app.add_handler(CommandHandler("orders", orders))