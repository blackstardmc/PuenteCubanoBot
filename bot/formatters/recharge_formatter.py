from html import escape


def country_flag(
    country_code: str | None,
) -> str:

    if not country_code:
        return "💰"

    code = country_code.upper().strip()

    if len(code) != 2:
        return "💰"

    return "".join(
        chr(ord(char) + 127397)
        for char in code
    )


def format_money(value: float) -> str:
    value = float(value)

    if value.is_integer():
        return f"{value:,.0f}"

    return f"{value:,.2f}".rstrip("0").rstrip(".")


def format_recharges(
    recharges: list[dict],
) -> str:

    lines = [
        "📲 <b>RECARGAS DISPONIBLES</b>",
        "",
    ]

    if not recharges:
        lines.append(
            "No hay recargas disponibles "
            "en este momento."
        )
        return "\n".join(lines)

    for index, recharge in enumerate(recharges):
        name = escape(recharge["name"])

        description = escape(
            recharge.get("description", "")
        )

        lines.append(
            f"📱 <b>{name}</b>"
        )

        if description:
            lines.append(description)

        lines.append("")
        lines.append("💰 <b>Precios:</b>")

        for price_data in recharge["prices"]:
            currency = price_data["currency"]

            code = escape(
                currency.get("code", "")
            )

            flag = country_flag(
                currency.get("countryCode")
            )

            price = format_money(
                price_data["price"]
            )

            lines.append(
                f"{flag} {code}: <b>{price}</b>"
            )

        if index < len(recharges) - 1:
            lines.extend([
                "",
                "────────────────",
                "",
            ])

    return "\n".join(lines)