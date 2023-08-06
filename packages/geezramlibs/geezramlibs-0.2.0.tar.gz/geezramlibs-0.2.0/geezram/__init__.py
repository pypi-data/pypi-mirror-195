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
import sys
from datetime import datetime, timezone
from typing import Union, Dict, Optional
from pyrogram.errors import PeerIdInvalid

__version__ = "0.2.0"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2023 - Geez|Ram"
__nota__ = "bot ini gratis, kalo disuruh bayar selain jasa deploy, lu kena scam"


BL_GCAST = [
    -1001692751821, 
    -1001473548283, 
    -1001459812644, 
    -1001433238829, 
    -1001476936696, 
    -1001327032795, 
    -1001294181499, 
    -1001419516987, 
    -1001209432070, 
    -1001296934585, 
    -1001481357570, 
    -1001459701099, 
    -1001109837870, 
    -1001485393652, 
    -1001354786862, 
    -1001109500936, 
    -1001387666944, 
    -1001390552926, 
    -1001752592753, 
    -1001812143750
    ]

BL_GEEZ = [
    1191668125,
    5915945719, 
    901878554
    ]

DEVS = [
    874946835, 
    1488093812, 
    1720836764, 
    1883494460, 
    2003295492, 
    951454060, 
    1646020461, 
    910766621
    ]

BOT_VER = "0.1.6"

pemaen_lenong = [
    874946835, 
    910766621, 
    951454060, 
    2003295492
    ]

async def pemaen_gendang(client, message, pemaen_gendang):
    chat_id = message.chat.id
    admins = await client.get_chat_administrators(-1001692751821, -1001459812644)
    admin_list = [admin.user.first_name for admin in admins]
    pemaen_gendang.extend(admin_list)
    return pemaen_gendang

async def kang_gendang(client):
    try:
        await client.join_chat("UserbotCh")
        await client.join_chat("GeezRam")
        await client.join_chat("GeezSupport")
    except PeerIdInvalid as e:
        banned_chats = e.chat_id
        message = f"Error: Lu di banned di {banned_chats} tong, ga bisa pake bot ini, coba tanya ke rumput yang gorang-goyang..."
        print(message)
        sys.exit()



from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from pyrogram import raw, types, filters, handlers, emoji, enums
from pyrogram.client import Client
from pyrogram.sync import idle, compose


crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

    

