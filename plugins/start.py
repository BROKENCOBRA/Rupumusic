from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    
    await message.reply_text(
        f"""**Hᴇʏ ɪᴛs {bn}** \n
**I ᴀᴍ ʟᴀᴢʏ Aʙᴏᴜᴛ ᴛʏᴘɪɴɢ sᴏᴍᴇᴛʜɪɴɢ ɴᴇᴡ..ɪᴛᴢ ᴀ ʙᴏᴛ ᴍᴀᴅᴇ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ Vᴄ.😈❣️
Dᴇᴠᴇʟᴏᴘᴇᴅ Bʏ : [𝐒•4•𝐒𝐡𝐢𝐯](https://t.me/shivamdemon)**.
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💞 ᴏᴡɴᴇʀ ", text="Fɪɴᴅɪɴɢ ʀᴜᴘᴀ🥺😇")
                  ],[
                    InlineKeyboardButton(
                        "🔥Aɴʏ Pʀᴏʙʟᴇᴍ", url="https://t.me/shivamdemon"
                    ),
                    InlineKeyboardButton(
                        "🐬 Gʀᴏᴜᴘ", url="https://t.me/Love_live_laughk"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "Aᴅᴅ ᴍʏ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴅᴀʀʟɪɴɢ🤭", url=f"https://t.me/itzrupu_vcbot?startgroup=true"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("alive") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""Bᴏᴛ ɪɴ Fᴏʀᴍ ʙᴀʙʏ 😈""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "😎 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Shivamdemon")
                ]
            ]
        )
   )
 
