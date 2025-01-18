import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from module_26_fastapi.homework.main import get_db

from module_26_fastapi.homework.main import app
from module_26_fastapi.homework.models import Base

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

def test_create_recipe(client):
    response = client.post(
        "/recipes",
        json={
            "title": "Test Recipe",
            "cook_time": 30,
            "ingredients": "Test ingredients",
            "description": "Test description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert data["cook_time"] == 30
    assert data["ingredients"] == "Test ingredients"
    assert data["description"] == "Test description"

def test_read_recipes(client):
    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_recipe(client):
    response = client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert data["cook_time"] == 30
    assert data["ingredients"] == "Test ingredients"
    assert data["description"] == "Test description"
