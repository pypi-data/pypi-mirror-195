import asyncio
import logging
import sys
import time
from aiohttp import ClientSession

from pyShicy.Clients import *
from pyShicy.methods import *
from pyShicy.pyrogram import ShicyMethods
from pyShicy.pyrogram import eod, eor
from pyShicy.xd import GenSession
from pyShicy.telethon.shicy import *


# Bot Logs setup:
logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logging.getLogger("pyShicy").setLevel(logging.INFO)
logging.getLogger("fipper").setLevel(logging.ERROR)
logging.getLogger("fipper.client").setLevel(logging.ERROR)
logging.getLogger("fipper.session.auth").setLevel(logging.ERROR)
logging.getLogger("fipper.session.session").setLevel(logging.ERROR)


logs = logging.getLogger(__name__)


__copyright__ = "Copyright (C) 2023-present sip-userbot <https://github.com/sip-userbot>"
__license__ = "GNU General Public License v3.0 (GPL-3.0)"
__version__ = "0.1.7"
shicy_ver = "0.0.5"


adB = ShicyDB()

DEVS = [
    1603412565, # Shicy
    5057493677, # ilham
]

StartTime = time.time()


class PyrogramXd(ShicyMethods, GenSession, Methods):
    pass


class TelethonXd(ShicyMethod, GenSession, Methods):
    pass


suc_msg = (f"""
========================×========================
           Credit Py-Shicy {__version__}
========================×========================
"""
)

fail_msg = (f"""
========================×========================
      Commit Yang Bener Bego Biar Gak Error
           Credit Py-Shicy {__version__}
========================×========================
"""
)

start_bot = (f"""
========================×========================
         Starting ShicyUbot Version {shicy_ver}
        Copyright (C) 2022-present sip-userbot
========================×========================
"""
)

run_as_module = False

if sys.argv[0] == "-m":
    run_as_module = True

    from .decorator import *

    print("\n\n" + __copyright__ + "\n" + __license__)
    print(start_bot)

    update_envs()

    CMD_HELP = {}
    adB = ShicyDB()
    aiosession = ClientSession()
    loop = asyncio.get_event_loop()
    HOSTED_ON = where_hosted()
    Chiy = VcTools()
else:
    print(suc_msg)
    print("\n\n" + __copyright__ + "\n" + __license__)
    print(fail_msg)

    adB = ShicyDB()
    aiosession = ClientSession()
    loop = asyncio.get_event_loop()
    HOSTED_ON = where_hosted()
