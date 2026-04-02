import os
import json
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# TRACKING
# =========================
def guardar_click(opcion):
    try:
        with open("stats.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[opcion] = data.get(opcion, 0) + 1

    with open("stats.json", "w") as f:
        json.dump(data, f)

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
# MENÚ PRINCIPAL
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Recomendado", callback_data="top")],
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
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# RESPUESTAS INTELIGENTES
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "ganar dinero" in text:
        await update.message.reply_text(
            "💸 Opciones para ganar dinero 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ver opciones", callback_data="ganar")]
            ])
        )

    elif "invertir" in text:
        await update.message.reply_text(
            "📈 Empieza aquí 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a bolsa", callback_data="bolsa")]
            ])
        )

# =========================
# HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    guardar_click(data)

    if data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu())

    elif data == "top":
        await query.edit_message_text(
            "⭐ Apps recomendadas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ])
        )

# =========================
# ERROR HANDLER
# =========================
async def error_handler(update, context):
    print("❌ Error:", context.error)

# =========================
# MAIN
# =========================
def main():
    print("🚀 Iniciando Investia...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error_handler)

    print("🔥 INVESTIA PRO ACTIVO")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
