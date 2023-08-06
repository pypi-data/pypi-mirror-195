"""backends.py"""
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from strangeworks.core.client.platform import API, Operation


get_backends_query = Operation(
    query="""
    query backends(
        $product_slugs: [String!]
        $backend_type_slugs: [String!]
        $statuses: [BackendStatus!]
        $backend_tags: [String!]
    ) {
        backends(
            productSlugs: $product_slugs
            backendTypeSlugs: $backend_type_slugs
            backendStatuses: $statuses
            backendTags: $backend_tags
        ) {
            name
            remoteBackendId
            status
            backendRegistrations {
                data
                backendType {
                    slug
                    displayName
                }
            }
            product {
                slug
                productType
                owner {
                    name
                }
            }
        }
    }
"""
)


@dataclass
class Product:
    slug: str
    type: str
    owner_name: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Product(
            slug=data.get("slug"),
            type=data.get("productType"),
            owner_name=data.get("owner").get("name") if data.get("owner") else None,
        )


@dataclass
class Backend:
    name: str
    status: str
    remote_id: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    type_slug: Optional[str] = None
    type_name: Optional[str] = None
    product: Optional[Product] = None

    @staticmethod
    def from_dict(backend_dict: Dict[str, Any]):
        product_info = backend_dict.get("product")
        registrations = backend_dict.get("backendRegistrations")
        backend_info = (
            registrations[0] if registrations and len(registrations) > 0 else None
        )
        data = backend_info.get("data") if backend_info else None
        return Backend(
            name=backend_dict.get("name"),
            status=backend_dict.get("status"),
            remote_id=backend_dict.get("remoteBackendId"),
            properties=json.loads(data) if data else None,
            product=Product.from_dict(product_info),
        )


def get(
    api: API,
    statuses: Optional[List[str]] = None,
    product_slugs: Optional[List[str]] = None,
) -> Optional[List[Backend]]:
    raw_results = api.execute(
        get_backends_query,
        statuses=statuses,
        product_slugs=product_slugs,
    ).get("backends")
    return list(map(lambda x: Backend.from_dict(x), raw_results))
