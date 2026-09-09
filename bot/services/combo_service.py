from bot.api.client import ApiClient


class ComboService:
    def __init__(self) -> None:
        self.api = ApiClient()

    async def get_combo_currencies(self) -> list[dict]:
        """
        Devuelve todas las monedas configuradas
        específicamente para los combos.
        """
        data = await self.api.get_combo_exchanges()
        return data.get("items", [])

    async def get_combos_for_currency(
        self,
        combo_exchange_id: str,
    ) -> dict:

        combos_data = await self.api.get_combos()
        categories_data = await self.api.get_combo_categories()
        exchanges_data = await self.api.get_combo_exchanges()

        combos = combos_data.get("items", [])
        categories = categories_data.get("items", [])
        exchanges = exchanges_data.get("items", [])

        # Buscamos la moneda seleccionada por ID.
        selected_exchange = next(
            (
                exchange
                for exchange in exchanges
                if exchange["id"] == combo_exchange_id
            ),
            None,
        )

        if selected_exchange is None:
            raise ValueError(
                f"ComboExchange no encontrado: {combo_exchange_id}"
            )

        categories_by_id = {
            category["id"]: category
            for category in categories
        }

        grouped: dict[str, list[dict]] = {}

        for combo in combos:
            # No mostramos combos no disponibles.
            if not combo.get("isAvailable", False):
                continue

            category = categories_by_id.get(
                combo.get("category")
            )

            category_name = (
                category.get("name", "Otros")
                if category
                else "Otros"
            )

            price = self._calculate_price(
                combo["price"],
                selected_exchange,
            )

            item = {
                "id": combo["id"],
                "name": combo.get("name", ""),
                "presentation": combo.get(
                    "presentation",
                    "",
                ),
                "description": combo.get(
                    "description",
                    "",
                ),
                "price": price,
            }

            grouped.setdefault(
                category_name,
                []
            ).append(item)

        return {
            "exchange": selected_exchange,
            "categories": grouped,
        }

    @staticmethod
    def _calculate_price(
        base_price: float,
        exchange: dict,
    ) -> float:

        factor = float(exchange["factor"])
        fixed = int(exchange["fixed"])

        price = float(base_price) / factor

        return round(price, fixed)