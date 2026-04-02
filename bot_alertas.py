import os
import asyncio
import json # Para guardar las estadísticas
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 123456789  # <--- ¡REEMPLAZA ESTO CON TU ID DE TELEGRAM!

# Archivo para guardar usuarios (persistencia)
DB_FILE = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(json.load(f))
    return set()

def guardar_usuario(user_id):
    usuarios = cargar_usuarios()
    usuarios.add(user_id)
    with open(DB_FILE, "w") as f:
        json.dump(list(usuarios), f)

# =========================
# LIMPIAR WEBHOOK
# =========================
async def limpiar():
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.close()

# Esto es mejor manejarlo fuera o al inicio del main
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
    # REGISTRAMOS AL USUARIO
    guardar_usuario(update.effective_user.id)
    
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando secreto para ver estadísticas"""
    if update.effective_user.id == ADMIN_ID:
        usuarios = cargar_usuarios()
        await update.message.reply_text(
            f"📊 *Estadísticas del Bot*\n\n"
            f"👤 Usuarios totales: {len(usuarios)}\n"
            f"IDs: `{list(usuarios)}`",
            parse_mode="Markdown"
        )

# =========================
# HANDLER DE BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await query.edit_message_text("Selecciona una opción 👇", reply_markup=main_menu())

    # ⭐ TOP
    elif data == "top":
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

    # ===== CRIPTO (Agregando Bitso y Binance con tus links) =====
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
        link_binance = "https://binance.com"
        await query.edit_message_text(
            formato_app("Binance","Trading y Staking","Alto","Global","Todo tipo de inversores","🎁 Bono: Reclama recompensa en USDC con este link."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Registrarse en Binance", url=link_binance)],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        link_bitso = "https://bitso.com"
        await query.edit_message_text(
            formato_app("Bitso","Compra/Venta Cripto","Alto","México/Latam","Principiantes","⚠️ IMPORTANTE: Usa el código 'lhubr' al registrarte."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Abrir cuenta Bitso", url=link_bitso)],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # ===== AHORRO (Link de Nu actualizado) =====
    elif data == "app_nu":
        link_nu = "https://nu.com.mx"
        await query.edit_message_text(
            formato_app("Nu Bank","Intereses diarios","Bajo","México","Empezar fácil","✔️ Aprovecha los rendimientos actuales."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Solicitar mi Nu", url=link_nu)],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )
    
    # ... (Aquí irían el resto de tus elif de Klar, CETES, etc. mantenlos igual)

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_stats)) # Comando para ti
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot corriendo...")
    application.run_polling()
