import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DB_FILE = "users.json"

# =========================
# BASE DE DATOS SEGURA
# =========================
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_users(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except:
        pass

# =========================
# MENÚ PRINCIPAL
# =========================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Criptomonedas", callback_data="cripto")],
        [InlineKeyboardButton("🧠 Asesor financiero", callback_data="asesor")],
        [InlineKeyboardButton("👤 Mi perfil", callback_data="perfil")]
    ]
    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users = load_users()

    if str(user.id) not in users:
        users[str(user.id)] = {
            "nombre": user.first_name,
            "objetivo": None,
            "riesgo": None,
            "monto": None
        }
        save_users(users)

    await update.message.reply_text(
        f"Hola {user.first_name} 👋\nSoy Investia Pro 💸\n\nElige una opción:",
        reply_markup=main_menu()
    )

# =========================
# BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    users = load_users()
    user_id = str(query.from_user.id)
    data = query.data

    if user_id not in users:
        users[user_id] = {
            "nombre": query.from_user.first_name,
            "objetivo": None,
            "riesgo": None,
            "monto": None
        }

    # =========================
    # AHORRO
    # =========================
    if data == "ahorro":
        keyboard = [
            [InlineKeyboardButton("Nu", url="https://nu.com.mx")],
            [InlineKeyboardButton("MercadoPago", url="https://www.mercadopago.com.mx")],
            [InlineKeyboardButton("Klar", url="https://www.klar.mx")],
            [InlineKeyboardButton("Ualá", url="https://www.uala.mx")],
            [InlineKeyboardButton("Hey Banco", url="https://heybanco.santander.com.mx/")],
            [InlineKeyboardButton("CETES", url="https://www.cetesdirecto.com")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("💰 Opciones para ahorrar:", reply_markup=InlineKeyboardMarkup(keyboard))

    # =========================
    # BOLSA
    # =========================
    elif data == "bolsa":
        keyboard = [
            [InlineKeyboardButton("GBM+", url="https://gbm.com")],
            [InlineKeyboardButton("Bitso (acciones USA)", url="https://bitso.com")],
            [InlineKeyboardButton("eToro", url="https://www.etoro.com")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("📈 Inversión en bolsa:", reply_markup=InlineKeyboardMarkup(keyboard))

    # =========================
    # CRIPTO
    # =========================
    elif data == "cripto":
        keyboard = [
            [InlineKeyboardButton("Bitso", url="https://bitso.com")],
            [InlineKeyboardButton("Binance", url="https://www.binance.com")],
            [InlineKeyboardButton("Bybit", url="https://www.bybit.com")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("🪙 Criptomonedas:", reply_markup=InlineKeyboardMarkup(keyboard))

    # =========================
    # ASESOR
    # =========================
    elif data == "asesor":
        keyboard = [
            [InlineKeyboardButton("💰 Ahorrar", callback_data="ahorrar")],
            [InlineKeyboardButton("📈 Invertir", callback_data="invertir")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text("🧠 Asesor financiero\n¿Qué quieres hacer?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "ahorrar":
        keyboard = [
            [InlineKeyboardButton("Emergencia", callback_data="obj_emergencia")],
            [InlineKeyboardButton("Viaje", callback_data="obj_viaje")],
            [InlineKeyboardButton("Casa", callback_data="obj_casa")]
        ]
        await query.edit_message_text("¿Para qué quieres ahorrar?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("obj_"):
        users[user_id]["objetivo"] = data.split("_")[1]
        save_users(users)

        keyboard = [
            [InlineKeyboardButton("$500-$1000", callback_data="monto_1000")],
            [InlineKeyboardButton("$1000-$5000", callback_data="monto_5000")],
            [InlineKeyboardButton("$5000+", callback_data="monto_10000")]
        ]
        await query.edit_message_text("¿Cuánto ahorrarás al mes?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("monto_"):
        users[user_id]["monto"] = data.split("_")[1]
        save_users(users)

        await query.edit_message_text(
            "💡 Recomendación:\nEmpieza con Nu, Klar o CETES según tu objetivo",
            reply_markup=main_menu()
        )

    elif data == "invertir":
        keyboard = [
            [InlineKeyboardButton("Bajo", callback_data="riesgo_bajo")],
            [InlineKeyboardButton("Medio", callback_data="riesgo_medio")],
            [InlineKeyboardButton("Alto", callback_data="riesgo_alto")]
        ]
        await query.edit_message_text("Nivel de riesgo:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("riesgo_"):
        users[user_id]["riesgo"] = data.split("_")[1]
        save_users(users)

        await query.edit_message_text(
            "📊 Recomendación:\nGBM (seguro), eToro (medio), Binance (alto)",
            reply_markup=main_menu()
        )

    # =========================
    # PERFIL
    # =========================
    elif data == "perfil":
        perfil = users[user_id]
        await query.edit_message_text(
            f"👤 Perfil\nObjetivo: {perfil['objetivo']}\nRiesgo: {perfil['riesgo']}\nMonto: {perfil['monto']}",
            reply_markup=main_menu()
        )

    elif data == "menu":
        await query.edit_message_text("Menú principal 👇", reply_markup=main_menu())

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot activo 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()

   
  
