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
        caption=f"""**اهلا بك {message.from_user.mention()}** 

انا بوت اختصاصي تشغيل الاغاني في المكالمات الصوتيه 

اضفني الى مجموعتك قم بترقيتي كمشرف في المجموعه 

بعد ذالك اضغط زر الاوامر لمعرفة طريقة تشغيلي عزيزي 📍""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🖥 ¦ الأوامــر", callback_data="cbcmnds"),
                    InlineKeyboardButton(
                        "⚙️ ¦ الـسـورس", callback_data="https://t.me/VFF35")
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
