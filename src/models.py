from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum as PyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Float

Base = declarative_base()

class DiscountType(str, PyEnum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    FIXED_AMOUNT_FIRST_PURCHASE = "fixed_amount_first_purchase"

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    expiration_date = Column(DateTime)
    max_uses = Column(Integer)
    min_purchase_amount = Column(Float)
    discount_type = Column(Enum(DiscountType))
    discount_amount = Column(Float)
    general_public = Column(Boolean)
    first_purchase_only = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

# ------------------------------------------

class CouponBase(BaseModel):
    code: str
    expiration_date: datetime
    max_uses: int
    min_purchase_amount: float
    discount_type: str
    discount_amount: float
    general_public: bool
    first_purchase_only: bool

class CouponCreate(CouponBase):
    pass

class CouponUpdate(CouponBase):
    code: Optional[str] = None

class CouponInDB(CouponBase):
    id: int

    class Config:
        orm_mode = True

class CouponOut(CouponInDB):
    pass