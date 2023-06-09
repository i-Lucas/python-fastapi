import pytest
from enum import Enum
from datetime import datetime
from fastapi import HTTPException, status

from services.coupon import (
    DiscountType,
    calculate_discount,
    validate_discount_type,
    validate_expiration_date,
    validate_max_uses
)

def test_calculate_discount_percentage():
    total_amount = 150
    discount_type = "percentage"
    discount_amount = 20
    result = calculate_discount(total_amount, discount_type, discount_amount)
    assert result == 30

def test_calculate_discount_fixed_amount():
    total_amount = 100
    discount_type = "fixed"
    discount_amount = 10
    result = calculate_discount(total_amount, discount_type, discount_amount)
    assert result == 10

# ----------------------------------------------------------------------------------------------

def test_validate_discount_type():
    valid_types = [
        DiscountType.PERCENTAGE,
        DiscountType.FIXED_AMOUNT,
        DiscountType.FIXED_AMOUNT_FIRST_PURCHASE
    ]

    invalid_type = "invalid_discount_type"

    # desconto válido
    for discount_type in valid_types:
        try:
            validate_discount_type(discount_type)
        except HTTPException:
            pytest.fail()

    # desconto inválido
    with pytest.raises(HTTPException) as exc_info:
        validate_discount_type(invalid_type)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Tipo de desconto inválido. Tipos aceitos: 'percentage', 'fixed_amount' ou 'fixed_amount_first_purchase'."

# ----------------------------------------------------------------------------------------------

def test_validate_expiration_date():

    expiration_date = datetime(2050, 12, 31);
    try:
        validate_expiration_date(expiration_date) # válido
    except HTTPException:
        pytest.fail()

    expiration_date = datetime.now()  # Data atual
    with pytest.raises(HTTPException) as exc:
        validate_expiration_date(expiration_date)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "A data de expiração deve ser posterior à data atual."

    expiration_date = datetime(2021, 5, 31);
    with pytest.raises(HTTPException) as exc:
        validate_expiration_date(expiration_date)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "A data de expiração deve ser posterior à data atual."

# ----------------------------------------------------------------------------------------------

def test_validate_max_uses():
    with pytest.raises(HTTPException) as exc_info:
        validate_max_uses(0)
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "O número máximo de utilizações deve ser maior que zero."

    with pytest.raises(HTTPException) as exc_info:
        validate_max_uses(-1)
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "O número máximo de utilizações deve ser maior que zero."