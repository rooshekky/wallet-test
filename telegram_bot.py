import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_URL = "https://YOURDOMAIN.up.railway.app"

BOT_TOKEN = "YOUR_TELEGRAM_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = update.effective_user.username

    r = requests.get(f"{API_URL}/user/create/{username}")

    wallet = r.json()

    await update.message.reply_text(
        f"Wallet created!\n\nAddress:\n{wallet['address']}"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = update.effective_user.username

    r = requests.get(f"{API_URL}/wallet/{username}")

    data = r.json()

    await update.message.reply_text(
        f"Balance: {data['balance']} ETH"
    )


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from_user = update.effective_user.username
    to_user = context.args[0]
    amount = context.args[1]

    requests.get(
        f"{API_URL}/tip/{from_user}/{to_user}/{amount}"
    )

    await update.message.reply_text("Tip sent")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("tip", tip))

app.run_polling()
