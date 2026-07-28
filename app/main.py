from tarfile import data_filter

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.core import database
from app.core.database import SessionLocal, engine
from app.models import database_model
from app.models.database_model import Base
from app.models.model import Product

app = FastAPI()

Base.metadata.create_all(bind=engine)

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=5, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=6, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def init_db():
    db = SessionLocal()

    try:
        count = db.query(database_model.Product).count()

        if count == 0:
            for product in products:
                db.add(database_model.Product(**product.model_dump()))

            db.commit()

    finally:
        db.close()


init_db()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):  # noqa: B008
    
    db_products = db.query(database_model.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()          #quesry == select, filter == where
    if db_product:
        return db_product
    return "product not fount"


@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/product")
def update_product(id: int, product: Product,  db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()          #quesry == select, filter == where

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated"

    else:
        return "No object found"


@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()    
    if db_product:
        db.delete(db_product)
        db.commit()
        return 'delete sucess'
    else:
        "No product found"      #quesry == select, filter == where
