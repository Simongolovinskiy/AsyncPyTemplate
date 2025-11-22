import uuid
import msgspec
from datetime import datetime


class AddProductResponse(msgspec.Struct, frozen=True, gc=False):
    guid: uuid.UUID
    name: str
    slug: str
    price_cents: int
    created_at: datetime
    updated_at: datetime