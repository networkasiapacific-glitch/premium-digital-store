import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8807689945:AAF75TANEt5FF40WpxheZywGj3wVRYLeS38"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Premium Digital Store!\n\n"
        "Click the 'Open Store' button below to browse products, adjust prices, and make secure purchases via Stripe."
    )

async def handle_mini_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    received_data = update.effective_message.web_app_data.data
    order_info = json.loads(received_data)
    
    user_chat_id = update.effective_chat.id
    net_total = order_info.get("net_total_sgd", "0.00")
    items = order_info.get("items", [])

    # Stripe confirmation log receipts
    await update.message.reply_text(
        f"💳 Stripe Secure Link Generated!\n"
        f"Total Amount: SGD {net_total}\n\n"
        f"Once your payment via Stripe QR/Card is complete, your premium books will download automatically below!"
    )

    for item in items:
        name = item['name']
        try:
            if "Premium Strategy" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Premium_Strategy_Guide.pdf", "rb"))
            elif "Mastery Telegram" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Mastery_Telegram.pdf", "rb"))
            elif "Digital Marketing" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Digital_Marketing_2027.pdf", "rb"))
            elif "E-Commerce Success" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("ECommerce_Success_Keys.pdf", "rb"))
            elif "Advanced Automation" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Advanced_Automation_Hub.pdf", "rb"))
            elif "Financial Freedom" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Financial_Freedom_Roadmap.pdf", "rb"))
            elif "AI Content Formula" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("AI_Content_Formula.pdf", "rb"))
            elif "Facebook Traffic" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Facebook_Marketing_Guide.pdf", "rb"))
            elif "TikTok Shorts" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("TikTok_Automation_Guide.pdf", "rb"))
            elif "YouTube Automation" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("YouTube_Monetization_Guide.pdf", "rb"))
            elif "WeChat Social" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("WeChat_Business_Guide.pdf", "rb"))
            elif "Instagram Reels" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Instagram_Growth_Guide.pdf", "rb"))
            elif "General Digital Business" in name:
                await context.bot.send_document(chat_id=user_chat_id, document=open("Digital_Business_Foundations.pdf", "rb"))
        except FileNotFoundError:
            await update.message.reply_text(f"❌ Document asset file currently offline for: {name}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_mini_app_data))
    app.run_polling()

if __name__ == '__main__':
    main()
