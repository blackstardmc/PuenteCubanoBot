from bot.api.client import ApiClient


class RechargeService:
    def __init__(self) -> None:
        self.api = ApiClient()

    async def get_recharges(self) -> list[dict]:
        recharges_data = await self.api.get_recharges()
        currencies_data = await self.api.get_currencies()
        exchanges_data = await self.api.get_exchanges()

        recharges = recharges_data.get("items", [])
        currencies = currencies_data.get("items", [])
        exchanges = exchanges_data.get("items", [])

        currencies_by_id = {
            currency["id"]: currency
            for currency in currencies
        }

        result = []

        for recharge in recharges:
            if not recharge.get("isAvailable", False):
                continue

            base_currency_id = recharge.get("currency")

            base_currency = currencies_by_id.get(
                base_currency_id
            )

            if not base_currency:
                continue

            prices = []

            # Primero añadimos el precio en su moneda original.
            prices.append({
                "currency": base_currency,
                "price": float(recharge["price"]),
            })

            # Buscamos todas las conversiones que terminan
            # en la moneda base de esta recarga.
            for exchange in exchanges:
                if exchange.get("receive") != base_currency_id:
                    continue

                sent_currency = currencies_by_id.get(
                    exchange.get("sent")
                )

                if not sent_currency:
                    continue

                sent_amount = float(
                    exchange["sentAmount"]
                )

                receive_amount = float(
                    exchange["receiveAmount"]
                )

                if receive_amount == 0:
                    continue

                converted_price = (
                    float(recharge["price"])
                    * sent_amount
                    / receive_amount
                )

                prices.append({
                    "currency": sent_currency,
                    "price": converted_price,
                })

            result.append({
                "id": recharge["id"],
                "name": recharge.get("name", ""),
                "description": recharge.get(
                    "description",
                    "",
                ),
                "prices": prices,
            })

        return result