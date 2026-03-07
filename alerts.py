from database import cursor
from crypto_api import get_price
import asyncio

async def check_alerts(app):

    while True:

        cursor.execute("SELECT * FROM alertas")

        rows = cursor.fetchall()

        for chat_id,crypto,price in rows:

            current = get_price(crypto)

            if current >= price:

                await app.bot.send_message(

                chat_id=chat_id,

                text=f"🚨 ALERTA\n{crypto} llegó a {current}"

                )

        await asyncio.sleep(60)
