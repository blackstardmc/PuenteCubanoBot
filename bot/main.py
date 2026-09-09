import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from bot.config import TELEGRAM_BOT_TOKEN

from bot.services.exchange_service import ExchangeService
from bot.services.combo_service import ComboService
from bot.services.recharge_service import RechargeService
from bot.services.product_service import ProductService

from bot.formatters.exchange_formatter import format_exchange_rates
from bot.formatters.combo_formatter import format_combos
from bot.formatters.recharge_formatter import format_recharges
from bot.formatters.product_formatter import format_products


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------

def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                "📦 Combos",
                callback_data="combos",
            ),
            InlineKeyboardButton(
                "📲 Recargas",
                callback_data="recharges",
            ),
        ],
        [
            InlineKeyboardButton(
                "🛍 Productos",
                callback_data="products",
            ),
            InlineKeyboardButton(
                "💱 Tasas de cambio",
                callback_data="exchanges",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ---------------------------------------------------------
# /START
# ---------------------------------------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await update.message.reply_text(
        "🌉 <b>Puente Cubano 360</b>\n\n"
        "Bienvenido a nuestro asistente de Telegram.\n\n"
        "Selecciona una opción:",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


# ---------------------------------------------------------
# CALLBACKS DE LOS BOTONES
# ---------------------------------------------------------

async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    await query.answer()

    option = query.data


    # -----------------------------------------------------
    # MENÚ PRINCIPAL
    # -----------------------------------------------------

    if option == "home":

        await query.edit_message_text(
            "🌉 <b>Puente Cubano 360</b>\n\n"
            "Selecciona una opción:",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(),
        )

        return


    # -----------------------------------------------------
    # SELECCIÓN DE MONEDA PARA COMBOS
    # -----------------------------------------------------

    if option.startswith("combo_currency:"):

        exchange_id = option.split(":", 1)[1]

        service = ComboService()

        data = await service.get_combos_for_currency(
            exchange_id
        )

        text = format_combos(data)

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Cambiar moneda",
                    callback_data="combos",
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Menú principal",
                    callback_data="home",
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return


    # -----------------------------------------------------
    # COMBOS
    # -----------------------------------------------------

    if option == "combos":

        service = ComboService()

        exchanges = await service.get_combo_currencies()

        keyboard = []

        for exchange in exchanges:

            name = exchange.get("name", "")
            code = exchange.get("code", "")

            keyboard.append([
                InlineKeyboardButton(
                    f"💱 {name} ({code})",
                    callback_data=(
                        f"combo_currency:{exchange['id']}"
                    ),
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "🏠 Menú principal",
                callback_data="home",
            )
        ])

        await query.edit_message_text(
            "📦 <b>COMBOS</b>\n\n"
            "Selecciona la moneda en la que deseas "
            "consultar los precios:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return


    # -----------------------------------------------------
    # RECARGAS
    # -----------------------------------------------------

    if option == "recharges":

        service = RechargeService()

        recharges = await service.get_recharges()

        text = format_recharges(recharges)

        keyboard = [
            [
                InlineKeyboardButton(
                    "🏠 Menú principal",
                    callback_data="home",
                )
            ]
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return


    # -----------------------------------------------------
    # PRODUCTOS
    # -----------------------------------------------------

    if option == "products":

        service = ProductService()

        products = await service.get_products()

        text = format_products(products)

        keyboard = [
            [
                InlineKeyboardButton(
                    "🏠 Menú principal",
                    callback_data="home",
                )
            ]
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return


    # -----------------------------------------------------
    # TASAS DE CAMBIO
    # -----------------------------------------------------

    if option == "exchanges":

        service = ExchangeService()

        rates = await service.get_exchange_rates()

        text = format_exchange_rates(rates)

        keyboard = [
            [
                InlineKeyboardButton(
                    "🏠 Menú principal",
                    callback_data="home",
                )
            ]
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return


    # -----------------------------------------------------
    # CALLBACK DESCONOCIDO
    # -----------------------------------------------------

    await query.edit_message_text(
        "⚠️ Opción no reconocida.",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


# ---------------------------------------------------------
# ERROR HANDLER
# ---------------------------------------------------------

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    logger.error(
        "Error procesando actualización de Telegram",
        exc_info=(
            type(context.error),
            context.error,
            context.error.__traceback__,
        )
        if context.error
        else None,
    )

    message = (
        "⚠️ <b>No pudimos completar la consulta.</b>\n\n"
        "Nuestro sistema no está disponible temporalmente.\n"
        "Por favor, inténtalo nuevamente en unos momentos."
    )

    try:

        if isinstance(update, Update):

            if update.callback_query:

                try:
                    await update.callback_query.answer()
                except Exception:
                    pass

                if update.callback_query.message:

                    await update.callback_query.message.reply_text(
                        message,
                        parse_mode="HTML",
                        reply_markup=main_menu_keyboard(),
                    )

            elif update.effective_message:

                await update.effective_message.reply_text(
                    message,
                    parse_mode="HTML",
                    reply_markup=main_menu_keyboard(),
                )

    except Exception:
        logger.exception(
            "No se pudo enviar el mensaje de error al usuario."
        )


# ---------------------------------------------------------
# ARRANQUE
# ---------------------------------------------------------

def main() -> None:

    logger.info("Iniciando Puente Cubano 360 Bot...")

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Comandos
    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    # Botones
    application.add_handler(
        CallbackQueryHandler(
            menu_callback
        )
    )

    # Errores
    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Bot iniciado correctamente. Esperando mensajes..."
    )

    application.run_polling()


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()