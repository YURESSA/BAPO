# tests/test_app.py
import pytest
import sys
import os
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app, get_session
from models import Base, Task

# Тестовая база данных в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


# Создаем клиент один раз для всех тестов
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Фикстура для настройки базы данных перед каждым тестом"""
    # Создание таблиц
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Сначала очищаем
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Очистка таблиц после каждого теста
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
def override_dependencies():
    """Фикстура для переопределения зависимостей перед каждым тестом"""
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.clear()


class TestTaskAPI:
    def test_get_tasks_empty(self):
        """Тест получения пустого списка задач"""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_task(self):
        """Тест создания задачи"""
        task_data = {
            "title": "Test Task",
            "description": "Test Description"
        }
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert "id" in data

    def test_create_task_minimal_data(self):
        """Тест создания задачи с минимальными данными (только title)"""
        task_data = {"title": "Minimal Task"}
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == ""  # Должно быть значение по умолчанию
        assert "id" in data

    def test_create_task_validation_error(self):
        """Тест валидации данных при создании задачи"""
        # Отсутствует обязательное поле title
        invalid_data = {"description": "Only description"}
        response = client.post("/tasks", json=invalid_data)
        assert response.status_code == 422  # Validation Error

    def test_get_task_by_id(self):
        """Тест получения задачи по ID"""
        # Сначала создаем задачу
        task_data = {
            "title": "Test Task",
            "description": "Test Description"
        }
        create_response = client.post("/tasks", json=task_data)
        task_id = create_response.json()["id"]

        # Получаем задачу по ID
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]

    def test_get_nonexistent_task(self):
        """Тест получения несуществующей задачи"""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_update_task(self):
        """Тест обновления задачи"""
        # Сначала создаем задачу
        task_data = {
            "title": "Original Task",
            "description": "Original Description"
        }
        create_response = client.post("/tasks", json=task_data)
        task_id = create_response.json()["id"]

        # Обновляем задачу
        updated_data = {
            "title": "Updated Task",
            "description": "Updated Description"
        }
        response = client.put(f"/tasks/{task_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == updated_data["title"]
        assert data["description"] == updated_data["description"]

    def test_update_nonexistent_task(self):
        """Тест обновления несуществующей задачи"""
        updated_data = {
            "title": "Updated Task",
            "description": "Updated Description"
        }
        response = client.put("/tasks/999", json=updated_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_delete_task(self):
        """Тест удаления задачи"""
        # Сначала создаем задачу
        task_data = {
            "title": "Task to Delete",
            "description": "Description"
        }
        create_response = client.post("/tasks", json=task_data)
        task_id = create_response.json()["id"]

        # Удаляем задачу
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204
        assert response.content == b''  # Нет тела ответа

        # Проверяем, что задача удалена
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_task(self):
        """Тест удаления несуществующей задачи"""
        response = client.delete("/tasks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_get_all_tasks_with_data(self):
        """Тест получения всех задач с данными"""
        tasks_data = [
            {"title": "Task 1", "description": "Description 1"},
            {"title": "Task 2", "description": "Description 2"},
            {"title": "Task 3", "description": "Description 3"}
        ]

        created_tasks = []
        for task_data in tasks_data:
            response = client.post("/tasks", json=task_data)
            created_tasks.append(response.json())

        response = client.get("/tasks")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == len(tasks_data)

    def test_task_workflow_complete(self):
        """Тест полного workflow создания, обновления и удаления задачи"""
        # 1. Создаем задачу
        create_data = {"title": "Workflow Task", "description": "Initial Description"}
        create_response = client.post("/tasks", json=create_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == create_data["title"]

        update_data = {"title": "Updated Workflow Task", "description": "Updated Description"}
        update_response = client.put(f"/tasks/{task_id}", json=update_data)
        assert update_response.status_code == 200

        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 204

        get_deleted_response = client.get(f"/tasks/{task_id}")
        assert get_deleted_response.status_code == 404


class TestAPIHealth:
    """Тесты здоровья API"""

    def test_api_docs_available(self):
        """Тест доступности документации API"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_api_openapi_schema(self):
        """Тест доступности OpenAPI схемы"""
        response = client.get("/openapi.json")
        assert response.status_code == 200