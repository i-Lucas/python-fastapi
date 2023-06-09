from datetime import datetime
from sqlalchemy import exists
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Coupon, CouponCreate, DiscountType

def calculate_discount(total_amount: float, discount_type: str, discount_amount: float):
    if discount_type == "percentage":
        return (total_amount * discount_amount) / 100
    else:
        return discount_amount

def validate_discount_type(discount_type: DiscountType):

    valid_discount_types = [
        DiscountType.PERCENTAGE,
        DiscountType.FIXED_AMOUNT,
        DiscountType.FIXED_AMOUNT_FIRST_PURCHASE
    ]

    if discount_type not in valid_discount_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de desconto inválido. Tipos aceitos: 'percentage', 'fixed_amount' ou 'fixed_amount_first_purchase'."
        )

def check_coupon_exists(coupon_code: str, db: Session):
    coupon_exists = db.query(exists().where(Coupon.code == coupon_code)).scalar()
    if coupon_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um cupom com esse código."
        )

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

def validate_coupon_expiration(coupon: Coupon):
    current_datetime = datetime.now()
    if current_datetime > coupon.expiration_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este cupom expirou e não pode mais ser utilizado."
        )

def validate_coupon_availability(coupon: Coupon):
    if coupon.max_uses <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este cupom não está mais disponível para utilização."
        )

def validate_coupon_purchase_amount(coupon: Coupon, total_amount: float):
    if total_amount < coupon.min_purchase_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor total da compra é menor que o valor mínimo necessário para utilizar este cupom."
        )

def validate_coupon_first_purchase(coupon: Coupon, first_purchase: bool):
    if coupon.first_purchase_only and not first_purchase:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este cupom é válido apenas para a primeira compra do cliente."
        )
    
def find_coupon_by_code(code: str, db: Session):
    coupon = db.query(Coupon).filter(Coupon.code == code).first()
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O cupom informado não foi encontrado."
        )
    return coupon


def validate_coupon_consumption(coupon: Coupon, total_amount: float, first_purchase: bool):
    validate_coupon_expiration(coupon)
    validate_coupon_availability(coupon)
    validate_coupon_purchase_amount(coupon, total_amount)
    validate_coupon_first_purchase(coupon, first_purchase)

def validate_create_coupon(coupon: CouponCreate, db: Session):
    check_coupon_exists(coupon.code, db);
    validate_expiration_date(coupon.expiration_date);
    validate_max_uses(coupon.max_uses);
    validate_discount_type(coupon.discount_type);
    validate_min_purchase_amount(coupon.min_purchase_amount);
