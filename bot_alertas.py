import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# TRACKING CLICKS
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
# TRACKING USUARIOS
# =========================
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
    guardar_usuario(update.effective_user.id)

    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# STATS
# =========================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("usuarios.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    try:
        with open("stats.json", "r") as f:
            clicks = json.load(f)
    except:
        clicks = {}

    await update.message.reply_text(
        f"📊 *Estadísticas*\n\n👤 Usuarios: {len(users)}\n\n📈 Clics:\n{clicks}",
        parse_mode="Markdown"
    )

# =========================
# HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    guardar_click(data)

    # ===== TOP =====
    if data == "top":
        await query.edit_message_text(
            "⭐ *Apps recomendadas*\n\nEmpieza aquí 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("CETES", callback_data="app_cetes")],
                [InlineKeyboardButton("GBM+", callback_data="app_gbm")],
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    # ===== AHORRO =====
    elif data == "ahorro":
        await query.edit_message_text(
            "💰 *Ahorro (bajo riesgo)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu ⭐", callback_data="app_nu")],
                [InlineKeyboardButton("Klar", callback_data="app_klar")],
                [InlineKeyboardButton("Ualá", callback_data="app_uala")],
                [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
                [InlineKeyboardButton("Hey Banco", callback_data="app_hey")],
                [InlineKeyboardButton("CETES ⭐", callback_data="app_cetes")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_nu":
        await query.edit_message_text(
            formato_app("Nu Bank","Intereses diarios","Bajo","México","Empezar fácil"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Abrir cuenta (BONO)", url="https://nu.com.mx/mgm/?id=RYg0YDZmlzJyPCGPbpqNXg&msg=06478&utm_channel=referral&utm_medium=other&utm_source=mgm")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=nu+bank+como+usar")],
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
            "🪙 *Cripto (alto riesgo)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance ⭐", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_binance":
        await query.edit_message_text(
            formato_app("Binance","Trading","Alto","Global","Avanzados"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Crear cuenta (BONO)", url="https://www.binance.com/es/referral/earn-together/refer2earn-usdc/claim?hl=es&ref=GRO_28502_HDMUZ&utm_source=referral_entrance")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=binance+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            formato_app("Bitso","Compra sencilla","Medio","México","Principiantes"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💸 Registrarme (BONO)", url="https://bitso.com/mx?adjust_referrer=adjust_reftag%3DcKzPOs3voLNkv")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=bitso+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # ===== MENÚ =====
    elif data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu())

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 INVESTIA PRO MAX ACTIVO")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
