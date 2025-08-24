from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    OWNER = "owner"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    balance_cents = Column(Integer, default=0)

def get_or_create_user(db, tg_id: int, username: str, full_name: str) -> User:
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        user = User(tg_id=tg_id, username=username, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.username = username
        user.full_name = full_name
        db.commit()
    return user