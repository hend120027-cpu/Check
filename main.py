import logging
from pyromod import Client
from pyrogram import filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import CallbackQuery, Message
from utilsdf.functions import bot_on
from utilsdf.db import Database
from utilsdf.vars import PREFIXES

# -----------------------------------
# ضع بياناتك هنا مباشرة
API_ID = 6843321125  # ضع هنا الـ API_ID الخاص بك
API_HASH = "YOUR_API_HASH"  # ضع هنا الـ API_HASH الخاص بك
BOT_TOKEN = "7834120140:AAG2HFrpuictfFSZisF1m1__EjE0zcnl_cE"  # ضع هنا التوكن
CHANNEL_LOGS = -1001494650944  # ضع هنا ID الجروب أو القناة
# -----------------------------------

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    parse_mode=ParseMode.HTML,
)

bot_on()
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.CRITICAL)


@app.on_callback_query()
async def warn_user(client: Client, callback_query: CallbackQuery):
    if callback_query.message.reply_to_message.from_user and (
        callback_query.from_user.id
        != callback_query.message.reply_to_message.from_user.id
    ):
        await callback_query.answer("Usa tu menu! ⚠️", show_alert=True)
        return
    await callback_query.continue_propagation()


@app.on_message(filters.text)
async def user_ban(client: Client, m: Message):
    if not m.from_user or not m.text:
        return

    try:
        if not m.text[0] in PREFIXES:
            return
    except UnicodeDecodeError:
        return

    chat_id = m.chat.id
    user_id = m.from_user.id
    username = m.from_user.username

    # فقط صاحب الـ ID هذا يمكنه تشغيل البوت
    if user_id != 6843321125:  # ضع هنا ID الخاص بك
        return

    with Database() as db:
        if chat_id == CHANNEL_LOGS:
            async for member in m.chat.get_members():
                if not member.user:
                    continue
                if member.status == ChatMemberStatus.ADMINISTRATOR:
                    continue
                member_id = member.user.id

                # أنت تعتبر أدمن دائمًا
                if db.is_seller_or_admin(member_id) or member_id == 6843321125:
                    continue
                if db.is_premium(member_id):
                    continue
                if db.user_has_credits(member_id):
                    continue

                await m.chat.ban_member(member_id)
                info = db.get_info_user(member_id)
                await client.send_message(
                    CHANNEL_LOGS,
                    f"<b>User eliminado: @{info['USERNAME']}</b>"
                )

        db.remove_expireds_users()
        banned = db.is_ban(user_id)
        if banned:
            return
        db.register_user(user_id, username)
        await m.continue_propagation()


if __name__ == "__main__":
    app.run()