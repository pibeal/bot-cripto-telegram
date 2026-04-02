import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# =========================
# REGISTRO DE USUARIOS
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
    except: pass

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
        "👋 *Bienvenido a Investia Pro*\n\nSelecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        total = obtener_conteo()
        await update.message.reply_text(f"📊 *Estadísticas*\n\nUsuarios: `{total}`", parse_mode="Markdown")

# =========================
# HANDLER DE BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- MENÚS PRINCIPALES ---
    if data == "menu":
        await query.edit_message_text("Selecciona una opción 👇", reply_markup=main_menu(), parse_mode="Markdown")

    elif data == "top":
        await query.edit_message_text("⭐ *Recomendados*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Nu", callback_data="app_nu")], [InlineKeyboardButton("CETES", callback_data="app_cetes")],
            [InlineKeyboardButton("GBM+", callback_data="app_gbm")], [InlineKeyboardButton("Binance", callback_data="app_binance")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "ahorro":
        await query.edit_message_text("💰 *Ahorro*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Nu ⭐", callback_data="app_nu")], [InlineKeyboardButton("Klar", callback_data="app_klar")],
            [InlineKeyboardButton("Ualá", callback_data="app_uala")], [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
            [InlineKeyboardButton("Hey Banco", callback_data="app_hey")], [InlineKeyboardButton("CETES ⭐", callback_data="app_cetes")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "bolsa":
        await query.edit_message_text("📈 *Bolsa*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("GBM+ ⭐", callback_data="app_gbm")], [InlineKeyboardButton("Kuspit", callback_data="app_kuspit")],
            [InlineKeyboardButton("Bursanet", callback_data="app_bursanet")], [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "cripto":
        await query.edit_message_text("🪙 *Cripto*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Binance ⭐", callback_data="app_binance")], [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "ganar":
        await query.edit_message_text("💸 *Ganar Dinero*\n\nPróximamente...", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menú", callback_data="menu")]]), parse_mode="Markdown")

    elif data == "asesor":
        await query.edit_message_text("🧠 *Asesor*\n\nPróximamente...", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menú", callback_data="menu")]]), parse_mode="Markdown")

    # --- DETALLES DE APPS ---
    elif data == "app_nu":
        url = "https://nu.com.mx"
        await query.edit_message_text(formato_app("Nu Bank","Rendimiento diario","Bajo","México","Ahorro fácil"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url=url)], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_binance":
        url = "https://binance.com"
        await query.edit_message_text(formato_app("Binance","Trading","Alto","Global","Activos"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url=url)], [InlineKeyboardButton("🔙", callback_data="cripto")]]), parse_mode="Markdown")

    elif data == "app_bitso":
        url = "https://bitso.com"
        await query.edit_message_text(formato_app("Bitso","Cripto","Alto","México","Principiantes","⚠️ Código: lhubr"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url=url)], [InlineKeyboardButton("🔙", callback_data="cripto")]]), parse_mode="Markdown")

    elif data == "app_klar":
        await query.edit_message_text(formato_app("Klar","Ahorro","Bajo","México","Nuevos"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://klar.mx")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_cetes":
        await query.edit_message_text(formato_app("CETES","Seguridad","Mínimo","México","Conservadores"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://cetesdirecto.com")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_gbm":
        await query.edit_message_text(formato_app("GBM+","Acciones","Medio","México","Inversores"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://gbm.com")], [InlineKeyboardButton("🔙", callback_data="bolsa")]]), parse_mode="Markdown")

    elif data == "app_kuspit":
        await query.edit_message_text(formato_app("Kuspit","Aprendizaje","Bajo","México","Estudiantes"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://kuspit.com")], [InlineKeyboardButton("🔙", callback_data="bolsa")]]), parse_mode="Markdown")

    elif data == "app_bursanet":
        await query.edit_message_text(formato_app("Bursanet","Trading","Medio","México","Pro"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://bursanet.mx")], [InlineKeyboardButton("🔙", callback_data="bolsa")]]), parse_mode="Markdown")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling(drop_pending_updates=True)
