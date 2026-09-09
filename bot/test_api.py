import asyncio

from bot.api.client import ApiClient


async def main() -> None:
    api = ApiClient()

    tests = {
        "products": api.get_products,
        "combos": api.get_combos,
        "combo_exchanges": api.get_combo_exchanges,
        "currencies": api.get_currencies,
        "exchanges": api.get_exchanges,
        "combo_categories": api.get_combo_categories,
        "recharges": api.get_recharges,
    }

    for name, function in tests.items():
        print("\n" + "=" * 60)
        print(name.upper())
        print("=" * 60)

        try:
            data = await function()

            print(f"page: {data.get('page')}")
            print(f"totalItems: {data.get('totalItems')}")
            print(f"totalPages: {data.get('totalPages')}")

            items = data.get("items", [])

            print(f"items recibidos: {len(items)}")

            if items:
                print("\nPrimer registro:")
                print(items[0])

        except Exception as error:
            print(f"ERROR: {error}")


if __name__ == "__main__":
    asyncio.run(main())