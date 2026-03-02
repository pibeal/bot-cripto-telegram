import requests
import yfinance as yf
import time

import os
TOKEN = os.getenv("8771204299:AAFe_mjO-J6K2Xpzq8-ST5NY9yZHRWq8DW8")

alertas = []

def enviar_mensaje(chat_id, mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": mensaje}
    requests.post(url, data=data)

def obtener_precio(simbolo):
    try:
        ticker = yf.Ticker(simbolo)
        df = ticker.history(period="1d")
        if df.empty:
            return None
        return df["Close"].iloc[-1]
    except:
        return None

print("🤖 Bot de alertas iniciado...")

update_offset = 0

while True:
    # Revisar mensajes nuevos
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 10, "offset": update_offset}
    response = requests.get(url, params=params).json()

    if "result" in response:
        for update in response["result"]:
            update_offset = update["update_id"] + 1

            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                texto = update["message"]["text"].lower()

                # COMANDO PRECIO
                if texto.startswith("/precio"):
                    partes = texto.split()
                    if len(partes) == 2:
                        simbolo = partes[1].upper() + "-USD"
                        precio = obtener_precio(simbolo)

                        if precio:
                            enviar_mensaje(chat_id, f"💰 {simbolo}: ${precio:.2f}")
                        else:
                            enviar_mensaje(chat_id, "❌ No encontrada")

                # COMANDO ALERTA
                if texto.startswith("/alerta"):
                    partes = texto.split()
                    if len(partes) == 3:
                        simbolo = partes[1].upper() + "-USD"
                        nivel = float(partes[2])

                        alertas.append({
                            "chat_id": chat_id,
                            "simbolo": simbolo,
                            "nivel": nivel
                        })

                        enviar_mensaje(chat_id, f"🔔 Alerta creada para {simbolo} en ${nivel}")

    # Revisar alertas activas
    for alerta in alertas[:]:
        precio_actual = obtener_precio(alerta["simbolo"])
        if precio_actual:

            if precio_actual >= alerta["nivel"]:
                enviar_mensaje(
                    alerta["chat_id"],
                    f"🚨 {alerta['simbolo']} llegó a ${precio_actual:.2f}"
                )
                alertas.remove(alerta)

    time.sleep(30)
