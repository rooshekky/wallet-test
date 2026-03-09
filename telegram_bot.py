import requests
from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes

API="https://YOURDOMAIN.up.railway.app"
TOKEN="YOUR_TELEGRAM_TOKEN"

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    uid=update.effective_user.id

    r=requests.get(f"{API}/user/create/{uid}")
    data=r.json()

    await update.message.reply_text(
        f"Wallet created\n\n{data['address']}"
    )

async def balance(update:Update,context:ContextTypes.DEFAULT_TYPE):

    uid=update.effective_user.id

    r=requests.get(f"{API}/wallet/{uid}")
    data=r.json()

    await update.message.reply_text(
        f"Balance: {data['balance']} ETH"
    )

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("balance",balance))

app.run_polling()
