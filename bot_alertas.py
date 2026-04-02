import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
# Variable de entorno en Railway para tu ID de Telegram
ADMIN_ID = int(os.getenv("ADMIN_ID", 0)) 

# =========================
# SISTEMA DE CONTEO (TXTS)
# =========================
def registrar_usuario(user_id):
    """Guarda el ID del usuario para conteo de personas reales."""
    try:
        usuarios = set()
        if os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "r") as f:
                usuarios = set(line.strip() for line in f)
        usuarios.add(str(user_id))
        with open("usuarios.txt", "w") as f:
            for uid in usuarios:
                f.write(f"{uid}\n")
    except: pass

def obtener_conteo():
    """Retorna el número de personas registradas."""
    if not os.path.exists("usuarios.txt"): return 0
    with open("usuarios.txt", "r") as f:
        return len(f.readlines())

# =========================
# LIMPIAR WEBHOOK
# =========================
async def limpiar():
    try:
        bot = Bot(TOKEN)
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.close()
    except: pass

# En Railway esto puede dar conflictos si se ejecuta en cada reinicio, 
# se recomienda dejar que run_polling maneje la conexión.
# asyncio.get_event_loop().run_until_complete(limpiar())

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
    registrar_usuario(update.effective_user.id) # REGISTRAR PERSONA
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# COMANDO ADMIN
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para que veas el conteo en Railway."""
    if update.effective_user.id == ADMIN_ID:
        total = obtener_conteo()
        await update.message.reply_text(f"📊 *Estadísticas*\n\nUsuarios totales: `{total}`", parse_mode="Markdown")

# =========================
# HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ⭐ TOP
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
        # TU LINK DE REFERIDO NU
        url_nu = "https://nu.com.mx"
        await query.edit_message_text(
            formato_app("Nu Bank","Intereses diarios","Bajo","México","Empezar fácil","✔️ Sin comisiones"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url=url_nu)],
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

    elif data == "app_uala":
        await query.edit_message_text(
            formato_app("Ualá","Cuenta digital","Bajo","México","Uso diario"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.uala.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=uala+app+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mp":
        await query.edit_message_text(
            formato_app("MercadoPago","Rendimiento automático","Bajo","México","Ahorro flexible"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.mercadopago.com.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=mercadopago+rendimiento")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_hey":
        await query.edit_message_text(
            formato_app("Hey Banco","Ahorro digital","Bajo","México","Usuarios bancarios"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.heybanco.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=hey+banco+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            formato_app("CETES","Intereses del gobierno","Muy bajo","México","Perfil conservador","✔️ Alta seguridad"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.cetesdirecto.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=cetes+directo+como+invertir")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    # ===== BOLSA =====
    elif data == "bolsa":
        await query.edit_message_text(
            "📈 *Bolsa (riesgo medio)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("GBM+ ⭐", callback_data="app_gbm")],
                [InlineKeyboardButton("Kuspit", callback_data="app_kuspit")],
                [InlineKeyboardButton("Bursanet", callback_data="app_bursanet")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_gbm":
        await query.edit_message_text(
            formato_app("GBM+","Acciones y ETFs","Medio","México","Inversión a largo plazo"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://gbm.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=gbm+como+invertir")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_kuspit":
        await query.edit_message_text(
            formato_app("Kuspit","Acciones y aprendizaje","Medio","México","Principiantes"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.kuspit.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bursanet":
        await query.edit_message_text(
            formato_app("Bursanet","Trading","Medio","México","Avanzados"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://bursanet.mx")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    # ===== CRIPTO =====
    elif data == "cripto":
        await query.edit_message_text(
            "🪙 *Criptomonedas*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance ⭐", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_binance":
        # TU LINK DE REFERIDO BINANCE
        url_bin = "https://binance.com"
        await query.edit_message_text(
            formato_app("Binance","Trading y Staking","Alto","Global","Activos","🎁 Bono USDC con este link."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url=url_bin)],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        # TU LINK DE REFERIDO BITSO
        url_bit = "https://bitso.com"
        await query.edit_message_text(
            formato_app("Bitso","Cripto fácil","Medio","México","Principiantes","⚠️ Usa el código lhubr"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url=url_bit)],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # ===== OTROS =====
    elif data == "ganar":
        await query.edit_message_text(
            "💸 *Formas de ganar dinero*",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menú", callback_data="menu")]]),
            parse_mode="Markdown"
        )

    elif data == "asesor":
        await query.edit_message_text(
            "🧠 *Asesor de inversión*\n\nPróximamente...",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menú", callback_data="menu")]]),
            parse_mode="Markdown"
        )

    elif data == "menu":
        await query.edit_message_text("Selecciona una opción 👇", reply_markup=main_menu(), parse_mode="Markdown")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot activo en Railway.")
    application.run_polling(drop_pending_updates=True)
