import os
import logging
from typing import AsyncGenerator

from dishka import Container, Provider, Scope, provide
from psqlpy import ConnectionPool

from app.infrastructure.adapters.amqp.kafka import KafkaMessageBroker
from app.domain.ports.repositories.product import ProductRepositoryPort
from app.infrastructure.adapters.persistence.repositories.sql.product import ProductRepository
from app.infrastructure.ports.amqp import MessageBrokerPort

logger = logging.getLogger(__name__)


class DatabaseProvider(Provider):

    scope = Scope.APP

    @provide
    async def get_pool(self) -> AsyncGenerator[ConnectionPool, None]:
        """Инициализируем пул соединений."""
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise RuntimeError("DATABASE_URL not set")

        db_pool = DatabasePool.get_instance( )
        await db_pool.init(
            dsn=db_url,
            min_size=int(os.getenv("DB_MIN_SIZE", "5")),
            max_size=int(os.getenv("DB_MAX_SIZE", "20")),
        )
        logger.info("✓ Database pool initialized")

        yield db_pool.get_pool( )

        await db_pool.close( )
        logger.info("✓ Database pool closed")


class RepositoryProvider(Provider):
    """Поставщик репозиториев."""

    scope = Scope.REQUEST

    @provide
    def get_product_repository(self) -> ProductRepositoryPort:
        return ProductRepository()


class MessageBrokerProvider(Provider):

    scope = Scope.APP

    @provide
    async def get_broker(self) -> AsyncGenerator[MessageBrokerPort, None]:
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        consumer_group = os.getenv("KAFKA_GROUP_ID", "my-app-group")

        broker = KafkaMessageBroker(
            bootstrap_servers=bootstrap_servers,
            consumer_group_id=consumer_group,
        )
        await broker.start( )
        logger.info("✓ Kafka broker started")

        yield broker

        await broker.close( )
        logger.info("✓ Kafka broker closed")


    """Создаём и конфигурируем DI контейнер."""

    container = Container(
        DatabaseProvider(),
        RepositoryProvider(),
        MessageBrokerProvider(),
    )

    return container


