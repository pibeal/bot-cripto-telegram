import os
import json
import requests
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

# 📂 CARGAR DATA
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 📂 USUARIOS
def cargar_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return []

def guardar_user(user_id):
    users = cargar_users()
    if user_id not in users:
        users.append(user_id)
        with open("users.json", "w") as f:
            json.dump(users, f)

# ⚠️ AVISO
async def aviso(update):
    await update.message.reply_text(
        "⚠️ Esto no es asesoría financiera. Toda inversión tiene riesgo."
    )

# 💰 PRECIO BTC
def precio(coin="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        return requests.get(url, timeout=10).json()[coin]["usd"]
    except:
        return None

# 🔔 ALERTAS AUTOMÁTICAS (SIN BUG)
async def enviar_alertas(app):
    ultimo_precio = None

    while True:
        try:
            btc = precio("bitcoin")

            if btc and btc < 100000 and btc != ultimo_precio:
                users = cargar_users()

                for u in users:
                    try:
                        await app.bot.send_message(
                            chat_id=u,
                            text=f"🚨 ALERTA BTC\nBitcoin está en ${btc}"
                        )
                    except:
                        pass

                ultimo_precio = btc

        except Exception as e:
            print("Error alertas:", e)

        await asyncio.sleep(300)  # cada 5 minutos

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    guardar_user(user_id)

    texto = (
        "💸 *FINANCE BOT PRO*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "Encuentra, compara y monitorea inversiones.\n\n"
        "👇 Elige una opción:"
    )

    keyboard = [
        [
            InlineKeyboardButton("💰 Ahorro", callback_data="ahorro"),
            InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")
        ],
        [
            InlineKeyboardButton("🪙 Cripto", callback_data="cripto"),
            InlineKeyboardButton("🏆 Ranking", callback_data="ranking")
        ],
        [
            InlineKeyboardButton("🆚 Comparar", callback_data="comparar")
        ]
    ]

    await update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

    await aviso(update)

# 📊 MOSTRAR OPCIONES
async def mostrar(update, tipo):
    resultados = [x for x in data if x["tipo"] == tipo]

    mensaje = f"*{tipo.upper()}*\n━━━━━━━━━━━━━━━\n\n"
    botones = []

    for r in resultados:
        mensaje += (
            f"🏦 *{r['nombre']}*\n"
            f"• Rendimiento: {r.get('rendimiento','N/A')}\n"
            f"• Liquidez: {r.get('liquidez','N/A')}\n"
            f"• Riesgo: {r['riesgo']}\n"
            f"• {r.get('descripcion','')}\n\n"
        )

        botones.append([
            InlineKeyboardButton(f"Abrir {r['nombre']}", url=r["link"])
        ])

    await update.message.reply_text(
        mensaje,
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode=ParseMode.MARKDOWN
    )

# 🏆 RANKING
async def ranking(update):
    def score(app):
        puntos = 0

        if app["riesgo"] == "bajo":
            puntos += 3
        elif app["riesgo"] == "medio":
            puntos += 2
        else:
            puntos += 1

        if "alta" in app.get("liquidez", ""):
            puntos += 2

        if "hasta" in app.get("rendimiento", ""):
            puntos += 2

        return puntos

    orden = sorted(data, key=score, reverse=True)

    mensaje = "*🏆 TOP OPCIONES*\n━━━━━━━━━━━━━━━\n\n"

    for i, r in enumerate(orden[:5], 1):
        mensaje += (
            f"{i}. *{r['nombre']}*\n"
            f"• Tipo: {r['tipo']}\n"
            f"• Rendimiento: {r.get('rendimiento')}\n\n"
        )

    await update.message.reply_text(
        mensaje,
        parse_mode=ParseMode.MARKDOWN
    )

# 🆚 COMPARADOR
async def comparar(update):
    ahorro = [x for x in data if x["tipo"] == "ahorro"]

    if len(ahorro) < 2:
        await update.message.reply_text("No hay suficientes opciones.")
        return

    a, b = ahorro[0], ahorro[1]

    mensaje = (
        "🆚 *COMPARACIÓN*\n━━━━━━━━━━━━━━━\n\n"
        f"*{a['nombre']} vs {b['nombre']}*\n\n"
        f"💰 Rendimiento:\n{a['rendimiento']} vs {b['rendimiento']}\n\n"
        f"⚠️ Riesgo:\n{a['riesgo']} vs {b['riesgo']}\n\n"
        f"💧 Liquidez:\n{a['liquidez']} vs {b['liquidez']}\n"
    )

    await update.message.reply_text(
        mensaje,
        parse_mode=ParseMode.MARKDOWN
    )

# 🎯 BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data

    if tipo == "cripto":
        btc = precio("bitcoin")
        await query.message.reply_text(f"💰 BTC: ${btc}")

    if tipo in ["ahorro", "bolsa", "cripto"]:
        await mostrar(query, tipo)

    elif tipo == "ranking":
        await ranking(query)

    elif tipo == "comparar":
        await comparar(query)

# 🧠 MENSAJES (IA SIMPLE)
async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if "btc" in texto or "bitcoin" in texto:
        tipo = "cripto"
    elif "bolsa" in texto or "acciones" in texto:
        tipo = "bolsa"
    else:
        tipo = "ahorro"

    await mostrar(update, tipo)
    await aviso(update)

# 🚀 MAIN CORREGIDO (SIN ERRORES)
def main():
    if not TOKEN:
        raise ValueError("Falta BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))

    # 🔔 ALERTAS SIN BUG
    async def iniciar_alertas(app):
        asyncio.create_task(enviar_alertas(app))

    app.post_init = iniciar_alertas

    print("🔥 BOT PRO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()



