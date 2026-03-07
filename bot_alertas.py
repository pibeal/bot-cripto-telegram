import asyncio
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,CallbackQueryHandler,ContextTypes

from config import TOKEN
from crypto_api import get_price,get_history
from charts import create_chart
from analysis import analyze
from market import market_scan
from alerts import check_alerts

def menu():

    keyboard=[

[InlineKeyboardButton("💰 Precio BTC",callback_data="price")],

[InlineKeyboardButton("📊 Grafica BTC",callback_data="chart")],

[InlineKeyboardButton("🤖 Analisis BTC",callback_data="analysis")],

[InlineKeyboardButton("🏆 Mercado",callback_data="market")]

]

    return InlineKeyboardMarkup(keyboard)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

"🚀 CRYPTO BOT PROFESIONAL",

reply_markup=menu()

)

async def buttons(update,context):

    query=update.callback_query

    await query.answer()

    data=query.data

    if data=="price":

        price=get_price("BTC-USD")

        await query.message.reply_text(f"BTC ${price}")

    if data=="chart":

        data=get_history("BTC-USD")

        file=create_chart(data,"BTC")

        await query.message.reply_photo(photo=open(file,"rb"))

    if data=="analysis":

        data=get_history("BTC-USD")

        trend,rsi,signal=analyze(data)

        await query.message.reply_text(

f"Tendencia: {trend}\nRSI:{rsi}\nSeñal:{signal}"

)

    if data=="market":

        top=market_scan()

        text="🏆 MERCADO\n\n"

        for c,p in top:

            text+=f"{c} {p:.2f}%\n"

        await query.message.reply_text(text)

async def main():

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))

    app.add_handler(CallbackQueryHandler(buttons))

    asyncio.create_task(check_alerts(app))

    print("BOT ACTIVO")

    await app.run_polling()

if __name__=="__main__":

    asyncio.run(main())
