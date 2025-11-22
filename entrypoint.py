import asyncio
import logging

from app.infrastructure.adapters.di.main import build_container
from app.infrastructure.ports.uow import UnitOfWorkPort

logger = logging.getLogger(__name__)


async def main() -> None:
    a = build_container( )

    tasks = [test_uow(a) for _ in range(5)]
    await asyncio.gather(*tasks)


async def test_uow(container):
    async with container() as request_container:
        uow = await request_container.get(UnitOfWorkPort)
        print(f"UoW: {uow._conn}")
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())