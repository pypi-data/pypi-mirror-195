from fipper import Client

from ..config import Var as Variable

Var = Variable()


hndlr = f"{Var.HNDLR[0]} {Var.HNDLR[1]} {Var.HNDLR[2]} {Var.HNDLR[3]} {Var.HNDLR[4]} {Var.HNDLR[5]}"

'''
try:
    import pytgcalls
except ImportError:
    print("'pytgcalls' not found")
    pytgcalls = None
'''


tgbot = (
    Client(
        name="tgbot",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        bot_token=Var.BOT_TOKEN,
    )
)

# For Publik Repository
SHICY1 = (
    Client(
        name="SHICY1",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_1,
        in_memory=True,
    )
    if Var.STRING_1
    else None
)


SHICY2 = (
    Client(
        name="SHICY2",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_2,
        in_memory=True,
    )
    if Var.STRING_2
    else None
)
        
SHICY3 = (
    Client(
        name="SHICY3",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_3,
        in_memory=True,
    )
    if Var.STRING_3
    else None
)

SHICY4 = (
    Client(
        name="SHICY4",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_4,
        in_memory=True,
    )
    if Var.STRING_4
    else None
)

SHICY5 = (
    Client(
        name="SHICY5",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_5,
        in_memory=True,
    )
    if Var.STRING_5
    else None
)

SHICY6 = (
    Client(
        name="SHICY6",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_6,
        in_memory=True,
    )
    if Var.STRING_6
    else None
)


SHICY7 = (
    Client(
        name="SHICY7",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_7,
        in_memory=True,
    )
    if Var.STRING_7
    else None
)
        
SHICY8 = (
    Client(
        name="SHICY8",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_8,
        in_memory=True,
    )
    if Var.STRING_8
    else None
)


SHICY9 = (
    Client(
        name="SHICY9",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_9,
        in_memory=True,
    )
    if Var.STRING_9
    else None
)
SHICY10 = (
    Client(
        name="SHICY10",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_10,
        in_memory=True,
    )
    if Var.STRING_10
    else None
)


Bots = [
    bot for bot in [
        SHICY1, 
        SHICY2, 
        SHICY3, 
        SHICY4, 
        SHICY5, 
        SHICY6, 
        SHICY7, 
        SHICY8,
        SHICY9,
        SHICY10,
    ] if bot
]

'''
if pytgcalls is not None:
    for bot in Bots:
        if not hasattr(bot, "group_call"):
            try:
                setattr(bot, "group_call", pytgcalls.GroupCallFactory(bot).get_group_call())
            except AttributeError:
                pass
'''
