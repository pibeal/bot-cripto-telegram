import requests
import json
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==============================
# TOKEN DESDE VARIABLE DE ENTORNO
# ==============================

TOKEN = os.getenv("TOKEN") or "8771204299:AAF-H6RWaRqsR7Yr9lyHrfmPk6-YHS14F0U"

# ==============================
# ARCHIVO DE ALERTAS
# ==============================

ARCHIVO_ALERTAS = "alertas.json"

def cargar_alertas():
    try:
        with open(ARCHIVO_ALERTAS, "r") as f:
            return json.load(f)
    except:
        return {}

def guardar_alertas(data):
    with open(ARCHIVO_ALERTAS, "w") as f:
        json.dump(data, f)

alertas = cargar_alertas()

# ==============================
# OBTENER PRECIO CRYPTO
# ==============================

def obtener_precio(cripto):

    ids = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "bnb": "binancecoin",
        "xrp": "ripple",
        "ada": "cardano",
        "sol": "solana",
        "doge": "dogecoin",
        "dot": "polkadot",
        "matic": "polygon",
        "ltc": "litecoin"
    }

    cripto = cripto.lower()

    if cripto not in ids:
        return None

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids[cripto]}&vs_currencies=usd"

    r = requests.get(url)
    data = r.json()

    return data[ids[cripto]]["usd"]

# ==============================
# COMANDO START
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot de alertas cripto activo\n\n"
        "Comandos:\n"
        "/precio btc\n"
        "/alerta btc 70000\n"
        "/misalertas\n"
        "/eliminaralertas"
    )

# ==============================
# VER PRECIO
# ==============================

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text("Usa: /precio btc")
        return

    cripto = context.args[0]

    precio = obtener_precio(cripto)

    if precio is None:
        await update.message.reply_text("Cripto no soportada")
        return

    await update.message.reply_text(f"💰 {cripto.upper()} = ${precio}")

# ==============================
# CREAR ALERTA
# ==============================

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        cripto = context.args[0]
        objetivo = float(context.args[1])
    except:
        await update.message.reply_text("Usa: /alerta btc 70000")
        return

    user = str(update.message.chat_id)

    if user not in alertas:
        alertas[user] = []

    alertas[user].append({
        "cripto": cripto,
        "precio": objetivo
    })

    guardar_alertas(alertas)

    await update.message.reply_text(
        f"🚨 Alerta creada\n{cripto.upper()} -> ${objetivo}"
    )

# ==============================
# VER ALERTAS
# ==============================

async def misalertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = str(update.message.chat_id)

    if user not in alertas or len(alertas[user]) == 0:
        await update.message.reply_text("No tienes alertas")
        return

    texto = "🚨 Tus alertas:\n\n"

    for a in alertas[user]:
        texto += f"{a['cripto'].upper()} -> ${a['precio']}\n"

    await update.message.reply_text(texto)

# ==============================
# ELIMINAR ALERTAS
# ==============================

async def eliminaralertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = str(update.message.chat_id)

    alertas[user] = []

    guardar_alertas(alertas)

    await update.message.reply_text("🗑 Alertas eliminadas")

# ==============================
# VERIFICAR ALERTAS
# ==============================

async def verificar_alertas(app):

    while True:

        for user in alertas:

            for alerta in alertas[user]:

                precio_actual = obtener_precio(alerta["cripto"])

                if precio_actual >= alerta["precio"]:

                    await app.bot.send_message(
                        chat_id=user,
                        text=f"🚨 ALERTA\n{alerta['cripto'].upper()} llegó a ${precio_actual}"
                    )

        await asyncio.sleep(60)

# ==============================
# MAIN
# ==============================

async def iniciar_verificador(app):
    while True:
        await verificar_alertas(app)

def main():

    if TOKEN is None:
        print("ERROR: TOKEN no configurado")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("misalertas", misalertas))
    app.add_handler(CommandHandler("eliminaralertas", eliminaralertas))

    print("Bot funcionando...")

    app.run_polling()

if __name__ == "__main__":
    main()
