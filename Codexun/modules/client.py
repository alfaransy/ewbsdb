import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp
import aiohttp
import random

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


from Codexun.tgcalls import calls, queues
from Codexun.tgcalls.youtube import download
from Codexun.tgcalls import convert as cconvert
from Codexun.tgcalls.calls import client as ASS_ACC
from Codexun.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)

from Codexun import BOT_NAME, BOT_USERNAME
from Codexun import app
import Codexun.tgcalls
from Codexun.tgcalls import youtube
from Codexun.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    START_IMG,
    SUPPORT,
    UPDATE,
    BOT_NAME,
    BOT_USERNAME,
)
from Codexun.utils.filters import command
from Codexun.utils.decorators import errors, sudo_users_only
from Codexun.utils.administrator import adminsOnly
from Codexun.utils.errors import DurationLimitError
from Codexun.utils.gets import get_url, get_file_name
from Codexun.modules.admins import member_permissions


def others_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc"),
        ],[
            InlineKeyboardButton(text="Manage", callback_data=f"cls"),
        ],
        
    ]
    return buttons


fifth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200% 🔊", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجـــوع", callback_data=f"cbmenu"),
        ],
    ]
)

fourth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150% 🔊", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجـــوع", callback_data=f"cbmenu"),
        ],
    ]
)

third_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100% 🔊", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجـــوع", callback_data=f"cbmenu"),
        ],
    ]
)

second_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50% 🔊", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجـــوع", callback_data=f"cbmenu"),
        ],
    ]
)

first_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20% 🔊", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجــــوع", callback_data=f"cbmenu"),
        ],
    ]
)
highquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Low Quality", callback_data="low"),],
         [   InlineKeyboardButton("Medium Quality", callback_data="medium"),
            
        ],[   InlineKeyboardButton("High Quality ✅", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجــوع", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="مسح 🗑️", callback_data=f"cls"),
        ],
    ]
)
lowquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Low Quality ✅", callback_data="low"),],
         [   InlineKeyboardButton("Medium Quality", callback_data="medium"),
            
        ],[   InlineKeyboardButton("High Quality", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجـــوع", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="مسح 🗑️", callback_data=f"cls"),
        ],
    ]
)
mediumquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Low Quality", callback_data="low"),],
         [   InlineKeyboardButton("Medium Quality ✅", callback_data="medium"),
            
        ],[   InlineKeyboardButton("High Quality", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجــوع", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="مسح 🗑️", callback_data=f"cls"),
        ],
    ]
)

dbclean_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Yes, Proceed !", callback_data="cleandb"),],
        [    InlineKeyboardButton("Nope, Cancel !", callback_data="cbmenu"),
            
        ],[
            InlineKeyboardButton(text="⬅️ رجوع", callback_data=f"cbmenu"),
        ],
    ]
)
menu_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
            
        ],[
            InlineKeyboardButton(text="Volume", callback_data=f"fifth"),
             InlineKeyboardButton(text="Quality", callback_data=f"high"),
        ],[
            InlineKeyboardButton(text="CleanDB", callback_data=f"dbconfirm"),
             InlineKeyboardButton(text="About", callback_data=f"nonabout"),
        ],[
             InlineKeyboardButton(text="🗑️ مسح", callback_data=f"cls"),
        ],
    ]
)


