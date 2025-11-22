import asyncio
import logging
import uuid

from datetime import datetime, timezone

import asyncpg
from app.domain.core.config.provider import EnvSourceProvider
from app.domain.core.config.settings import DatabaseConfig
from app.domain.dto.product import Product
from app.infrastructure.adapters.persistence.repositories.sql.migration_apply import db_yoyo_migration
from app.infrastructure.adapters.persistence.repositories.sql.product import ProductRepository


logger = logging.getLogger(__name__)


async def main() -> None:
    conn: asyncpg.Connection = await asyncpg.connect(
        host="localhost",
        port=8087,
        user="postgres",
        password="postgres",
        database="products_db",
    )


    repo = ProductRepository(conn=conn)

    guid = uuid.uuid4()
    product = Product(
        guid=guid,
        name="Тестовый товар",
        slug="testovyj-tovar-1233",
        price_cents=99999,
        description="Это тестовый продукт для проверки asyncpg",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    await repo.add(product)
    print("Продукт успешно добавлен!")

    fetched = await repo.get_by_guid(guid)
    print("Получили из БД:", fetched)

    by_slug = await repo.find_by_slug("testovyj-tovar-1233")
    print("По slug:", by_slug)

    await conn.close()
    print("closed")

if __name__ == "__main__":
    db_yoyo_migration(DatabaseConfig.load(EnvSourceProvider()).connection_string.replace("+asyncpg", ""))
    asyncio.run(main())