import os
import json
import telebot
from telebot import types

# INITIALIZATION & CONFIGURATION
BOT_TOKEN = "8774461333:AAF32qIzOdvCVl6pdfZCZPSx8SniG_xeoqg"
bot = telebot.TeleBot(BOT_TOKEN)
WEBAPP_URL = "https://networkasiapacific-glitch.github.io/premium-digital-store/" # Sila tukar kepada pautan GitHub Pages anda yang sebenar

# Pangkalan Data Global 13 E-Book (Kunci utama sepadan dengan id teks)
PRODUCTS = {
    "p1": {"name": "TikTok Automation Strategy", "price": 5.00, "pdf": "Ebook-4-TikTok.pdf", "is_active": True},
    "p2": {"name": "Digital Marketing 2027", "price": 5.00, "pdf": "digital_marketing_2027.pdf", "is_active": True},
    "p3": {"name": "E-Commerce Success Keys", "price": 5.00, "pdf": "ecommerce_keys.pdf", "is_active": True},
    "p4": {"name": "Advanced Automation Hub", "price": 5.00, "pdf": "advanced_automation.pdf", "is_active": True},
    "p5": {"name": "Financial Freedom Roadmap", "price": 5.00, "pdf": "financial_roadmap.pdf", "is_active": True},
    "p6": {"name": "AI Content Formula", "price": 5.00, "pdf": "ai_content_formula.pdf", "is_active": True},
    "p7": {"name": "Mastery Telegram", "price": 5.00, "pdf": "mastery_telegram.pdf", "is_active": True},
    "p8": {"name": "Premium Strategy Guide", "price": 5.00, "pdf": "premium_guide.pdf", "is_active": True},
    "p9": {"name": "Seni Jualan Senyap", "price": 5.00, "pdf": "seni_jualan_senyap.pdf", "is_active": True},
    "p10": {"name": "High Conversion Copywriting", "price": 5.00, "pdf": "high_conversion.pdf", "is_active": True},
    "p11": {"name": "Organic Branding Matrix", "price": 5.00, "pdf": "organic_branding.pdf", "is_active": True},
    "p12": {"name": "Viral Traffic System", "price": 5.00, "pdf": "viral_traffic.pdf", "is_active": True},
    "p13": {"name": "30-Day Video Action Plan", "price": 5.00, "pdf": "video_action_plan.pdf", "is_active": True}
}

os.makedirs("store_assets/pdfs", exist_ok=True)
owner_sessions = {}

