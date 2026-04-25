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

TOKEN = "7707742168:AAGYX7yJBHjm-aVECNFHJ8n68YMPRThD76w"
bot = telebot.TeleBot(TOKEN)

GATEWAYS = {
    "stripe": {
        "name": "Stripe",
        "category": "processor",
        "integration": ["elements", "checkout", "payment_intents"],
        "fingerprints": ["js.stripe.com", "stripe.com/v1"]
    },
    "paypal": {
        "name": "PayPal",
        "category": "wallet",
        "integration": ["redirect", "smart_buttons", "rest"],
        "fingerprints": ["paypal.com/sdk/js", "api.paypal.com"]
    },
    "braintree": {
        "name": "Braintree",
        "category": "processor",
        "integration": ["dropin", "custom"],
        "fingerprints": ["braintreegateway.com"]
    },
    "adyen": {
        "name": "Adyen",
        "category": "processor",
        "integration": ["dropin", "components", "api"],
        "fingerprints": ["checkoutshopper-live.adyen.com"]
    },
    "checkout": {
        "name": "Checkout.com",
        "category": "processor",
        "integration": ["frames", "api"],
        "fingerprints": ["cdn.checkout.com"]
    },
    "worldpay": {
        "name": "Worldpay",
        "category": "processor",
        "integration": ["redirect", "api"],
        "fingerprints": ["worldpay.com"]
    },
    "square": {
        "name": "Square",
        "category": "processor",
        "integration": ["web_payments_sdk"],
        "fingerprints": ["squareup.com"]
    },
    "authorize": {
        "name": "Authorize.Net",
        "category": "processor",
        "integration": ["accept.js", "api"],
        "fingerprints": ["authorize.net"]
    },
    "cybersource": {
        "name": "Cybersource",
        "category": "processor",
        "integration": ["flex", "api"],
        "fingerprints": ["cybersource.com"]
    },
    "klarna": {
        "name": "Klarna",
        "category": "bnpl",
        "integration": ["widget", "api"],
        "fingerprints": ["klarna.com"]
    },
    "paddle": {
        "name": "Paddle",
        "category": "subscription",
        "integration": ["overlay", "api"],
        "fingerprints": ["paddle.com"]
    },
    "razorpay": {
        "name": "Razorpay",
        "category": "processor",
        "integration": ["checkout", "api"],
        "fingerprints": ["razorpay.com"]
    },
    "payu": {
        "name": "PayU",
        "category": "processor",
        "integration": ["redirect", "api"],
        "fingerprints": ["payu.com"]
    },
    "skrill": {
        "name": "Skrill",
        "category": "wallet",
        "integration": ["redirect"],
        "fingerprints": ["skrill.com"]
    },
    "payoneer": {
        "name": "Payoneer",
        "category": "wallet",
        "integration": ["redirect"],
        "fingerprints": ["payoneer.com"]
    },
    "2checkout": {
        "name": "2Checkout",
        "category": "processor",
        "integration": ["inline", "redirect"],
        "fingerprints": ["2checkout.com"]
    },
    "recurly": {
        "name": "Recurly",
        "category": "subscription",
        "integration": ["api"],
        "fingerprints": ["recurly.com"]
    },
    "bolt": {
        "name": "Bolt",
        "category": "checkout",
        "integration": ["one_click"],
        "fingerprints": ["bolt.com"]
    },
    "amazon_pay": {
        "name": "Amazon Pay",
        "category": "wallet",
        "integration": ["widget"],
        "fingerprints": ["amazon.com/pay"]
    },
    "apple_pay": {
        "name": "Apple Pay",
        "category": "wallet",
        "integration": ["native", "web"],
        "fingerprints": ["apple.com/apple-pay"]
    },
    "google_pay": {
        "name": "Google Pay",
        "category": "wallet",
        "integration": ["web", "android"],
        "fingerprints": ["pay.google.com"]
    },
    "alipay": {
        "name": "Alipay",
        "category": "wallet",
        "integration": ["redirect", "qr"],
        "fingerprints": ["alipay.com"]
    },
    "wechat_pay": {
        "name": "WeChat Pay",
        "category": "wallet",
        "integration": ["qr", "api"],
        "fingerprints": ["wechat.com"]
    },
    "paytm": {
        "name": "Paytm",
        "category": "wallet",
        "integration": ["redirect"],
        "fingerprints": ["paytm.com"]
    },
    "upi": {
        "name": "UPI",
        "category": "bank_transfer",
        "integration": ["intent"],
        "fingerprints": ["upi"]
    },
    "flutterwave": {
        "name": "Flutterwave",
        "category": "processor",
        "integration": ["inline", "api"],
        "fingerprints": ["flutterwave.com"]
    },
    "paystack": {
        "name": "Paystack",
        "category": "processor",
        "integration": ["inline", "api"],
        "fingerprints": ["paystack.com"]
    },
    "mollie": {
        "name": "Mollie",
        "category": "processor",
        "integration": ["components", "api"],
        "fingerprints": ["mollie.com"]
    },
    "ebanx": {
        "name": "EBANX",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["ebanx.com"]
    }
},
    "paytabs": {
        "name": "PayTabs",
        "category": "processor",
        "integration": ["redirect", "api"],
        "fingerprints": ["paytabs.com"]
    },
    "tap": {
        "name": "Tap Payments",
        "category": "processor",
        "integration": ["api", "checkout"],
        "fingerprints": ["tap.company"]
    },
    "myfatoorah": {
        "name": "MyFatoorah",
        "category": "processor",
        "integration": ["api", "redirect"],
        "fingerprints": ["myfatoorah.com"]
    },
    "payfort": {
        "name": "Amazon Payment Services",
        "category": "processor",
        "integration": ["redirect", "api"],
        "fingerprints": ["payfort.com"]
    },
    "hyperpay": {
        "name": "HyperPay",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["hyperpay.com"]
    },
    "network": {
        "name": "Network International",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["network.ae"]
    },
    "paysera": {
        "name": "Paysera",
        "category": "processor",
        "integration": ["redirect"],
        "fingerprints": ["paysera.com"]
    },
    "paytrail": {
        "name": "Paytrail",
        "category": "processor",
        "integration": ["redirect"],
        "fingerprints": ["paytrail.com"]
    },
    "payfast": {
        "name": "PayFast",
        "category": "processor",
        "integration": ["redirect"],
        "fingerprints": ["payfast.co.za"]
    },
    "payhere": {
        "name": "PayHere",
        "category": "processor",
        "integration": ["redirect"],
        "fingerprints": ["payhere.lk"]
    },
    "iyzico": {
        "name": "iyzico",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["iyzipay.com"]
    },
    "payzen": {
        "name": "PayZen",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["payzen.eu"]
    },
    "hipay": {
        "name": "HiPay",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["hipay.com"]
    },
    "paymill": {
        "name": "Paymill",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["paymill.com"]
    },
    "wirecard": {
        "name": "Wirecard",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["wirecard.com"]
    },
    "bluepay": {
        "name": "BluePay",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["bluepay.com"]
    },
    "moneris": {
        "name": "Moneris",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["moneris.com"]
    },
    "payjunction": {
        "name": "PayJunction",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["payjunction.com"]
    },
    "cardconnect": {
        "name": "CardConnect",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["cardconnect.com"]
    },
    "heartland": {
        "name": "Heartland",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["heartlandpaymentsystems.com"]
    },
    "merchantone": {
        "name": "Merchant One",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["merchantone.com"]
    },
    "paykickstart": {
        "name": "PayKickstart",
        "category": "subscription",
        "integration": ["api"],
        "fingerprints": ["paykickstart.com"]
    },
    "fastspring": {
        "name": "FastSpring",
        "category": "subscription",
        "integration": ["overlay", "api"],
        "fingerprints": ["fastspring.com"]
    },
    "2c2p": {
        "name": "2C2P",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["2c2p.com"]
    },
    "paymaya": {
        "name": "PayMaya",
        "category": "wallet",
        "integration": ["api"],
        "fingerprints": ["paymaya.com"]
    },
    "gcash": {
        "name": "GCash",
        "category": "wallet",
        "integration": ["api"],
        "fingerprints": ["gcash.com"]
    },
    "doku": {
        "name": "DOKU",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["doku.com"]
    },
    "omise": {
        "name": "Omise",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["omise.co"]
    },
    "senangpay": {
        "name": "SenangPay",
        "category": "processor",
        "integration": ["redirect"],
        "fingerprints": ["senangpay.my"]
    },
    "eghl": {
        "name": "eGHL",
        "category": "processor",
        "integration": ["api"],
        "fingerprints": ["e-ghl.com"]
    },
    "dragonpay": {
        "name": "DragonPay",
        "category": "bank_transfer",
        "integration": ["redirect"],
        "fingerprints": ["dragonpay.ph"]
    }

})

