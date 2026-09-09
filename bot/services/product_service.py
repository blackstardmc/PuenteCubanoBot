from bot.api.client import ApiClient


class ProductService:
    def __init__(self) -> None:
        self.api = ApiClient()

    async def get_products(self) -> list[dict]:
        data = await self.api.get_products()

        products = data.get("items", [])

        result = []

        for product in products:
            if not product.get("isAvailable", False):
                continue

            result.append({
                "id": product["id"],
                "name": product.get("name", ""),
                "price": float(product.get("price", 0)),
            })

        return result