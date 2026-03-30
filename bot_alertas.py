import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# LIMPIAR WEBHOOK
# =========================
async def limpiar():
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.get_event_loop().run_until_complete(limpiar())

# =========================
# MENÚ PRINCIPAL
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Invertir (Bolsa)", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("💸 Ganar dinero", callback_data="ganar")],
        [InlineKeyboardButton("🧠 Asesor inteligente", callback_data="asesor")]
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido a *Investia Pro*\n\n"
        "💸 Tu guía para ahorrar, invertir y ganar dinero.\n\n"
        "Selecciona lo que quieres hacer 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# PLANTILLA RESPUESTA PRO
# =========================
def formato_app(nombre, ganancia, riesgo, disponibilidad, ideal, extra=""):
    return (
        f"💰 *{nombre}*\n\n"
        f"📈 Cómo ganas: {ganancia}\n"
        f"⚠️ Riesgo: {riesgo}\n"
        f"🌎 Disponible en: {disponibilidad}\n"
        f"🎯 Ideal para: {ideal}\n\n"
        f"{extra}"
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
        await query.edit_message_text(
            "💰 *Opciones para ahorrar*\n\nElige una app 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🥇 Nu", callback_data="app_nu")],
                [InlineKeyboardButton("Klar", callback_data="app_klar")],
                [InlineKeyboardButton("CETES", callback_data="app_cetes")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_nu":
        await query.edit_message_text(
            formato_app(
                "Nu Bank",
                "Intereses diarios sobre tu dinero",
                "Bajo",
                "México",
                "Personas que empiezan a ahorrar",
                "✔️ Liquidez diaria\n✔️ Sin comisiones"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://nu.com.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            formato_app(
                "Klar",
                "Intereses por ahorro",
                "Bajo",
                "México",
                "Usuarios que quieren tarjeta + ahorro",
                "✔️ App sencilla\n✔️ Tarjeta incluida"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.klar.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            formato_app(
                "CETES",
                "Intereses del gobierno",
                "Muy bajo",
                "México",
                "Personas conservadoras",
                "✔️ Respaldo gubernamental"
            ),
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
        await query.edit_message_text(
            "📈 *Invertir en bolsa*\n\nSelecciona una plataforma 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🥇 GBM+", callback_data="app_gbm")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_gbm":
        await query.edit_message_text(
            formato_app(
                "GBM+",
                "Compra de acciones y ETFs",
                "Medio",
                "México",
                "Usuarios que quieren invertir a largo plazo",
                "✔️ Acciones (Apple, Tesla)\n✔️ ETFs"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://gbm.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # CRIPTO
    # =========================
    elif data == "cripto":
        await query.edit_message_text(
            "🪙 *Criptomonedas*\n\nSelecciona una plataforma 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_binance":
        await query.edit_message_text(
            formato_app(
                "Binance",
                "Trading, staking y compra de crypto",
                "Alto",
                "Global",
                "Usuarios avanzados",
                "⚠️ Puede ser volátil"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.binance.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            formato_app(
                "Bitso",
                "Compra fácil de criptomonedas",
                "Medio",
                "México",
                "Principiantes en crypto"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://bitso.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # GANAR DINERO
    # =========================
    elif data == "ganar":
        await query.edit_message_text(
            "💸 *Ganar dinero online*\n\nElige una opción 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Apps", callback_data="apps_top")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "apps_top":
        await query.edit_message_text(
            "📱 Apps para ganar dinero 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Google Rewards", callback_data="app_google")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ])
        )

    elif data == "app_google":
        await query.edit_message_text(
            formato_app(
                "Google Rewards",
                "Responder encuestas",
                "Muy bajo",
                "Global",
                "Cualquier persona"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com/store/apps/details?id=com.google.android.apps.paidtasks")],
                [InlineKeyboardButton("🔙", callback_data="apps_top")]
            ]),
            parse_mode="Markdown"
        )

    # =========================
    # ASESOR INTELIGENTE
    # =========================
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 *Asesor Investia*\n\n"
            "Te recomiendo según tu nivel:\n\n"
            "👶 Nuevo → Ahorro (Nu / CETES)\n"
            "📈 Intermedio → GBM+\n"
            "🔥 Avanzado → Cripto\n\n"
            "💡 Próximamente: asesor personalizado automático",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "menu":
        await query.edit_message_text(
            "📌 Menú principal 👇",
            reply_markup=main_menu()
        )

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 INVESTIA PRO MEJORADO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
    
