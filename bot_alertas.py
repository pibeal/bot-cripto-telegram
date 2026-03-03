import asyncio
import requests
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# -------------------------------
# Configuración usando variables de entorno
# -------------------------------
TOKEN = os.getenv("8771204299:AAF-H6RWaRqsR7Yr9lyHrfmPk6-YHS14F0U")      # Token de Telegram
CHAT_ID = os.getenv("8521853388")  # ID del chat de Telegram
INTERVALO = 300                 # 5 minutos
CAMBIO_MINIMO = 5.0
CSV_FILE = "historial_criptos.csv"

# Criptos más populares
CRIPTOS = [
    "BTC", "ETH", "USDT", "BNB", "XRP",
    "SOL", "USDC", "DOGE", "TRX", "ADA",
    "LINK", "XLM", "AVAX", "LTC", "BCH",
    "MATIC", "NEAR", "ATOM", "ALGO", "FTM"
]

ultimos_cambios = {}  # Para /top

# -------------------------------
# Funciones
# -------------------------------
def obtener_precio(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data[symbol.lower()]["usd"]
    except Exception as e:
        print(f"Error obteniendo precio de {symbol}: {e}")
        return None

def guardar_historial(crypto, precio, cambio_pct):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fila = [ahora, crypto, f"{precio:.2f}", f"{cambio_pct:+.2f}"]
    try:
        with open(CSV_FILE, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fila)
    except Exception as e:
        print("Error guardando CSV:", e)

# -------------------------------
# Bucle de alertas
# -------------------------------
async def alerta_loop(app):
    ultimos_precios = {}
    global ultimos_cambios
    while True:
        mensajes = []
        cambios = {}

        for crypto in CRIPTOS:
            precio = obtener_precio(crypto)
            if precio is None:
                continue

            cambio_pct = 0.0
            if crypto in ultimos_precios:
                cambio_pct = ((precio - ultimos_precios[crypto]) / ultimos_precios[crypto]) * 100
                if abs(cambio_pct) >= CAMBIO_MINIMO:
                    direccion = "📈 subió" if cambio_pct > 0 else "📉 bajó"
                    mensajes.append(f"{crypto} {direccion} a ${precio:.2f} ({cambio_pct:+.2f}%)")
                    cambios[crypto] = cambio_pct

            ultimos_precios[crypto] = precio
            guardar_historial(crypto, precio, cambio_pct)

        ultimos_cambios = cambios

        if mensajes:
            mensaje_resumen = "\n".join(mensajes)

            subidas = sorted([c for c in cambios.items() if c[1] > 0], key=lambda x: x[1], reverse=True)[:3]
            bajadas = sorted([c for c in cambios.items() if c[1] < 0], key=lambda x: x[1])[:3]

            if subidas:
                mensaje_resumen += "\n\n🔥 Top 3 subidas:\n" + "\n".join([f"{c[0]} ({c[1]:+.2f}%)" for c in subidas])
            if bajadas:
                mensaje_resumen += "\n\n❄️ Top 3 bajadas:\n" + "\n".join([f"{c[0]} ({c[1]:+.2f}%)" for c in bajadas])

            try:
                await app.bot.send_message(chat_id=CHAT_ID, text=mensaje_resumen)
                print("Alerta enviada:\n", mensaje_resumen)
            except Exception as e:
                print("Error enviando mensaje:", e)

        await asyncio.sleep(INTERVALO)

# -------------------------------
# Gráficas avanzadas diarias
# -------------------------------
async def enviar_graficas_avanzadas(app):
    if not os.path.exists(CSV_FILE):
        print("No hay historial para graficar.")
        return

    df = pd.read_csv(CSV_FILE, parse_dates=["FechaHora"])
    if df.empty:
        print("CSV vacío, no hay datos para graficar.")
        return

    volatilidad = df.groupby("Cripto")["CambioPorc"].apply(lambda x: x.abs().sum())
    top5_volatil = volatilidad.sort_values(ascending=False).head(5).index.tolist()

    if not top5_volatil:
        print("No hay cripto con volatilidad suficiente.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    for crypto in top5_volatil:
        df_crypto = df[df["Cripto"] == crypto]
        precios = df_crypto["PrecioUSD"]
        cambios = df_crypto["CambioPorc"]
        color = "green" if cambios.iloc[-1] > 0 else "red"
        ax.plot(df_crypto["FechaHora"], precios, label=f"{crypto} ({cambios.iloc[-1]:+.2f}%)", color=color)

    ax.set_xlabel("FechaHora")
    ax.set_ylabel("Precio USD")
    ax.set_title("Top 5 Criptos más volátiles del día")
    ax.legend()
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.tight_layout()
    plt.grid(True)

    filename = "graficas_avanzadas.png"
    plt.savefig(filename)
    plt.close()

    try:
        with open(filename, "rb") as f:
            await app.bot.send_photo(chat_id=CHAT_ID, photo=InputFile(f))
        print("Gráfico avanzado diario enviado.")
    except Exception as e:
        print("Error enviando gráfico:", e)
    finally:
        if os.path.exists(filename):
            os.remove(filename)

async def tarea_graficas_diarias(app):
    while True:
        await enviar_graficas_avanzadas(app)
        await asyncio.sleep(24 * 60 * 60)  # 24h

# -------------------------------
# Comandos de Telegram
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot de alertas de criptos iniciado correctamente!")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos:\n"
        "/start - Inicia el bot\n"
        "/ayuda - Muestra ayuda\n"
        "/top - Top 3 subidas/bajadas del último intervalo\n"
        "Escribe el símbolo de una cripto para consultar su precio (ej: BTC)"
    )

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ultimos_cambios
    if not ultimos_cambios:
        await update.message.reply_text("Aún no hay datos de cambios recientes.")
        return
    subidas = sorted([c for c in ultimos_cambios.items() if c[1] > 0], key=lambda x: x[1], reverse=True)[:3]
    bajadas = sorted([c for c in ultimos_cambios.items() if c[1] < 0], key=lambda x: x[1])[:3]
    mensaje = ""
    if subidas:
        mensaje += "🔥 Top 3 subidas:\n" + "\n".join([f"{c[0]} ({c[1]:+.2f}%)" for c in subidas]) + "\n"
    if bajadas:
        mensaje += "❄️ Top 3 bajadas:\n" + "\n".join([f"{c[0]} ({c[1]:+.2f}%)" for c in bajadas])
    await update.message.reply_text(mensaje)

async def consultar_precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.upper()
    if msg in CRIPTOS:
        precio = obtener_precio(msg)
        if precio:
            await update.message.reply_text(f"💰 {msg} ahora está en ${precio:.2f}")
        else:
            await update.message.reply_text(f"No se pudo obtener el precio de {msg}")
    else:
        await update.message.reply_text("Cripto no reconocida. Escribe el símbolo, p.ej., BTC")

# -------------------------------
# Crear aplicación
# -------------------------------
def crear_aplicacion():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, consultar_precio))
    app.create_task(alerta_loop(app))
    app.create_task(tarea_graficas_diarias(app))
    return app

# -------------------------------
# Ejecutar bot
# -------------------------------
async def main():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["FechaHora", "Cripto", "PrecioUSD", "CambioPorc"])
    app = crear_aplicacion()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
