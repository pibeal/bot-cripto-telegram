import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

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
        "💸 Empieza a ganar dinero desde hoy:\n\n"
        "1️⃣ Sin riesgo → Nu\n"
        "2️⃣ Intermedio → Bitso\n"
        "3️⃣ Alto potencial → Binance\n\n"
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
            "💸 Estas son las mejores opciones 👇",
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

    # ===== MENÚ =====
    if data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu())

    # ===== TOP =====
    elif data == "top":
        await query.edit_message_text(
            "⭐ *Apps recomendadas*\n\nEmpieza aquí 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Binance (GANA DINERO)", callback_data="app_binance")],
                [InlineKeyboardButton("💰 Nu Bank", callback_data="app_nu")],
                [InlineKeyboardButton("🇲🇽 Bitso", callback_data="app_bitso")],
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
            "💰 *Nu Bank (AHORRO SEGURO)*\n\n"
            "✔️ Sin comisiones\n"
            "✔️ Intereses diarios\n"
            "✔️ Fácil de usar\n\n"
            "🎁 Beneficios por registrarte\n\n"
            "👇 Crea tu cuenta GRATIS:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Abrir cuenta gratis", url="https://nu.com.mx/mgm/?id=RYg0YDZmlzJyPCGPbpqNXg&msg=06478&utm_channel=referral&utm_medium=other&utm_source=mgm")],
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
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_uala":
        await query.edit_message_text(
            formato_app("Ualá","Cuenta digital","Bajo","México","Uso diario"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.uala.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mp":
        await query.edit_message_text(
            formato_app("MercadoPago","Rendimiento automático","Bajo","México","Ahorro flexible"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.mercadopago.com.mx")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_hey":
        await query.edit_message_text(
            formato_app("Hey Banco","Ahorro digital","Bajo","México","Usuarios bancarios"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.heybanco.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            formato_app("CETES","Intereses del gobierno","Muy bajo","México","Perfil conservador"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.cetesdirecto.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    # ===== CRIPTO =====
    elif data == "cripto":
        await query.edit_message_text(
            "🪙 *Cripto (alto riesgo)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Binance (GANA DINERO)", callback_data="app_binance")],
                [InlineKeyboardButton("🇲🇽 Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("Bybit", callback_data="app_bybit")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_binance":
        await query.edit_message_text(
            "🔥 *Binance (RECOMENDADO)*\n\n"
            "💰 Gana dinero con criptomonedas\n"
            "📈 Trading + staking\n\n"
            "🎁 Bonos disponibles al registrarte\n\n"
            "👇 Crea tu cuenta GRATIS:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Crear cuenta y ganar", url="https://www.binance.com/es/referral/earn-together/refer2earn-usdc/claim?hl=es&ref=GRO_28502_HDMUZ&utm_source=referral_entrance")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            "🇲🇽 *Bitso (Fácil para empezar)*\n\n"
            "💰 Compra criptomonedas en pesos\n"
            "🎁 Gana dinero al registrarte\n\n"
            "📌 Código: *lhubr*\n\n"
            "👇 Empieza aquí:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💸 Registrarme y ganar", url="https://bitso.com/mx?adjust_referrer=adjust_reftag%3DcKzPOs3voLNkv")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # ===== GANAR DINERO =====
    elif data == "ganar":
        await query.edit_message_text(
            "💸 *Ganar dinero*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Google Rewards", callback_data="app_google")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_google":
        await query.edit_message_text(
            formato_app("Google Rewards","Encuestas","Muy bajo","Global","Cualquiera"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    # ===== ASESOR =====
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 *Asesor Investia*\n\nSelecciona tu nivel 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👶 Nuevo", callback_data="nivel_nuevo")],
                [InlineKeyboardButton("📈 Intermedio", callback_data="nivel_intermedio")],
                [InlineKeyboardButton("🔥 Avanzado", callback_data="nivel_avanzado")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "nivel_nuevo":
        await query.edit_message_text(
            "👶 Empieza con bajo riesgo 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a ahorro", callback_data="ahorro")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ])
        )

    elif data == "nivel_intermedio":
        await query.edit_message_text(
            "📈 Nivel intermedio 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a bolsa", callback_data="bolsa")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ])
        )

    elif data == "nivel_avanzado":
        await query.edit_message_text(
            "🔥 Nivel avanzado 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a cripto", callback_data="cripto")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
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
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("🔥 INVESTIA PRO MAX ACTIVO")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
