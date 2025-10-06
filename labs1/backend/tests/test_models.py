# tests/test_models.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base, Task


class TestTaskModel:
    @pytest.fixture
    async def setup_db(self):
        """Фикстура для настройки тестовой базы данных"""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем асинхронную фабрику сессий
        AsyncSessionLocal = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        yield AsyncSessionLocal

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @pytest.mark.asyncio
    async def test_task_creation_and_persistence(self, setup_db):
        """Тест создания и сохранения задачи в БД"""
        AsyncSessionLocal = setup_db
        async with AsyncSessionLocal() as session:
            # Создаем задачу
            task = Task(title="Test Task", description="Test Description")
            session.add(task)
            await session.commit()
            await session.refresh(task)

            # Проверяем, что задача сохранилась
            assert task.id is not None
            assert task.title == "Test Task"
            assert task.description == "Test Description"

    @pytest.mark.asyncio
    async def test_task_default_description(self, setup_db):
        """Тест значения по умолчанию для description"""
        AsyncSessionLocal = setup_db
        async with AsyncSessionLocal() as session:
            task = Task(title="Test Task")
            session.add(task)
            await session.commit()
            await session.refresh(task)

            assert task.description == ""

    def test_task_table_name(self):
        """Тест имени таблицы"""
        assert Task.__tablename__ == "tasks"

    def test_task_columns(self):
        """Тест наличия колонок"""
        columns = [col.name for col in Task.__table__.columns]
        expected_columns = ['id', 'title', 'description']

        for col in expected_columns:
            assert col in columns

    def test_task_primary_key(self):
        """Тест первичного ключа"""
        assert Task.id.primary_key

    def test_title_constraints(self):
        """Тест ограничений для title"""
        assert not Task.title.nullable  # Должно быть NOT NULL

    def test_string_length_limits(self):
        """Тест ограничений длины строк"""
        assert Task.title.type.length == 255

    def test_task_repr(self):
        """Тест строкового представления задачи"""
        task = Task(title="Test Task", description="Test Description")
        # Проверяем, что у задачи есть строковое представление
        assert hasattr(task, '__repr__')