import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, UserNotParticipant
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from Codexun.utils.filters import command

from Codexun import BOT_NAME, BOT_USERNAME
from Codexun.config import BOT_USERNAME 
from Codexun.config import BOT_NAME
from Codexun.config import START_IMG

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_IMG}",
        caption=f"""**اهلا بك ماهذا النور {message.from_user.mention()}** 👋

انا اقوا بوت متطور لتشغيل الاغاني في المكالمات الصوتية بصوت رائع وبدون تقطيع يمكنك اضافتي الى مجموعتك وترقيتي كمشرف.

اعطني ڪامل الصلاحيات لكي اعمل بشكل صحيح عزيزي عليك الضغط على زر الاوامر لمعرفة طريقة تشغيلي شكرا لك!

كل الشكر والاحترام لمن قام بأضافة بوتاتنا 📍""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🖥 ¦ الأوامــر", callback_data="cbcmnds"),
                    InlineKeyboardButton(
                        "⚙️ ¦ الـسـورس", callback_data="cbabout")
                ],
                [
                    InlineKeyboardButton(
                        "🧨 ¦ دلـيل الاسـتخـدام", callback_data="cbguide")
                ],
                [
                    InlineKeyboardButton(
                        "🎯 ¦ اضـفـني لـي مـجمـوعـتك ¦ 🎯", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
           ]
        ),
    )