VBV_KEYWORDS = ['3D-Secure', 'threeDSecureInfo', 'VBV', '3DSecure', '3D Secure']
AUTH_PATHS = ['/my-account', '/account', '/login', '/signin']
SECURITY_TERMS = ['captcha', 'recaptcha', "i'm not a robot"]
CLOUDFLARE_TERMS = ["Cloudflare", "cdnjs.cloudflare.com"]

user_api_keys = {}
user_search_results = {}
user_language = {}

def fetch_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        scraper = cloudscraper.create_scraper()
        return scraper.get(url, timeout=10)
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

def format_result(display_url, gateways, security, elapsed, user=None):
    domain = extract_domain(display_url)
    display = domain if len(display_url) < 50 else display_url[:50] + "..."

    check_by = f"\n┃•➤ Checked by ➜ [{user.first_name}](tg://user?id={user.id}) 🕷" if user else ""
    return f"""
┏━━━━━━━⍟
┃•Website Analysis ✅
┗━━━━━━━━━━━━⊛
┏━━━━━━━⍟
┃•➤ Site ➜ `{display}` ⎙
┃•➤ Gateways ➜ {', '.join(gateways)} 🍂
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

        final_url = resp.url
        domain = extract_domain(final_url)
        html = resp.text

        gateways = detect_gateways(html)
        security = check_security(html, domain)
        elapsed = round(time.time() - start, 2)
        return format_result(url, gateways, security, elapsed, user)
    except Exception as e:
        elapsed = round(time.time() - start, 2)
        return f"❌ Failed to check: {url}\n   Error: {str(e)} (after {elapsed}s)"

def test_api_key(api_key):
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {'q': 'test', 'engine': 'google', 'api_key': api_key}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if 'error' in data:
            error_msg = data['error']
            if 'invalid api key' in error_msg.lower() or 'unauthorized' in error_msg.lower():
                return False, "مفتاح API غير صالح"
            else:
                return False, f"خطأ في API: {error_msg}"
        else:
            return True, "مفتاح API صالح"
    except Exception as e:
        return False, f"خطأ في الاتصال: {str(e)}"

def search_with_dork(query, api_key):
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {'q': query, 'engine': 'google', 'api_key': api_key, 'num': 20}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        if 'error' in data:
            error_msg = data['error']
            if 'invalid api key' in error_msg.lower():
                return "مفتاح API غير صالح. يرجى تحديث المفتاح باستخدام /addkey", []
            elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                return "تم تجاوز حصة API. يرجى التحقق من حساب SearchApi.io الخاص بك", []
            else:
                return f"خطأ في API: {error_msg}", []
        return format_dork_results(data, query)
    except Exception as e:
        return f"خطأ في البحث: {str(e)}", []

def search_normal(query, api_key):
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {'q': query, 'engine': 'google', 'api_key': api_key, 'num': 20}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        if 'error' in data:
            error_msg = data['error']
            if 'invalid api key' in error_msg.lower():
                return "مفتاح API غير صالح. يرجى تحديث المفتاح باستخدام /addkey", []
            elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                return "تم تجاوز حصة API. يرجى التحقق من حساب SearchApi.io الخاص بك", []
            else:
                return f"خطأ في API: {error_msg}", []
        return format_normal_results(data, query)
    except Exception as e:
        return f"خطأ في البحث: {str(e)}", []

def format_dork_results(data, query):
    if 'organic_results' not in data or not data['organic_results']:
        return "لا توجد نتائج لاستعلامك", []
    
    results_text = f"نتائج البحث المتقدم\n\n"
    urls = []
    seen = set()
    counter = 1
    for result in data['organic_results']:
        link = result.get('link')
        if link and link.startswith(('http://', 'https://')) and link not in seen:
            seen.add(link)
            results_text += f"{counter}. {link}\n\n"
            urls.append(link)
            counter += 1
            if counter > 20:
                break
    
    if not urls:
        return "لا توجد روابط صالحة في النتائج", []
    
    results_text += f"إجمالي النتائج: {len(urls)}\n"
    results_text += "لتحميل الروابط استخدم الأمر /export"
    return results_text, urls

def format_normal_results(data, query):
    if 'organic_results' not in data or not data['organic_results']:
        return "لا توجد نتائج لاستعلامك", []
    
    results_text = f"نتائج البحث العادي\n\n"
    urls = []
    seen = set()
    counter = 1
    for result in data['organic_results']:
        link = result.get('link')
        if link and link.startswith(('http://', 'https://')) and link not in seen:
            seen.add(link)
            results_text += f"{counter}. {link}\n\n"
            urls.append(link)
            counter += 1
            if counter > 20:
                break
    
    if not urls:
        return "لا توجد روابط صالحة في النتائج", []
    
    results_text += f"إجمالي النتائج: {len(urls)}\n"
    results_text += "لتحميل الروابط استخدم الأمر /export"
    return results_text, urls

def create_txt_file(urls, query):
    if not urls:
        return None
    clean_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_query = clean_query[:30]
    filename = f"نتائج_{clean_query}_{datetime.now().strftime('%H%M%S')}.txt"
    file_content = f"نتائج البحث عن: {query}\n"
    file_content += f"تم الإنشاء في: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    file_content += f"إجمالي الروابط: {len(urls)}\n\n"
    for i, url in enumerate(urls, 1):
        file_content += f"{i}. {url}\n"
    file_buffer = io.BytesIO(file_content.encode('utf-8'))
    file_buffer.name = filename
    return file_buffer

def get_text(lang, key):
    texts = {
        'ar': {
            'welcome': "اختر القسم الذي تريده من الأزرار أدناه:",
            'search_section': "🔍 *قسم استخراج بوابات الدفع*\n\nالأوامر المتاحة:\n/dork - بحث متقدم (باستخدام Google Dorks)\n/search - بحث عادي\n/addkey - إضافة مفتاح API\n/mykey - عرض المفتاح الحالي\n/removekey - حذف المفتاح\n/testkey - اختبار صحة المفتاح\n/export - تصدير آخر نتائج البحث كملف نصي\n/getkey - كيفية الحصول على مفتاح\n/status - حالة البوت\n\nللبحث، اكتب الأمر متبوعاً باستعلامك.\nمثال: /dork intext:password site:example.com",
            'gateway_section': "🛡 *قسم فحص بوابات الدفع*\n\nالأوامر المتاحة:\n/check <url> — فحص موقع واحد (مع أو بدون https://)\n/combo — فحص عدة مواقع (رابط واحد لكل سطر بعد الأمر)\n\nأمثلة:\n/check example.com\n/combo\nexample1.com/donate\nexample2.org/support",
            'help': "طريقة الاستخدام:\n\n1. استخراج بوابات الدفع: استخدم /dork أو /search مع استعلام (يتطلب مفتاح API)\n2. فحص بوابات الدفع: استخدم /check أو /combo\n3. لمزيد من التفاصيل عن كل قسم، اختر من القائمة الرئيسية (/start)",
            'choose_language': "🌐 اختر لغتك المفضلة / Choose your preferred language:"
        },
        'en': {
            'welcome': "Choose the section you want from the buttons below:",
            'search_section': "🔍 *Payment Gateways Extraction Section*\n\nAvailable commands:\n/dork - Advanced search (using Google Dorks)\n/search - Normal search\n/addkey - Add API key\n/mykey - Show current key\n/removekey - Delete key\n/testkey - Test key validity\n/export - Export last search results as text file\n/getkey - How to get a key\n/status - Bot status\n\nTo search, type the command followed by your query.\nExample: /dork intext:password site:example.com",
            'gateway_section': "🛡 *Payment Gateways Checker Section*\n\nAvailable commands:\n/check <url> — Check single site (with or without https://)\n/combo — Check multiple sites (one URL per line after the command)\n\nExamples:\n/check example.com\n/combo\nexample1.com/donate\nexample2.org/support",
            'help': "Usage:\n\n1. Payment Gateways Extraction: Use /dork or /search with a query (requires API key)\n2. Payment Gateways Checker: Use /check or /combo\n3. For more details about each section, choose from the main menu (/start)",
            'choose_language': "🌐 Choose your preferred language:"
        }
    }
    return texts.get(lang, texts['ar']).get(key, '')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if user_id not in user_language:
        btn_ar = types.InlineKeyboardButton("🇮🇶 Arabic", callback_data="lang_ar")
        btn_en = types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
        markup.add(btn_ar, btn_en)
        bot.send_message(message.chat.id, get_text('ar', 'choose_language'), reply_markup=markup)
    else:
        lang = user_language[user_id]
        btn1 = types.InlineKeyboardButton("🔍 استخراج بوابات الدفع" if lang == 'ar' else "🔍 Payment Gateways Extraction", callback_data="search")
        btn2 = types.InlineKeyboardButton("🛡 فحص بوابات الدفع" if lang == 'ar' else "🛡 Payment Gateways Checker", callback_data="gateways")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, get_text(lang, 'welcome'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    if call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        user_language[user_id] = lang
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("🔍 استخراج بوابات الدفع" if lang == 'ar' else "🔍 Payment Gateways Extraction", callback_data="search")
        btn2 = types.InlineKeyboardButton("🛡 فحص بوابات الدفع" if lang == 'ar' else "🛡 Payment Gateways Checker", callback_data="gateways")
        markup.add(btn1, btn2)
        
        bot.edit_message_text(
            get_text(lang, 'welcome'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    elif call.data == "search":
        lang = user_language.get(user_id, 'ar')
        bot.edit_message_text(
            get_text(lang, 'search_section'),
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
    elif call.data == "gateways":
        lang = user_language.get(user_id, 'ar')
        bot.edit_message_text(
            get_text(lang, 'gateway_section'),
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['help'])
def send_help(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, 'ar')
    bot.reply_to(message, get_text(lang, 'help'))

@bot.message_handler(commands=['check'])
def handle_check(message):
    try:
        url = message.text.split()[1].strip()
    except IndexError:
        bot.reply_to(message, "⚠ Wrong format!\nUse `/check example.com/path`", parse_mode='Markdown')
        return

    msg = bot.reply_to(message, "⏳ Checking...")
    result = check_site(url, message.from_user)
    bot.edit_message_text(result, message.chat.id, msg.message_id, parse_mode='Markdown')

@bot.message_handler(commands=['combo'])
def handle_combo(message):
    lines = message.text.split('\n')[1:]
    urls = [line.strip() for line in lines if line.strip()]
    if not urls:
        bot.reply_to(message, "⚠ Please provide URLs, one per line.\nExample:\n/combo\nexample1.com/donate\nexample2.org/support")
        return

    progress = bot.reply_to(message, f"🔍 Starting combo ({len(urls)} sites)...")

    for i, url in enumerate(urls, 1):
        bot.edit_message_text(
            f"🔍 Checking {i}/{len(urls)}: {url}",
            message.chat.id,
            progress.message_id
        )

        result = check_site(url, message.from_user)
        bot.send_message(message.chat.id, result, parse_mode='Markdown')
        time.sleep(1)

    bot.edit_message_text(
        f"✅ Combo completed! Checked {len(urls)} sites.",
        message.chat.id,
        progress.message_id
    )

@bot.message_handler(commands=['addkey'])
def add_key(message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "يرجى إرسال المفتاح: /addkey <المفتاح>")
        return
    api_key = parts[1].strip()
    bot.reply_to(message, "جارٍ اختبار المفتاح...")
    is_valid, msg = test_api_key(api_key)
    if is_valid:
        user_api_keys[user_id] = api_key
        bot.reply_to(message, "تم حفظ المفتاح بنجاح!")
    else:
        bot.reply_to(message, f"خطأ: {msg}")

@bot.message_handler(commands=['testkey'])
def test_key(message):
    user_id = message.from_user.id
    api_key = user_api_keys.get(user_id)
    if not api_key:
        bot.reply_to(message, "لا يوجد مفتاح مضاف. استخدم /addkey")
        return
    bot.reply_to(message, "جارٍ اختبار المفتاح...")
    is_valid, msg = test_api_key(api_key)
    if is_valid:
        bot.reply_to(message, f"المفتاح صالح: {msg}")
    else:
        bot.reply_to(message, f"المفتاح غير صالح: {msg}")

@bot.message_handler(commands=['removekey'])
def remove_key(message):
    user_id = message.from_user.id
    if user_id in user_api_keys:
        del user_api_keys[user_id]
        if user_id in user_search_results:
            del user_search_results[user_id]
        bot.reply_to(message, "تم حذف المفتاح بنجاح!")
    else:
        bot.reply_to(message, "لا يوجد مفتاح للحذف.")

@bot.message_handler(commands=['mykey'])
def show_key(message):
    user_id = message.from_user.id
    api_key = user_api_keys.get(user_id)
    if api_key:
        masked = api_key[:8] + "..." + api_key[-6:]
        bot.reply_to(message, f"المفتاح الحالي: {masked}")
    else:
        bot.reply_to(message, "لا يوجد مفتاح مضاف.")

@bot.message_handler(commands=['status'])
def show_status(message):
    user_id = message.from_user.id
    api_key = user_api_keys.get(user_id)
    api_status = "غير مضاف"
    if api_key:
        is_valid, _ = test_api_key(api_key)
        api_status = "صالح" if is_valid else "غير صالح"
    status_text = f"""
