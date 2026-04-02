import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 123456789  # <--- REEMPLAZA ESTO CON TU ID DE TELEGRAM

# =========================
# SISTEMA DE CONTEO
# =========================
def registrar_usuario(user_id):
    try:
        usuarios = set()
        if os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "r") as f:
                usuarios = set(line.strip() for line in f)
        usuarios.add(str(user_id))
        with open("usuarios.txt", "w") as f:
            for uid in usuarios:
                f.write(f"{uid}\n")
    except:
        pass

def obtener_conteo():
    if not os.path.exists("usuarios.txt"): return 0
    with open("usuarios.txt", "r") as f:
        return len(f.readlines())

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
# MENÚS
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
# COMANDOS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    registrar_usuario(update.effective_user.id)
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        total = obtener_conteo()
        await update.message.reply_text(f"📊 *Estadísticas*\n\nUsuarios únicos: `{total}`", parse_mode="Markdown")

# =========================
# HANDLER DE BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await query.edit_message_text("Selecciona una opción 👇", reply_markup=main_menu())

    elif data == "top":
        await query.edit_message_text(
            "⭐ *Apps recomendadas*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("CETES", callback_data="app_cetes")],
                [InlineKeyboardButton("GBM+", callback_data="app_gbm")],
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]), parse_mode="Markdown"
        )

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
            ]), parse_mode="Markdown"
        )

    # --- DETALLES DE APPS ---
    elif data == "app_nu":
        link_nu = "https://nu.com.mx"
        await query.edit_message_text(
            formato_app("Nu Bank","Intereses diarios","Bajo","México","Empezar fácil","✔️ Sin comisiones"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url=link_nu)],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            formato_app("Klar","Ahorro con rendimiento","Bajo","México","Usuarios nuevos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://klar.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_uala":
        await query.edit_message_text(
            formato_app("Ualá","Cuenta digital","Bajo","México","Uso diario"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://uala.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_mp":
        await query.edit_message_text(
            formato_app("MercadoPago","Rendimiento automático","Bajo","México","Ahorro flexible"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://mercadopago.com.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_hey":
        await query.edit_message_text(
            formato_app("Hey Banco","Ahorro digital","Bajo","México","Usuarios bancarios"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://heybanco.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            formato_app("CETES","Intereses del gobierno","Muy bajo","México","Perfil conservador","✔️ Alta seguridad"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://cetesdirecto.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]), parse_mode="Markdown"
        )

    elif data == "bolsa":
        await query.edit_message_text(
            "📈 *Bolsa (riesgo medio)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("GBM+ ⭐", callback_data="app_gbm")],
                [InlineKeyboardButton("Kuspit", callback_data="app_kuspit")],
                [InlineKeyboardButton("Bursanet", callback_data="app_bursanet")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_gbm":
        await query.edit_message_text(
            formato_app("GBM+","Acciones y ETFs","Medio","México","Inversión a largo plazo"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://gbm.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]), parse_mode="Markdown"
        )

    elif data == "cripto":
        await query.edit_message_text(
            "🪙 *Criptomonedas*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance ⭐", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_binance":
        link_binance = "https://binance.com"
        await query.edit_message_text(
            formato_app("Binance","Trading Cripto","Alto","Global","Inversores activos","🎁 Recompensa en USDC con este link."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url=link_binance)],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]), parse_mode="Markdown"
        )

    elif data == "app_bitso":
        link_bitso = "https://bitso.com"
        await query.edit_message_text(
            formato_app("Bitso","Cripto fácil","Alto","México","Principiantes","⚠️ Código sugerido: lhubr"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url=link_bitso)],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://youtube.com")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]), parse_mode="Markdown"
        )

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot activo. Usa /admin para estadísticas.")
    application.run_polling(drop_pending_updates=True)


        )
