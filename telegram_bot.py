import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API = "https://YOURDOMAIN.up.railway.app"
BOT_TOKEN = "YOUR_TELEGRAM_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    r = requests.get(f"{API}/telegram/create/{telegram_id}")

    wallet = r.json()

    await update.message.reply_text(
        f"Wallet created\n\nAddress:\n{wallet['address']}"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    r = requests.get(f"{API}/telegram/balance/{telegram_id}")

    data = r.json()

    await update.message.reply_text(
        f"Balance: {data['balance']} ETH"
    )


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from_id = update.effective_user.id
    to_id = context.args[0]
    amount = context.args[1]

    requests.get(
        f"{API}/telegram/tip/{from_id}/{to_id}/{amount}"
    )

    await update.message.reply_text("Tip sent")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("tip", tip))

app.run_polling()
