from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from mangum import Mangum
import models, database, schemas # schemas එක මෙතනට එකතු කළා

app = FastAPI()

# Database tables හදන්න
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Welcome to Grocery Shop API"}

# CRUD: Get All Products
# response_model එක දාපුවම output එක schemas.Product වලට අනුව filter වෙනවා
@app.get("/products", response_model=list[schemas.Product])
def read_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

# CRUD: Create Product
# මෙතනදී schemas.ProductCreate පාවිච්චි කරලා Request Body එකක් විදියට ඩේටා ගන්නවා
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    # Schema එකෙන් එන ඩේටා models එකට දාන විදිය
    new_product = models.Product(
        name=product.name, 
        price=product.price, 
        description=product.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# AWS Lambda Handler!!
handler = Mangum(app)
