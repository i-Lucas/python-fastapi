import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status
from sqlalchemy_utils import database_exists, create_database

from models import Base, Coupon
from utils import get_database_url

from services.coupon import (
    check_coupon_exists,
    find_coupon_by_code
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

# ----------------------------------------------------------------------------------------------

def test_check_coupon_exists(get_db_test):

    db = get_db_test
    coupon_code = "COUPON123"
    coupon = Coupon(code=coupon_code)
    db.add(coupon)
    db.commit()

    with pytest.raises(HTTPException) as exception:
        check_coupon_exists(coupon_code, db)
    
    assert exception.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exception.value.detail == "Já existe um cupom com esse código."

# ----------------------------------------------------------------------------------------------

def test_find_coupon_by_code(get_db_test):

    db = get_db_test
    coupon_code = "TEMCUPOM"
    coupon = Coupon(code=coupon_code)
    db.add(coupon)
    db.commit()

    result = find_coupon_by_code(coupon_code, db)
    assert result == coupon

def test_find_coupon_by_code_not_found(get_db_test):

    db = get_db_test
    coupon_code = "NAOTEMCUPOM"

    with pytest.raises(HTTPException) as exception:
        find_coupon_by_code(coupon_code, db)
    
    assert exception.value.status_code == status.HTTP_404_NOT_FOUND
    assert exception.value.detail == "O cupom informado não foi encontrado."

# ----------------------------------------------------------------------------------------------