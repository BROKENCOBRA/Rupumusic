
import os
from os import path
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from Client import callsmusic, queues
from Client.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import yt_dlp
from youtube_search import YoutubeSearch
import converter
from youtube import youtube
from config import DURATION_LIMIT, que, SUDO_USERS
from cache.admins import admins as a
from helpers.filters import command
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from helpers.channelmusic import get_chat_id
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

# plus
chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes or cb.from_user.id in SUDO_USERS:
            return await func(client, cb)
        await cb.answer("Yᴏᴜ ᴀɪɴ'ᴛ ᴛᴏ ᴘʟᴀʏ!", show_alert=True)
        return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    async def generate_cover(title, thumbnail):
    async with aiohttp.ClientSession() as session, session.get(thumbnail) as resp:
          if resp.status == 200:
              f = await aiofiles.open("background.png", mode="wb")
              await f.write(await resp.read())
              await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/regular.ttf", 52)
    font2 = ImageFont.truetype("etc/medium.ttf", 76)
    draw.text((27, 538), f"Playing..", (0, 0, 0), font=font)
    draw.text((27, 612), f"{title[:18]}...", (0, 0, 0), font=font2)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")

@Client.on_message(
    command("Maintainmode") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "I only recognize `/Maintainmode on` and /Maintainmode `off only`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ["OFF", "Off", "off"]:
        lel = await message.reply("`Processing...`")
        if message.chat.id not in DISABLED_GROUPS:
            await lel.edit("This Chat is not In maintainence mode")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"Maintainence Mode disabled In **{message.chat.title}** Chat"
        )

    elif status in ["ON", "On", "on"]:
        lel = await message.reply("`Processing...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("maintainence mode  already active in This Chat")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"Maintainence mode is now enabled in **{message.chat.title}** Chat"
        )
    else:
        await message.reply_text(
            "I only recognize `/Maintainmode on` and /Maintainmode `off only"
        )


@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
@cb_admin_check
@authorized_users_only
async def m_cb(b, cb):
    global que
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    if type_ == "cls":
        await cb.answer("Closed menu")
        await cb.message.delete()


# play
@Client.on_message(
    command("play")
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    chat_id = message.chat.id
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        await message.reply("**maintainence mode is on, ask admin to disable it!**")
        return
    lel = await message.reply("🔄**Pʟᴀʏɪɴɢ...Aᴜᴅɪᴏ**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "rupu_Assistant"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                await lel.edit(
                    "<b>Remember to add Assistant to your channel</b>",
                )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "⚠️ **ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ғɪʀsᴛ ⚠️**",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "**ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ 👍🏻 ɴᴏᴡ ᴘʟᴀʏ ʏᴏᴜʀ ᴍᴜsɪᴄ ғʀᴇᴇʟʏ** ❣️",
                    )
                    await lel.edit(
                        "**ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ 👍🏻 ɴᴏᴡ ᴘʟᴀʏ ʏᴏᴜʀ ᴍᴜsɪᴄ ғʀᴇᴇʟʏ** ❣️",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(f"⚠️ **ғʟᴏᴏᴅ ᴡᴀɪᴛ ᴇʀʀᴏʀ ⚠️ ᴄʜᴇᴄᴋ ᴍᴀʏʙᴇ ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ᴏʀ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ**.!"
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"😒 **ᴀssɪsᴛᴀɴᴛ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ sᴏ sᴇɴᴅ /userbotjoin ᴄᴏᴍᴍᴀɴᴅ ғɪʀsᴛ ᴛᴏ ᴊᴏɪɴ ᴀssɪsᴛᴀɴᴛ ʜᴇʀᴇ**"
        )
        return

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"🙃 **ʜᴇʏ ʏᴏᴜʀ sᴏɴɢ ᴅᴜʀᴀᴛɪᴏɴ ɪs {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs..Sᴇᴀʀᴄʜ ғᴏʀ sᴍᴀʟʟ ᴍᴜsɪᴄ.** ️🤞!"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/22e0f6fd383b078132fd0.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❣️ Rᴜᴘᴜ Oᴡɴᴇʀ", text=f"Fɪɴᴅɪɴɢ ʜᴇʀ🧐🥺"
                    ),
                    InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ🎵", url=f"https://t.me/shivamdemon"),
                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❣️ Rᴜᴘᴜ Oᴡɴᴇʀ", text=f"Fɪɴᴅɪɴɢ ʜᴇʀ🧐🥺"
                    ),
                    InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ🎵", url=f"https://t.me/shivamdemon"),
                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/22e0f6fd383b078132fd0.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url="https://youtube.com")]]
            )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"🙃 **ʜᴇʏ ʏᴏᴜʀ sᴏɴɢ ᴅᴜʀᴀᴛɪᴏɴ ɪs {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs..sᴇᴀʀᴄʜ ғᴏʀ sᴍᴀʟʟ ᴍᴜsɪᴄ.** ️🤞"
 !"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "🙃 **ʜᴇʏ ᴛʏᴘᴇ ᴛʜᴇ sᴏᴍᴇᴛʜɪɴɢ ʀᴇᴀʟ...**"
            )
        await lel.edit("🔎 **ᴄᴏɴɴᴇᴄᴛɪɴɢ...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🔍 **ᴡᴀɪᴛɪɴɢ ᴛᴏ ᴘʟᴀʏ...** ")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "⚠️ **sᴏʀʀʏ sᴏɴɢ ɴᴀᴍᴇ ᴡʀᴏɴɢ, ᴛʀʏ ᴡɪᴛʜ ʀɪɢʜᴛ ɴᴀᴍᴇ** 😾😒."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❣️ Rᴜᴘᴜ Oᴡɴᴇʀ", text=f"Fɪɴᴅɪɴɢ ʜᴇʀ🧐🥺"
                    ),
                    InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ🎵", url=f"https://t.me/shivamdemon"),
                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"🙃 **ʜᴇʏ ʏᴏᴜʀ sᴏɴɢ ᴅᴜʀᴀᴛɪᴏɴ ɪs {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs..sᴇᴀʀᴄʜ ғᴏʀ sᴍᴀʟʟ ᴍᴜsɪᴄ** ️🤞!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ Qᴜᴇᴜᴇ »** `{position}`\n\n🏷 **ɴᴀᴍᴇ:** [{title[:80]}]({url})\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
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
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"☑️ **ɴᴀᴍᴇ:** [{title[:80]}]({url})\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n💡 **ꜱᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n"
            + f"🎧 **ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.mention}"
            ),
        )

    os.remove("final.png")
    return await lel.delete()
