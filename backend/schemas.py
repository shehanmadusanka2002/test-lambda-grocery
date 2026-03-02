from pydantic import BaseModel
from typing import Optional

# පොදුවේ පාවිච්චි කරන fields
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# Product එකක් Create කරද්දී පාවිච්චි කරන schema එක
class ProductCreate(ProductBase):
    pass 

# API එකෙන් ඩේටා ආපහු යවද්දී (Response) පාවිච්චි කරන schema එක
class Product(ProductBase):
    id: int

    class Config:
        # SQLAlchemy models පාවිච්චි කරන නිසා මේක අනිවාර්යයෙන්ම ඕනේ
        from_attributes = True
