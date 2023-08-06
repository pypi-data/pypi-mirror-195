import logging
import sys

from pyShicy.config import Var as Variable

from ..methods._database import ShicyDB
from ..methods.helpers import Helpers
from ..methods.hosting import where_hosted

from .client import *


adB = ShicyDB()
logs = logging.getLogger(__name__)
HOSTED_ON = where_hosted()
Var = Variable()
Xd = Helpers()


async def SHICY_client(client):
    try:
        await client.join_chat("ShicyyXCode")
        await client.join_chat("ShicyxCod")
        await client.join_chat("StoryyCard")
    except Exception:
        pass


clients = []
client_id = []


async def StartPyrogram():
    try:
        bot_plugins = Xd.import_module(
            "assistant/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{bot_plugins} Total Plugins Bot")
        plugins = Xd.import_module(
            "ShicyXd/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{plugins} Total Plugins User")
    except BaseException as e:
        logs.info(e)
        sys.exit()
    if tgbot:
        await tgbot.start()
        me = await tgbot.get_me()
        tgbot.id = me.id
        tgbot.mention = me.mention
        tgbot.username = me.username
        if me.last_name:
            tgbot.name = me.first_name + " " + me.last_name
        else:
            tgbot.name = me.first_name
        logs.info(
            f"TgBot in {tgbot.name} | [ {tgbot.id} ]"
        )
        client_id.append(tgbot.id)
    if SHICY1:
        try:
            await SHICY1.start()
            clients.append(1)
            await SHICY_client(SHICY1)
            me = await SHICY1.get_me()
            SHICY1.id = me.id
            SHICY1.mention = me.mention
            SHICY1.username = me.username
            if me.last_name:
                SHICY1.name = me.first_name + " " + me.last_name
            else:
                SHICY1.name = me.first_name
            #SHICY1.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY1 in {SHICY1.name} | [ {SHICY1.id} ]"
            )
            client_id.append(SHICY1.id)
        except Exception as e:
            logs.info(f"[STRING_1] ERROR: {e}")
    if SHICY2:
        try:
            await SHICY2.start()
            clients.append(2)
            await SHICY_client(SHICY2)
            me = await SHICY2.get_me()
            SHICY2.id = me.id
            SHICY2.mention = me.mention
            SHICY2.username = me.username
            if me.last_name:
                SHICY2.name = me.first_name + " " + me.last_name
            else:
                SHICY2.name = me.first_name
            #SHICY2.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY2 in {SHICY2.name} | [ {SHICY2.id} ]"
            )
            client_id.append(SHICY2.id)
        except Exception as e:
            logs.info(f"[STRING_2] ERROR: {e}")
    if SHICY3:
        try:
            await SHICY3.start()
            clients.append(3)
            await SHICY_client(SHICY3)
            me = await SHICY3.get_me()
            SHICY3.id = me.id
            SHICY3.mention = me.mention
            SHICY3.username = me.username
            if me.last_name:
                SHICY3.name = me.first_name + " " + me.last_name
            else:
                SHICY3.name = me.first_name
            #SHICY3.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY3 in {SHICY3.name} | [ {SHICY3.id} ]"
            )
            client_id.append(SHICY3.id)
        except Exception as e:
            logs.info(f"[STRING_3] ERROR: {e}")
    if SHICY4:
        try:
            await SHICY4.start()
            clients.append(4)
            await SHICY_client(SHICY4)
            me = await SHICY4.get_me()
            SHICY4.id = me.id
            SHICY4.mention = me.mention
            SHICY4.username = me.username
            if me.last_name:
                SHICY4.name = me.first_name + " " + me.last_name
            else:
                SHICY4.name = me.first_name
            #SHICY4.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY4 in {SHICY4.name} | [ {SHICY4.id} ]"
            )
            client_id.append(SHICY4.id)
        except Exception as e:
            logs.info(f"[STRING_4] ERROR: {e}")
    if SHICY5:
        try:
            await SHICY5.start()
            clients.append(5)
            await SHICY_client(SHICY5)
            me = await SHICY5.get_me()
            SHICY5.id = me.id
            SHICY5.mention = me.mention
            SHICY5.username = me.username
            if me.last_name:
                SHICY5.name = me.first_name + " " + me.last_name
            else:
                SHICY5.name = me.first_name
            #SHICY5.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY5 in {SHICY5.name} | [ {SHICY5.id} ]"
            )
            client_id.append(SHICY5.id)
        except Exception as e:
            logs.info(f"[STRING_5] ERROR: {e}")
    if SHICY6:
        try:
            await SHICY6.start()
            clients.append(6)
            await SHICY_client(SHICY6)
            me = await SHICY6.get_me()
            SHICY6.id = me.id
            SHICY6.mention = me.mention
            SHICY6.username = me.username
            if me.last_name:
                SHICY6.name = me.first_name + " " + me.last_name
            else:
                SHICY6.name = me.first_name
            #SHICY1.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY6 in {SHICY6.name} | [ {SHICY6.id} ]"
            )
            client_id.append(SHICY6.id)
        except Exception as e:
            logs.info(f"[STRING_6] ERROR: {e}")
    if SHICY7:
        try:
            await SHICY7.start()
            clients.append(7)
            await SHICY_client(SHICY7)
            me = await SHICY7.get_me()
            SHICY7.id = me.id
            SHICY7.mention = me.mention
            SHICY7.username = me.username
            if me.last_name:
                SHICY7.name = me.first_name + " " + me.last_name
            else:
                SHICY7.name = me.first_name
            #SHICY7.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY7 in {SHICY7.name} | [ {SHICY7.id} ]"
            )
            client_id.append(SHICY7.id)
        except Exception as e:
            logs.info(f"[STRING_7] ERROR: {e}")
    if SHICY8:
        try:
            await SHICY8.start()
            clients.append(8)
            await SHICY_client(SHICY8)
            me = await SHICY8.get_me()
            SHICY8.id = me.id
            SHICY8.mention = me.mention
            SHICY8.username = me.username
            if me.last_name:
                SHICY8.name = me.first_name + " " + me.last_name
            else:
                SHICY8.name = me.first_name
            #SHICY8.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY8 in {SHICY8.name} | [ {SHICY8.id} ]"
            )
            client_id.append(SHICY8.id)
        except Exception as e:
            logs.info(f"[STRING_8] ERROR: {e}")
    if SHICY9:
        try:
            await SHICY9.start()
            clients.append(9)
            await SHICY_client(SHICY9)
            me = await SHICY9.get_me()
            SHICY9.id = me.id
            SHICY9.mention = me.mention
            SHICY9.username = me.username
            if me.last_name:
                SHICY9.name = me.first_name + " " + me.last_name
            else:
                SHICY9.name = me.first_name
            #SHICY9.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY9 in {SHICY9.name} | [ {SHICY9.id} ]"
            )
            client_id.append(SHICY9.id)
        except Exception as e:
            logs.info(f"[STRING_9] ERROR: {e}")
    if SHICY10:
        try:
            await SHICY10.start()
            clients.append(10)
            await SHICY_client(SHICY10)
            me = await SHICY10.get_me()
            SHICY10.id = me.id
            SHICY10.mention = me.mention
            SHICY10.username = me.username
            if me.last_name:
                SHICY10.name = me.first_name + " " + me.last_name
            else:
                SHICY10.name = me.first_name
            #SHICY10.has_a_bot = True if tgbot else False
            logs.info(
                f"SHICY10 in {SHICY10.name} | [ {SHICY10.id} ]"
            )
            client_id.append(SHICY10.id)
        except Exception as e:
            logs.info(f"[STRING_10] ERROR: {e}")
    logs.info(f"Connecting Database To {adB.name}")
    if adB.ping():
        logs.info(f"Succesfully Connect On {adB.name}")
    logs.info(
        f"Connect On [ {HOSTED_ON} ]\n"
    )