حالة البوت:

المستخدم: {message.from_user.first_name}
حالة المفتاح: {api_status}
الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
عدد المستخدمين النشطين: {len(user_api_keys)}
    """
    bot.reply_to(message, status_text)

@bot.message_handler(commands=['dork'])
def handle_dork(message):
    user_id = message.from_user.id
    api_key = user_api_keys.get(user_id)
    if not api_key:
        bot.reply_to(message, "لا يوجد مفتاح API. أضف مفتاحك أولاً باستخدام /addkey")
        return
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "يرجى إرسال استعلام البحث: /dork <استعلام>")
        return
    query = " ".join(parts[1:])
    bot.reply_to(message, f"جاري البحث عن: {query}")
    results_text, urls = search_with_dork(query, api_key)
    user_search_results[user_id] = {
        'urls': urls,
        'query': query,
        'timestamp': datetime.now()
    }
    if len(results_text) > 4096:
        for i in range(0, len(results_text), 4000):
            bot.send_message(message.chat.id, results_text[i:i+4000])
    else:
        bot.reply_to(message, results_text)

@bot.message_handler(commands=['search'])
def handle_search(message):
    user_id = message.from_user.id
    api_key = user_api_keys.get(user_id)
    if not api_key:
        bot.reply_to(message, "لا يوجد مفتاح API. أضف مفتاحك أولاً باستخدام /addkey")
        return
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "يرجى إرسال استعلام البحث: /search <استعلام>")
        return
    query = " ".join(parts[1:])
    bot.reply_to(message, f"جاري البحث عن: {query}")
    results_text, urls = search_normal(query, api_key)
    user_search_results[user_id] = {
        'urls': urls,
        'query': query,
        'timestamp': datetime.now()
    }
    if len(results_text) > 4096:
        for i in range(0, len(results_text), 4000):
            bot.send_message(message.chat.id, results_text[i:i+4000])
    else:
        bot.reply_to(message, results_text)

@bot.message_handler(commands=['export'])
def handle_export(message):
    user_id = message.from_user.id
    if user_id not in user_search_results or not user_search_results[user_id]['urls']:
        bot.reply_to(message, "لا توجد نتائج سابقة للتصدير. قم بالبحث أولاً.")
        return
    data = user_search_results[user_id]
    urls = data['urls']
    query = data['query']
    file = create_txt_file(urls, query)
    if file:
        bot.send_document(message.chat.id, file, caption=f"تم تصدير {len(urls)} رابط لـ: {query}")
    else:
        bot.reply_to(message, "حدث خطأ في إنشاء الملف.")

@bot.message_handler(commands=['getkey'])
def get_key_guide(message):
    guide_text = """
كيفية الحصول على مفتاح API:

1. اذهب إلى: https://www.searchapi.io
2. اضغط على Get Started Free
3. سجل باستخدام بريدك الإلكتروني
4. فعّل بريدك
5. اذهب إلى لوحة التحكم
6. انسخ المفتاح (يبدأ بـ sk_)
7. استخدم الأمر /addkey متبوعاً بالمفتاح

الخطة المجانية: 100 بحث شهرياً
    """
    bot.reply_to(message, guide_text)

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, 'ar')
    bot.reply_to(message, "أمر غير معروف. استخدم /start لعرض القائمة الرئيسية." if lang == 'ar' else "Unknown command. Use /start to show main menu.")

if __name__ == "__main__":
    print("تم تشيغل البوت يا شيطان الكوفي @Hammdn...")
    bot.infinity_polling()
