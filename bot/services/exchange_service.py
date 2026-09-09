from bot.api.client import ApiClient


class ExchangeService:
    def __init__(self) -> None:
        self.api = ApiClient()

    async def get_exchange_rates(self) -> list[dict]:
        currencies_data = await self.api.get_currencies()
        exchanges_data = await self.api.get_exchanges()

        currencies = currencies_data.get("items", [])
        exchanges = exchanges_data.get("items", [])

        currencies_by_id = {
            currency["id"]: currency
            for currency in currencies
        }

        result = []

        for exchange in exchanges:
            sent_currency = currencies_by_id.get(exchange["sent"])
            receive_currency = currencies_by_id.get(exchange["receive"])

            if not sent_currency or not receive_currency:
                continue

            result.append({
                "id": exchange["id"],
                "sent_currency": sent_currency,
                "receive_currency": receive_currency,
                "sent_amount": exchange["sentAmount"],
                "receive_amount": exchange["receiveAmount"],
                "min_amount": exchange["minAmount"],
            })

        return result