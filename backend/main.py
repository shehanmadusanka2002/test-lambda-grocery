from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import List
from mangum import Mangum # 👈 අලුතින් එක් කළා

# 1. Database Configuration this section එකේ DATABASE_URL එක ලැම්ඩා සෙටින්ග්ස් වල අන්තිමට '/postgres' ලෙස තිබිය යුතුයි
# DATABASE_URL එක ලැම්ඩා සෙටින්ග්ස් වල අන්තිමට '/postgres' ලෙස තිබිය යුතුයි
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Product Model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)

Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. CRUD Endpoints
@app.get("/")
def read_root():
    return {"status": "online", "message": "Grocery API is working"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/products")
def create_product(product_data: dict, db: Session = Depends(get_db)):
    db_product = Product(
        name=product_data.get("name"),
        price=product_data.get("price"),
        description=product_data.get("description")
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: dict, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.name = product_data.get("name")
    db_product.price = product_data.get("price")
    db_product.description = product_data.get("description")
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Deleted successfully"}

# 5. Lambda Handler 👈 මෙය අනිවාර්යයි!
handler = Mangum(app)