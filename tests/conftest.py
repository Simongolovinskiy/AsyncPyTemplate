import pytest
import asyncio
from unittest.mock import AsyncMock
from dishka import Container, Provider, Scope, provide

from app.domain.ports.repositories.product import ProductRepositoryPort
from app.infrastructure.ports.amqp import MessageBrokerPort


class TestProvider(Provider):
    scope = Scope.APP

    @provide
    def get_mock_product_repo(self) -> ProductRepositoryPort:
        return AsyncMock(spec=ProductRepositoryPort)

    @provide
    def get_mock_broker(self) -> MessageBrokerPort:
        return AsyncMock(spec=MessageBrokerPort)


@pytest.fixture
def test_container() -> Container:
    return Container(TestProvider())


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()