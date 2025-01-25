import pytest
import pytest_asyncio
from httpx import AsyncClient

from fastapi_app.database import engine  # Импортируйте ваш движок базы данных
from fastapi_app.models import Base


# Фикстура для асинхронного клиента
@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        # Возвращаем асинхронный клиент для использования в тестах
        yield async_client


# Фикстура для очистки базы данных после всех тестов
@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_database():
    # Создаем таблицы перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Выполняем все тесты
    # Удаляем таблицы после завершения всех тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Тест на создание рецепта
@pytest.mark.asyncio
async def test_create_recipe(client: AsyncClient):
    response = await client.post(
        "/recipes",
        json={
            "title": "Test Recipe",
            "cook_time": 30,
            "ingredients": "Test ingredients",
            "description": "Test description",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert data["cook_time"] == 30
    assert data["ingredients"] == "Test ingredients"
    assert data["description"] == "Test description"


# Тест на получение всех рецептов
@pytest.mark.asyncio
async def test_read_recipes(client: AsyncClient):
    response = await client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# Тест на получение конкретного рецепта по ID
@pytest.mark.asyncio
async def test_read_recipe(client: AsyncClient):
    response = await client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert data["cook_time"] == 30
    assert data["ingredients"] == "Test ingredients"
    assert data["description"] == "Test description"
