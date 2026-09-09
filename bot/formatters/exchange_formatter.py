def country_flag(country_code: str | None) -> str:
    if not country_code:
        return "💱"

    code = country_code.upper().strip()

    if len(code) != 2:
        return "💱"

    try:
        return "".join(
            chr(ord(char) + 127397)
            for char in code
        )
    except Exception:
        return "💱"


def format_number(value: float) -> str:
    number = float(value)

    if number.is_integer():
        return f"{number:,.0f}"

    return f"{number:,.2f}".rstrip("0").rstrip(".")


def format_exchange_rates(rates: list[dict]) -> str:
    if not rates:
        return (
            "💱 <b>Tasas de cambio</b>\n\n"
            "No hay tasas disponibles en este momento."
        )

    lines = [
        "💱 <b>TASAS DE CAMBIO</b>",
        "",
    ]

    for rate in rates:
        sent = rate["sent_currency"]
        receive = rate["receive_currency"]

        sent_flag = country_flag(sent.get("countryCode"))
        receive_flag = country_flag(receive.get("countryCode"))

        sent_code = sent.get("code", "")
        receive_code = receive.get("code", "")

        sent_amount = format_number(rate["sent_amount"])
        receive_amount = format_number(rate["receive_amount"])
        min_amount = format_number(rate["min_amount"])

        lines.extend([
            f"{sent_flag} <b>{sent_code}</b> → "
            f"{receive_flag} <b>{receive_code}</b>",
            "",
            f"{sent_amount} {sent_code} = "
            f"{receive_amount} {receive_code}",
            f"📌 Mínimo a enviar: "
            f"{min_amount} {sent_code}",
            "",
            "────────────────",
            "",
        ])

    # Quitamos el último separador
    return "\n".join(lines[:-3])