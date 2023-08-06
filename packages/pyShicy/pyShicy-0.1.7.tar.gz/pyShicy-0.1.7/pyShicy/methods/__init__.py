from ._database import ShicyDB
from ._misc import _Misc
from .changer import Changers
from .converter import Convert
from .func import Funci
from .funcb import FuncBot
from .helpers import Helpers, run_async, update_envs
from .hosting import where_hosted
from .inlinebot import InlineBot
from .queue import Queues
from .thumbnail import Thumbnail


class Methods(
    _Misc,
    Changers,
    Convert,
    Funci,
    FuncBot,
    InlineBot,
    Helpers,
    Queues,
    Thumbnail,
):
    pass
