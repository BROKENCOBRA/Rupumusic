# Credit DaisyXMusic, Changes By Blaze, Improve Code By Decode

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from Client.callsmusic import client as USER
from config import SUDO_USERS


@Client.on_message(filters.command(["userbotjoin", "join"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me admin first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "@ruppu_assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} Aʟʀᴇᴀᴅʏ ʜᴇʀᴇ ʙᴀʙᴇs ..❤️</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"😒 **ᴀssɪsᴛᴀɴᴛ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ sᴏ sᴇɴᴅ /userbotjoin ᴄᴏᴍᴍᴀɴᴅ ғɪʀsᴛ ᴛᴏ ᴊᴏɪɴ ᴀssɪsᴛᴀɴᴛ ʜᴇʀᴇ**",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} Join Seccsesfully</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "⚠️ **ғʟᴏᴏᴅ ᴡᴀɪᴛ ᴇʀʀᴏʀ ⚠️ ᴄʜᴇᴄᴋ ᴍᴀʏʙᴇ ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ᴏʀ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ**."
        )

        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("**Asisten Meninggalkan semua obrolan**")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠɪɴɢ... Lᴇғᴛ: {left} chats. Fᴀɪʟᴇᴅ: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠɪɴɢ... Lᴇғᴛ: {left} chats. Fᴀɪʟᴇᴅ: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Lᴇғᴛ {left} chats. Fᴀɪʟᴇᴅ{failed} chats."
    )

