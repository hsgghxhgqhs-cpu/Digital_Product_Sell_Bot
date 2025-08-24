from sqlalchemy.orm import Session
from models.user import User
from models.payment import Payment, PaymentStatus

def get_balance_cents(db: Session, user_id: int) -> int:
    u = db.query(User).filter(User.id == user_id).first()
    return u.balance_cents if u else 0

def adjust_balance_cents(db: Session, user_id: int, delta_cents: int) -> int | None:
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        return None
    u.balance_cents = max(0, (u.balance_cents or 0) + delta_cents)
    db.commit()
    return u.balance_cents

def create_deposit_request(db: Session, user_id: int, amount_cents: int, screenshot_file_id: str) -> Payment:
    p = Payment(user_id=user_id, amount_cents=amount_cents, status=PaymentStatus.PENDING, screenshot_file_id=screenshot_file_id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p