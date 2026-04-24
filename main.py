import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from strategy import analyze

TOKEN = os.environ.get("BOT_TOKEN")

WATCHLIST = ["SPY", "QQQ", "NVDA", "COIN"]

def format_signal(signal):
    return f"""
🚀 تأكيد دخول صفقة

الأصل: {signal['symbol']}
نوع الصفقة: {signal['type']}

━━━━━━━━━━━━━━━
📍 الدخول: {signal['entry']}
📊 الدعم: {signal['support']}
📊 المقاومة: {signal['resistance']}

━━━━━━━━━━━━━━━
📌 هذه صفقة عالية الجودة
"""

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = "📊 فحص السوق...\n\n"
    found = False

    for symbol in WATCHLIST:
        result = analyze(symbol)

        if result:
            msg += format_signal(result) + "\n"
            found = True

    if not found:
        msg += "❌ لا توجد صفقات قوية حالياً"

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("check", check))

app.run_polling()
