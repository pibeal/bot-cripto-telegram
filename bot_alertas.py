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
# FORMATO PRO
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
# MENÚ
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("💸 Ganar dinero", callback_data="ganar")],
        [InlineKeyboardButton("🧠 Asesor", callback_data="asesor")]
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Aprende a ahorrar, invertir y ganar dinero.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
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

    # ===== AHORRO =====
    if data == "ahorro":
        await query.edit_message_text(
            "💰 *Opciones de ahorro*\n\nElige una 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("Klar", callback_data="app_klar")],
                [InlineKeyboardButton("CETES", callback_data="app_cetes")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_nu":
        await query.edit_message_text(
            formato_app("Nu Bank","Intereses diarios","Bajo","México","Principiantes"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://nu.com.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=nu+bank+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            formato_app("Klar","Ahorro con rendimiento","Bajo","México","Usuarios nuevos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.klar.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=klar+app+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            formato_app("CETES","Intereses del gobierno","Muy bajo","México","Perfil conservador"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.cetesdirecto.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=cetes+directo+como+invertir")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    # ===== CRIPTO =====
    elif data == "cripto":
        await query.edit_message_text(
            "🪙 *Criptomonedas*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_binance":
        await query.edit_message_text(
            formato_app("Binance","Trading y staking","Alto","Global","Usuarios avanzados"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.binance.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=binance+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            formato_app("Bitso","Compra sencilla","Medio","México","Principiantes"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://bitso.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=bitso+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # ===== GANAR =====
    elif data == "ganar":
        await query.edit_message_text(
            "💸 *Ganar dinero online*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Google Rewards", callback_data="app_google")],
                [InlineKeyboardButton("Mode", callback_data="app_mode")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_google":
        await query.edit_message_text(
            formato_app("Google Rewards","Encuestas","Muy bajo","Global","Cualquiera"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com/store/apps/details?id=com.google.android.apps.paidtasks")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=google+rewards+como+funciona")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mode":
        await query.edit_message_text(
            formato_app("Mode","Escuchar música","Bajo","Global","Ingresos pasivos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com/store/apps/details?id=us.current.android")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=mode+earn+app+como+funciona")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    # ===== ASESOR INTELIGENTE =====
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 *Asesor Investia*\n\nSelecciona tu nivel 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👶 Soy nuevo", callback_data="nivel_nuevo")],
                [InlineKeyboardButton("📈 Tengo algo de experiencia", callback_data="nivel_intermedio")],
                [InlineKeyboardButton("🔥 Soy avanzado", callback_data="nivel_avanzado")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "nivel_nuevo":
        await query.edit_message_text(
            "👶 *Recomendación para empezar*\n\n💰 Nu\n🏦 CETES\n\nEmpieza con bajo riesgo 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a ahorro", callback_data="ahorro")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "nivel_intermedio":
        await query.edit_message_text(
            "📈 *Nivel intermedio*\n\n📊 GBM+\n💰 Bitso\n\nDiversifica tus inversiones 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a invertir", callback_data="bolsa")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "nivel_avanzado":
        await query.edit_message_text(
            "🔥 *Nivel avanzado*\n\n🪙 Binance\n📊 Trading\n\nMayor riesgo, mayor potencial 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a cripto", callback_data="cripto")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu())

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 INVESTIA PRO PRO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
