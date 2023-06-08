from database import get_db
from datetime import datetime
from sqlalchemy.orm import Session
from models import Coupon, CouponCreate, CouponOut
from fastapi import APIRouter, Depends, HTTPException, status

coupon_router = APIRouter(prefix="/coupons")

def validate_expiration_date(expiration_date: datetime):
    current_datetime = datetime.now()
    if expiration_date <= current_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de expiração deve ser posterior à data atual."
        )

def validate_max_uses(max_uses: int):
    if max_uses <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O número máximo de utilizações deve ser maior que zero."
        )

def validate_min_purchase_amount(min_purchase_amount: float):
    if min_purchase_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor mínimo de compra deve ser maior que zero."
        )

def validate_coupon_create(coupon: CouponCreate):
    validate_expiration_date(coupon.expiration_date)
    validate_max_uses(coupon.max_uses)
    validate_min_purchase_amount(coupon.min_purchase_amount)

@coupon_router.post("/", response_model=CouponOut)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    validate_coupon_create(coupon)

    new_coupon = Coupon(
        code=coupon.code,
        expiration_date=coupon.expiration_date,
        max_uses=coupon.max_uses,
        min_purchase_amount=coupon.min_purchase_amount,
        discount_type=coupon.discount_type,
        discount_amount=coupon.discount_amount,
        general_public=coupon.general_public,
        first_purchase_only=coupon.first_purchase_only
    )

    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    return new_coupon