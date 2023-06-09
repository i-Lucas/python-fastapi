from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models import Coupon, CouponCreate, CouponOut

from services.coupon import (
    validate_coupon_consumption,
    validate_create_coupon,
    find_coupon_by_code,
    calculate_discount
)

coupon_router = APIRouter(prefix="/coupons");

@coupon_router.post("/", response_model=CouponOut)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):

    validate_create_coupon(coupon, db);

    new_coupon = Coupon(
        code=coupon.code,
        expiration_date=coupon.expiration_date,
        max_uses=coupon.max_uses,
        min_purchase_amount=coupon.min_purchase_amount,
        discount_type=coupon.discount_type,
        discount_amount=coupon.discount_amount,
        general_public=coupon.general_public,
        first_purchase_only=coupon.first_purchase_only
    );

    db.add(new_coupon);
    db.commit();
    db.refresh(new_coupon);
    return new_coupon;

@coupon_router.post("/consume/{code}")
def consume_coupon_by_code(code: str, request_data: dict, db: Session = Depends(get_db)):
    total_amount = request_data.get("total_amount")
    first_purchase = request_data.get("first_purchase")

    coupon = find_coupon_by_code(code, db);
    validate_coupon_consumption(coupon, total_amount, first_purchase);

    coupon.max_uses -= 1;
    db.commit();

    discount_amount = calculate_discount(total_amount, coupon.discount_type, coupon.discount_amount);
    return {
        "message": "Cupom consumido com sucesso!",
        "discount_amount": discount_amount,
        "coupon_code": coupon.code
    }