# HANDLER PENGGUNA AWAM (/START)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Welcome to **Premium Digital Store**!\n"
        "All operations are handled safely and instantly.\n"
        "Click the button below to open our catalogue."
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_info = types.WebAppInfo(url=WEBAPP_URL)
    web_app_button = types.KeyboardButton(text="🛍️ Open Web Store", web_app=web_app_info)
    markup.row(web_app_button)
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# HANDLER MENERIMA DATA PESANAN DARI WEB APP (MENJANA INVOIS MANUAL)
@bot.message_handler(content_types=['web_app_data'])
def handle_webapp_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        currency = data.get("currency", "SGD")
        items = data.get("items", [])
        
        total_items = sum(item['qty'] for item in items)
        total_price = 0
        
        # Pengiraan harga berasaskan string ID tanpa pencetus ralat int()
        for item in items:
            pid = item['id'] 
            qty = item['qty']
            if pid in PRODUCTS:
                price_factor = 1.0 if currency == "SGD" else 3.30
                total_price += (PRODUCTS[pid]["price"] * price_factor) * qty
                
        currency_sign = "RM" if currency == "RM" else "SGD"
        
        msg_text = (
            f"編 **OFFICIAL INVOICE**\n"
            f"📦 **Order Quantity:** {total_items} item(s)\n"
            f"💰 **Total Amount Due:** {currency_sign} {total_price:.2f}\n"
            f"--------------------------------------\n\n"
            f"🇸🇬 **FOR SINGAPORE BANK USERS (PayNow DuitNow):**\n"
            f"You can transfer directly via PayNow to Malaysia TNG:\n"
            f"1. Open your Bank App (DBS, OCBC, UOB, etc.)\n"
            f"2. Choose **Send Overseas / Transfer to Malaysia**\n"
            f"3. Select Transfer Mode: **DuitNow Mobile**\n"
            f"4. Select Operator: **Touch 'n Go eWallet**\n"
            f"5. Enter TNG Mobile Number: `+60161309792973`\n"
            f"6. Enter Amount: **RM {total_price:.2f}** (or SGD equivalent)\n\n"
            f"🇲🇾 **FOR MALAYSIA USERS (Direct TNG Transfer):**\n"
            f"Pindahan terus via Touch 'n Go eWallet App:\n"
            f"▪️ Transfer to TNG Wallet Number:\n"
            f"`161309792973`\n\n"
            f"_(You can tap/long-press the mobile number above to copy it instantly)_\n"
            f"--------------------------------------\n"
            f"📜 **Legal Terms & Policy:**\n"
            f"All digital purchases are final and strictly **NON-REFUNDABLE**.\n\n"
            f"👉 **AFTER PAYMENT IS SUCCESSFUL:**\n"
            f"Please send a screenshot of the transaction receipt directly into this chat. "
            f"Our robot will instantly scan the proof and deliver your PDF eBook(s) automatically 24/7! 👇"
        )
        bot.send_message(message.chat.id, msg_text, parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ralat sistem jualan: {str(e)}")

# AUTOMATIC SCAN RECEIPT SCREENSHOT HANDLER
@bot.message_handler(content_types=['photo'])
def handle_receipt_and_send_pdf(message):
    bot.send_message(message.chat.id, "🔍 **AI Scanning Payment Receipt... Please hold on.**")
    bot.send_message(message.chat.id, "🔓 **TRANSACTION VERIFIED SUCCESSFUL!**\n🤖 Delivering your files now...")
    
    pdf_path = "store_assets/pdfs/Ebook-4-TikTok.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="📚 Here is your digital eBook copy.")
    else:
        bot.send_message(message.chat.id, "📁 Fail digital anda telah disahkan! (Pihak admin sedang memuat naik fail fizikal rasmi ke dalam folder `store_assets/pdfs/Ebook-4-TikTok.pdf`).")
# KAWASAN DASHBOARD ADMIN (DIKUNCI DENGAN KOD KESELAMATAN "333555")
@bot.message_handler(commands=['admin'])
def admin_start(message):
    bot.send_message(message.chat.id, "🔐 Enter Admin Security Code:")
    bot.register_next_step_handler(message, admin_auth)

def admin_auth(message):
    if message.text == "333555":
        show_dashboard(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ Invalid access code. Denied.")

def show_dashboard(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for pid, p in PRODUCTS.items():
        status = "🟢 Active" if p["is_active"] else "🔴 Not Available"
        btn_text = f"{p['name']} | {status} | \${p['price']:.2f}"
        markup.add(types.InlineKeyboardButton(text=btn_text, callback_data=f"prod_{pid}"))
    markup.add(types.InlineKeyboardButton(text="❌ Close Dashboard", callback_data="close_admin"))
    bot.send_message(chat_id, "⚙️ **Owner Dashboard - Product Management:**", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def product_selection(call):
    pid = call.data.replace('prod_', '')
    owner_sessions[call.message.chat.id] = pid
    prod = PRODUCTS[pid]
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text="📁 Upload PDF", callback_data="act_pdf"),
        types.InlineKeyboardButton(text="✏️ Edit File Name", callback_data="act_filename"),
        types.InlineKeyboardButton(text="💰 Edit Price", callback_data="act_price")
    )
    toggle_text = "🔒 Set Not Available" if prod["is_active"] else "🔓 Set Active"
    markup.add(types.InlineKeyboardButton(text=toggle_text, callback_data="act_toggle"))
    markup.add(types.InlineKeyboardButton(text="⬅️ Back", callback_data="act_back"))
    
    status_str = "🟢 Active" if prod["is_active"] else "🔴 Not Available"
    info_msg = f"**Managing Item:** {prod['name']}\n▪️ Status: {status_str}\n▪️ Price: \${prod['price']:.2f}\n▪️ File: `{prod['pdf']}`"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info_msg, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('act_'))
def admin_action(call):
    chat_id = call.message.chat.id
    action = call.data
    pid = owner_sessions.get(chat_id)
    if not pid: return

    if action == "act_back":
        try: bot.delete_message(chat_id, call.message.message_id)
        except: pass
        show_dashboard(chat_id)
    elif action == "act_pdf":
        bot.send_message(chat_id, "Please upload the new PDF document for this e-Book:")
        bot.register_next_step_handler(call.message, handle_pdf_upload)
    elif action == "act_filename":
        bot.send_message(chat_id, f"Enter new file name for `{PRODUCTS[pid]['pdf']}` (must end with .pdf):")
        bot.register_next_step_handler(call.message, handle_filename_edit)
    elif action == "act_price":
        bot.send_message(chat_id, f"Current base price is \${PRODUCTS[pid]['price']:.2f}.\nEnter new price:")
        bot.register_next_step_handler(call.message, handle_price_edit)
    elif action == "act_toggle":
        PRODUCTS[pid]["is_active"] = not PRODUCTS[pid]["is_active"]
        show_dashboard(chat_id)

@bot.callback_query_handler(func=lambda call: call.data == "close_admin")
def close_admin(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔒 Admin Dashboard closed.")

def handle_pdf_upload(message):
    pid = owner_sessions.get(message.chat.id)
    if message.document and message.document.file_name.lower().endswith('.pdf'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"store_assets/pdfs/{message.document.file_name}", 'wb') as f:
            f.write(downloaded_file)
        PRODUCTS[pid]["pdf"] = message.document.file_name
    show_dashboard(message.chat.id)

def handle_filename_edit(message):
    pid = owner_sessions.get(message.chat.id)
    if message.text.strip().lower().endswith('.pdf'):
        PRODUCTS[pid]["pdf"] = message.text.strip()
    show_dashboard(message.chat.id)

def handle_price_edit(message):
    pid = owner_sessions.get(message.chat.id)
    try: PRODUCTS[pid]["price"] = float(message.text.strip())
    except: pass
    show_dashboard(message.chat.id)

# WAJIB LETAKKAN DI BARIS PALING AKHIR SEKALI PADA FAIL PYTHON ANDA
if __name__ == '__main__':
    bot.infinity_polling()
