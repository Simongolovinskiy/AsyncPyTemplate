from typing import Protocol
from app.domain.ports.repositories.product import ProductRepositoryPort


class UnitOfWorkPort(Protocol):
    products: ProductRepositoryPort

    async def __aenter__(self) -> "UnitOfWorkPort":
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError

    @property
    def in_transaction(self) -> bool:
        raise NotImplementedError
