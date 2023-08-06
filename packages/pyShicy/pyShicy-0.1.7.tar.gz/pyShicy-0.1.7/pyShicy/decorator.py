import logging
from datetime import datetime
from traceback import format_exc
import pytz
from fipper import ContinuePropagation, StopPropagation, filters
from fipper.enums import ChatMemberStatus, ChatType
from fipper.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from fipper.handlers import MessageHandler

from pyShicy.pyrogram import eor

from . import DEVS
from .config import Var as Variable
from .Clients import *


Var = Variable()


async def is_admin_or_owner(message, user_id) -> bool:
    """Check If A User Is Creator Or Admin Of The Current Group"""
    if message.chat.type in [ChatType.PRIVATE, ChatType.BOT]:
        # You Are Boss Of Pvt Chats.
        return True
    user_s = await message.chat.get_member(int(user_id))
    if user_s.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR):
        return True
    return False


def Shicy(
    cmd: list,
    group: int = 0,
    devs: bool = False,
    pm_only: bool = False,
    group_only: bool = False,
    channel_only: bool = False,
    admin_only: bool = False,
    pass_error: bool = False,
    propagate_to_next_handler: bool = True,
):
    """- Main Decorator To Register Commands. -"""
    if not devs:
        filterm = (
            filters.me
            & filters.command(cmd, Var.HNDLR)
            & ~filters.via_bot
            & ~filters.forwarded
        )
    else:
        filterm = (
            filters.user(DEVS)
            & filters.command(cmd, "")
        )

    def decorator(func):
        async def wrapper(client, message):
            message.client = client
            chat_type = message.chat.type
            if admin_only and not await is_admin_or_owner(
                message, (client.me).id
            ):
                await eor(
                    message, "<code>Perintah Ini Hanya Bisa Digunakan Jika Anda Admin Di Group Ini!</code>"
                )
                return
            if group_only and chat_type != (ChatType.GROUP, ChatType.SUPERGROUP):
                await eor(message, "<code>Apakah Ini Grup Tod?</code>")
                return
            if channel_only and chat_type != ChatType.CHANNEL:
                await eor(message, "Perintah Ini Hanya Bisa Digunakan Di Channel!")
                return
            if pm_only and chat_type != ChatType.PRIVATE:
                await eor(message, "<code>Perintah Ini Hanya Bisa Digunakan Di PM!</code>")
                return
            if pass_error:
                await func(client, message)
            else:
                try:
                    await func(client, message)
                except StopPropagation:
                    raise StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModified:
                    pass
                except MessageIdInvalid:
                    logging.warning(
                        "Please Don't Delete Commands While it's Processing..."
                    )
                except UserNotParticipant:
                    pass
                except ContinuePropagation:
                    raise ContinuePropagation
                except BaseException:
                    logging.error(
                        f"Exception - {func.__module__} - {func.__name__}"
                    )
                    TZZ = pytz.timezone(Var.TZ)
                    datetime_tz = datetime.now(TZZ)
                    text = "<b>!ERROR - REPORT!</b>\n\n"
                    text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                    text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                    text += f"\n<b>Plugin-Name :</b> <code>{func.__module__}</code>"
                    text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                    text += datetime_tz.strftime(
                        "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                    )
                    try:
                        xx = await tgbot.send_message(Var.LOG_CHAT, text)
                        await xx.pin(disable_notification=False)
                    except BaseException:
                        logging.error(text)
        add_handler(filterm, wrapper, cmd)
        return wrapper

    return decorator


def listen(filter_s):
    """Simple Decorator To Handel Custom Filters"""
    def decorator(func):
        async def wrapper(client, message):
            try:
                await func(client, message)
            except StopPropagation:
                raise StopPropagation
            except ContinuePropagation:
                raise ContinuePropagation
            except UserNotParticipant:
                pass
            except MessageEmpty:
                pass
            except BaseException:
                logging.error(
                    f"Exception - {func.__module__} - {func.__name__}")
                TZZ = pytz.timezone(Var.TZ)
                datetime_tz = datetime.now(TZZ)
                text = "<b>!ERROR WHILE HANDLING UPDATES!</b>\n\n"
                text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                text += f"\n<b>Plugin Name :</b> <code>{func.__module__}</code>"
                text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                text += datetime_tz.strftime(
                    "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                )
                try:
                    xx = await tgbot.send_message(Var.LOG_CHAT, text)
                    await xx.pin(disable_notification=False)
                except BaseException:
                    logging.error(text)
            message.continue_propagation()
        if SHICY1:
            SHICY1.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY2:
            SHICY2.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY3:
            SHICY3.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY4:
            SHICY4.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY5:
            SHICY5.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY6:
            SHICY6.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY7:
            SHICY7.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY8:
            SHICY8.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY9:
            SHICY9.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY10:
            SHICY10.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        '''
        if SHICY11:
            SHICY11.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY12:
            SHICY12.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY13:
            SHICY13.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY14:
            SHICY14.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY15:
            SHICY15.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY16:
            SHICY16.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY17:
            SHICY17.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY18:
            SHICY18.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY19:
            SHICY19.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY20:
            SHICY20.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY21:
            SHICY21.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY22:
            SHICY22.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY23:
            SHICY23.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY24:
            SHICY24.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY25:
            SHICY25.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY26:
            SHICY26.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY27:
            SHICY27.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY28:
            SHICY28.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY29:
            SHICY29.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY30:
            SHICY30.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY31:
            SHICY31.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY32:
            SHICY32.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY33:
            SHICY33.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY34:
            SHICY34.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY35:
            SHICY35.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY36:
            SHICY36.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY37:
            SHICY37.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY38:
            SHICY38.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY39:
            SHICY39.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY40:
            SHICY40.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY41:
            SHICY41.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY42:
            SHICY42.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY43:
            SHICY43.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY44:
            SHICY44.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY45:
            SHICY45.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY46:
            SHICY46.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY47:
            SHICY47.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY48:
            SHICY48.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY49:
            SHICY49.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY50:
            SHICY50.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY51:
            SHICY51.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY52:
            SHICY52.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY53:
            SHICY53.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY54:
            SHICY54.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY55:
            SHICY55.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY56:
            SHICY56.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY57:
            SHICY57.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY58:
            SHICY58.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY59:
            SHICY59.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY60:
            SHICY60.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY61:
            SHICY61.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY62:
            SHICY62.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY63:
            SHICY63.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY64:
            SHICY64.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY65:
            SHICY65.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY66:
            SHICY66.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY67:
            SHICY67.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY68:
            SHICY68.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY69:
            SHICY69.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY70:
            SHICY70.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY71:
            SHICY71.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY72:
            SHICY72.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY73:
            SHICY73.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY74:
            SHICY74.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY75:
            SHICY75.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY76:
            SHICY76.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY77:
            SHICY77.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY78:
            SHICY78.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY79:
            SHICY79.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY80:
            SHICY80.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY81:
            SHICY81.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY82:
            SHICY82.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY83:
            SHICY83.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY84:
            SHICY84.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY85:
            SHICY85.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY86:
            SHICY86.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY87:
            SHICY87.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY88:
            SHICY88.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY89:
            SHICY89.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY90:
            SHICY90.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY91:
            SHICY91.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY92:
            SHICY92.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY93:
            SHICY93.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY94:
            SHICY94.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY95:
            SHICY95.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY96:
            SHICY96.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY97:
            SHICY97.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY98:
            SHICY98.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY99:
            SHICY99.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if SHICY100:
            SHICY100.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        '''
        return wrapper

    return decorator


def add_handler(filter_s, func_, cmd):
    if SHICY1:
        SHICY1.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY2:
        SHICY2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY3:
        SHICY3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY4:
        SHICY4.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY5:
        SHICY5.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY6:
        SHICY6.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY7:
        SHICY7.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY8:
        SHICY8.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY9:
        SHICY9.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY10:
        SHICY10.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    '''
    if SHICY11:
        SHICY11.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY12:
        SHICY12.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY13:
        SHICY13.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY14:
        SHICY14.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY15:
        SHICY15.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY16:
        SHICY16.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY17:
        SHICY17.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY18:
        SHICY18.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY19:
        SHICY19.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY20:
        SHICY20.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY21:
        SHICY21.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY22:
        SHICY22.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY23:
        SHICY23.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY24:
        SHICY24.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY25:
        SHICY25.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY26:
        SHICY26.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY27:
        SHICY27.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY28:
        SHICY28.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY29:
        SHICY29.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY30:
        SHICY30.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY31:
        SHICY31.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY32:
        SHICY32.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY33:
        SHICY33.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY34:
        SHICY34.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY35:
        SHICY35.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY36:
        SHICY36.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY37:
        SHICY37.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY38:
        SHICY38.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY39:
        SHICY39.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY40:
        SHICY40.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY41:
        SHICY41.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY42:
        SHICY42.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY43:
        SHICY43.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY44:
        SHICY44.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY45:
        SHICY45.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY46:
        SHICY46.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY47:
        SHICY47.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY48:
        SHICY48.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY49:
        SHICY49.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY50:
        SHICY50.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY51:
        SHICY51.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY52:
        SHICY52.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY53:
        SHICY53.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY54:
        SHICY54.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY55:
        SHICY55.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY56:
        SHICY56.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY57:
        SHICY57.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY58:
        SHICY58.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY59:
        SHICY59.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY60:
        SHICY60.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY61:
        SHICY61.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY62:
        SHICY62.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY63:
        SHICY63.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY64:
        SHICY64.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY65:
        SHICY65.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY66:
        SHICY66.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY67:
        SHICY67.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY68:
        SHICY68.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY69:
        SHICY69.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY70:
        SHICY70.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY71:
        SHICY71.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY72:
        SHICY72.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY73:
        SHICY73.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY74:
        SHICY74.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY75:
        SHICY75.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY76:
        SHICY76.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY77:
        SHICY77.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY78:
        SHICY78.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY79:
        SHICY79.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY80:
        SHICY80.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY81:
        SHICY81.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY82:
        SHICY82.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY83:
        SHICY83.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY84:
        SHICY84.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY85:
        SHICY85.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY86:
        SHICY86.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY87:
        SHICY87.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY88:
        SHICY88.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY89:
        SHICY89.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY90:
        SHICY90.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY91:
        SHICY91.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY92:
        SHICY92.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY93:
        SHICY93.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY94:
        SHICY94.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY95:
        SHICY95.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY96:
        SHICY96.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY97:
        SHICY97.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY98:
        SHICY98.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY99:
        SHICY99.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if SHICY100:
        SHICY100.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    '''
