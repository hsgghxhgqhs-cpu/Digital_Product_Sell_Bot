def money(cents: int) -> str:
    return f"{cents/100:.2f}৳"

def render_products_list(products) -> str:
    text = "📦 উপলব্ধ পণ্যসমূহ:\n\n"
    for p in products:
        text += f"ID: {p.id} | {p.name} - {money(p.price_cents)}\n"
    return text

def render_orders_list(orders) -> str:
    text = "🧾 আপনার অর্ডারসমূহ:\n\n"
    for o in orders:
        text += f"Order {o.id}: {o.quantity} pcs - {money(o.total_cents)}\n"
    return text