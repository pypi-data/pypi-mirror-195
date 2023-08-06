from __future__ import annotations

import abc
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from .validators import is_valid_isbn, is_valid_url, sanitize_isbn


class QuerySchema(BaseModel):
    pass


class MutationSchema(BaseModel, abc.ABC):
    @abc.abstractmethod
    def to_input_data(self) -> dict:
        raise NotImplementedError


class ShopifyShop(QuerySchema):
    gid: str
    name: str
    myshopify_domain: str

    @property
    def id(self) -> int:
        return int(self.gid.split("/")[-1])


class ShopifyBook(QuerySchema):
    gid: str
    isbn: str
    title: str
    author: str
    price: Decimal
    subtitle: Optional[str]
    description: Optional[str]
    publisher: Optional[str]
    published_date: Optional[str]

    @property
    def id(self) -> int:
        return int(self.gid.split("/")[-1])


class CreateBookInput(MutationSchema):
    isbn: str
    title: str
    author: str
    price: Decimal
    subtitle: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    cover_image: Optional[str] = None

    @validator("isbn")
    def isbn_must_be_10_or_13_digits(cls, v):
        if not is_valid_isbn(v):
            raise ValueError("ISBN must be 10 or 13 digits")
        return sanitize_isbn(v)

    @validator("cover_image")
    def cover_image_must_be_url(cls, v):
        if v is None:
            return v
        if not is_valid_url(v):
            raise ValueError("Cover image must be a URL")
        return v

    def to_input_data(self) -> dict:
        data = {
            "title": self.title,
            "vendor": self.publisher,
            "descriptionHtml": self.description,
            "productType": "Book",
            "variants": [
                {
                    "sku": self.isbn,
                    "barcode": self.isbn,
                    "price": str(self.price),
                }
            ],
            "metafields": [
                {
                    "key": "author",
                    "namespace": "book",
                    "value": self.author,
                },
                {
                    "key": "published_date",
                    "namespace": "book",
                    "value": self.published_date,
                },
            ],
        }
        if self.cover_image:
            data["images"] = [{"altText": self.title, "src": self.cover_image}]
        return data


class UpdateBookInput(MutationSchema):
    product_id: int
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None

    @validator("isbn")
    def isbn_must_be_10_or_13_digits(cls, v):
        if v is None:
            return v
        if not is_valid_isbn(v):
            raise ValueError("ISBN must be 10 or 13 digits")
        return sanitize_isbn(v)


class MetafieldDefinition(QuerySchema):
    gid: str
    key: str
    name: str
    namespace: str
    description: Optional[str]

    @property
    def id(self) -> int:
        return int(self.gid.split("/")[-1])


class MetafieldType(str, Enum):
    boolean = "boolean"
    collection_reference = "collection_reference"
    color = "color"
    date = "date"
    date_time = "date_time"
    dimension = "dimension"
    file_reference = "file_reference"
    json = "json"
    metaobject_reference = "metaobject_reference"
    mixed_reference = "mixed_reference"
    money = "money"
    multi_line_text_field = "multi_line_text_field"
    number_decimal = "number_decimal"
    number_integer = "number_integer"
    page_reference = "page_reference"
    product_reference = "product_reference"
    rating = "rating"
    single_line_text_field = "single_line_text_field"
    url = "url"
    variant_reference = "variant_reference"
    volume = "volume"
    weight = "weight"


class CreateMetafieldDefinitionInput(MutationSchema):
    name: str
    key: str
    type: MetafieldType
    namespace: str = "book"
    owner_type: str = "PRODUCT"

    def to_input_data(self) -> dict:
        return {
            "key": self.key,
            "type": self.type,
            "name": self.name,
            "ownerType": self.owner_type,
            "namespace": self.namespace,
        }
