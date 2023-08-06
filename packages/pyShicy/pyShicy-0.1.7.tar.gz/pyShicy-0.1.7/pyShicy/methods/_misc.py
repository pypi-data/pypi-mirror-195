from time import time
from datetime import datetime

from fipper import __version__ as fip_ver, Client
from fipper.enums import ParseMode
from fipper.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
from platform import python_version

from ..config import Var as Variable
from ..Clients import *

from ._database import ShicyDB
from .hosting import where_hosted

adB = ShicyDB()
var = Variable()
HOSTED_ON = where_hosted()


class _Misc(object):
    async def alive(self, cb: str):
        from pyShicy import __version__, shicy_ver
        from pyShicy import CMD_HELP
        
        output = (
            f"**Tʜᴇ [Shicy Ubot](https://github.com/sip-userbot/ShicyUbot)**\n\n"
            f"**{var.ALIVE_TEXT}**\n\n"
            f"╭✠╼━━━━━━━━━━━━━━━✠╮\n"
            f"≽ **Bᴀsᴇ Oɴ :** •[{adB.name}]•\n"
            f"≽ **Mᴏᴅᴜʟᴇs :** `{len(CMD_HELP)} Modules` \n"
            f"≽ **Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ :** `{python_version()}`\n"
            f"≽ **Pʏʀᴏɢʀᴀᴍ Vᴇʀsɪᴏɴ :** `{fip_ver}`\n"
            f"≽ **Pʏ-Aʏɪɪɴ Vᴇʀsɪᴏɴ :** `{__version__}`\n"
            f"≽ **Aʏɪɪɴ Vᴇʀsɪᴏɴ :** `{shicy_ver}` [{HOSTED_ON}]\n"
            "╰✠╼━━━━━━━━━━━━━━━✠╯\n\n"
        )
        buttons = [
            [
                InlineKeyboardButton("•• Help ••", callback_data=cb),
            ]
        ]
        results=[
            (
                InlineQueryResultPhoto(
                    photo_url=Var.ALIVE_PIC,
                    title="Alive",
                    description="inline ShicyUbot.",
                    caption=output,
                    reply_markup=InlineKeyboardMarkup(
                        buttons
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
            )
        ]
        return results
    
    async def info_inline_func(self, client: Client, answers, peer):
        not_found = InlineQueryResultArticle(
            title="PEER NOT FOUND",
            input_message_content=InputTextMessageContent("PEER NOT FOUND"),
        )
        try:
            user = await client.get_users(peer)
            caption, _ = await self.get_user_info(user, True)
        except IndexError:
            try:
                chat = await client.get_chat(peer)
                caption, _ = await self.get_chat_info(chat, True)
            except Exception:
                return [not_found]
        except Exception:
            return [not_found]

        answers.append(
            InlineQueryResultArticle(
                title="Found Peer.",
                input_message_content=InputTextMessageContent(
                    caption, disable_web_page_preview=True
                ),
            )
        )
    
    
