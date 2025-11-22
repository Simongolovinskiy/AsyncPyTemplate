from app.domain.common.handlers import RequestHandler
from app.domain.dto import Product
from app.infrastructure.ports.uow import UnitOfWorkPort

from .request import AddProductRequest
from .response import AddProductResponse


class AddProductHandler(
    RequestHandler[AddProductRequest, AddProductResponse]
):
    def __init__(
        self,
        uow: UnitOfWorkPort,
    ) -> None:
        self._uow = uow

    async def handle(self, request: AddProductRequest) -> AddProductResponse:
        async with self._uow as uow:
            product_repo = uow.products
            product = Product(
                    request.name,
                    request.slug,
                    request.price_cents,
                    request.description
                )

            await product_repo.add(product)

        return AddProductResponse(
            guid=product.guid,
            name=product.name,
            slug=product.slug,
            price_cents=product.price_cents,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
