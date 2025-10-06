# tests/test_database.py
import pytest
import os
from database import AsyncSessionLocal


class TestDatabase:
    def test_database_url_environment_variables(self):
        """Тест наличия переменных окружения"""
        assert 'POSTGRES_USER' in os.environ
        assert 'POSTGRES_PASSWORD' in os.environ
        assert 'POSTGRES_DB' in os.environ

    def test_async_session_local_creation(self):
        """Тест создания асинхронной сессии"""
        assert AsyncSessionLocal is not None

    @pytest.mark.asyncio
    async def test_init_db_integration(self):
        """Интеграционный тест инициализации БД с SQLite"""
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy.pool import StaticPool
        from models import Base

        # Создаем тестовую базу данных в памяти
        test_engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        # Временно подменяем engine
        import database
        original_engine = database.engine
        database.engine = test_engine

        try:
            await database.init_db()
            # Если не возникло исключений, тест пройден
            assert True
        except Exception as e:
            pytest.fail(f"init_db failed with exception: {e}")
        finally:
            # Восстанавливаем оригинальный engine
            database.engine = original_engine