import json
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

DB_FILE = "users.json"

# =========================
# 📁 BASE DE DATOS SEGURA
# =========================
def load_users():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except:
        return {}

def save_users(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error guardando usuarios:", e)

# =========================
# 📱 MENÚ PRINCIPAL
# =========================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Ahorrar", callback_data="ahorrar")],
        [InlineKeyboardButton("📈 Invertir", callback_data="invertir")],
        [InlineKeyboardButton("👤 Mi perfil", callback_data="perfil")]
    ]
    return InlineKeyboardMarkup(keyboard)

# =========================
# 🚀 START
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
        f"Hola {user.first_name} 👋\nSoy *Investia Pro*\n\n¿Qué quieres hacer hoy?",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# 🔘 BOTONES
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    users = load_users()
    user_id = str(query.from_user.id)
    data = query.data

    # Seguridad extra (por si Railway borra datos)
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
    if data == "ahorrar":
        keyboard = [
            [InlineKeyboardButton("🚨 Emergencia", callback_data="obj_emergencia")],
            [InlineKeyboardButton("✈️ Viaje", callback_data="obj_viaje")],
            [InlineKeyboardButton("🏠 Casa", callback_data="obj_casa")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]
        await query.edit_message_text(
            "¿Para qué quieres ahorrar?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("obj_"):
        objetivo = data.split("_")[1]
        users[user_id]["objetivo"] = objetivo
        save_users(users)

        keyboard = [
            [InlineKeyboardButton("$500 - $1000", callback_data="monto_1000")],
            [InlineKeyboardButton("$1000 - $5000", callback_data="monto_5000")],
            [InlineKeyboardButton("$5000+", callback_data="monto_10000")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]

        await query.edit_message_text(
            "¿Cuánto puedes ahorrar al mes?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("monto_"):
        monto = data.split("_")[1]
        users[user_id]["monto"] = monto
        save_users(users)

        recomendacion = generar_recomendacion(users[user_id])

        await query.edit_message_text(
            recomendacion,
            reply_markup=main_menu()
        )

    # =========================
    # INVERTIR
    # =========================
    elif data == "invertir":
        keyboard = [
            [InlineKeyboardButton("🟢 Bajo riesgo", callback_data="riesgo_bajo")],
            [InlineKeyboardButton("🟡 Medio riesgo", callback_data="riesgo_medio")],
            [InlineKeyboardButton("🔴 Alto riesgo", callback_data="riesgo_alto")],
            [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
        ]

        await query.edit_message_text(
            "¿Qué nivel de riesgo prefieres?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("riesgo_"):
        riesgo = data.split("_")[1]
        users[user_id]["riesgo"] = riesgo
        save_users(users)

        texto = generar_inversion(users[user_id])

        await query.edit_message_text(
            texto,
            reply_markup=main_menu()
        )

    # =========================
    # PERFIL
    # =========================
    elif data == "perfil":
        perfil = users[user_id]

        texto = f"""
👤 *Tu perfil*

Objetivo: {perfil['objetivo']}
Riesgo: {perfil['riesgo']}
Ahorro mensual: {perfil['monto']}
"""

        await query.edit_message_text(
            texto,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

    # =========================
    # MENÚ
    # =========================
    elif data == "menu":
        await query.edit_message_text(
            "Menú principal 👇",
            reply_markup=main_menu()
        )

# =========================
# 🧠 LÓGICA
# =========================
def generar_recomendacion(user):
    objetivo = user["objetivo"]
    monto = user["monto"]

    if objetivo == "emergencia":
        return f"""
🚨 Fondo de emergencia

Te recomiendo:
- Nu
- MercadoPago

💡 Ahorra 3-6 meses de gastos
Monto: ${monto}
"""

    elif objetivo == "viaje":
        return f"""
✈️ Ahorro para viaje

Te recomiendo:
- Cuenta con rendimiento
- Ahorro automático

Monto: ${monto}
"""

    elif objetivo == "casa":
        return f"""
🏠 Ahorro para casa

Te recomiendo:
- CETES
- Inversión segura

Monto: ${monto}
"""

    return "Sigue explorando 💡"

def generar_inversion(user):
    riesgo = user["riesgo"]

    if riesgo == "bajo":
        return """
🟢 Bajo riesgo

- CETES
- Bonos

✔️ Seguro
"""

    elif riesgo == "medio":
        return """
🟡 Riesgo medio

- ETFs

✔️ Balance
"""

    elif riesgo == "alto":
        return """
🔴 Alto riesgo

- Cripto
- Acciones

⚠️ Volátil
"""

    return "Define tu perfil"

# =========================
# ▶️ MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot en ejecución 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()

  
