from html import escape


def format_price(value: float) -> str:
    value = float(value)

    if value.is_integer():
        return f"{value:,.0f}"

    return f"{value:,.2f}".rstrip("0").rstrip(".")


def format_products(products: list[dict]) -> str:
    lines = [
        "🛍 <b>PRODUCTOS DISPONIBLES</b>",
        "",
    ]

    if not products:
        lines.append(
            "No hay productos disponibles "
            "en este momento."
        )
        return "\n".join(lines)

    for index, product in enumerate(products):
        name = escape(product["name"])
        price = format_price(product["price"])

        lines.extend([
            f"🔹 <b>{name}</b>",
            f"💰 <b>${price} USD</b>",
        ])

        if index < len(products) - 1:
            lines.extend([
                "",
                "────────────────",
                "",
            ])

    return "\n".join(lines)