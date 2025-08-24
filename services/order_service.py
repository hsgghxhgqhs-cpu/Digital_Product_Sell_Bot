from sqlalchemy.orm import Session
from models.product import Product, StockItem
from models.order import Order, OrderItem
from services.payment_service import get_balance_cents, adjust_balance_cents

def get_product_by_id_safe(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

def list_user_orders(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).limit(20).all()

def buy_product_by_id(db: Session, user_id: int, product_id: int, qty: int):
    product = db.query(Product).filter(Product.id == product_id, Product.active.is_(True)).first()
    if not product:
        return False, "❌ পণ্য অনুপলব্ধ।"

    available = db.query(StockItem).filter(StockItem.product_id == product_id, StockItem.is_sold.is_(False)).order_by(StockItem.id.asc()).limit(qty).all()
    if len(available) < qty:
        return False, "⚠️ স্টক পর্যাপ্ত নেই।"

    total_cents = product.price_cents * qty
    bal = get_balance_cents(db, user_id)
    if bal < total_cents:
        return False, "💳 ব্যালেন্স অপর্যাপ্ত। প্রথমে /deposit করে ব্যালেন্স যোগ করুন।"

    adjust_balance_cents(db, user_id, -total_cents)

    order = Order(user_id=user_id, product_id=product_id, quantity=qty, total_cents=total_cents)
    db.add(order)
    db.commit()
    db.refresh(order)

    items_for_user = []
    for it in available:
        it.is_sold = True
        it.sold_to_user_id = user_id
        it.sold_order_id = order.id
        items_for_user.append({"link": it.link, "text": it.text})
    db.commit()

    for it in available:
        db.add(OrderItem(order_id=order.id, link=it.link, text=it.text))
    db.commit()

    return True, (order, items_for_user)