@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Only admin with manage voice chat permission can do this.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**Skip Button Used By** {rpk}
• No more songs in Queue
`Leaving Voice Chat..`
"""
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
            await CallbackQuery.answer("Voice Chat Skip.!", show_alert=True)     

@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music_off(chat_id)
            await calls.pytgcalls.pause_stream(chat_id)
            await CallbackQuery.answer("Music Paused Successfully.", show_alert=True)
            
        else:
            await CallbackQuery.answer(f"Nothing is playing on voice chat!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"Nothing is playing in on voice chat!", show_alert=True)


@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Only admin with manage voice chat permission can do this.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "Nothing is paused in the voice chat.",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await calls.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("Music resumed successfully.", show_alert=True)
            
    else:
        await CallbackQuery.answer(f"Nothing is playing.", show_alert=True)


@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Music stream ended.", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"**• Music successfully stopped by {rpk}.**")
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)

@Client.on_callback_query(filters.regex("cleandb"))
async def cleandb(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Db cleaned successfully!", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.edit_message_text(
        f"✅ __Erased queues successfully__\n│\n╰ Database cleaned by {rpk}",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("مسح 🗑️", callback_data="cls")]])
        
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)


@Client.on_callback_query(filters.regex("cbcmnds"))
async def cbcmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**{BOT_NAME} Bot Commands 💡**

• /play هذا الامر
- مع اسم الاغنيه لتشغيل

• /pause 
- For pausing music

• /resume 
- For resuming music

• /skip 
- لتخطي الاغنيه

• /search (song name) 
- For searching music

• /song 
- For download music

Powered by **@{UPDATE}** !""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton(
                        "لاعــليك", callback_data="cbstgs"),
                    InlineKeyboardButton(
                        "التـــالي", callback_data="cbowncmnds")
                ],
              [InlineKeyboardButton("🔙  رجــوع", callback_data="cbhome")]]
        ),
    )
@Client.on_callback_query(filters.regex("cbowncmnds"))
async def cbowncmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Owner & Sudo Commands 💡**

• /broadcast (massage)
- Broadcast msg through bot

• /gcast (massage) 
- Broadcast msg with pin

• /restart 
- Restart bot from server

• /exec
- Execute any code

• /stats
- Get all statistics

• /ping 
- Pinging uptime

• /update
- Update bot with latest version

• /gban or /ungban
- Global Ban system

• /leaveall 
- leaving assistant from all chats

قناة البوت **@{UPDATE}** !""",
        reply_markup=InlineKeyboardMarkup(
            [
              
              [InlineKeyboardButton("🔙  رجـــوع", callback_data="cbcmnds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**About {BOT_NAME} Bot 💡**

**[{BOT_NAME}](https://t.me/{BOT_USERNAME})** Music Bot is the bot designed by **@{UPDATE}** for playing a high quality and unbreakable music in your groups voice chat.

This bot helps you to play music, to search music from youtube and to download music from youtube server and many more features related to telegram voice chat feature.

**Assistant :- @{ASSUSERNAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("Support 🚶", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("Updates 🤖", url=f"https://t.me/{UPDATE}")
                ],
            [InlineKeyboardButton("Make Your Own Bot", callback_data="cbtuto")],
            [InlineKeyboardButton("🔙  Back Home", callback_data="cbhome")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbstgs"))
async def cbstgs(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**لاعليك بهذا الزر اخرج من هنا 💡**

After you played your song some menu buttons will be comes to manage your music playing on voice chat. They are as follows :

• ▷ 
- Resume Music
• II 
- Pause Music
• ▢  
- End Music
• ‣‣ 
- Skip Music

You can also open this menu through /menu and /settings command.

**Only admins can use this buttons 📍**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("🔙  رجـــوع", callback_data="cbcmnds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**اهلا بك عزيزي 💡**

• ان واجهة مشكلة لي البوت

• عليك فقط ارسال امر تحديث

• لكي تتحدث قاعة البيانات

• هذا الامر /reload لكي يتحدث البوت

• وبعد ذالك عليك سوا ارسال 

• هذه play مع اسم الاغنيه يتم التشغيل !""",
        reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton("المـــســــاعد", callback_data="cberror")],
              [InlineKeyboardButton("🔙  رجــــوع", callback_data="cbhome")]]
        ),
    )


@Client.on_callback_query(filters.regex("cberror"))
async def cberror(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**اهلا بك في زر حساب المساعد**

اهلا انهو حساب المساعد لبوت الاغاني اضف البوت وقم بكتابة انضم لكي يدخل المساعد الى مجموعتك @{ASSUSERNAME} ان لم يدخل تأكد ان ليس هناك حظر او تقييد لحساب المساعد في مجموعتك ان كلشيئ على مايرام تواصل مع مبرمج السورس.\n\n**معرف حساب المساعد:- @{ASSUSERNAME}**\n\n**شكرأ لقرائتك !**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [
                    InlineKeyboardButton("الحــساب المساعد", url=f"https://t.me/{ASSUSERNAME}")
                ],
              [InlineKeyboardButton("🔙  رجــــوع", callback_data="cbguide")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbtuto"))
async def cbtuto(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**اهلا بك في زر مبرمج السورس 💡**

يمــــكنك التـــواصل مــــع مبــــرمـــج الســـورس فــــي اي وقـــت تنصـــيب بــــوتات ميـــوزك وغـــيرها بــــيع كـــافة المـــلفات!

عــــزيزي القـــارئ يمــــنك تــــنصيب بــــوتات على ســـورســــنا مــــجاني ولــــدينا مــــدفوعه قنــاة الســــورس فـــي الاســـفل.

**🔗 قنــاة الســـورس : https://t.me/VFF35**

**شكرا لك !""",
       reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton("𝐒𝐈𝐅 𝐂𝐎𝐁𝐑𝐀", url=f"https://t.me/QABNADLIB")
                ],
              [InlineKeyboardButton("🔙  رجـــوع", callback_data="cbabout")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbhome"))
async def cbhome(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""هلا بك ماهذا النور {message.from_user.mention()}** 👋

انا اقوا بوت متطور لتشغيل الاغاني في المكالمات الصوتية بصوت رائع وبدون تقطيع يمكنك اضافتي الى مجموعتك وترقيتي كمشرف.

اعطني ڪامل الصلاحيات لكي اعمل بشكل صحيح عزيزي عليك الضغط على زر الاوامر لمعرفة طريقة تشغيلي شكرا لك!

كل الشكر والاحترام لمن قام بأضافة بوتاتنا 📍""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🖥 ¦ الأوامــر", callback_data="cbcmnds"),
                    InlineKeyboardButton(
                        "⚙️ ¦ الـسـورس", callback_data="https:/t.me/VFF35")
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

@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
async def closed(_, query: CallbackQuery):
    from_user = query.from_user
    permissions = await member_permissions(query.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await query.answer(
            "You don't have enough permissions to perform this action.",
            show_alert=True,
        )
    await query.message.delete()

@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("Only admins cam use this..!", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**⚙️ {BOT_NAME} Bot Settings**\n\n📮 Group : {query.message.chat.title}.\n📖 Grp ID : {query.message.chat.id}\n\n**Manage Your Groups Music System By Pressing Buttons Given Below 💡**",

              reply_markup=menu_keyboard
         )
    else:
        await query.answer("nothing is currently streaming", show_alert=True)



@Client.on_callback_query(filters.regex("high"))
async def high(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in high quality!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Quality 🔊**\n\nChoose your option from given below to manage audio quality.",
        reply_markup=highquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)


@Client.on_callback_query(filters.regex("low"))
async def low(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in low quality!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Quality 🔊**\n\nChoose your option from given below to manage audio quality.",
        reply_markup=lowquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)

@Client.on_callback_query(filters.regex("medium"))
async def medium(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in medium quality!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Quality 🔊**\n\nChoose your option from given below to manage audio quality.",
        reply_markup=mediumquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)

@Client.on_callback_query(filters.regex("fifth"))
async def fifth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in 200% volume!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Volume 🔊**\n\nIf you want to manage volume through buttons then make a assistant Admin first.",
        reply_markup=fifth_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)

@Client.on_callback_query(filters.regex("fourth"))
async def fourth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming 150 volume!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Volume 🔊**\n\nIf you want to manage volume through buttons then make a assistant Admin first.",
        reply_markup=fourth_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)

@Client.on_callback_query(filters.regex("third"))
async def third(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in 100% volume!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Volume 🔊**\n\nIf you want to manage volume through buttons then make a assistant Admin first.",
        reply_markup=third_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)


@Client.on_callback_query(filters.regex("second"))
async def second(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in 50% volume!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Volume 🔊**\n\nIf you want to manage volume through buttons then make a assistant Admin first.",
        reply_markup=second_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)


@Client.on_callback_query(filters.regex("first"))
async def first(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Now streaming in 20% volume!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Manage Audio Volume 🔊**\n\nIf you want to manage volume through buttons then make a assistant Admin first.",
        reply_markup=first_keyboard
    )
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)

@Client.on_callback_query(filters.regex("nonabout"))
async def nonabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**اهلا بك في ازرار كروب السورس وقناة السورس شكرا لكم اعزائي الكرام لقرائتكم بوتاتنا الافضل والاقوى!**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("🥇 ¦ الــكروب", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("⚙️ ¦ الـسـورس", url=f"https://t.me/{UPDATE}")
                ],
              [InlineKeyboardButton("🔙 رجــــوع", callback_data="cbmenu")]]
        ),
    )


@Client.on_callback_query(filters.regex("dbconfirm"))
async def dbconfirm(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("Only admins cam use this..!", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**Confirmation ⚠️**\n\nAre you sure want to end stream in {query.message.chat.title} and clean all Queued songs in db ?**",

              reply_markup=dbclean_keyboard
         )
    else:
        await query.answer("nothing is currently streaming", show_alert=True)

