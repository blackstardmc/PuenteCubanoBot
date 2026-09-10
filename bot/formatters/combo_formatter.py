from html import escape


CATEGORY_EMOJIS = {
    "CÁRNICOS": "🥩🥩🍖",
    "LÁCTEOS": "🥛🧈🍼",
    "LÍQUIDOS": "🥛🍷🥃🍹",
    "GRANOS Y PASTAS": "🍚🍜",
    "HIGIENE Y ASEO": "🧻🧼🧴🧽",
    "BEBIDAS": "🍷🥃🍹🧉🍸🧃",
    "PAQUETES ADICIONALES": "📦",
"COCINA" : "🧂🧄🧅"
}


def normalize_category_name(name: str) -> str:
    return name.strip().upper()


def get_category_emoji(name: str) -> str:
    normalized = normalize_category_name(name)
    return CATEGORY_EMOJIS.get(normalized, "📦")



def format_combo_price(
    price: float,
    exchange: dict,
) -> str:
    code = exchange.get("code", "")
    symbol = exchange.get("symbol", "")
    fixed = int(exchange.get("fixed", 2))

    formatted = f"{price:,.{fixed}f}"

    return f"{formatted} {symbol}".strip()


def format_combos(data: dict) -> str:
    exchange = data["exchange"]
    categories = data["categories"]

    lines = [
        "🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁",
        "",
        "🔁🔁 <b>TIENDA ONLINE &gt;&gt;&gt; Cuba 🇨🇺</b> 🔁🔁",
        "",
        "💯 Tenemos los mejores precios del mercado.",
        "",
        "Compruébelo usted mismo.",
        "",
    ]

    if not categories:
        lines.append(
            "No hay productos disponibles en este momento."
        )
        return "\n".join(lines)

    for category_name, combos in categories.items():
        normalized_name = normalize_category_name(category_name)
        emoji = get_category_emoji(category_name)
        lines.append("")
        lines.append(
            f"<b>{escape(normalized_name)} {emoji}</b>"
        )
        lines.append("")

        for combo in combos:
          
            name = escape(
                combo.get("name", "")
            )

            presentation = escape(
                combo.get("presentation", "")
            )

            price = format_combo_price(
                combo["price"],
                exchange,
            )

            if presentation:
                lines.append(
                    f"{name} ({presentation}) = "
                    f"{escape(price)}"
                )
            else:
                lines.append(
                    f"{name} = "
                    f"{escape(price)}"
                )
                lines.append("")
    lines.extend([
        "💎💎💎💎💎 <b>ACEPTAMOS PAGOS DE DIVERSOS PAÍSES.</b>",
        "",
        "COMUNÍCATE CON NOSOTROS Y TE DECIMOS "
        "SI HAY PAGOS PARA TU REGIÓN Y LA TASA DE CAMBIO 💎💎💎💎",
        
        "",
        "<b>Chat de grupo:</b>",
        "",
        "https://chat.whatsapp.com/CaShkBUillW8QVT57QRsok",
    ])

    return "\n".join(lines)