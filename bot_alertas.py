import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

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

def guardar_usuario(user_id):
    try:
        with open("usuarios.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    if user_id not in data:
        data.append(user_id)
    with open("usuarios.json", "w") as f:
        json.dump(data, f)

# =========================
# FORMATO
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
    guardar_usuario(update.effective_user.id)
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\nSelecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# STATS
# =========================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        users = json.load(open("usuarios.json"))
    except:
        users = []
    try:
        clicks = json.load(open("stats.json"))
    except:
        clicks = {}

    await update.message.reply_text(
        f"👤 Usuarios: {len(users)}\n📊 Clics:\n{clicks}"
    )

# =========================
# HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    guardar_click(data)

    # ===== MENÚ =====
    if data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu())

    # ===== TOP =====
    elif data == "top":
        await query.edit_message_text(
            "⭐ Apps recomendadas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("CETES", callback_data="app_cetes")],
                [InlineKeyboardButton("GBM+", callback_data="app_gbm")],
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("🔙", callback_data="menu")]
            ])
        )

    # ===== AHORRO =====
    elif data == "ahorro":
        await query.edit_message_text(
            "💰 Ahorro",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("Klar", callback_data="app_klar")],
                [InlineKeyboardButton("Ualá", callback_data="app_uala")],
                [InlineKeyboardButton("🔙", callback_data="menu")]
            ])
        )

    elif data == "app_nu":
        await query.edit_message_text(
            formato_app("Nu","Intereses","Bajo","México","Inicio"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Abrir cuenta", url="https://nu.com.mx/mgm/?id=RYg0YDZmlzJyPCGPbpqNXg")],
                [InlineKeyboardButton("🎥 Tutorial", url="https://youtube.com/results?search_query=nu+bank")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    elif data == "app_klar":
        await query.edit_message_text(
            formato_app("Klar","Ahorro","Bajo","México","Inicio"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://klar.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    elif data == "app_uala":
        await query.edit_message_text(
            formato_app("Ualá","Cuenta digital","Bajo","México","Uso diario"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://uala.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ])
        )

    # ===== CRIPTO =====
    elif data == "cripto":
        await query.edit_message_text(
            "🪙 Cripto",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("🔙", callback_data="menu")]
            ])
        )

    elif data == "app_binance":
        await query.edit_message_text(
            formato_app("Binance","Trading","Alto","Global","Avanzado"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Crear cuenta", url="https://www.binance.com/es/referral/...")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ])
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            formato_app("Bitso","Compra","Medio","México","Principiante"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💸 Registro", url="https://bitso.com/...")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ])
        )

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 BOT ACTIVO")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
