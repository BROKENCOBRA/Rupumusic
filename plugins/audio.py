from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream
from Client import callsmusic, queues

import converter
from youtube import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ACTV_CALLS = []

@Client.on_message(command("audio") & other_filters)
@errors
async def stream(_, message: Message):
    chat_id = message.chat.id

    lel = await message.reply("🎵 **Pʀᴏᴄᴇssɪɴɢ ᴍᴇᴅɪᴀ**...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ ɢʀᴏᴜᴘ°",
                        url=f"https://t.me/Decodesupport"),
                    InlineKeyboardButton(
                        text="💞 sᴜᴘᴘᴏʀᴛ°",
                        url=f"https://t.me/shivamdemon")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Vɪᴅᴇᴏ ʟᴏɴɢᴇʀ ᴛʜᴀɴ ᴡʜɪᴄʜ ᴀʟʟᴏᴡ {DURATION_LIMIT} ᴍɪɴs!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("ɴᴏᴏʙ ɢɪᴠᴇ ᴍᴇ ᴀᴜᴅɪᴏ ғɪʟᴇ ᴏʀ ʏᴛ ʟɪɴᴋ❗")
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))    
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"#⃣  𝐲𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠 𝐰𝐚𝐬 𝐚𝐝𝐝𝐞𝐝 𝐭𝐨 *𝐪𝐮𝐞𝐮𝐞* 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!\n\n⚡ __𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 𝐃𝐞𝐂𝐨𝐝𝐞 𝐀.𝐈__")
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            ) 
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"🎧 **ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ**ᴀs ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ{costumer}!\n\n⚡Pᴏᴡᴇʀᴇᴅ ʙʏ ᴏᴡɴᴇʀ ʀᴜᴘᴀ"
        )
        return await lel.delete()
