from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import models.user
    import models.product
    import models.order
    import models.payment
    Base.metadata.create_all(bind=engine)