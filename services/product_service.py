from sqlalchemy.orm import Session
from models.product import Product

def list_products_brief(db: Session):
    return db.query(Product).filter(Product.active.is_(True)).all()