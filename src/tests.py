import pytest
from fastapi import status
from sqlalchemy.orm import Session
from utils import get_database_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Base, CouponCreate, Coupon
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from routes import (
    validate_expiration_date,
    validate_max_uses,
    validate_min_purchase_amount,
    validate_coupon_create,
    create_coupon,
)

@pytest.fixture
def get_db_test():
    engine = create_engine(get_database_url(TEST=True))

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    session.begin()
    session.query(Coupon).delete()
    session.commit()

    yield session
    session.close()

def test_validate_expiration_date():
    current_datetime = datetime.now()

    # Expiração no passado
    past_datetime = current_datetime - timedelta(days=1)
    with pytest.raises(Exception) as e:
        validate_expiration_date(past_datetime)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST

    # Expiração no futuro
    future_datetime = current_datetime + timedelta(days=1)
    validate_expiration_date(future_datetime)


def test_validate_max_uses():
    # Número máximo de utilizações negativo
    with pytest.raises(Exception) as e:
        validate_max_uses(-1)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST

    # Número máximo de utilizações igual a zero
    with pytest.raises(Exception) as e:
        validate_max_uses(0)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST

    # Número máximo de utilizações positivo
    validate_max_uses(10)


def test_validate_min_purchase_amount():
    # Valor mínimo de compra negativo
    with pytest.raises(Exception) as e:
        validate_min_purchase_amount(-1)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST

    # Valor mínimo de compra igual a zero
    with pytest.raises(Exception) as e:
        validate_min_purchase_amount(0)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST

    # Valor mínimo de compra positivo
    validate_min_purchase_amount(100)


def test_validate_coupon_create():
    coupon = CouponCreate(
        code="TEST123",
        expiration_date=datetime.now() + timedelta(days=1),
        max_uses=10,
        min_purchase_amount=100,
        discount_type="percentage",
        discount_amount=20,
        general_public=True,
        first_purchase_only=False,
    )

    # Validação bem-sucedida
    validate_coupon_create(coupon)

    # Validação com erro na data de expiração
    coupon.expiration_date = datetime.now() - timedelta(days=1)
    with pytest.raises(Exception) as e:
        validate_coupon_create(coupon)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_create_coupon(get_db_test):
    coupon = CouponCreate(
        code="TEST123",
        expiration_date=datetime.now() + timedelta(days=1),
        max_uses=10,
        min_purchase_amount=100,
        discount_type="percentage",
        discount_amount=20,
        general_public=True,
        first_purchase_only=False,
    )

    # Criação do cupom
    new_coupon = create_coupon(coupon, get_db_test)

    # Verifica se o cupom foi criado corretamente
    assert new_coupon.code == coupon.code
    assert new_coupon.expiration_date == coupon.expiration_date
    assert new_coupon.max_uses == coupon.max_uses
    assert new_coupon.min_purchase_amount == coupon.min_purchase_amount
    assert new_coupon.discount_type == coupon.discount_type
    assert new_coupon.discount_amount == coupon.discount_amount
    assert new_coupon.general_public == coupon.general_public
    assert new_coupon.first_purchase_only == coupon.first_purchase_only
