import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

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
    registrar_usuario(update.effective_user.id)
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# ADMIN
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        total = obtener_conteo()
        await update.message.reply_text(f"📊 *Estadísticas*\n\nUsuarios totales: `{total}`", parse_mode="Markdown")

# =========================
# HANDLER DE BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- MENÚS ---
    if data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu(), parse_mode="Markdown")

    elif data == "top":
        await query.edit_message_text("⭐ *Apps recomendadas*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Nu", callback_data="app_nu")], [InlineKeyboardButton("CETES", callback_data="app_cetes")],
            [InlineKeyboardButton("GBM+", callback_data="app_gbm")], [InlineKeyboardButton("Binance", callback_data="app_binance")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "ahorro":
        await query.edit_message_text("💰 *Ahorro (bajo riesgo)*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Nu ⭐", callback_data="app_nu")], [InlineKeyboardButton("Klar", callback_data="app_klar")],
            [InlineKeyboardButton("Ualá", callback_data="app_uala")], [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
            [InlineKeyboardButton("Hey Banco", callback_data="app_hey")], [InlineKeyboardButton("CETES ⭐", callback_data="app_cetes")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "bolsa":
        await query.edit_message_text("📈 *Bolsa (riesgo medio)*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("GBM+ ⭐", callback_data="app_gbm")], [InlineKeyboardButton("Kuspit", callback_data="app_kuspit")],
            [InlineKeyboardButton("Bursanet", callback_data="app_bursanet")], [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    elif data == "cripto":
        await query.edit_message_text("🪙 *Criptomonedas*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Binance ⭐", callback_data="app_binance")], [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]), parse_mode="Markdown")

    # --- APPS ESPECÍFICAS (AHORRO/BOLSA/CRIPTO) ---
    elif data == "app_nu":
        url_nu = "https://nu.com.mx"
        await query.edit_message_text(formato_app("Nu Bank","Intereses diarios","Bajo","México","Empezar fácil"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url=url_nu)], [InlineKeyboardButton("🎥 Tutorial", url="https://youtube.com")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_klar":
        await query.edit_message_text(formato_app("Klar","Rendimiento","Bajo","México","Nuevos"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://klar.mx")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_uala":
        await query.edit_message_text(formato_app("Ualá","Cuenta digital","Bajo","México","Diario"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://uala.mx")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_mp":
        await query.edit_message_text(formato_app("MercadoPago","Rendimiento","Bajo","México","Ahorro"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://mercadopago.com.mx")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_hey":
        await query.edit_message_text(formato_app("Hey Banco","Ahorro","Bajo","México","Usuarios"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://heybanco.com")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_cetes":
        await query.edit_message_text(formato_app("CETES","Seguridad","Muy bajo","México","Conservadores"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://cetesdirecto.com")], [InlineKeyboardButton("🔙", callback_data="ahorro")]]), parse_mode="Markdown")

    elif data == "app_gbm":
        await query.edit_message_text(formato_app("GBM+","Acciones","Medio","México","Largo plazo"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://gbm.com")], [InlineKeyboardButton("🔙", callback_data="bolsa")]]), parse_mode="Markdown")

    elif data == "app_kuspit":
        await query.edit_message_text(formato_app("Kuspit","Aprendizaje","Bajo","México","Aprender"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://kuspit.com")], [InlineKeyboardButton("🔙", callback_data="bolsa")]]), parse_mode="Markdown")

    elif data == "app_bursanet":
        await query.edit_message_text(formato_app("Bursanet","Trading","Medio","México","Pro"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://bursanet.mx")], [InlineKeyboardButton("🔙", callback_data="bolsa")]]), parse_mode="Markdown")

    elif data == "app_binance":
        url_bin = "https://binance.com"
        await query.edit_message_text(formato_app("Binance","Trading","Alto","Global","Activos"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url=url_bin)], [InlineKeyboardButton("🔙", callback_data="cripto")]]), parse_mode="Markdown")

    elif data == "app_bitso":
        url_bit = "https://bitso.com"
        await query.edit_message_text(formato_app("Bitso","Cripto fácil","Medio","México","Principiantes","🎁 Código: lhubr"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url=url_bit)], [InlineKeyboardButton("🔙", callback_data="cripto")]]), parse_mode="Markdown")

    # ===== GANAR DINERO =====
    elif data == "ganar":
        await query.edit_message_text("💸 *Ganar dinero*", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Google Rewards ⭐", callback_data="app_google")], [InlineKeyboardButton("Viewpoints", callback_data="app_view")],
                [InlineKeyboardButton("Nicequest", callback_data="app_nice")], [InlineKeyboardButton("Mode", callback_data="app_mode")],
                [InlineKeyboardButton("Atlas Earth", callback_data="app_atlas")], [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]), parse_mode="Markdown")

    elif data == "app_google":
        await query.edit_message_text(formato_app("Google Rewards","Encuestas","Muy bajo","Global","Cualquiera"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://google.com")], [InlineKeyboardButton("🔙", callback_data="ganar")]]), parse_mode="Markdown")

    elif data == "app_view":
        await query.edit_message_text(formato_app("Viewpoints","Encuestas","Muy bajo","Global","Casual"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://fb.com")], [InlineKeyboardButton("🔙", callback_data="ganar")]]), parse_mode="Markdown")

    elif data == "app_nice":
        await query.edit_message_text(formato_app("Nicequest","Encuestas","Muy bajo","Global","Pacientes"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://nicequest.com")], [InlineKeyboardButton("🔙", callback_data="ganar")]]), parse_mode="Markdown")

    elif data == "app_mode":
        await query.edit_message_text(formato_app("Mode","Música","Bajo","Global","Pasivos"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://current.us")], [InlineKeyboardButton("🔙", callback_data="ganar")]]), parse_mode="Markdown")

    elif data == "app_atlas":
        await query.edit_message_text(formato_app("Atlas Earth","Renta virtual","Medio","Global","Curiosos"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📲 Ir", url="https://google.com")], [InlineKeyboardButton("🔙", callback_data="ganar")]]), parse_mode="Markdown")

    # ===== ASESOR =====
    elif data == "asesor":
        await query.edit_message_text("🧠 *Asesor Investia*\n\nSelecciona tu nivel 👇", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👶 Nuevo", callback_data="nivel_nuevo")], [InlineKeyboardButton("📈 Intermedio", callback_data="nivel_intermedio")],
                [InlineKeyboardButton("🔥 Avanzado", callback_data="nivel_avanzado")], [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]), parse_mode="Markdown")

    elif data == "nivel_nuevo":
        await query.edit_message_text("👶 Empieza con bajo riesgo 👇", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ir a ahorro", callback_data="ahorro")], [InlineKeyboardButton("🔙", callback_data="asesor")]]))

    elif data == "nivel_intermedio":
        await query.edit_message_text("📈 Nivel intermedio 👇", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ir a bolsa", callback_data="bolsa")], [InlineKeyboardButton("🔙", callback_data="asesor")]]))

    elif data == "nivel_avanzado":
        await query.edit_message_text("🔥 Nivel avanzado 👇", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ir a cripto", callback_data="cripto")], [InlineKeyboardButton("🔙", callback_data="asesor")]]))

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("🔥 INVESTIA PRO MAX ACTIVO")
    application.run_polling(drop_pending_updates=True)
