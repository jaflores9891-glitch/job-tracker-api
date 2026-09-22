import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pytest

from fastapi.testclient import TestClient
from app.database import get_db
from main import app

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db_session():
    conexion = engine.connect()
    transaccion = conexion.begin()
    sesion = TestingSessionLocal(bind = conexion)
    yield sesion
    sesion.close()
    transaccion.rollback()
    conexion.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()