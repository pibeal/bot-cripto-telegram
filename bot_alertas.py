import json
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DB_FILE = "users.json"

# =========================
# DB
# =========================
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# MENU
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("💸 Ganar dinero", callback_data="ganar")],
        [InlineKeyboardButton("🧠 Asesor financiero", callback_data="asesor")],
        [InlineKeyboardButton("👤 Perfil", callback_data="perfil")]
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
        await query.edit_message_text("💰 Ahorro:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Nu", callback_data="app_nu")],
            [InlineKeyboardButton("Klar", callback_data="app_klar")],
            [InlineKeyboardButton("Ualá", callback_data="app_uala")],
            [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
            [InlineKeyboardButton("Hey Banco", callback_data="app_hey")],
            [InlineKeyboardButton("CETES", callback_data="app_cetes")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]))

    elif data == "app_uala":
        await query.edit_message_text(
            "💳 Ualá\nCuenta digital sin comisiones",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Descargar", url="https://www.uala.mx")],
                [InlineKeyboardButton("🔙 Volver", callback_data="ahorro")]
            ])
        )

    elif data == "app_hey":
        await query.edit_message_text(
            "🏦 Hey Banco\nCuenta con rendimiento",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Descargar", url="https://www.heybanco.com")],
                [InlineKeyboardButton("🔙 Volver", callback_data="ahorro")]
            ])
        )

    # =========================
    # CRIPTO
    # =========================
    elif data == "cripto":
        await query.edit_message_text("🪙 Cripto:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
            [InlineKeyboardButton("Bybit", callback_data="app_bybit")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]))

    elif data == "app_bitso":
        await query.edit_message_text(
            "💰 Bitso\nCompra y vende cripto fácil",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a Bitso", url="https://bitso.com")],
                [InlineKeyboardButton("🔙 Volver", callback_data="cripto")]
            ])
        )

    elif data == "app_bybit":
        await query.edit_message_text(
            "📊 Bybit\nTrading avanzado",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a Bybit", url="https://www.bybit.com")],
                [InlineKeyboardButton("🔙 Volver", callback_data="cripto")]
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
            [InlineKeyboardButton("Viewpoints", callback_data="app_view")],
            [InlineKeyboardButton("Nicequest", callback_data="app_nice")],
            [InlineKeyboardButton("🔙", callback_data="ganar")]
        ]))

    elif data == "app_atlas":
        await query.edit_message_text(
            "🌍 Atlas Earth\nGana con terrenos virtuales",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Descargar", url="https://www.atlasearth.com")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ])
        )

    elif data == "app_mode":
        await query.edit_message_text(
            "🎧 Mode\nGana escuchando música",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Descargar", url="https://www.modeapp.com")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ])
        )

    elif data == "app_view":
        await query.edit_message_text(
            "📊 Viewpoints\nEncuestas pagadas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://viewpoints.fb.com")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ])
        )

    elif data == "app_nice":
        await query.edit_message_text(
            "🎁 Nicequest\nGana recompensas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.nicequest.com")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ])
        )

    # =========================
    # ASESOR (YA FUNCIONA)
    # =========================
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 Asesor financiero\n\n"
            "💡 Si eres principiante:\nEmpieza con Nu o CETES\n\n"
            "📈 Si quieres invertir:\nUsa GBM\n\n"
            "🪙 Si te gusta el riesgo:\nCripto (Binance)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ])
        )

    # =========================
    # MENU
    # =========================
    elif data == "menu":
        await query.edit_message_text("Menú 👇", reply_markup=main_menu())

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    asyncio.get_event_loop().run_until_complete(
        app.bot.delete_webhook(drop_pending_updates=True)
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 BOT ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
 
     
