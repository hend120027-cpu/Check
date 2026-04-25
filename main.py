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
    "stripe": "stripe",
    "paypal": "paypal",
    "braintree": "braintree",
    "adyen": "adyen",
    "checkout_com": "checkout_com",
    "worldpay": "worldpay",
    "square": "square",
    "authorize_net": "authorize_net",
    "cybersource": "cybersource",
    "klarna": "klarna",
    "affirm": "affirm",
    "afterpay": "afterpay",
    "sezzle": "sezzle",
    "zip": "zip",
    "splitit": "splitit",
    "paddle": "paddle",
    "recurly": "recurly",
    "razorpay": "razorpay",
    "payu": "payu",
    "paystack": "paystack",
    "flutterwave": "flutterwave",
    "mollie": "mollie",
    "ebanx": "ebanx",
    "mercadopago": "mercadopago",
    "cielo": "cielo",
    "pagseguro": "pagseguro",
    "stone": "stone",
    "ebanx_brazil": "ebanx_brazil",
    "boltmx": "boltmx",
    "ebanx_latam": "ebanx_latam",
    "dlocal": "dlocal",
    "payoneer": "payoneer",
    "skrill": "skrill",
    "neteller": "neteller",
    "wise": "wise",
    "revolut_pay": "revolut_pay",
    "apple_pay": "apple_pay",
    "google_pay": "google_pay",
    "amazon_pay": "amazon_pay",
    "venmo": "venmo",
    "alipay": "alipay",
    "wechat_pay": "wechat_pay",
    "paytm": "paytm",
    "gcash": "gcash",
    "paymaya": "paymaya",
    "grabpay": "grabpay",
    "touchngo": "touchngo",
    "boost": "boost",
    "fawry": "fawry",
    "paymob": "paymob",
    "myfatoorah": "myfatoorah",
    "tap_payments": "tap_payments",
    "paytabs": "paytabs",
    "hyperpay": "hyperpay",
    "network_international": "network_international",
    "paysera": "paysera",
    "paytrail": "paytrail",
    "payfast": "payfast",
    "payhere": "payhere",
    "iyzico": "iyzico",
    "payzen": "payzen",
    "hipay": "hipay",
    "bluepay": "bluepay",
    "moneris": "moneris",
    "payjunction": "payjunction",
    "cardconnect": "cardconnect",
    "heartland": "heartland",
    "merchantone": "merchantone",
    "fastspring": "fastspring",
    "2checkout": "2checkout",
    "2c2p": "2c2p",
    "doku": "doku",
    "omise": "omise",
    "senangpay": "senangpay",
    "eghl": "eghl",
    "dragonpay": "dragonpay",
    "ipay88": "ipay88",
    "molpay": "molpay",
    "ipaymu": "ipaymu",
    "xendit": "xendit",
    "midtrans": "midtrans",
    "duitku": "duitku",
    "qpay": "qpay",
    "knet": "knet",
    "benefitpay": "benefitpay",
    "stc_pay": "stc_pay",
    "mada": "mada",
    "unionpay": "unionpay",
    "jcb": "jcb",
    "discover": "discover",
    "visa_checkout": "visa_checkout",
    "masterpass": "masterpass",
    "samsung_pay": "samsung_pay",
    "huawei_pay": "huawei_pay",
    "zelle": "zelle",
    "chase_pay": "chase_pay",
    "barclaycard": "barclaycard",
    "sagepay": "sagepay",
    "opayo": "opayo",
    "worldline": "worldline",
    "ingenico": "ingenico",
    "stripe_terminal": "stripe_terminal",
    "adyen_pos": "adyen_pos",
    "square_pos": "square_pos",
    "paypal_here": "paypal_here",
    "mena_gateway_105": "mena_gateway_105",
    "latam_processor_106": "latam_processor_106",
    "africa_pay_107": "africa_pay_107",
    "eu_pay_service_108": "eu_pay_service_108",
    "us_acquirer_109": "us_acquirer_109",
    "asia_checkout_110": "asia_checkout_110",
    "mena_wallet_111": "mena_wallet_111",
    "latam_gateway_112": "latam_gateway_112",
    "africa_processor_113": "africa_processor_113",
    "eu_pay_114": "eu_pay_114",
    "us_pay_service_115": "us_pay_service_115",
    "asia_acquirer_116": "asia_acquirer_116",
    "mena_checkout_117": "mena_checkout_117",
    "latam_wallet_118": "latam_wallet_118",
    "africa_gateway_119": "africa_gateway_119",
    "eu_processor_120": "eu_processor_120",
    "us_pay_121": "us_pay_121",
    "asia_pay_service_122": "asia_pay_service_122",
    "mena_acquirer_123": "mena_acquirer_123",
    "latam_checkout_124": "latam_checkout_124",
    "africa_wallet_125": "africa_wallet_125",
    "eu_gateway_126": "eu_gateway_126",
    "us_processor_127": "us_processor_127",
    "asia_pay_128": "asia_pay_128",
    "mena_pay_service_129": "mena_pay_service_129",
    "latam_acquirer_130": "latam_acquirer_130",
    "africa_checkout_131": "africa_checkout_131",
    "eu_wallet_132": "eu_wallet_132",
    "us_gateway_133": "us_gateway_133",
    "asia_processor_134": "asia_processor_134",
    "mena_pay_135": "mena_pay_135",
    "latam_pay_service_136": "latam_pay_service_136",
    "africa_acquirer_137": "africa_acquirer_137",
    "eu_checkout_138": "eu_checkout_138",
    "us_wallet_139": "us_wallet_139",
    "asia_gateway_140": "asia_gateway_140",
    "mena_processor_141": "mena_processor_141",
    "latam_pay_142": "latam_pay_142",
    "africa_pay_service_143": "africa_pay_service_143",
    "eu_acquirer_144": "eu_acquirer_144",
    "us_checkout_145": "us_checkout_145",
    "asia_wallet_146": "asia_wallet_146",
    "mena_gateway_147": "mena_gateway_147",
    "latam_processor_148": "latam_processor_148",
    "africa_pay_149": "africa_pay_149",
    "eu_pay_service_150": "eu_pay_service_150",
    "us_acquirer_151": "us_acquirer_151",
    "asia_checkout_152": "asia_checkout_152",
    "mena_wallet_153": "mena_wallet_153",
    "latam_gateway_154": "latam_gateway_154",
    "africa_processor_155": "africa_processor_155",
    "eu_pay_156": "eu_pay_156",
    "us_pay_service_157": "us_pay_service_157",
    "asia_acquirer_158": "asia_acquirer_158",
    "mena_checkout_159": "mena_checkout_159",
    "latam_wallet_160": "latam_wallet_160",
    "africa_gateway_161": "africa_gateway_161",
    "eu_processor_162": "eu_processor_162",
    "us_pay_163": "us_pay_163",
    "asia_pay_service_164": "asia_pay_service_164",
    "mena_acquirer_165": "mena_acquirer_165",
    "latam_checkout_166": "latam_checkout_166",
    "africa_wallet_167": "africa_wallet_167",
    "eu_gateway_168": "eu_gateway_168",
    "us_processor_169": "us_processor_169",
    "asia_pay_170": "asia_pay_170",
    "mena_pay_service_171": "mena_pay_service_171",
    "latam_acquirer_172": "latam_acquirer_172",
    "africa_checkout_173": "africa_checkout_173",
    "eu_wallet_174": "eu_wallet_174",
    "us_gateway_175": "us_gateway_175",
    "asia_processor_176": "asia_processor_176",
    "mena_pay_177": "mena_pay_177",
    "latam_pay_service_178": "latam_pay_service_178",
    "africa_acquirer_179": "africa_acquirer_179",
    "eu_checkout_180": "eu_checkout_180",
    "us_wallet_181": "us_wallet_181",
    "asia_gateway_182": "asia_gateway_182",
    "mena_processor_183": "mena_processor_183",
    "latam_pay_184": "latam_pay_184",
    "africa_pay_service_185": "africa_pay_service_185",
    "eu_acquirer_186": "eu_acquirer_186",
    "us_checkout_187": "us_checkout_187",
    "asia_wallet_188": "asia_wallet_188",
    "mena_gateway_189": "mena_gateway_189",
    "latam_processor_190": "latam_processor_190",
    "africa_pay_191": "africa_pay_191",
    "eu_pay_service_192": "eu_pay_service_192",
    "us_acquirer_193": "us_acquirer_193",
    "asia_checkout_194": "asia_checkout_194",
    "mena_wallet_195": "mena_wallet_195",
    "latam_gateway_196": "latam_gateway_196",
    "africa_processor_197": "africa_processor_197",
    "eu_pay_198": "eu_pay_198",
    "us_pay_service_199": "us_pay_service_199",
    "asia_acquirer_200": "asia_acquirer_200",
    "mena_checkout_201": "mena_checkout_201",
    "latam_wallet_202": "latam_wallet_202",
    "africa_gateway_203": "africa_gateway_203",
    "eu_processor_204": "eu_processor_204",
    "us_pay_205": "us_pay_205",
    "asia_pay_service_206": "asia_pay_service_206",
    "mena_acquirer_207": "mena_acquirer_207",
    "latam_checkout_208": "latam_checkout_208",
    "africa_wallet_209": "africa_wallet_209",
    "eu_gateway_210": "eu_gateway_210",
    "us_processor_211": "us_processor_211",
    "asia_pay_212": "asia_pay_212",
    "mena_pay_service_213": "mena_pay_service_213",
    "latam_acquirer_214": "latam_acquirer_214",
    "africa_checkout_215": "africa_checkout_215",
    "eu_wallet_216": "eu_wallet_216",
    "us_gateway_217": "us_gateway_217",
    "asia_processor_218": "asia_processor_218",
    "mena_pay_219": "mena_pay_219",
    "latam_pay_service_220": "latam_pay_service_220",
    "africa_acquirer_221": "africa_acquirer_221",
    "eu_checkout_222": "eu_checkout_222",
    "us_wallet_223": "us_wallet_223",
    "asia_gateway_224": "asia_gateway_224",
    "mena_processor_225": "mena_processor_225",
    "latam_pay_226": "latam_pay_226",
    "africa_pay_service_227": "africa_pay_service_227",
    "eu_acquirer_228": "eu_acquirer_228",
    "us_checkout_229": "us_checkout_229",
    "asia_wallet_230": "asia_wallet_230",
    "mena_gateway_231": "mena_gateway_231",
    "latam_processor_232": "latam_processor_232",
    "africa_pay_233": "africa_pay_233",
    "eu_pay_service_234": "eu_pay_service_234",
    "us_acquirer_235": "us_acquirer_235",
    "asia_checkout_236": "asia_checkout_236",
    "mena_wallet_237": "mena_wallet_237",
    "latam_gateway_238": "latam_gateway_238",
    "africa_processor_239": "africa_processor_239",
    "eu_pay_240": "eu_pay_240",
    "us_pay_service_241": "us_pay_service_241",
    "asia_acquirer_242": "asia_acquirer_242",
    "mena_checkout_243": "mena_checkout_243",
    "latam_wallet_244": "latam_wallet_244",
    "africa_gateway_245": "africa_gateway_245",
    "eu_processor_246": "eu_processor_246",
    "us_pay_247": "us_pay_247",
    "asia_pay_service_248": "asia_pay_service_248",
    "mena_acquirer_249": "mena_acquirer_249",
    "latam_checkout_250": "latam_checkout_250",
    "africa_wallet_251": "africa_wallet_251",
    "eu_gateway_252": "eu_gateway_252",
    "us_processor_253": "us_processor_253",
    "asia_pay_254": "asia_pay_254",
    "mena_pay_service_255": "mena_pay_service_255",
    "latam_acquirer_256": "latam_acquirer_256",
    "africa_checkout_257": "africa_checkout_257",
    "eu_wallet_258": "eu_wallet_258",
    "us_gateway_259": "us_gateway_259",
    "asia_processor_260": "asia_processor_260",
    "mena_pay_261": "mena_pay_261",
    "latam_pay_service_262": "latam_pay_service_262",
    "africa_acquirer_263": "africa_acquirer_263",
    "eu_checkout_264": "eu_checkout_264",
    "us_wallet_265": "us_wallet_265",
    "asia_gateway_266": "asia_gateway_266",
    "mena_processor_267": "mena_processor_267",
    "latam_pay_268": "latam_pay_268",
    "africa_pay_service_269": "africa_pay_service_269",
    "eu_acquirer_270": "eu_acquirer_270",
    "us_checkout_271": "us_checkout_271",
    "asia_wallet_272": "asia_wallet_272",
    "mena_gateway_273": "mena_gateway_273",
    "latam_processor_274": "latam_processor_274",
    "africa_pay_275": "africa_pay_275",
    "eu_pay_service_276": "eu_pay_service_276",
    "us_acquirer_277": "us_acquirer_277",
    "asia_checkout_278": "asia_checkout_278",
    "mena_wallet_279": "mena_wallet_279",
    "latam_gateway_280": "latam_gateway_280",
    "africa_processor_281": "africa_processor_281",
    "eu_pay_282": "eu_pay_282",
    "us_pay_service_283": "us_pay_service_283",
    "asia_acquirer_284": "asia_acquirer_284",
    "mena_checkout_285": "mena_checkout_285",
    "latam_wallet_286": "latam_wallet_286",
    "africa_gateway_287": "africa_gateway_287",
    "eu_processor_288": "eu_processor_288",
    "us_pay_289": "us_pay_289",
    "asia_pay_service_290": "asia_pay_service_290",
    "mena_acquirer_291": "mena_acquirer_291",
    "latam_checkout_292": "latam_checkout_292",
    "africa_wallet_293": "africa_wallet_293",
    "eu_gateway_294": "eu_gateway_294",
    "us_processor_295": "us_processor_295",
    "asia_pay_296": "asia_pay_296",
    "mena_pay_service_297": "mena_pay_service_297",
    "latam_acquirer_298": "latam_acquirer_298",
    "africa_checkout_299": "africa_checkout_299",
    "eu_wallet_300": "eu_wallet_300",
    "us_gateway_301": "us_gateway_301",
    "asia_processor_302": "asia_processor_302",
    "mena_pay_303": "mena_pay_303",
    "latam_pay_service_304": "latam_pay_service_304",
    "africa_acquirer_305": "africa_acquirer_305",
    "eu_checkout_306": "eu_checkout_306",
    "us_wallet_307": "us_wallet_307",
    "asia_gateway_308": "asia_gateway_308",
    "mena_processor_309": "mena_processor_309",
    "latam_pay_310": "latam_pay_310",
    "africa_pay_service_311": "africa_pay_service_311",
    "eu_acquirer_312": "eu_acquirer_312",
    "us_checkout_313": "us_checkout_313",
    "asia_wallet_314": "asia_wallet_314",
    "mena_gateway_315": "mena_gateway_315",
    "latam_processor_316": "latam_processor_316",
    "africa_pay_317": "africa_pay_317",
    "eu_pay_service_318": "eu_pay_service_318",
    "us_acquirer_319": "us_acquirer_319",
}
                        
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
