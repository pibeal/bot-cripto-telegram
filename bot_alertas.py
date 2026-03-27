import json
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DB_FILE = "users.json"

# =========================
# BASE DE DATOS
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
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except:
        pass

# =========================
# MENÚ PRINCIPAL
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("💸 Ganar dinero", callback_data="ganar")],
        [InlineKeyboardButton("🧠 Asesor financiero", callback_data="asesor")],
        [InlineKeyboardButton("👤 Mi perfil", callback_data="perfil")]
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    user = update.effective_user

    if str(user.id) not in users:
        users[str(user.id)] = {
            "nombre": user.first_name,
            "objetivo": None,
            "riesgo": None,
            "monto": None
        }
        save_users(users)

    await update.message.reply_text(
        "Hola 👋\nSoy *Investia Pro* 💸\n\nSelecciona una opción:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # =========================
    # AHORRO
    # =========================
    if data == "ahorro":
        keyboard = [
            [InlineKeyboardButton("🥇 Nu", callback_data="app_nu")],
            [InlineKeyboardButton("Klar", callback_data="app_klar")],
            [InlineKeyboardButton("Ualá", callback_data="app_uala")],
            [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
            [InlineKeyboardButton("Hey Banco", callback_data="app_hey")],
            [InlineKeyboardButton("CETES", callback_data="app_cetes")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("💰 Opciones de ahorro:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "app_nu":
        await query.edit_message_text(
            "🥇 *Nu Bank*\n\n💰 Alto rendimiento\n📊 Riesgo bajo\n\n✔️ Sin comisiones\n✔️ Rendimientos diarios\n\n💡 Ideal para empezar",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a Nu", url="https://nu.com.mx")],
                [InlineKeyboardButton("🔙 Volver", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            "💳 *Klar*\n\n💰 Rendimiento medio\n📊 Riesgo bajo\n\n✔️ Cuenta digital\n✔️ Tarjeta incluida",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a Klar", url="https://www.klar.mx")],
                [InlineKeyboardButton("🔙 Volver", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mp":
        await query.edit_message_text(
            "💰 *MercadoPago*\n\n✔️ Rendimientos automáticos\n✔️ Dinero disponible\n\n💡 Ideal para ahorro flexible",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a MercadoPago", url="https://www.mercadopago.com.mx")],
                [InlineKeyboardButton("🔙 Volver", callback_data="ahorro")]
            ])
        )

    # =========================
    # BOLSA
    # =========================
    elif data == "bolsa":
        keyboard = [
            [InlineKeyboardButton("🥇 GBM+", callback_data="app_gbm")],
            [InlineKeyboardButton("eToro", callback_data="app_etoro")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("📈 Inversión en bolsa:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "app_gbm":
        await query.edit_message_text(
            "🥇 *GBM+*\n\n📈 Acciones y ETFs\n💰 Rendimiento variable\n\n💡 Ideal para invertir",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a GBM", url="https://gbm.com")],
                [InlineKeyboardButton("🔙 Volver", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # CRIPTO
    # =========================
    elif data == "cripto":
        keyboard = [
            [InlineKeyboardButton("🥇 Binance", callback_data="app_binance")],
            [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
            [InlineKeyboardButton("Bybit", callback_data="app_bybit")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("🪙 Criptomonedas:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "app_binance":
        await query.edit_message_text(
            "🥇 *Binance*\n\n💰 Trading cripto\n📊 Alto riesgo\n\n💡 Para usuarios avanzados",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir a Binance", url="https://www.binance.com")],
                [InlineKeyboardButton("🔙 Volver", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # GANAR DINERO
    # =========================
    elif data == "ganar":
        keyboard = [
            [InlineKeyboardButton("⭐ Apps recomendadas", callback_data="apps_top")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("💸 Ganar dinero online:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "apps_top":
        keyboard = [
            [InlineKeyboardButton("Atlas Earth", callback_data="app_atlas")],
            [InlineKeyboardButton("Mode", callback_data="app_mode")],
            [InlineKeyboardButton("Google Rewards", callback_data="app_google")],
            [InlineKeyboardButton("Viewpoints", callback_data="app_view")],
            [InlineKeyboardButton("Nicequest", callback_data="app_nice")],
            [InlineKeyboardButton("Animal Merge", callback_data="app_animal")],
            [InlineKeyboardButton("🔙 Volver", callback_data="ganar")]
        ]
        await query.edit_message_text("⭐ Apps confiables:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "app_mode":
        await query.edit_message_text(
            "🎧 *Mode App*\n\n💰 Gana escuchando música\n✔️ Ingreso pasivo",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Descargar", url="https://www.modeapp.com")],
                [InlineKeyboardButton("🔙 Volver", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # MENÚ
    # =========================
    elif data == "menu":
        await query.edit_message_text("Menú principal 👇", reply_markup=main_menu())

# =========================
# MAIN (CORREGIDO)
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # 🔥 limpiar conflictos
    asyncio.get_event_loop().run_until_complete(
        app.bot.delete_webhook(drop_pending_updates=True)
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 Investia Pro activo")
    app.run_polling()

if __name__ == "__main__":
    main()
     
