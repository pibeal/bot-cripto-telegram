import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# LIMPIAR CONFLICTO
# =========================
async def limpiar():
    from telegram import Bot
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.get_event_loop().run_until_complete(limpiar())

# =========================
# MENU
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("💸 Ganar dinero", callback_data="ganar")],
        [InlineKeyboardButton("🧠 Asesor financiero", callback_data="asesor")]
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola 👋\nSoy *Investia Pro* 💸\n\nSelecciona una opción:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # =========================
    # AHORRO
    # =========================
    if data == "ahorro":
        await query.edit_message_text("💰 Opciones de ahorro:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🥇 Nu", callback_data="app_nu")],
            [InlineKeyboardButton("Klar", callback_data="app_klar")],
            [InlineKeyboardButton("Ualá", callback_data="app_uala")],
            [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
            [InlineKeyboardButton("Hey Banco", callback_data="app_hey")],
            [InlineKeyboardButton("CETES", callback_data="app_cetes")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]))

    elif data == "app_nu":
        await query.edit_message_text(
            "🥇 *Nu Bank*\n\n💰 9% - 15% anual\n📊 Bajo riesgo\n\nIdeal para empezar",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://nu.com.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            "💳 *Klar*\n\n💰 ~10% anual\n📊 Bajo riesgo",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.klar.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_uala":
        await query.edit_message_text(
            "💳 Ualá\nCuenta digital sin comisiones",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.uala.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    elif data == "app_mp":
        await query.edit_message_text(
            "💰 MercadoPago\nRendimientos + liquidez",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.mercadopago.com.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    elif data == "app_hey":
        await query.edit_message_text(
            "🏦 Hey Banco\nCuenta con rendimiento",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.heybanco.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            "🏦 CETES\n\n💰 10% - 11%\n📊 Muy bajo riesgo",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.cetesdirecto.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    # =========================
    # BOLSA
    # =========================
    elif data == "bolsa":
        await query.edit_message_text("📈 Bolsa:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🥇 GBM+", callback_data="app_gbm")],
            [InlineKeyboardButton("Kuspit", callback_data="app_kuspit")],
            [InlineKeyboardButton("Bursanet", callback_data="app_bursanet")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]))

    elif data == "app_gbm":
        await query.edit_message_text(
            "🥇 GBM\nAcciones y ETFs\nEj: Apple, Tesla",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://gbm.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ])
        )

    elif data == "app_kuspit":
        await query.edit_message_text(
            "📊 Kuspit\nAcciones mexicanas\nIdeal para aprender",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.kuspit.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ])
        )

    elif data == "app_bursanet":
        await query.edit_message_text(
            "📈 Bursanet\nPlataforma avanzada",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.bursanet.mx")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ])
        )

    # =========================
    # CRIPTO
    # =========================
    elif data == "cripto":
        await query.edit_message_text("🪙 Cripto:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Binance", callback_data="app_binance")],
            [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
            [InlineKeyboardButton("Bybit", callback_data="app_bybit")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]))

    elif data == "app_binance":
        await query.edit_message_text(
            "🪙 Binance\nCompra BTC, ETH\n⚠️ Alto riesgo",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.binance.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ])
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            "💰 Bitso\nCripto fácil",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://bitso.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ])
        )

    elif data == "app_bybit":
        await query.edit_message_text(
            "📊 Bybit\nTrading avanzado",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.bybit.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ])
        )

    # =========================
    # GANAR DINERO
    # =========================
    elif data == "ganar":
        await query.edit_message_text("💸 Ganar dinero:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Apps", callback_data="apps_top")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]))

    elif data == "apps_top":
        await query.edit_message_text("Apps:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Atlas Earth", callback_data="app_atlas")],
            [InlineKeyboardButton("Mode", callback_data="app_mode")],
            [InlineKeyboardButton("Google Rewards", callback_data="app_google")],
            [InlineKeyboardButton("Viewpoints", callback_data="app_view")],
            [InlineKeyboardButton("Nicequest", callback_data="app_nice")],
            [InlineKeyboardButton("Animal Merge", callback_data="app_animal")],
            [InlineKeyboardButton("🔙", callback_data="ganar")]
        ]))

    elif data == "app_google":
        await query.edit_message_text(
            "🧠 Encuestas pagadas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Descargar", url="https://play.google.com/store/apps/details?id=com.google.android.apps.paidtasks")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ])
        )

    # =========================
    # ASESOR
    # =========================
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 Asesor:\n\n"
            "Nuevo → Nu o CETES\n"
            "Intermedio → GBM\n"
            "Avanzado → Cripto",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙", callback_data="menu")]
            ])
        )

    elif data == "menu":
        await query.edit_message_text("Menú 👇", reply_markup=main_menu())

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🔥 BOT ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
