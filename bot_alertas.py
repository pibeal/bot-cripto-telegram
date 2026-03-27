import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# LIMPIAR WEBHOOK (ANTI-CONFLICT)
# =========================
async def limpiar():
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.get_event_loop().run_until_complete(limpiar())

# =========================
# MENU PRINCIPAL
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
            "🥇 *Nu Bank*\n\n"
            "💰 Rendimiento: 9% - 15% anual\n"
            "📊 Riesgo: Bajo\n\n"
            "✔️ Liquidez diaria\n✔️ Sin comisiones\n\n"
            "💡 Ideal para empezar",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://nu.com.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            "💳 *Klar*\n\n"
            "💰 ~10% anual\n📊 Bajo riesgo\n\n"
            "✔️ Tarjeta incluida\n✔️ App sencilla",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.klar.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_uala":
        await query.edit_message_text(
            "💳 *Ualá*\n\n"
            "✔️ Cuenta digital\n✔️ Sin comisiones\n\n"
            "💡 Ideal para manejo diario",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.uala.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mp":
        await query.edit_message_text(
            "💰 *MercadoPago*\n\n"
            "✔️ Rendimiento automático\n✔️ Dinero disponible\n\n"
            "💡 Ahorro flexible",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.mercadopago.com.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_hey":
        await query.edit_message_text(
            "🏦 *Hey Banco*\n\n"
            "💰 Rendimiento moderado\n✔️ Cuenta digital",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.heybanco.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            "🏦 *CETES*\n\n"
            "💰 10% - 11% anual\n📊 Muy bajo riesgo\n\n"
            "✔️ Respaldo gobierno",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.cetesdirecto.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
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
            "🥇 *GBM+*\n\n"
            "📈 Acciones (Apple, Tesla)\n📊 ETFs\n\n"
            "💰 Ganancia variable\n📊 Riesgo medio",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://gbm.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_kuspit":
        await query.edit_message_text(
            "📊 *Kuspit*\n\n"
            "✔️ Acciones mexicanas\n💡 Ideal para aprender",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.kuspit.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bursanet":
        await query.edit_message_text(
            "📈 *Bursanet*\n\n"
            "✔️ Plataforma más avanzada\n✔️ Fondos y acciones",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.bursanet.mx")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
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
            "🪙 *Binance*\n\n"
            "💰 Compra BTC, ETH\n📊 Trading\n\n"
            "⚠️ Riesgo alto",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.binance.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            "💰 *Bitso*\n\n"
            "✔️ Cripto fácil\n✔️ Ideal principiantes",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://bitso.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bybit":
        await query.edit_message_text(
            "📊 *Bybit*\n\n"
            "✔️ Trading avanzado\n⚠️ Alto riesgo",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.bybit.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
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
        await query.edit_message_text("Apps para ganar dinero:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Atlas Earth", callback_data="app_atlas")],
            [InlineKeyboardButton("Mode", callback_data="app_mode")],
            [InlineKeyboardButton("Google Rewards", callback_data="app_google")],
            [InlineKeyboardButton("Viewpoints", callback_data="app_view")],
            [InlineKeyboardButton("Nicequest", callback_data="app_nice")],
            [InlineKeyboardButton("Animal Merge", callback_data="app_animal")],
            [InlineKeyboardButton("🔙", callback_data="ganar")]
        ]))

    elif data == "app_atlas":
        await query.edit_message_text(
            "🌍 *Atlas Earth*\n\nTerrenos virtuales que generan renta",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Play Store", url="https://play.google.com/store/search?q=atlas+earth&c=apps")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mode":
        await query.edit_message_text(
            "🎧 *Mode*\n\nGana escuchando música",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Play Store", url="https://play.google.com/store/apps/details?id=com.currentmusic")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_google":
        await query.edit_message_text(
            "🧠 *Google Rewards*\n\nEncuestas pagadas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Play Store", url="https://play.google.com/store/apps/details?id=com.google.android.apps.paidtasks")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_view":
        await query.edit_message_text(
            "📊 *Viewpoints*\n\nEncuestas de Meta",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://viewpoints.fb.com")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_nice":
        await query.edit_message_text(
            "🎁 *Nicequest*\n\nGana premios por encuestas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.nicequest.com")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_animal":
        await query.edit_message_text(
            "🐾 *Animal Merge*\n\nJuego con recompensas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Play Store", url="https://play.google.com/store/search?q=animal+merge&c=apps")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # ASESOR
    # =========================
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 *Asesor financiero*\n\n"
            "👶 Nuevo → Nu / CETES\n"
            "📈 Intermedio → GBM\n"
            "🔥 Avanzado → Cripto",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙", callback_data="menu")]
            ]),
            parse_mode="Markdown"
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
    print("🔥 INVESTIA PRO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
